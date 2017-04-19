from unittest import TestCase
from Project.Game import load_board_state


class TestStandaloneFuncs(TestCase):
    def test_load_board_state(self):
        a = [['X', 'X', 'X', 'X', 'X', 'X'],
             ['X', ' ', ' ', 'X', ' ', 'X'],
             ['X', 'X', ' ', 'X', ' ', 'X'],
             ['X', 'P', ' ', ' ', ' ', 'X'],
             ['X', 'X', 'X', 'X', 'X', 'X']]
        self.assertEqual(a, load_board_state('Project/test_map.txt'))
