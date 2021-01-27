



def getDigit(number, index) -> int: # index is from the right, start from 0
    return number // 10 ** index % 10


def genSin(number) -> int:
    sum_odd = getDigit(number, 7) + getDigit(number, 5) + getDigit(number, 3) + getDigit(number, 1)
    print(sum_odd)
    sum_even_sq = getDigit(getDigit(number, 6) * 2, 0) + getDigit(getDigit(number, 6) * 2, 1) + getDigit(getDigit(number, 4) * 2, 0) + getDigit(getDigit(number, 4) * 2, 1)+ getDigit(getDigit(number, 2) * 2, 0) + getDigit(getDigit(number, 2) * 2, 1)+ getDigit(getDigit(number, 0) * 2, 0) + getDigit(getDigit(number, 0) * 2, 1)
    print(sum_even_sq)
    return number * 10 + 10 - getDigit((sum_odd + sum_even_sq), 0)

print(genSin(12140000))
print(genSin(64075429))
print(getDigit(123,0))