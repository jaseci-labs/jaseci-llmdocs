"""RAG integration for Jac documentation pipeline.

Provides semantic retrieval via ChromaDB for:
1. jac_rules -- assembly prompt syntax rules, topic definitions, verified examples
2. jac_sources -- extracted code examples from Stage 1 (re-indexed each run)

Falls back gracefully if chromadb/sentence-transformers are not installed.
"""
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class RuleNugget:
    id: str
    content: str
    topic_ids: list[str] = field(default_factory=list)
    construct_types: list[str] = field(default_factory=list)
    priority: int = 2
    category: str = "syntax_rule"


class EmbeddingProvider:
    """Lazy-loads sentence-transformers model for embedding generation."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self._model_name = model_name
        self._model = None

    def _load(self):
        if self._model is not None:
            return
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(self._model_name)

    def encode(self, texts: list[str]) -> list[list[float]]:
        self._load()
        embeddings = self._model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()


class RuleStore:
    """Manages the jac_rules ChromaDB collection (persistent across runs)."""

    def __init__(self, client, embedding_provider: EmbeddingProvider, collection_name: str = "jac_rules"):
        self._client = client
        self._embedder = embedding_provider
        self._collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def is_indexed(self) -> bool:
        return self._collection.count() > 0

    def index_rules(self, rules: list[RuleNugget]) -> int:
        if not rules:
            return 0

        ids = [r.id for r in rules]
        documents = [r.content for r in rules]
        metadatas = [
            {
                "topic_ids": ",".join(r.topic_ids),
                "construct_types": ",".join(r.construct_types),
                "priority": r.priority,
                "category": r.category,
            }
            for r in rules
        ]
        embeddings = self._embedder.encode(documents)

        self._collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )
        return len(rules)

    def query_by_topic(
        self,
        topic_id: str,
        construct_types: list[str],
        n_results: int = 15,
    ) -> list[dict]:
        """Retrieve rules relevant to a topic and set of construct types."""
        query_text = f"{topic_id} {' '.join(construct_types)}"
        query_embedding = self._embedder.encode([query_text])[0]

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, self._collection.count()),
        )

        if not results["documents"] or not results["documents"][0]:
            return []

        output = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            meta_topics = set(meta.get("topic_ids", "").split(","))
            meta_constructs = set(meta.get("construct_types", "").split(","))

            relevance_boost = 0.0
            if topic_id in meta_topics:
                relevance_boost += 0.3
            if meta_constructs & set(construct_types):
                relevance_boost += 0.2
            if meta.get("priority", 2) == 1:
                relevance_boost += 0.1

            output.append({
                "content": doc,
                "category": meta.get("category", ""),
                "priority": meta.get("priority", 2),
                "score": 1.0 - dist + relevance_boost,
                "topic_ids": list(meta_topics),
                "construct_types": list(meta_constructs),
            })

        output.sort(key=lambda x: (-x["score"]))
        return output[:n_results]


class ExampleStore:
    """Manages the jac_sources ChromaDB collection (re-indexed each run)."""

    def __init__(self, client, embedding_provider: EmbeddingProvider, collection_name: str = "jac_sources"):
        self._client = client
        self._embedder = embedding_provider
        self._collection_name = collection_name
        # Delete and recreate to ensure fresh index each run
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass
        self._collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def index_examples(self, examples: dict) -> int:
        """Index extracted examples from Stage 1. examples: construct_type -> list[CodeExample]."""
        all_ids = []
        all_docs = []
        all_metas = []
        idx = 0

        for construct_type, example_list in examples.items():
            for ex in example_list:
                idx += 1
                doc_text = f"[{construct_type}] {ex.code}"
                all_ids.append(f"src-{construct_type}-{idx:04d}")
                all_docs.append(doc_text)
                all_metas.append({
                    "construct_type": construct_type,
                    "source_file": getattr(ex, "source_file", ""),
                    "line_count": getattr(ex, "line_count", 0),
                    "keywords": ",".join(getattr(ex, "has_keywords", [])),
                })

        if not all_ids:
            return 0

        embeddings = self._embedder.encode(all_docs)

        batch_size = 500
        for start in range(0, len(all_ids), batch_size):
            end = start + batch_size
            self._collection.upsert(
                ids=all_ids[start:end],
                documents=all_docs[start:end],
                metadatas=all_metas[start:end],
                embeddings=embeddings[start:end],
            )

        return len(all_ids)

    def query_mmr(
        self,
        query: str,
        construct_type: str,
        n_results: int = 3,
        lambda_mult: float = 0.5,
    ) -> list[dict]:
        """MMR retrieval for diverse examples of a given construct type."""
        query_text = f"[{construct_type}] {query}"
        query_embedding = self._embedder.encode([query_text])[0]

        fetch_k = min(n_results * 5, self._collection.count())
        if fetch_k == 0:
            return []

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=fetch_k,
            where={"construct_type": construct_type} if self._has_type(construct_type) else None,
        )

        if not results["documents"] or not results["documents"][0]:
            return []

        candidates = []
        for doc, meta, emb_dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            candidates.append({
                "content": doc,
                "metadata": meta,
                "distance": emb_dist,
            })

        if not candidates:
            return []

        candidate_texts = [c["content"] for c in candidates]
        candidate_embeddings = self._embedder.encode(candidate_texts)

        selected = self._apply_mmr(
            candidates, candidate_embeddings, query_embedding, n_results, lambda_mult
        )
        return selected

    def _has_type(self, construct_type: str) -> bool:
        """Check if collection has any documents with this construct_type."""
        try:
            result = self._collection.get(
                where={"construct_type": construct_type},
                limit=1,
            )
            return bool(result["ids"])
        except Exception:
            return False

    @staticmethod
    def _apply_mmr(
        candidates: list[dict],
        candidate_embeddings: list,
        query_embedding: list,
        k: int,
        lambda_mult: float,
    ) -> list[dict]:
        """Maximal Marginal Relevance scoring."""
        import numpy as np

        query_vec = np.array(query_embedding)
        cand_vecs = np.array(candidate_embeddings)

        # Cosine similarity to query
        query_norm = np.linalg.norm(query_vec)
        if query_norm == 0:
            return candidates[:k]

        relevance = cand_vecs @ query_vec / (
            np.linalg.norm(cand_vecs, axis=1) * query_norm + 1e-10
        )

        selected_indices = []
        remaining = list(range(len(candidates)))

        for _ in range(min(k, len(candidates))):
            if not remaining:
                break

            best_idx = None
            best_score = -float("inf")

            for idx in remaining:
                rel_score = relevance[idx]

                max_sim = 0.0
                if selected_indices:
                    selected_vecs = cand_vecs[selected_indices]
                    cand_norm = np.linalg.norm(cand_vecs[idx])
                    if cand_norm > 0:
                        sims = selected_vecs @ cand_vecs[idx] / (
                            np.linalg.norm(selected_vecs, axis=1) * cand_norm + 1e-10
                        )
                        max_sim = float(np.max(sims))

                mmr_score = lambda_mult * rel_score - (1 - lambda_mult) * max_sim

                if mmr_score > best_score:
                    best_score = mmr_score
                    best_idx = idx

            if best_idx is not None:
                selected_indices.append(best_idx)
                remaining.remove(best_idx)

        return [
            {
                "content": candidates[i]["content"],
                "metadata": candidates[i]["metadata"],
                "score": float(relevance[i]),
            }
            for i in selected_indices
        ]


class RAGRetriever:
    """Orchestrates RAG retrieval for the assembly stage."""

    def __init__(self, config: dict):
        self._config = config.get("rag", {})
        self._embedder = None
        self._rule_store = None
        self._example_store = None
        self._available = None

        persist_dir = self._config.get("persist_dir", "data/chromadb")
        self._persist_path = Path(__file__).parents[1] / persist_dir

    @property
    def available(self) -> bool:
        if self._available is not None:
            return self._available
        try:
            import chromadb  # noqa: F401
            import sentence_transformers  # noqa: F401
            import numpy  # noqa: F401
            self._available = True
        except ImportError as exc:
            logger.warning("RAG dependencies not available: %s", exc)
            self._available = False
        return self._available

    def _init_stores(self):
        if self._rule_store is not None:
            return

        import chromadb

        model_name = self._config.get("embedding_model", "all-MiniLM-L6-v2")
        self._embedder = EmbeddingProvider(model_name)

        self._persist_path.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(self._persist_path))

        self._rule_store = RuleStore(client, self._embedder)
        self._example_store = ExampleStore(client, self._embedder)

    def ensure_rules_indexed(self, rules_path: Path) -> int:
        """Load and index rules from rules.jsonl if not already indexed."""
        self._init_stores()

        if self._rule_store.is_indexed():
            count = self._rule_store._collection.count()
            logger.info("Rules already indexed (%d entries)", count)
            return count

        if not rules_path.exists():
            logger.warning("Rules file not found: %s", rules_path)
            return 0

        nuggets = []
        with open(rules_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                nuggets.append(RuleNugget(
                    id=data["id"],
                    content=data["content"],
                    topic_ids=data.get("topic_ids", []),
                    construct_types=data.get("construct_types", []),
                    priority=data.get("priority", 2),
                    category=data.get("category", "syntax_rule"),
                ))

        return self._rule_store.index_rules(nuggets)

    def index_extracted_examples(self, extracted) -> int:
        """Re-index extracted examples from Stage 1."""
        self._init_stores()
        return self._example_store.index_examples(extracted.examples)

    def retrieve_for_assembly(self, extracted, topic_definitions: dict = None) -> dict:
        """Retrieve relevant rules and examples for prompt assembly.

        Returns {"rules": [str, ...], "examples": {construct_type: [str, ...]}}
        """
        self._init_stores()
        rag_config = self._config
        rules_per = rag_config.get("rules_per_section", 15)
        examples_per = rag_config.get("examples_per_section", 3)
        mmr_lambda = rag_config.get("mmr_lambda", 0.5)

        detected_constructs = list(extracted.keywords_found)
        construct_types_from_examples = list(extracted.examples.keys())
        all_constructs = list(set(detected_constructs + construct_types_from_examples))

        # Retrieve relevant rules
        seen_rule_content = set()
        all_rules = []

        for construct in all_constructs[:20]:
            results = self._rule_store.query_by_topic(
                topic_id=construct,
                construct_types=[construct],
                n_results=rules_per,
            )
            for r in results:
                content_key = r["content"][:200]
                if content_key not in seen_rule_content:
                    seen_rule_content.add(content_key)
                    all_rules.append(r)

        all_rules.sort(key=lambda x: (-x.get("priority", 2) * -1, -x["score"]))
        # priority 1 first (lower number = higher priority), then by score
        all_rules.sort(key=lambda x: (x.get("priority", 2), -x["score"]))

        # Retrieve diverse examples via MMR
        all_examples = {}
        for construct in construct_types_from_examples[:15]:
            query = f"{construct} syntax example"
            mmr_results = self._example_store.query_mmr(
                query=query,
                construct_type=construct,
                n_results=examples_per,
                lambda_mult=mmr_lambda,
            )
            if mmr_results:
                all_examples[construct] = [r["content"] for r in mmr_results]

        rule_texts = [r["content"] for r in all_rules]

        return {
            "rules": rule_texts,
            "examples": all_examples,
            "stats": {
                "rules_retrieved": len(rule_texts),
                "example_types": len(all_examples),
                "constructs_queried": len(all_constructs),
            },
        }
