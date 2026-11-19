from pathlib import Path
import zipfile

sources = [
    Path(r"c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_001.docx"),
    Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs\Platform_Service_Document_005.docx"),
]

for src in sources:
    out_dir = Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs") / "extracted_images" / src.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(src, 'r') as zf:
        for name in zf.namelist():
            if name.startswith("word/media/"):
                out = out_dir / Path(name).name
                out.write_bytes(zf.read(name))
    print(src)
    print(out_dir)
