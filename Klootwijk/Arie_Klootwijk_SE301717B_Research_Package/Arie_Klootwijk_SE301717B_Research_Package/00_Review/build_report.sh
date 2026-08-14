#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

command -v pandoc >/dev/null 2>&1 || { echo "pandoc is required" >&2; exit 1; }
command -v xelatex >/dev/null 2>&1 || { echo "xelatex is required" >&2; exit 1; }

pandoc Review_Source.md \
  --from=markdown+raw_tex+link_attributes \
  --pdf-engine=xelatex \
  --output=Arie_Klootwijk_SE301717B_Technical_Review.pdf

echo "Built: $(pwd)/Arie_Klootwijk_SE301717B_Technical_Review.pdf"
