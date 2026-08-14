#!/usr/bin/env python3
from pathlib import Path
import csv, json, hashlib, sys

root = Path(__file__).resolve().parents[1]
required = [
    "README.md",
    "Corpus_Decoder_Report.pdf",
    "Corpus_Decoder_Report.html",
    "data/alchemical_to_technical_lexicon.csv",
    "data/equations_and_operators.csv",
    "data/claims_evidence_matrix.csv",
    "data/concept_ontology.json",
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    print("Missing:", missing)
    sys.exit(1)

with open(root/"data/alchemical_to_technical_lexicon.csv", newline="", encoding="utf-8") as f:
    lex = list(csv.DictReader(f))
with open(root/"data/equations_and_operators.csv", newline="", encoding="utf-8") as f:
    eq = list(csv.DictReader(f))
with open(root/"data/claims_evidence_matrix.csv", newline="", encoding="utf-8") as f:
    claims = list(csv.DictReader(f))
with open(root/"data/concept_ontology.json", encoding="utf-8") as f:
    ontology = json.load(f)

print(f"Lexicon rows: {len(lex)}")
print(f"Equation rows: {len(eq)}")
print(f"Claim rows: {len(claims)}")
print(f"Ontology nodes: {len(ontology['nodes'])}")
print("Validation OK")
