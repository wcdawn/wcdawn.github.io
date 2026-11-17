import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams["lines.linewidth"] = 2
matplotlib.rcParams["font.size"] = 14

import sympy
from sympy import sqrt


def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


x, y, R = sympy.symbols("x y R")

y = sympy.sqrt(R**2 - x**2)

radius = 10.0
xcoord = np.linspace(0.0, 0.9999 * radius, 1024)

max_ord = 20
f = np.zeros((len(xcoord), max_ord // 2))
for i in range(0, max_ord, 2):
    dy = sympy.diff(y, (x, i))
    fp = dy.subs({R: radius, x: 0.0})
    f[:, i // 2] = f[:, i // 2 - 1] + fp / factorial(i) * xcoord**i

fun = sympy.utilities.lambdify(x, y.subs({R: radius}), modules="numpy")

p1 = plt.figure()
plt.plot(xcoord, fun(xcoord), label="Exact")
for i in range(0, max_ord, 2):
    plt.plot(xcoord, f[:, i // 2], label="n={:d}".format(i))
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.axis("square")
plt.title("Taylor Series Approximation of a Circle")
plt.tight_layout()
plt.savefig("circle.png", dpi=600)

plt.show()
