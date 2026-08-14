#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD="$ROOT/07_Build"
REPORT="$ROOT/00_Report"
RENDER="$BUILD/report_render_final"
DOCX="$REPORT/Klootwijk_Generational_Topology_Comparative_Review.docx"
PDF_NAME="Klootwijk_Generational_Topology_Comparative_Review.pdf"

python "$BUILD/build_supporting_files.py"
python "$BUILD/build_report.py"

rm -rf "$RENDER"
mkdir -p "$RENDER"
python /home/oai/skills/pdfs/scripts/lo_convert_to_pdf.py "$DOCX" --out_dir "$RENDER"
python /home/oai/skills/pdfs/scripts/render_pdf.py "$RENDER/$PDF_NAME" \
  --out_dir "$RENDER" --prefix page --dpi 160 --engine pdfium
cp "$RENDER/$PDF_NAME" "$REPORT/$PDF_NAME"

python /home/oai/skills/pdfs/scripts/pdf_preflight.py "$REPORT/$PDF_NAME" \
  > "$BUILD/pdf_preflight_report.txt"
python "$BUILD/finalize_package.py"

echo "Built: $REPORT/$PDF_NAME"
