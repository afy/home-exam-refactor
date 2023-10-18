import unittest

class TestServer(unittest.TestCase):
    def testRequirement1(self):
        self.assertEqual(1, 1, "True test")

    def test(self):
        self.assertNotEqual(1, 0, "False test")

class TestClient(unittest.TestCase):
    def testRequirement1(self):
        self.assertEqual(1, 1, "True test")

    def test(self):
        self.assertNotEqual(1, 0, "False test")

if __name__ == "__main__":
    unittest.main()