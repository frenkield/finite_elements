import unittest
from src.maillage.chargeur_maillage import ChargeurMaillage


class TestChargeurMaillage(unittest.TestCase):

    def test_charger_maillage1(self):

        chargeur_maillage = ChargeurMaillage()
        maillage = chargeur_maillage.charger_maillage("data/maillages/maillage1_1.txt")

        self.assertEqual(maillage.get_node_count(), 41)
        self.assertEqual(len(maillage.noeuds), 41)
        self.assertEqual(maillage.noeuds[0][0], 1.0)
        self.assertEqual(maillage.noeuds[40][0], 0.122301806695)

        self.assertEqual(maillage.get_element_count(), 64)
        self.assertEqual(len(maillage.elements), 64)
        self.assertEqual(maillage.elements[0][0], 17)
        self.assertEqual(maillage.elements[63][0], 22)

    def test_charger_maillage2(self):

        chargeur_maillage = ChargeurMaillage()
        maillage = chargeur_maillage.charger_maillage("data/maillages/maillage2_3.txt")

        self.assertEqual(maillage.get_node_count(), 411)
        self.assertEqual(len(maillage.noeuds), 411)
        self.assertEqual(maillage.noeuds[0][0], 0.0)
        self.assertEqual(maillage.noeuds[410][0], 0.809956559275)

        self.assertEqual(maillage.get_element_count(), 740)
        self.assertEqual(len(maillage.elements), 740)
        self.assertEqual(maillage.elements[0][0], 317)
        self.assertEqual(maillage.elements[739][0], 337)


if __name__ == '__main__':
    unittest.main()
