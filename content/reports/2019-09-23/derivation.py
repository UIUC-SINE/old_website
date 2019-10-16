from sympy import symbols, simplify, expand, factor, fraction
from sympy.matrices import Matrix, det

# %% 2by2

l11, l12, l21, l22 = symbols('l11 l12 l21 l22')

l = Matrix(((l11, l12), (l21, l22)))

# %% 3by3

(l11, l12, l13,
 l21, l22, l23,
 l31, l32, l33
) = symbols(
    '\
    l11 l12 l13 \
    l21 l22 l23 \
    l31 l32 l33 \
    '
)

l = Matrix(
    (
        (l11, l12, l13),
        (l21, l22, l23),
        (l31, l32, l33)
    )
)

# %% compute

result = factor((l.T @ l).inv().trace())
num, denom = fraction(result)

print('\n\nnum\n----------\n')
print(num)
print('\n\ndenom\n----------\n')
print(denom)
print('\n\ndet\n----------\n')
print(factor(det(l.T @ l)))
