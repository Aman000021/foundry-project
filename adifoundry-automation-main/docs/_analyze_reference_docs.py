from docx import Document

paths = [
    r"c:\Users\XSPriyaGa\Downloads\Call with Kamaraj,Manikandan,IN-Bangalore (3).docx",
    r"c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_001.docx",
]

for p in paths:
    print("=" * 100)
    print("FILE:", p)
    print("=" * 100)
    doc = Document(p)

    print("\nHEADINGS:")
    for para in doc.paragraphs:
        if para.style and para.style.name.startswith("Heading"):
            txt = para.text.strip()
            if txt:
                print(f"- {para.style.name}: {txt}")

    print("\nNON-EMPTY PARAGRAPHS (first 220):")
    count = 0
    for para in doc.paragraphs:
        txt = para.text.strip()
        if txt:
            print(f"{count+1:03d}. {txt}")
            count += 1
            if count >= 220:
                break

    print("\nTOTAL PARAGRAPHS:", len(doc.paragraphs))
