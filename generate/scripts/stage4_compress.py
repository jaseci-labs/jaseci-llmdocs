import re
from pathlib import Path
from llm import LLM

class Compressor:
    def __init__(self, llm: LLM, config: dict):
        self.llm = llm
        self.out_dir = Path(config.get('ultra_compression', {}).get('output_dir', 'output/4_final'))
        self.out_dir.mkdir(parents=True, exist_ok=True)
        
        root = Path(__file__).parents[1]
        with open(root / "config/stage4_compress_prompt.txt") as f: self.prompt = f.read()

    def run(self, in_path: Path, out_name: str):
        self.out_dir.mkdir(parents=True, exist_ok=True)
        print("Stage 4: Compressing...")
        text = in_path.read_text()
        
        # 1. LLM Format
        formatted = self.llm.query(text, self.prompt)
        
        # 2. Regex Minify
        lines = []
        for line in formatted.split('\n'):
            line = line.strip()
            if not line: continue
            if line.startswith('#') or line.startswith('```') or line.startswith('-'):
                lines.append(line)
            else:
                # Merge plain paragraphs
                if lines and not (lines[-1].startswith('#') or lines[-1].startswith('```') or lines[-1].startswith('-')):
                    lines[-1] += " " + line
                else:
                    lines.append(line)
        
        final = "\n".join(lines)
        (self.out_dir / out_name).write_text(final)
        print(f"  Saved {len(text)} -> {len(final)} chars")
        return {'success': True}