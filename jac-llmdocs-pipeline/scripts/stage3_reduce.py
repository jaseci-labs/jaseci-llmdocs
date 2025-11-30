import math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from llm import LLM

class Reducer:
    def __init__(self, llm: LLM, config: dict):
        self.llm = llm
        self.in_dir = Path(config.get('merge', {}).get('output_dir', 'output/2_merged'))
        self.out_dir = Path(config.get('hierarchical_merge', {}).get('output_dir', 'output/3_hierarchical'))
        self.out_dir.mkdir(parents=True, exist_ok=True)
        
        root = Path(__file__).parents[1]
        with open(root / "config/stage3_reduce_prompt.txt") as f: self.prompt = f.read()

    def run(self, ratio=4):
        self.out_dir.mkdir(parents=True, exist_ok=True)
        files = sorted(self.in_dir.glob("*.txt"))
        if not files: return
        
        print(f"Stage 3: Reducing {len(files)} files (Ratio {ratio}:1)...")
        current = [f.read_text() for f in files]
        
        pass_num = 1
        while len(current) > 1:
            print(f"  Pass {pass_num}: {len(current)} -> {math.ceil(len(current)/ratio)}")
            groups = ["\n\n".join(current[i:i+ratio]) for i in range(0, len(current), ratio)]
            
            with ThreadPoolExecutor(max_workers=8) as pool:
                current = list(pool.map(self.merge_group, groups))
            pass_num += 1

        out_path = self.out_dir / "unified_doc.txt"
        out_path.write_text(current[0])
        print(f"  Saved to {out_path}")
        return {'success': True, 'output_path': str(out_path)}

    def merge_group(self, content):
        return self.llm.query(content, self.prompt)