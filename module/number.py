import decimal


class BigNumber(decimal.Decimal):

    def __init__(self, value, **kwargs):
        if isinstance(value, (int, float)):
            value = str(value)
        if not isinstance(value, str):
            raise TypeError("Должно быть числом или строкой")
        super().__init__(value, **kwargs)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            other = BigNumber(other)
        return super().__truediv__(other)
