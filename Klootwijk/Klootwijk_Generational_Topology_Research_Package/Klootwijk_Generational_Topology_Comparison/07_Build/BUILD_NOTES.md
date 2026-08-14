# Build and verification notes

## Pipeline

1. `build_supporting_files.py` regenerates machine-readable tables, figures, prototype schemas, and synthetic demonstrations.
2. `build_report.py` regenerates the DOCX and Markdown report from local package content.
3. `/home/oai/skills/docx/render_docx.py` converts the DOCX to PDF and renders every page to PNG.
4. `/home/oai/skills/pdfs/scripts/pdf_preflight.py` checks that the PDF opens, is not encrypted, and has a usable text layer.
5. `finalize_package.py` generates the manifest and SHA-256 checksums.

## Verified final report

- Format: A4 PDF 1.7
- Pages: 34
- Searchable text: yes
- Tagged PDF: yes
- Encryption: none
- Visual QA: every rendered page was reviewed; no clipping, broken tables, blank trailing pages, missing glyphs, or split table rows remained.

## Main software dependencies

- Python 3
- python-docx
- matplotlib
- Pillow
- LibreOffice headless
- Poppler/PDF utilities

## Reproducibility limits

The source PDFs are family-provided design records. The external bibliography is a citation map; full third-party papers are not redistributed. The prototype time series and event logs are synthetic and use fixed random seeds. They demonstrate file formats and event semantics, not physical performance.
