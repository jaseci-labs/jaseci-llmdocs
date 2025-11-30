import re
import yaml
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from llm import LLM

class Merger:
    def __init__(self, llm: LLM, config: dict):
        self.llm = llm
        self.in_dir = Path(config.get('extraction', {}).get('output_dir', 'output/1_extracted'))
        self.out_dir = Path(config.get('merge', {}).get('output_dir', 'output/2_merged'))
        self.out_dir.mkdir(parents=True, exist_ok=True)
        
        root = Path(__file__).parents[1]
        with open(root / "config/stage2_merge_prompt.txt") as f: self.prompt = f.read()
        with open(root / "config/topics.yaml") as f: self.topics = yaml.safe_load(f)['topics']

    def run(self):
        self.out_dir.mkdir(parents=True, exist_ok=True)
        files = [f for f in self.in_dir.glob("*.md") if f.stat().st_size > 0]
        print(f"Stage 2: Merging {len(files)} topics...")
        
        with ThreadPoolExecutor(max_workers=16) as pool:
            list(tqdm(pool.map(self.process, files), total=len(files)))

    def process(self, path: Path):
        topic = path.stem
        name = self.topics.get(topic, {}).get('name', topic)
        try:
            content = path.read_text().strip()
            merged = self.merge_content(content, name)
            if merged:
                (self.out_dir / f"{topic}.txt").write_text(f"# {name}\n\n{merged}")
        except Exception as e:
            print(f"Error {topic}: {e}")

    def merge_content(self, text: str, topic: str) -> str:
        # Direct merge if small enough
        if len(text) < 20000:
            return self.llm.query(text, f"Topic: {topic}\n\n{self.prompt}")

        tqdm.write(f"  Topic '{topic}' large ({len(text)} chars), splitting...")

        # Chunking logic
        chunks = []
        curr = []
        for part in re.split(r'(?=\n## )', text):
            if len("".join(curr) + part) > 15000:
                chunks.append("".join(curr))
                curr = []
            curr.append(part)
        if curr: chunks.append("".join(curr))

        if len(chunks) == 1: # Fallback split
             chunks = [text[i:i+15000] for i in range(0, len(text), 15000)]

        # Parallel Merge
        merged_parts = []
        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = []
            for chunk in chunks:
                futures.append(pool.submit(self.llm.query, chunk, f"Topic: {topic}\n\n{self.prompt}"))
            
            merged_parts = [f.result() for f in futures if f.result().strip()]

        return "\n\n".join(merged_parts)