# Publication Plan - August 16, 2026

## Recommended release sequence

1. **GitHub repository** - living implementation, paper, SVG architecture, tests, references, and version history: https://github.com/nicholasastjohn/Persistent_Agency. Keep public milestones tagged as releases.
2. **Zenodo** - archive a fixed GitHub release and obtain a digital object identifier.
3. **arXiv, primary category `cs.AI`** - primary scholarly preprint. Convert to TeX/LaTeX before submission if practical; the PDF remains the human-review release candidate.
4. **Hugging Face Papers / Daily Papers** - after an arXiv identifier exists, use for AI-community discovery and link future code, models, datasets, or demos to the paper.
5. **LessWrong** - use for adversarial discussion rather than archival publication. Adapt the discussion draft to the site's current authorship and model-assistance rules before posting.
6. **Transactions on Machine Learning Research** - target after empirical results. The peer-review version should add controlled baseline results, ablations, cost and latency data, failure modes, and reproducibility artifacts, and be converted to the venue's required format.

## Current manuscript status

The v1.2 manuscript is appropriate as an **architecture preprint**, not as a paper claiming experimental validation.

## Terminology strategy

Use terms only when they sharpen a mechanism or connect the work to an active research area: **agentic systems**, **agent harness**, **long-horizon autonomy**, **continual learning**, **hierarchical memory**, **procedural memory**, **memory consolidation**, **multimodal agents**, and **inference-time computation**. Sampling **temperature** is an implementation parameter, not an architectural primitive. **Singularity** is intentionally excluded from the technical framing because it does not improve the falsifiable claim.
