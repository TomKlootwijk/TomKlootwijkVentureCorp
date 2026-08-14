from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT / 'specs'
OUT = Path(__file__).resolve().parent


def esc(s: str) -> str:
    repl = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '≤': r'$\leq$',
        '≥': r'$\geq$',
        'χ': r'$\chi$',
        '∩': r'$\cap$',
        '→': r'$\rightarrow$',
        'Φ': r'$\Phi$',
        'φ': r'$\phi$',
        'π': r'$\pi$',
        'ρ': r'$\rho$',
        'θ': r'$\theta$',
        'Δ': r'$\Delta$',
        '∈': r'$\in$',
        '×': r'$\times$',
    }
    out = []
    for ch in s:
        out.append(repl.get(ch, ch))
    return ''.join(out)


def status_macro(status: str) -> str:
    key = status.lower().strip()
    mapping = {
        'retain': r'\statusretain',
        'translate': r'\statustranslate',
        'demote': r'\statusdemote',
        'correct': r'\statuscorrect',
        'reject': r'\statusreject',
    }
    return mapping.get(key, esc(status))


with (SPECS / 'concept_inventory.csv').open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
lines = [
    r'\begin{landscape}',
    r'\begingroup',
    r'\scriptsize',
    r'\setlength{\tabcolsep}{2pt}',
    r'\setlength{\LTleft}{0pt}',
    r'\setlength{\LTright}{0pt}',
    r'\renewcommand{\arraystretch}{1.10}',
    r'\begin{longtable}{@{}L{12mm}L{38mm}L{54mm}L{89mm}L{24mm}L{32mm}@{}}',
    r"\caption{Complete extracted concept inventory. ``Source expression'' preserves the corpus framing; ``normalized operator'' is the technical implementation used by UGTS-0.}\label{tab:concept-inventory}\\",
    r'\toprule',
    r'ID & Category / name & Source expression & Normalized operator and qualification & Status & Source trace \\',
    r'\midrule',
    r'\endfirsthead',
    r'\multicolumn{6}{l}{\small\itshape Table \ref{tab:concept-inventory} continued}\\',
    r'\toprule',
    r'ID & Category / name & Source expression & Normalized operator and qualification & Status & Source trace \\',
    r'\midrule',
    r'\endhead',
    r'\midrule\multicolumn{6}{r}{\small continued on next page}\\',
    r'\endfoot',
    r'\bottomrule',
    r'\endlastfoot',
]
for row in rows:
    catname = r'\textbf{' + esc(row['name']) + r'}\par{\tiny\color{UGTSGray} ' + esc(row['category']) + '}'
    source = esc(row['source_expression'])
    normalized = esc(row['normalized_operator']) + r'\par{\tiny\color{UGTSGray} ' + esc(row['notes']) + '}'
    status = status_macro(row['status'])
    trace = r'{\tiny ' + esc(row['sources']) + ', pp. ' + esc(row['pages']) + '}'
    lines.append(esc(row['id']) + ' & ' + catname + ' & ' + source + ' & ' + normalized + ' & ' + status + ' & ' + trace + r' \\')
    lines.append(r'\addlinespace[2pt]')
lines.extend([r'\end{longtable}', r'\endgroup', r'\end{landscape}'])
(OUT / 'generated_concepts.tex').write_text('\n'.join(lines) + '\n', encoding='utf-8')

with (SPECS / 'claims_ledger.csv').open(newline='', encoding='utf-8') as f:
    claims = list(csv.DictReader(f))
lines = [
    r'\begin{longtable}{@{}p{0.07\textwidth}p{0.31\textwidth}p{0.13\textwidth}p{0.43\textwidth}@{}}',
    r'\caption{Claims ledger: corrections and rejected totalizing claims.}\label{tab:claims-ledger}\\',
    r'\toprule ID & Source claim & Disposition & Technical reason \\ \midrule',
    r'\endfirsthead',
    r'\multicolumn{4}{l}{\small\itshape Table \ref{tab:claims-ledger} continued}\\',
    r'\toprule ID & Source claim & Disposition & Technical reason \\ \midrule',
    r'\endhead',
    r'\midrule\multicolumn{4}{r}{\small continued on next page}\\\endfoot',
    r'\bottomrule\endlastfoot',
]
for row in claims:
    lines.append(f"{esc(row['id'])} & {esc(row['source_claim'])} & {status_macro(row['disposition'])} & {esc(row['technical_reason'])}" + r' \\')
    lines.append(r'\addlinespace[3pt]')
lines.append(r'\end{longtable}')
(OUT / 'generated_claims.tex').write_text('\n'.join(lines) + '\n', encoding='utf-8')

with (SPECS / 'sources.csv').open(newline='', encoding='utf-8') as f:
    sources = list(csv.DictReader(f))
lines = [
    r'\begingroup',
    r'\footnotesize',
    r'\setlength{\tabcolsep}{2.5pt}',
    r'\renewcommand{\arraystretch}{1.08}',
    r'\begin{longtable}{@{}L{0.055\textwidth}L{0.19\textwidth}L{0.34\textwidth}L{0.37\textwidth}@{}}',
    r'\caption{Source corpus and role in the extraction. File names are concise aliases; source IDs and page ranges are authoritative within this package.}\label{tab:sources}\\',
    r'\toprule Ref & Short name & File alias & Role \\ \midrule',
    r'\endfirsthead',
    r'\multicolumn{4}{l}{\small\itshape Table \ref{tab:sources} continued}\\',
    r'\toprule Ref & Short name & File alias & Role \\ \midrule',
    r'\endhead',
    r'\bottomrule\endlastfoot',
]
for row in sources:
    short = r'\path{' + row['short'] + r'}\par{\tiny ' + esc(row['pages']) + ' pages}'
    lines.append(esc(row['id']) + ' & ' + short + ' & ' + r'\path{' + row['filename'] + '}' + ' & ' + esc(row['role']) + r' \\')
    lines.append(r'\addlinespace[3pt]')
lines.extend([r'\end{longtable}', r'\endgroup'])
(OUT / 'generated_sources.tex').write_text('\n'.join(lines) + '\n', encoding='utf-8')

print('generated LaTeX tables')
