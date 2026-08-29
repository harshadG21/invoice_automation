from paddleocr import PaddleOCR


# Initialize OCR once
ocr = PaddleOCR(
    lang="en"
)


def extract_text_from_file(file_path):
    """
    Extract text from an invoice PDF or image.
    """

    result = ocr.predict(file_path)

    extracted_text = []

    for page in result:

        texts = page.get("rec_texts", [])

        for text in texts:
            extracted_text.append(text)

    return extracted_text


def extract_text_as_string(file_path):
    """
    Extract OCR text and return it as one string.
    """

    texts = extract_text_from_file(file_path)

    return "\n".join(texts)