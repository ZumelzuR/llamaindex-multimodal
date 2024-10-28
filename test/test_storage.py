import unittest
from utils.storage import create_meta_from_name


class TestStorageFunctions(unittest.TestCase):

    def test_create_meta_from_name_real_valid(self):
        result = create_meta_from_name(
            "/Users/czu/multimodal/data/temp/fredde-gaming-desk-black__AA-2508156-1-100/fredde-gaming-desk-black__AA-2508156-1-100_1.png"
        )
        expected = {
            "file_path": "/Users/czu/multimodal/data/temp/fredde-gaming-desk-black__AA-2508156-1-100/fredde-gaming-desk-black__AA-2508156-1-100_1.png",
            "item": "fredde-gaming-desk-black",
            "page": "1",
        }
        self.assertEqual(result, expected)

    def test_create_meta_from_name_valid(self):

        result = create_meta_from_name(
            "fredde-gaming-desk-black__AA-2508156-1-100_1.png"
        )
        expected = {
            "file_path": "fredde-gaming-desk-black__AA-2508156-1-100_1.png",
            "item": "fredde-gaming-desk-black",
            "page": "1",
        }
        self.assertEqual(result, expected)

    def test_create_meta_from_name_invalid(self):
        with self.assertRaises(ValueError):
            create_meta_from_name(2222)
        with self.assertRaises(ValueError):
            create_meta_from_name("xxxxxx")
        with self.assertRaises(ValueError):
            create_meta_from_name("xxxxxx.png")
        with self.assertRaises(ValueError):
            create_meta_from_name("xxxxxx_1.png")
        with self.assertRaises(ValueError):
            create_meta_from_name("xxxxxx__1.png")


if __name__ == "__main__":
    unittest.main()
