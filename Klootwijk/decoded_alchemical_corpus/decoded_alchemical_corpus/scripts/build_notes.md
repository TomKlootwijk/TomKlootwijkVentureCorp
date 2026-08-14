# Build Notes

- Source PDFs were read page by page with PyMuPDF.
- The PDF report was authored as HTML and rendered with WeasyPrint, then rendered to PNG for visual inspection.
- 2D chemical diagrams and MOL/SDF/PDB files were generated with RDKit from standard SMILES.
- 3D conceptual geometry was generated parametrically and exported as OBJ.
- SVG diagrams are explicit technical schematics, not AI-generated imagery.
- External scientific grounding is isolated in `references/primary_references.md`.
- No OCR was used; the PDFs contained extractable text.
- Original PDFs are not duplicated in the ZIP.
