# Release Audit - v1.2

Date: 2026-08-16

## Manuscript

- Title: **Persistent Agency: A Three-Loop Cognitive Architecture for Artificial General Intelligence**.
- Code Availability points directly to the canonical repository: https://github.com/nicholasastjohn/Persistent_Agency.
- 8 rendered pages.
- All 8 Word-rendered pages visually inspected after the final repository-link correction.
- The emitted PDF was separately rendered as 8 pages for PDF verification.
- No tracked insertions or deletions.
- No reviewer comments.
- No stale `Persistant_Agency` repository references remain in the Word package.
- Numeric references and scientific section hierarchy retained.
- Accessibility audit: 0 high, 0 medium, 1 low finding. The sole low finding is intentional: the Code Availability section displays the canonical GitHub URL as raw hyperlink text so the repository is directly visible in print and PDF.
- The manuscript explicitly identifies itself as an architecture proposal with predicted rather than observed results.

## Figure

- Final v1.2 architecture included as editable SVG and high-resolution PNG.
- Reactive, deliberative, consolidation, and information/control paths use distinct visual encodings.
- Arrow routing was revised to minimize line crossings and avoid component text.

## Code

- Deterministic architecture smoke test only; no claim of intelligence.
- `PYTHONPATH=src python -m pytest -q`: 4 tests passed.
- `PYTHONPATH=src python examples/run_smoke_test.py`: successful.
- Tests cover endogenous state progression, human interruption, scheduled mode transitions, and consolidation into long-term memory.

## Repository

- Canonical repository: https://github.com/nicholasastjohn/Persistent_Agency
- Repository spelling verified as **Persistent_Agency** on 2026-08-16.

## Remaining author choices

- No software license has been selected. Add one only if and when third-party reuse should be affirmatively permitted.
- Add a Zenodo digital object identifier to citation metadata after the archival release exists.
