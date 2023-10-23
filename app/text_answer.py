import json
import logging

from aiogram.types import Message

from module.matrix import Matrix

log = logging.getLogger("app.text_answer")


async def mathematica(msg: Message):
    await msg.answer(
        "Для того чтобы работать с математическими операциями введите слудующий текст в своем клавиатуре:\n\n"
        "Для вычесление матрицы отправьте сообщение с началом m>\nПример:\n"
        "m> 12,45,33|12,44,22+15,43,22|22,12,44\n"
        "m> 1,3,0|3,2,0|0,0,3!   для вычисление обратной матрицы\n"
        "m> e+3 Для получение единичной матрицы + 3 это его уровень\n"
        "m> 12,4,5|4,3,2|1,44,1: Для вычисление детерминанта"
        "h> Математические операции:"
        "\n   > : Детерминант\n"
        "\n   > / Не доступен\n"
        "\n   > * Умножение (матрица на матрицу или матрица на ламбду)\n"
        "\n   > + Сложение\n"
        "\n   > - Вычитание\n"
        "\n   > ! Обратная матрица\n"
        "a> Тут будет ответ вычеслений ващей матрицы. Пожалуйста не комбинируйте несколько операции в данный "
        "момент доступна толька одна комбинация и система не умеет определять приоритетность")


async def all_text(msg: Message):
    txt = msg.text.lower()
    if not txt.startswith("m>"):
        return await msg.answer("a> Вы ввели не доступную команду")
    txt = txt.replace(" ", "")
    for i in txt.split('\n'):
        try:
            i = i.lstrip("m>")
            if i.endswith(":"):
                i = i.rstrip(":")
                m = Matrix(i)
                r = m.determinate()
                await msg.answer(f"a> |D|\n{r[1]}")
                continue
            if i.endswith("!"):
                i = i.rstrip("!")
                m = Matrix(i)
                r = m.reverse()
                await msg.answer(f"a> {r[1]}")
                continue
            if i.endswith('/'):
                await msg.answer("a> Данная операция еще не реализовано\nm>%s" % i)
                continue
            if i.startswith("e") or i.startswith("е"):
                l = 2
                if "+" in i:
                    [j, c] = i.split("+")
                    l = int(c)
                m = Matrix.single(l)
                await msg.answer("a> Единичная матрица: \n> %s" % json.dumps(m.array))
                continue
            if (
                    "+" not in i and
                    ":" not in i and
                    not i.startswith("e") and
                    '-' not in i and
                    '*' not in i
            ):
                m = Matrix(i)
                await msg.answer("a> Вы отправили следущею матрицу:\n %s" % json.dumps(m.array))
                continue
            if "+" in i:
                [m1, m2] = i.split("+")
                m1 = Matrix(m1)
                m2 = Matrix(m2)
                c = m1 + m2
                r = c.result()
                await msg.answer("a> Ответ вычесление матрицы состовляет: \n" + r[1])
                continue
            if "*" in i:
                [m1, m2] = i.split("*")
                if not Matrix.is_matrix(m1):
                    m1 = float(m1)
                else:
                    m1 = Matrix(m1)
                if not Matrix.is_matrix(m2):
                    m2 = float(m2)
                else:
                    m2 = Matrix(m2)
                if not isinstance(m1, Matrix) and not isinstance(m2, Matrix):
                    await msg.answer("a> Матрица не найдено в ващей задаче")
                c = m1 * m2
                r = c.result()
                await msg.answer("a> Ответ вычесление матрицы состовляет: \n" + r[1])
                continue
            if "-" in i:
                [m1, m2] = i.split("-")
                m1 = Matrix(m1)
                m2 = Matrix(m2)
                c = m1 - m2
                r = c.result()
                await msg.answer("a> Ответ вычесление матрицы состовляет: \n" + r[1])
        except Exception as e:
            await msg.answer("e> При выполении операции возникла ошибка: \n%s" % str(e))
    log.debug(txt.split("\n"))
