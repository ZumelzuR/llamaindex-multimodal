import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
import numpy as np
from utils.pdf import process_pdf


class TestPDFProcessing(unittest.TestCase):

    def setUp(self):
        self.test_dir = "./test_data"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("utils.pdf.fitz_open")
    @patch("utils.pdf.os.makedirs")
    @patch("utils.pdf.cv2.imwrite")
    def test_process_pdf_success(self, mock_imwrite, mock_makedirs, mock_fitz_open):
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_pix = MagicMock()
        mock_pix.samples = np.random.bytes(100 * 100 * 3)
        mock_pix.width = 100
        mock_pix.height = 100
        mock_page.get_pixmap.return_value = mock_pix
        mock_pdf.__getitem__.return_value = mock_page
        mock_pdf.page_count = 1
        mock_fitz_open.return_value = mock_pdf

        process_pdf(self.test_dir, "test.pdf")

        mock_fitz_open.assert_called_once_with("test.pdf")
        mock_makedirs.assert_called_once_with(f"./{self.test_dir}/temp/test")
        mock_imwrite.assert_called_once()

    @patch("utils.pdf.fitz_open")
    @patch("utils.pdf.os.makedirs")
    @patch("utils.pdf.cv2.imwrite")
    def test_process_pdf_missing_pixmap(
        self, mock_imwrite, mock_makedirs, mock_fitz_open
    ):
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_page.get_pixmap.return_value = None
        mock_pdf.__getitem__.return_value = mock_page
        mock_pdf.page_count = 1
        mock_fitz_open.return_value = mock_pdf

        process_pdf(self.test_dir, "test.pdf")

        mock_fitz_open.assert_called_once_with("test.pdf")
        mock_makedirs.assert_called_once_with(f"./{self.test_dir}/temp/test")
        mock_imwrite.assert_not_called()

    @patch("utils.pdf.fitz_open")
    @patch("utils.pdf.os.makedirs")
    @patch("utils.pdf.cv2.imwrite")
    def test_process_pdf_missing_samples(
        self, mock_imwrite, mock_makedirs, mock_fitz_open
    ):
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_pix = MagicMock()
        mock_pix.samples = None
        mock_page.get_pixmap.return_value = mock_pix
        mock_pdf.__getitem__.return_value = mock_page
        mock_pdf.page_count = 1
        mock_fitz_open.return_value = mock_pdf

        process_pdf(self.test_dir, "test.pdf")

        mock_fitz_open.assert_called_once_with("test.pdf")
        mock_makedirs.assert_called_once_with(f"./{self.test_dir}/temp/test")
        mock_imwrite.assert_not_called()


if __name__ == "__main__":
    unittest.main()
