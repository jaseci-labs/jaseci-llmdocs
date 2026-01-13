import re
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from .llm import LLM


class CodeBlockExtractor:
    """Extracts and preserves code blocks during processing."""

    def __init__(self):
        self.blocks = {}

    def extract(self, text):
        """Replace code blocks with placeholders, return modified text."""
        self.blocks = {}
        counter = [0]

        def replace(match):
            block = match.group(0)
            key = f"__CODE_BLOCK_{counter[0]}__"
            self.blocks[key] = block
            counter[0] += 1
            return key

        result = re.sub(r'```[\s\S]*?```', replace, text)
        return result

    def restore(self, text):
        """Restore code blocks from placeholders."""
        result = text
        for key, block in self.blocks.items():
            result = result.replace(key, block)
        return result


class Deduplicator:
    """Removes truly redundant content while preserving unique information."""

    def __init__(self):
        self.seen_hashes = set()
        self.seen_code = set()

    def normalize(self, text):
        """Normalize text for comparison."""
        text = re.sub(r'\s+', ' ', text.lower().strip())
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def hash_content(self, text):
        """Create hash of normalized content."""
        normalized = self.normalize(text)
        return hashlib.md5(normalized.encode()).hexdigest()[:16]

    def is_duplicate_paragraph(self, text):
        """Check if paragraph is duplicate."""
        if len(text.strip()) < 50:
            return False

        h = self.hash_content(text)
        if h in self.seen_hashes:
            return True
        self.seen_hashes.add(h)
        return False

    def is_duplicate_code(self, code):
        """Check if code block is duplicate."""
        normalized = re.sub(r'\s+', '', code)
        h = hashlib.md5(normalized.encode()).hexdigest()[:16]
        if h in self.seen_code:
            return True
        self.seen_code.add(h)
        return False

    def deduplicate(self, text):
        """Remove duplicate paragraphs and code blocks."""
        code_extractor = CodeBlockExtractor()
        text_only = code_extractor.extract(text)

        paragraphs = re.split(r'\n\n+', text_only)
        unique_paragraphs = []

        for para in paragraphs:
            if para.startswith('__CODE_BLOCK_'):
                key = para.strip()
                if key in code_extractor.blocks:
                    code = code_extractor.blocks[key]
                    if not self.is_duplicate_code(code):
                        unique_paragraphs.append(key)
            elif para.startswith('#'):
                unique_paragraphs.append(para)
            elif not self.is_duplicate_paragraph(para):
                unique_paragraphs.append(para)

        result = '\n\n'.join(unique_paragraphs)
        return code_extractor.restore(result)


class FillerRemover:
    """Removes filler phrases while keeping natural language intact."""

    FILLER_PATTERNS = [
        (r"let'?s\s+(see|look at|consider|explore|take a look at)\s+", ''),
        (r"here\s+(we|is|are)\s+(going to|gonna)?\s*", ''),
        (r"now\s+(we|let's|we'll)\s+", ''),
        (r"in\s+this\s+(section|example|case),?\s*", ''),
        (r"as\s+(you\s+can\s+see|shown|mentioned|noted)\s*(above|below)?,?\s*", ''),
        (r"it\s+is\s+(important|worth|useful)\s+to\s+(note|mention)\s+that\s+", ''),
        (r"please\s+note\s+that\s+", ''),
        (r"keep\s+in\s+mind\s+that\s+", ''),
        (r"it\s+should\s+be\s+noted\s+that\s+", ''),
        (r"the\s+following\s+(example|code|snippet)\s+(shows|demonstrates|illustrates)\s+", ''),
        (r"for\s+instance,?\s*", ''),
        (r"basically,?\s*", ''),
        (r"essentially,?\s*", ''),
        (r"simply\s+put,?\s*", ''),
        (r"in\s+other\s+words,?\s*", ''),
        (r"as\s+we\s+(can\s+)?see,?\s*", ''),
    ]

    def remove_fillers(self, text):
        """Remove filler phrases while preserving meaning."""
        result = text
        for pattern, replacement in self.FILLER_PATTERNS:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        result = re.sub(r'\s+', ' ', result)
        result = re.sub(r'\n ', '\n', result)
        result = re.sub(r' +', ' ', result)

        return result.strip()


class ContentOrganizer:
    """Organizes content hierarchically by topic."""

    def __init__(self):
        self.sections = {}

    def parse_sections(self, text):
        """Parse text into sections by headers."""
        lines = text.split('\n')
        current_section = "Overview"
        current_content = []

        for line in lines:
            if line.startswith('## '):
                if current_content:
                    self.sections[current_section] = '\n'.join(current_content)
                current_section = line[3:].strip()
                current_content = []
            elif line.startswith('# '):
                if current_content:
                    self.sections[current_section] = '\n'.join(current_content)
                current_section = line[2:].strip()
                current_content = []
            else:
                current_content.append(line)

        if current_content:
            self.sections[current_section] = '\n'.join(current_content)

        return self.sections


class Reducer:
    """Intelligent documentation reducer using natural language summarization."""

    def __init__(self, llm: LLM, config: dict, on_progress=None):
        self.llm = llm
        self.on_progress = on_progress or (lambda *a: None)
        self.in_dir = Path(config.get('merge', {}).get('output_dir', 'output/2_merged'))
        self.out_dir = Path(config.get('hierarchical_merge', {}).get('output_dir', 'output/3_hierarchical'))
        self.out_dir.mkdir(parents=True, exist_ok=True)

        hier_cfg = config.get('hierarchical_merge', {})
        self.target_ratio = hier_cfg.get('target_ratio', 5)
        self.max_workers = hier_cfg.get('max_workers', 8)
        self.chunk_size = hier_cfg.get('chunk_size', 8000)

        self.code_extractor = CodeBlockExtractor()
        self.deduplicator = Deduplicator()
        self.filler_remover = FillerRemover()
        self.organizer = ContentOrganizer()

        root = Path(__file__).parents[2]
        prompt_path = root / "config/stage3_reduce_prompt.txt"
        with open(prompt_path) as f:
            self.summarize_prompt = f.read()

    def run(self, ratio=None):
        """Execute natural language reduction pipeline."""
        self.out_dir.mkdir(parents=True, exist_ok=True)
        files = sorted(self.in_dir.glob("*.txt"))
        if not files:
            return None

        contents = {f.stem: f.read_text() for f in files}
        total_input = sum(len(c) for c in contents.values())

        total_steps = 5
        step = 0

        self.on_progress(step, total_steps, "Removing filler phrases...")
        cleaned = {}
        for name, content in contents.items():
            cleaned[name] = self.filler_remover.remove_fillers(content)
        step += 1

        self.on_progress(step, total_steps, "Deduplicating content...")
        deduped = {}
        for name, content in cleaned.items():
            deduped[name] = self.deduplicator.deduplicate(content)
        step += 1

        self.on_progress(step, total_steps, "Organizing by topic...")
        all_sections = {}
        for name, content in deduped.items():
            sections = self.organizer.parse_sections(content)
            for section_name, section_content in sections.items():
                key = f"{name}:{section_name}"
                all_sections[key] = section_content
        step += 1

        self.on_progress(step, total_steps, "Summarizing with LLM...")
        combined = '\n\n'.join(f"## {name}\n{content}" for name, content in deduped.items())
        chunks = self._split_into_chunks(combined)
        summarized = self._parallel_summarize(chunks)
        step += 1

        self.on_progress(step, total_steps, "Finalizing output...")
        final_output = '\n\n'.join(summarized)
        final_output = self._final_cleanup(final_output)

        out_path = self.out_dir / "unified_doc.txt"
        out_path.write_text(final_output)

        total_output = len(final_output)
        achieved_ratio = total_input / max(total_output, 1)

        self.on_progress(total_steps, total_steps,
                        f"Complete: {achieved_ratio:.1f}x reduction")

        intermediate_dir = self.out_dir / "intermediate"
        intermediate_dir.mkdir(exist_ok=True)
        (intermediate_dir / "1_cleaned.txt").write_text(
            '\n\n---\n\n'.join(f"# {k}\n{v}" for k, v in cleaned.items()))
        (intermediate_dir / "2_deduped.txt").write_text(
            '\n\n---\n\n'.join(f"# {k}\n{v}" for k, v in deduped.items()))

        return {
            'success': True,
            'output_path': str(out_path),
            'input_size': total_input,
            'output_size': total_output,
            'compression_ratio': achieved_ratio
        }

    def _split_into_chunks(self, text):
        """Split text into chunks, preserving code blocks and sections."""
        chunks = []
        current_chunk = []
        current_size = 0

        code_extractor = CodeBlockExtractor()
        text = code_extractor.extract(text)

        paragraphs = re.split(r'\n\n+', text)

        for para in paragraphs:
            para_with_code = code_extractor.restore(para)
            para_size = len(para_with_code)

            if para.startswith('## ') or para.startswith('# '):
                if current_chunk and current_size > self.chunk_size // 2:
                    chunks.append(code_extractor.restore('\n\n'.join(current_chunk)))
                    current_chunk = []
                    current_size = 0

            if current_size + para_size > self.chunk_size and current_chunk:
                chunks.append(code_extractor.restore('\n\n'.join(current_chunk)))
                current_chunk = [para]
                current_size = para_size
            else:
                current_chunk.append(para)
                current_size += para_size

        if current_chunk:
            chunks.append(code_extractor.restore('\n\n'.join(current_chunk)))

        return chunks

    def _parallel_summarize(self, chunks):
        """Summarize chunks in parallel using LLM."""
        results = [None] * len(chunks)

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futures = {
                pool.submit(self._summarize_chunk, chunk, i): i
                for i, chunk in enumerate(chunks)
            }

            for future in as_completed(futures):
                idx = futures[future]
                try:
                    results[idx] = future.result()
                except Exception as e:
                    print(f"Summarization error for chunk {idx}: {e}")
                    results[idx] = chunks[idx]

        return [r for r in results if r]

    def _summarize_chunk(self, chunk, idx):
        """Summarize a single chunk via LLM."""
        if len(chunk) < 200:
            return chunk

        code_blocks = re.findall(r'```[\s\S]*?```', chunk)
        if len('\n'.join(code_blocks)) > len(chunk) * 0.7:
            return chunk

        try:
            result = self.llm.query(chunk, self.summarize_prompt)
            if result and len(result) > 100:
                return result
            return chunk
        except Exception as e:
            print(f"LLM error: {e}")
            return chunk

    def _final_cleanup(self, text):
        """Final cleanup pass on the output."""
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+\n', '\n', text)
        text = re.sub(r'\n[ \t]+', '\n', text)

        lines = text.split('\n')
        cleaned_lines = []
        prev_empty = False

        for line in lines:
            is_empty = not line.strip()
            if is_empty and prev_empty:
                continue
            cleaned_lines.append(line)
            prev_empty = is_empty

        return '\n'.join(cleaned_lines).strip()
