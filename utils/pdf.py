from fitz import open as fitz_open
import os
import numpy as np
import cv2


def process_pdf(data_path, pdf_path):
    """
    Processes a PDF file and extracts each page as an image, saving them to a specified directory.

    Args:
        data_path (str): The base directory where the extracted images will be saved.
        pdf_path (str): The path to the PDF file to be processed.

    Raises:
        Exception: If an error occurs during the processing of the PDF.

    """
    try:
        pdf_document = fitz_open(pdf_path)
        file_name = pdf_path.split("/")[-1].split(".")[0]
        if not os.path.exists(f"./{data_path}/temp/{file_name}"):
            os.makedirs(f"./{data_path}/temp/{file_name}")

        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            pix = page.get_pixmap()
            if pix is None:
                print(f"Warning: Could not get pixmap for page {page_number + 1}")
                continue
            if pix.samples is None:
                print(f"Warning: Pixmap samples are None for page {page_number + 1}")
                continue
            try:
                image_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                    pix.height, pix.width, 3
                )
            except ValueError as e:
                print(f"Error: {e} for page {page_number + 1}")
                continue
            cv2.imwrite(
                f"./{data_path}/temp/{file_name}/{file_name}_{page_number + 1}.png",
                image_array,
            )
        pdf_document.close()
    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")


def parse_pdf_folder(pdf_folder):
    """
    Parses a folder containing PDF files and processes each PDF.

    Args:
        pdf_folder (str): The path to the folder containing PDF files.

    Returns:
        None
    """
    pdfs = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    for pdf in pdfs:
        process_pdf(pdf_folder, f"{pdf_folder}/{pdf}")
