import unittest
import day12_package

content = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

12x5: 1 0 1 0 3 2
""".strip()


class TestDay12(unittest.TestCase):
    def test_convert_to_matrix(self):
        shape = (('#', '#', '#'), ('#', '#', '.'), ('#', '#', '.'))
        result = [[1, 1, 1], [1, 1, 0], [1, 1, 0]]
        self.assertEqual(day12_package.convert_to_matrix(shape), result)

    def test_rotate(self):
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
        result_90_clockwise = [
            [7, 4, 1],
            [8, 5, 2],
            [9, 6, 3],
        ]
        result_90_clockwise_tuple = tuple(map(tuple, result_90_clockwise))
        self.assertEqual(day12_package.rotate(matrix, 90), result_90_clockwise_tuple)

    def test_can_fit(self):
        """
        AAA.
        ABAB
        ABAB
        .BBB
        """
        start_cell = (1, 1)
        num_rows, num_cols = 4, 4
        empty_cells = [(0, 3), (1, 1), (1, 3), (2, 1), (2, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        shape = (('#', '#', '#'), ('#', '.', '#'), ('#', '.', '#'))
        new_shape = day12_package.rotate(shape, 180)
        can_fit = day12_package.can_fit(start_cell, num_rows, num_cols, empty_cells, new_shape)
        self.assertTrue(can_fit)
    
    def test_set_test(self):
        input = {2, 3, 11}
        result = {2, 3, 11, 5, 9}
        day12_package.set_test(input)
        self.assertEqual(input, result)

    def test_empty_cells_possily_fit(self):
        width, height = 4, 4
        num_rows, num_cols = height, width
        all_cells = set([(row, col) for row in range(num_rows) for col in range(num_cols)])
        shape = (('#', '#', '#'), ('#', '.', '#'), ('#', '.', '#'))
        used_cells = ((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2))
        result = set(((0, 3), (1, 1), (1, 3), (2, 1), (2, 3), (3, 0), (3, 1), (3, 2), (3, 3)))
        posssibly_fit_cells = day12_package.empty_cells_possily_fit(width, height, all_cells, used_cells, shape)
        self.assertEqual(posssibly_fit_cells, result)

        width, height = 4, 4
        num_rows, num_cols = height, width
        all_cells = set([(row, col) for row in range(num_rows) for col in range(num_cols)])
        shape = (('#', '#', '#', '.'), ('#', '#', '#', '#'), ('#', '#', '#', '#'), ('.', '#', '#', '#'))
        used_cells = ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3), (3,1), (3, 2), (3,3))
        result = set()
        posssibly_fit_cells = day12_package.empty_cells_possily_fit(width, height, all_cells, used_cells, shape)
        self.assertEqual(posssibly_fit_cells, result)

if __name__ == '__main__':
    unittest.main()  
        