import os
from PIL import Image
import pytesseract
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.text import partition_text
from unstructured.partition.image import partition_image


def process_file(file_path: str):
    """
    Reads PDF, text, or image files and extracts readable text for RAG pipeline.
    Supports: .txt, .pdf, .png, .jpg, .jpeg
    """
    try:
        ext = os.path.splitext(file_path)[1].lower()
        text = ""

        # ✅ TXT file
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

        # ✅ PDF file
        elif ext == ".pdf":
            elements = partition_pdf(filename=file_path)
            text = "\n".join([el.text for el in elements if hasattr(el, "text")])

        # ✅ Image file (OCR)
        elif ext in [".png", ".jpg", ".jpeg"]:
            try:
                # Path to tesseract (update if installed elsewhere)
                pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
            except Exception as e:
                return {"status": "error", "message": f"OCR failed: {str(e)}"}

        else:
            return {"status": "error", "message": f"Unsupported file type: {ext}"}

        # ✅ Clean result
        text = text.strip()
        if not text:
            return {"status": "error", "message": "No readable text found in file"}

        # ✅ Create preview sample
        content_sample = text[:500] + "..." if len(text) > 500 else text

        return {
            "status": "success",
            "full_text": text,
            "content_sample": content_sample
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}