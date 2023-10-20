import unittest
import math

import backend.boomerang
import backend.server
import backend.boomerangaus

from shared.constants import *
from shared.custom_exceptions import *



# Tests 1-8
class RequirementTesting1(unittest.TestCase):
    def test_requirement1(self):
        self.assertRaises(Boomerang_InvalidArgException, backend.server.Server, 1, 0, True, False)
        self.assertRaises(Boomerang_InvalidArgException, backend.server.Server, 5, 0, True, False)
        backend.server.Server(2, 0, preventSocketStart=True, logging=False)
        backend.server.Server(3, 0, preventSocketStart=True, logging=False)
        backend.server.Server(4, 0, preventSocketStart=True, logging=False)


    def test_requirement2(self):
        pass


    def test_requirement3(self):
        game = backend.boomerangaus.BoomerangAustralia()
        arr1 = game.deck
        game.shuffleDeck()
        arr2 = game.deck
        # Shuffle does not gaurantee all elements are shuffled;
        # Allow some flexibility
        n = 0
        for i in range(0, len(game.deck)):
            if arr1[i].code == arr2[i].code:
                n += 1
        self.assertTrue(n > math.log2(len(game.deck)))


    def test_requirement4(self):
        s = backend.server.Server(2, 1, preventSocketStart=True, logging=False)
        self.assertEquals(len(s.game.getBots()[0].hand), 7)


    def test_requirement5(self):
        pass


    def test_requirement6(self):
        pass


    def test_requirement7(self):
        pass


    def test_requirement8(self):
        pass



# tests 9-12
class RequirementTesting2(unittest.TestCase):
    def test_requirement9(self):
        pass

    def test_requirement10a(self):
        pass

    def test_requirement10b(self):
        pass

    def test_requirement10c(self):
        pass

    def test_requirement10d(self):
        pass

    def test_requirement10e(self):
        pass

    def test_requirement11(self):
        pass

    def test_requirement12(self):
        pass


if __name__ == "__main__":
    unittest.main()