# Report source

`Unified_Geometric_Topological_Substrate.pdf` is the compiled 45-page report. The source is `main.tex`; the three `generated_*.tex` files are produced from CSV files under `../specs/` by `generate_tables.py`.

Build from the package root:

```bash
python report/generate_tables.py
cd report
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

The original source PDFs are intentionally absent. Source traceability is expressed as source IDs S1-S9 and page ranges in the concept inventory and source notes.
