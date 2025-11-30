#!/usr/bin/env python3
import sys
import yaml
import shutil
import glob
from pathlib import Path

from llm import LLM
from stage1_extract import Extractor
from stage2_merge import Merger
from stage3_reduce import Reducer
from stage4_compress import Compressor

class Pipeline:
    def __init__(self, cfg_path):
        self.root = Path(__file__).parents[1]
        with open(cfg_path) as f: self.cfg = yaml.safe_load(f)
        self.src = Path(self.cfg['source_dir'])
        
        # Init Components with stage-specific LLMs
        self.extractor = Extractor(LLM(self.cfg, self.cfg.get('extraction')), self.cfg)
        self.merger = Merger(LLM(self.cfg, self.cfg.get('merge')), self.cfg)
        self.reducer = Reducer(LLM(self.cfg, self.cfg.get('hierarchical_merge')), self.cfg)
        self.compressor = Compressor(LLM(self.cfg, self.cfg.get('ultra_compression')), self.cfg)

    def run(self):
        # Clean
        out = self.root / "output"
        if out.exists(): shutil.rmtree(out)
        
        # Stages
        self.extractor.run(self.src, self.cfg['processing'].get('skip_patterns'))
        self.merger.run()
        res = self.reducer.run(self.cfg['hierarchical_merge']['ratio'])
        if res:
            self.compressor.run(Path(res['output_path']), "jac_docs_final.txt")
            self.release()

    def release(self):
        rel_dir = self.root.parent / "release" / "0.4"
        rel_dir.mkdir(parents=True, exist_ok=True)
        
        src = self.compressor.out_dir / "jac_docs_final.txt"
        if not src.exists(): return

        # Versioning
        nums = [int(f.stem.replace("jac_docs_final", "") or 1) 
                for f in rel_dir.glob("jac_docs_final*.txt") 
                if f.stem.replace("jac_docs_final", "").isdigit() or f.stem == "jac_docs_final"]
        
        ver = max(nums) + 1 if nums else 1
        dest = rel_dir / f"jac_docs_final{ver}.txt"
        shutil.copy(src, dest)
        print(f"Stage 5: Released to {dest}")

if __name__ == '__main__':
    default_config = Path(__file__).parents[1] / "config" / "config.yaml"
    Pipeline(sys.argv[1] if len(sys.argv) > 1 else default_config).run()