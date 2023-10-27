import unittest

from module.matrix import Matrix, MatrixCombination


class TestParsingMatrixFromString(unittest.TestCase):

    def test_partial(self):
        matrix = Matrix.parse_array_from_str("1,2,3|")

        self.assertListEqual(matrix, [
            [1, 2, 3]
        ])

    def test_third(self):
        matrix = Matrix.parse_array_from_str("1,2,3|12,45,12|331,123,44.123")

        self.assertListEqual(matrix, [
            [1, 2, 3], [12, 45, 12], [331, 123, 44.123]
        ])

    def test_full(self):
        matrix = Matrix.parse_array_from_str("1,2,3|1,2,3")

        self.assertListEqual(matrix, [
            [1, 2, 3], [1, 2, 3]
        ])


class TestMathMatrixFromString(unittest.TestCase):

    def test_plus(self):
        a = Matrix("1,2,3|4,5,2")
        b = Matrix("4,512,54|44,23,44")
        c = a + b

        self.assertIsInstance(c, MatrixCombination)

        result = c.result()
        self.assertEqual("""[
   1.0 + 4.0  2.0 + 512.0  3.0 + 54.0  
   4.0 + 44.0  5.0 + 23.0  2.0 + 44.0  
]

[
   5.0   514.0   57.0   
   48.0   28.0   46.0   
]""", result[1])
        self.assertListEqual(result[0], [[5.0, 514.0, 57.0], [48.0, 28.0, 46.0]])

    def test_minus(self):
        a = Matrix('1,53,55|12,44,12')
        b = Matrix("44,12,55|21,33,14")
        c = a - b
        self.assertIsInstance(c, MatrixCombination)
        result = c.result()
        self.assertEqual("""[
   1.0 - 44.0  53.0 - 12.0  55.0 - 55.0  
   12.0 - 21.0  44.0 - 33.0  12.0 - 14.0  
]

[
   -43.0   41.0   0.0   
   -9.0   11.0   -2.0   
]""", result[1])
        self.assertListEqual(result[0], [[-43.0, 41.0, 0.0], [-9.0, 11.0, -2.0]])

    def test_multiply(self):
        a = Matrix("1,3,2|3,2,5|2,4,1")
        b = Matrix("4,5,2|4,5,6|2,1,9")

        """
           |> 1 3 2 - 4 5 2
           |> 3 2 5 - 4 5 6
           |> 2 4 1 - 2 1 9
        """

        c = a * b
        result = c.result()
        self.assertIsInstance(c, MatrixCombination)
        self.assertEqual("""[
   1.0 * 4.0 + 3.0 * 4.0 + 2.0 * 2.0   1.0 * 5.0 + 3.0 * 5.0 + 2.0 * 1.0   1.0 * 2.0 + 3.0 * 6.0 + 2.0 * 9.0
   3.0 * 4.0 + 2.0 * 4.0 + 5.0 * 2.0   3.0 * 5.0 + 2.0 * 5.0 + 5.0 * 1.0   3.0 * 2.0 + 2.0 * 6.0 + 5.0 * 9.0
   2.0 * 4.0 + 4.0 * 4.0 + 1.0 * 2.0   2.0 * 5.0 + 4.0 * 5.0 + 1.0 * 1.0   2.0 * 2.0 + 4.0 * 6.0 + 1.0 * 9.0
]

[
   4.0 + 12.0 + 4.0   5.0 + 15.0 + 2.0   2.0 + 18.0 + 18.0
   12.0 + 8.0 + 10.0   15.0 + 10.0 + 5.0   6.0 + 12.0 + 45.0
   8.0 + 16.0 + 2.0   10.0 + 20.0 + 1.0   4.0 + 24.0 + 9.0
]

[
   20.0   22.0   38.0
   30.0   30.0   63.0
   26.0   31.0   37.0
]""", result[1])
        self.assertListEqual([[20.0, 22.0, 38.0], [30.0, 30.0, 63.0], [26.0, 31.0, 37.0]], result[0])

    def test_single(self):
        m = Matrix.single(2)
        m2 = Matrix.single(3)
        self.assertListEqual([[1, 0], [0, 1]], m.array)
        self.assertListEqual([[1, 0, 0], [0, 1, 0], [0, 0, 1]], m2.array)

    def test_determinant(self):
        m = Matrix("43,31,22|90,22,12")
        m2 = Matrix("1,2,0|3,1,2|0,0,3")
        d1 = m.determinate()
        d2 = m2.determinate()

        self.assertEqual(-15, d2[0])
        self.assertEqual(-1844.0, d1[0])

    def test_reverse(self):
        m = Matrix("1,2,0|3,1,2|0,0,3")
        m2 = Matrix('1,2,0|3,3,1')
        r = m.reverse()
        r2 = m2.reverse()
        r3 = Matrix(r2[0])
        c = m2 * r3
        e = Matrix.single(2)

        self.assertListEqual(
            [[-0.2, 0.4, -0.26666666666666666], [0.6, -0.2, 0.13333333333333333], [-0.0, 0.0, 0.3333333333333333]],
            r[0])
        self.assertListEqual(c.result()[0], e.array)
        self.assertListEqual([[-1.0, 0.6666666666666666], [1.0, -0.3333333333333333]], r2[0])

    def test_lambda(self):
        m = Matrix("1,2,0|3,1,2|0,0,3")
        c = m * 5
        r = c.result()

        self.assertListEqual([[5.0, 10.0, 0.0], [15.0, 5.0, 10.0], [0.0, 0.0, 15.0]], r[0])

    def test_line_equation_reverse(self):
        m = Matrix("7,8|5,6")
        m2 = Matrix("22|16")

        self.assertListEqual([
            [7, 8], [5, 6]
        ], m.array)

        self.assertListEqual([
            [22], [16]
        ], m2.array)

        c = m.equation_reverse(m2.array)

        self.assertListEqual([
            [2], [1]
        ], c[0])

    def test_line_equation_determinant(self):
        m = Matrix("7,8|5,6")
        m2 = Matrix('22|16')
        c = m.kramer_method(m2.array)
        self.assertListEqual([
            2, 1
        ], c[0])


if __name__ == '__main__':
    unittest.main()
