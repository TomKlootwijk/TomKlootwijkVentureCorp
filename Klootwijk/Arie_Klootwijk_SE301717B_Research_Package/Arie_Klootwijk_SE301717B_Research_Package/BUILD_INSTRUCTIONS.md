# Build instructions

## Technical review PDF

Required:

- Pandoc
- XeLaTeX with common packages used by `report_header.tex`
- Lato font family
- DejaVu Sans Mono

Run:

```bash
cd 00_Review
./build_report.sh
```

The Markdown source uses relative image paths into `../05_Figures/`; preserve the package directory structure.

## Figures

Required Python packages:

- NumPy
- pandas
- Matplotlib
- Pillow
- RDKit
- PyMuPDF (optional, used only to regenerate the two documentary patent crops)

Run from the package root:

```bash
python 05_Figures/build_figures.py
```

The supplied PNGs are the exact figures used in the delivered report. The script is portable within this package and reads CSV/PDF inputs by relative path. Without PyMuPDF, the analytical figures are regenerated and the two bundled documentary crops are left in place. Regeneration may produce small rendering differences across library versions.

## Integrity check

On Linux or macOS:

```bash
sha256sum -c SHA256SUMS.txt
```

On systems without `sha256sum`, use an equivalent SHA-256 verification utility and compare against the recorded relative paths and hashes.
