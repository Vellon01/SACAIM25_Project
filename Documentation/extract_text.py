import sys
import os

def install_and_import(package, import_name):
    import importlib
    try:
        importlib.import_module(import_name)
    except ImportError:
        import subprocess
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[import_name] = importlib.import_module(import_name)

try:
    install_and_import('python-docx', 'docx')
    install_and_import('pypdf', 'pypdf')

    doc_dir = r"c:\Users\vello\OneDrive\Desktop\imp\SACAIM\SACAIM25_Project\Documentation"

    print("Extracting docx...")
    doc = docx.Document(os.path.join(doc_dir, 'Domain_Knowledge.docx'))
    with open(os.path.join(doc_dir, 'domain_text.txt'), 'w', encoding='utf-8') as f:
        for para in doc.paragraphs:
            f.write(para.text + '\n')

    def extract_pdf(pdf_path, txt_path):
        print(f"Extracting {pdf_path}...")
        reader = pypdf.PdfReader(pdf_path)
        with open(txt_path, 'w', encoding='utf-8') as f:
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    f.write(text + '\n')

    extract_pdf(os.path.join(doc_dir, '232107_Evita.pdf'), os.path.join(doc_dir, 'evita_text.txt'))
    extract_pdf(os.path.join(doc_dir, 'Akhil W-192003.pdf'), os.path.join(doc_dir, 'akhil_text.txt'))

    print("Extraction complete")
except Exception as e:
    print(f"Error: {e}")
