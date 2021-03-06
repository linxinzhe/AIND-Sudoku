import unittest
from solution import *

naked_twins_example = {"G7": "1569", "G6": "134568", "G5": "13568", "G4": "134568", "G3":
    "2", "G2": "34589", "G1": "7", "G9": "5689", "G8": "15", "C9": "56",
                       "C8": "3", "C3": "7", "C2": "1245689", "C1": "1245689", "C7": "2456",
                       "C6": "1245689", "C5": "12568", "C4": "1245689", "E5": "4", "E4":
                           "135689", "F1": "1234589", "F2": "12345789", "F3": "34589", "F4":
                           "123589", "F5": "12358", "F6": "123589", "F7": "14579", "F8": "6",
                       "F9": "3579", "B4": "1234567", "B5": "123567", "B6": "123456", "B7":
                           "8", "B1": "123456", "B2": "123456", "B3": "345", "B8": "9", "B9":
                           "567", "I9": "578", "I8": "27", "I1": "458", "I3": "6", "I2": "458",
                       "I5": "9", "I4": "124578", "I7": "3", "I6": "12458", "A1": "2345689",
                       "A3": "34589", "A2": "2345689", "E9": "2", "A4": "23456789", "A7":
                           "24567", "A6": "2345689", "A9": "1", "A8": "4", "E7": "159", "E6":
                           "7", "E1": "135689", "E3": "3589", "E2": "135689", "E8": "15", "A5":
                           "235678", "H8": "27", "H9": "4", "H2": "3589", "H3": "1", "H1":
                           "3589", "H6": "23568", "H7": "25679", "H4": "235678", "H5": "235678",
                       "D8": "8", "D9": "3579", "D6": "123569", "D7": "14579", "D4":
                           "123569", "D5": "12356", "D2": "12345679", "D3": "3459", "D1":
                           "1234569"}

sudoku_example = "9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................"


# class TestNakedTwinsFunction(unittest.TestCase):
#     def test_not_contain_naked_twins(self):
#         display(naked_twins_example)
#         values = naked_twins(naked_twins_example)
#         print("-----")
#         display(values)


class TestSolveFunction(unittest.TestCase):
    def test_solve_not_false(self):
        display(grid_values(sudoku_example))
        print("()()()()()()()(")
        result = solve(sudoku_example)
        self.assertTrue(result)
        display(result)
