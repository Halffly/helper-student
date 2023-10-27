import decimal
from types import FunctionType
from fractions import Fraction


def matrix_plus_or_minus(matrix, matrix2, is_plus=True):
    # проверяем, что матрицы имеют одинаковый размер
    if len(matrix) != len(matrix2) or len(matrix[0]) != len(matrix2[0]):
        raise ValueError("Матрицы не имееют одинаковую длину для расчета")

    # создаем новую матрицу, заполненную нулями
    result = [[0 for j in range(len(matrix[0]))] for i in range(len(matrix))]
    txt = "[\n"
    answer = txt
    _operator = '+' if is_plus else "-"

    # складываем соответствующие элементы матриц
    for i in range(len(matrix)):
        c = '   '
        c2 = c
        for j in range(len(matrix[0])):
            c += f"{matrix[i][j]} {_operator} {matrix2[i][j]}  "
            if is_plus:
                result[i][j] = matrix[i][j] + matrix2[i][j]
            else:
                result[i][j] = matrix[i][j] - matrix2[i][j]
            c2 += f"{result[i][j]}   "
        c += '\n'
        c2 += '\n'
        txt += c
        answer += c2
    txt += ']'
    answer += ']'
    txt += '\n\n' + answer
    return [result, txt]


def fraction_denominator(n):
    return Fraction(n).limit_denominator()


def fraction(x, y):
    return Fraction(x, y)


def determinant(matrix):
    n = len(matrix)
    if n == 1:
        d = matrix[0][0]
        return d, f"{d}"
    elif n == 2:
        x1, x2 = matrix[0][0], matrix[0][1]
        y1, y2 = matrix[1][0], matrix[1][1]
        lft = x1 * y2
        rgt = x2 * y1
        d = lft - rgt
        txt = f' > {x1} * {y2} - {x2} * {y1}\n > {lft}-{rgt}\n > {d}'
        return d, txt
    else:
        det = 0
        lst = ""
        for j in range(n):
            index = (-1) ** j
            txt = f'  (-1)^1+{j + 1}\n[\n'
            ndt = []
            for i in range(1, n):
                m = matrix[i][0:j] + matrix[i][j + 1:]
                for ii in m:
                    txt += f"   {ii}"
                txt = txt.rstrip("  ") + '\n'
                ndt.append(m)
            lst += txt
            lst += ']\n'
            [dtr, _] = determinant(ndt)
            lst += _
            det += index * matrix[0][j] * dtr
            lst += f'\n > {index} * {matrix[0][j]} * {dtr} = {det}' + '\n\n'
        return det, lst.rstrip("\n")


def matrix_reverse(matrix):
    [det_A, _] = determinant(matrix)
    txt = '|D| = ' + _ + '\n---------------------\n Алгебраические дополнение:\n\n'

    # вычисляем матрицу алгебраических дополнений
    def cofactor(A):
        c_txt = ''
        n = len(A)
        C = [[0] * n for i in range(n)]
        for i in range(n):
            c = ''
            for j in range(n):
                c += '[\n'
                minor = []
                for k in list(range(0, i)) + list(range(i + 1, n)):
                    lft = A[k][0:j]
                    rht = A[k][j + 1:]
                    lft_rht = lft + rht
                    for ii in lft_rht:
                        c += f"   {ii}"
                    c += '\n'
                    minor.append(lft_rht)

                c += ']\n'
                [d, _] = determinant(minor)
                c += _ + f'\n\n>(-1)^({i + 1}+{j + 1}) * {d}'
                C[i][j] = ((-1) ** (i + j)) * d
                c += f'\n>{C[i][j]}\n--------------\n'
            c_txt += c + '\n'
        return C, c_txt

    [adj_A, _] = cofactor(matrix)
    txt += _
    for i in range(len(adj_A)):
        for j in range(i, len(adj_A)):
            adj_A[i][j], adj_A[j][i] = adj_A[j][i], adj_A[i][j]

    # вычисляем обратную матрицу
    A_inv = []
    txt_rd = "[\n"
    txt_rda = "[\n"
    for i in range(len(adj_A)):
        lst = []
        for j in range(len(adj_A)):
            txt_rd += f'    {adj_A[i][j]}/{det_A}'
            txt_rda += f"   {fraction_denominator(adj_A[i][j] / det_A)}"
            lst.append(adj_A[i][j] / det_A)
        txt_rd += '\n'
        txt_rda += '\n'
        A_inv.append(lst)
    txt += txt_rd + ']'
    txt += '\n' + txt_rda + ']'
    return A_inv, txt


def matrix_multiply(matrix, matrix2):
    # определяем размерности матриц
    m = len(matrix)
    n = len(matrix2[0])

    # создаем новую матрицу, заполненную нулями
    result = [[0 for j in range(n)] for i in range(m)]
    txt = '[\n'
    answer = txt
    answer2 = txt
    # вычисляем элементы новой матрицы
    for i in range(m):
        for j in range(n):
            c = "   "
            c2 = c
            c3 = c
            for k in range(len(matrix2)):
                c += f"{matrix[i][k]} * {matrix2[k][j]} + "
                r = matrix[i][k] * matrix2[k][j]
                c2 += f"{r} + "
                result[i][j] += r
            c3 += f"{result[i][j]} "
            c = c.rstrip(" + ")
            answer += c2.rstrip(" + ")
            answer2 += c3.rstrip(" ")
            txt += c
        txt += '\n'
        answer += '\n'
        answer2 += '\n'
    txt += ']'
    answer += ']'
    answer2 += ']'
    txt += "\n\n" + answer + '\n\n' + answer2
    return result, txt


def lambda_matrix(x, x2):
    lmbda = 0
    matrix = []
    if isinstance(x, (int, float)) and isinstance(x2, (int, float)):
        raise TypeError('Матрица не найдена в функции')
    if isinstance(x, (int, float)):
        lmbda = x
        matrix = x2
    if isinstance(x2, (int, float)):
        lmbda = x2
        matrix = x
    result = []
    txt = '[\n'
    ans = '[\n'
    for row in matrix:
        new_row = []
        c = ''
        c2 = ''
        for element in row:
            a = lmbda * element
            c += f'   {a}'
            c2 += f"    {lmbda} * {element}"
            new_row.append(lmbda * element)
        c += '\n'
        c2 += '\n'
        txt += c2
        ans += c
        result.append(new_row)
    txt += ']'
    ans += ']'
    txt += '\n' + ans
    return result, txt


def equation_reverse(matrix, matrix2):
    m_reverse, txt = matrix_reverse(matrix)
    m = Matrix(m_reverse)
    m2 = Matrix(matrix2)
    c = m * m2
    r = c.result()
    txt += f'\n\nУмножение A^(-1)*B\n\n-------------------------\n\n{r[1]}'
    return r[0], txt

def kramer_method(A, B):
    # Проверяем, что матрица коэффициентов A квадратная
    if len(A) != len(A[0]):
        raise ValueError("Матрица коэффициентов должна быть квадратной")

    # Проверяем, что размер матрицы коэффициентов A совпадает с размером вектора свободных членов B
    if len(A) != len(B):
        raise ValueError("Размер матрицы коэффициентов должен совпадать с размером вектора свободных членов")

    # Находим определитель матрицы A
    det_A, txt = determinant(A)

    # Проверяем, что определитель не равен нулю
    if det_A == 0:
        raise ValueError("Система не имеет решений")
    else:
        # Создаем пустой список для хранения решений
        x = []

        # Вычисляем решение для каждой неизвестной
        for i in range(len(A)):
            # Создаем копию матрицы коэффициентов A
            A_copy = [row[:] for row in A]

            # Заменяем i-ый столбец матрицы коэффициентов A на вектор свободных членов B
            for j in range(len(B)):
                A_copy[j][i] = B[j][0]
            # Вычисляем определитель новой матрицы
            det_A_copy, txt2 = determinant(A_copy)
            # Вычисляем значение i-ой неизвестной
            x_i = det_A_copy / det_A
            txt += '\n\n----------D--------\n\n' + txt2 \
                + f'\n{det_A_copy} / {det_A}={fraction_denominator(x_i)}'

            # Добавляем значение i-ой неизвестной в список решений
            x.append(x_i)

        return x, txt


def matrix_plus(matrix, matrix2):
    return matrix_plus_or_minus(matrix, matrix2)


def matrix_minus(matrix, matrix2):
    return matrix_plus_or_minus(matrix, matrix2, False)


operators = {
    "+": matrix_plus,
    "-": matrix_minus,
    "*": matrix_multiply,
    "/": None,
    "lambda": lambda_matrix
}


def get_mul_matrix_combination(matrix, matrix2):
    _ = "*"
    if not isinstance(matrix2, (int, float, decimal.Decimal, Matrix, MatrixCombination)):
        raise TypeError(
            "При умножении на матриц можно использовать только число, матрицу или комбимацию из матриц а не %s" %
            type(
                matrix2))
    if isinstance(matrix2, (int, float, decimal.Decimal)):
        _ = 'lambda'
    return MatrixCombination(matrix, matrix2, _)


class MatrixCombination:
    _matrix = None
    _result_cache = None

    def __init__(self, matrix, matrix2, operator):
        if (
                operator != 'lambda' and (
                not isinstance(matrix, (Matrix, MatrixCombination)) or
                not isinstance(matrix2, (Matrix, MatrixCombination))
        )
        ):
            raise TypeError("Переданный тип не соотвествует заданым параметрам")
        self._matrix = {
            "matrix_left": matrix,
            "matrix_right": matrix2,
            "operator": operator
        }

    @property
    def matrix(self):
        return self._matrix

    def is_valid(self, is_raise=True):
        valid = self._matrix is not None and isinstance(self._matrix, dict)
        if is_raise and not valid:
            raise TypeError("Переданная вещь не является данными для матрицы")
        return valid

    def is_valid_instance(self, other, is_raise=True):
        not_valid = not isinstance(other, (Matrix, MatrixCombination))
        if not_valid and is_raise:
            raise TypeError("Прибавляемая число должна быть матрицей или комбинацией из матриц а не %s" % type(other))

        return not not_valid

    @property
    def lft(self):
        self.is_valid()
        return self._matrix.get("matrix_left")

    @property
    def rgt(self):
        self.is_valid()
        return self._matrix.get("matrix_right")

    @property
    def operator(self) -> FunctionType | None:
        self.is_valid()
        _: str = self._matrix.get("operator", None)
        if not isinstance(_, str):
            return
        return operators.get(_, None)

    # ==
    def __eq__(self, other):
        pass

    # +
    def __add__(self, other):
        self.is_valid_instance(other)
        return MatrixCombination(self, other, "+")

    # -
    def __sub__(self, other):
        self.is_valid_instance(other)
        return MatrixCombination(self, other, "-")

    # *
    def __mul__(self, other):
        return get_mul_matrix_combination(self, other)

    # /
    def __truediv__(self, other):
        pass

    def result(self):
        txt = ""
        array_1 = self.lft
        array_2 = self.rgt

        if self.operator is None:
            raise TypeError("Заданный оператор не был найден в списке реализованных операторов")

        if isinstance(array_1, MatrixCombination):
            [array_1, txt_1] = array_1.result()
            txt += f"{txt_1}\n\n"
        if isinstance(array_2, MatrixCombination):
            [array_2, txt_2] = array_2.result()
            txt += f"{txt_2}\n\n"

        if isinstance(array_1, Matrix):
            array_1 = array_1.array

        if isinstance(array_2, Matrix):
            array_2 = array_2.array

        [answer, _] = self.operator(array_1, array_2)
        txt += _

        return [answer, txt]


class Matrix:
    _array = []

    def __init__(self, array: str | list):
        self.array = array

    @staticmethod
    def parse_array_from_str(array: str):
        """
        :param array:
           The param is array should be type is str:
        :return:
        """
        if not isinstance(array, str):
            raise TypeError("Должно быть строкой")

        a = array.split("|")
        b = []
        for i in a:
            i = i.split(",")
            c = []
            for j in i:
                j = str(j)
                if not j:
                    continue
                try:
                    c.append(float(j))
                except Exception as e:
                    raise ValueError('Error: %s \nValue: %s\nMessage: %s' % (
                        e, j, "В данном списке присуствует символы которые не допускаются "))
            if len(c) > 0:
                b.append(c)

        return b

    @property
    def array(self):
        return self._array

    @array.setter
    def array(self, value):
        if isinstance(value, str):
            value = Matrix.parse_array_from_str(value)
        if not isinstance(value, list):
            raise TypeError("Тип матрицы не соотвествует заданным параметрам")

        self._array = value

    @staticmethod
    def is_matrix(array):
        try:
            if "," in array:
                m = Matrix.parse_array_from_str(array)
                return isinstance(m, list)
            if '.' in array:
                array = float(array)
            else:
                array = int(array)
            return True
        except Exception as e:
            return False

    def __str__(self):
        return f"Matrix: {self.array}"

    def __repr__(self):
        return f"<class Matrix {hex(id(self))} {self.array}>"

    def is_valid_instance(self, other, is_raise=True):
        not_valid = not isinstance(other, (Matrix, MatrixCombination))
        if not_valid and is_raise:
            raise TypeError("Заданая задача должна быть матрицей или комбинацией из матриц а не %s" % type(other))

        return not not_valid

    @staticmethod
    def single(level):
        array = []

        if not isinstance(level, int):
            raise TypeError("Уровень единичной матрицы должна быть в числовом формате")

        i = 0
        while True:
            if len(array) == level:
                break
            row = []
            for j in range(level):
                if j == i:
                    row.append(1)
                else:
                    row.append(0)
            array.append(row)
            i += 1

        return Matrix(array)

    def equation_reverse(self, matrix):
        return equation_reverse(self.array, matrix)

    def kramer_method(self, matrix):
        return kramer_method(self.array, matrix)

    def determinate(self):
        return determinant(self.array)

    def reverse(self):
        return matrix_reverse(self.array)

    # ==
    def __eq__(self, other):
        pass

    # +
    def __add__(self, other):
        if not self.is_valid_instance(other, is_raise=False):
            raise TypeError("Прибавляемая число должна быть матрицей или комбинацией из матриц а не %s" % type(other))
        return MatrixCombination(self, other, "+")

    # -
    def __sub__(self, other):
        if not self.is_valid_instance(other, is_raise=False):
            raise TypeError(
                "При вычитании матриц передаваемая значние должна быть матрицей или комбинацией а не %s" % type(other))
        return MatrixCombination(self, other, "-")

    # *
    def __mul__(self, other):
        return get_mul_matrix_combination(self, other)

    # /
    def __truediv__(self, other):
        raise NotImplementedError("Еще не реализовано")
