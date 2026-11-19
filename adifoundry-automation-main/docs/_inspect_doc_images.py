from docx import Document

paths = [
    r"c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_001.docx",
    r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs\Platform_Service_Document_001.docx",
]

for p in paths:
    d = Document(p)
    print("="*80)
    print(p)
    print("paragraphs:", len(d.paragraphs))
    print("inline_shapes:", len(d.inline_shapes))
    for i, s in enumerate(d.inline_shapes, 1):
        print(f"shape {i}: width={s.width}, height={s.height}")
