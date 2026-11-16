from docx import Document
from pathlib import Path
import re

repo_root = Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template")
platform_doc = Path(r"c:\Users\XSPriyaGa\Downloads\Platform_Service_Document_FINAL_v2.docx")
transcript_doc = Path(r"c:\Users\XSPriyaGa\Downloads\Call with Kamaraj,Manikandan,IN-Bangalore (4).docx")

for src, label in [(platform_doc, 'PLATFORM_DOC'), (transcript_doc, 'TRANSCRIPT_DOC')]:
    print('='*120)
    print(label, src)
    print('='*120)
    d = Document(src)

    print('\nHEADINGS:')
    for p in d.paragraphs:
        t = p.text.strip()
        if t and p.style and p.style.name.startswith('Heading'):
            print(f"- {p.style.name}: {t}")

    print('\nTABLES:')
    print(len(d.tables))
    for i, table in enumerate(d.tables, 1):
        print(f"Table {i} rows={len(table.rows)} cols={len(table.columns)}")
        for r in table.rows[:3]:
            print(' | '.join(c.text.strip() for c in r.cells))

    print('\nPARAGRAPHS (non-empty, first 260):')
    count = 0
    for p in d.paragraphs:
        t = p.text.strip()
        if t:
            count += 1
            print(f"{count:03d}. {t}")
            if count >= 260:
                break

    # path-like patterns
    text = '\n'.join(p.text for p in d.paragraphs if p.text)
    path_pattern = r"(?:\.github/workflows/[\w\-\.]+|(?:environments|iac|docs|src_var|images)/[\w\-\./]+|[\w\-]+\.tfvars|[\w\-]+\.ya?ml|[\w\-]+\.tf)"
    found = sorted(set(re.findall(path_pattern, text)))
    print('\nPATH-LIKE REFERENCES:')
    for p in found:
        print('-', p)

    print('\nTOTAL PARAGRAPHS:', len(d.paragraphs))

# Validate all repo files list snapshot for quick grepping
print('='*120)
print('REPO FILE SNAPSHOT')
print('='*120)
for p in sorted(repo_root.rglob('*')):
    if p.is_file() and '.git' not in p.parts:
        rel = p.relative_to(repo_root).as_posix()
        print(rel)
