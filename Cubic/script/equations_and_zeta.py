import numpy as np
from scipy.optimize import brentq
from scipy.special import zeta

# --- PDF-based implementations ---
def quadratic_roots_from_A(A):
    a = 1
    b = -1
    c = A * (A - 1)
    return solve_quadratic(a, b, c)

def cubic_roots_from_A(A):
    # Cubic: x^3 - x^2 + x - (A^3 - A^2 + A) = 0
    # Note: A = 16.6274544422428 gives the first zeta zero for this cubic equation.
    # This solution matches the first zeta zero only for A = 16.6274544422428 and beta = 1.
    a = 1
    b = -1
    c = 1
    d = -(A**3 - A**2 + A)
    return solve_cubic(a, b, c, d, A)

def cubic_distribution_roots(A, beta):
    # Cubic: x^3 - (2A-1)x^2 + (A^2-2A+1)x - (A^3-A^2+A)*beta = 0
    a = 1
    b = -(2*A-1)
    c = (A**2 - 2*A + 1)
    d = -(A**3 - A**2 + A) * beta
    return solve_cubic(a, b, c, d,A)

def quadratic_distribution_roots(beta):
    # Quadratic: x^2 - x + beta = 0
    a = 1
    b = -1
    c = beta
    return solve_quadratic(a, b, c)

# Quadratic equation solver: ax^2 + bx + c = 0
def solve_quadratic(a, b, c):
    D = b**2 - 4*a*c
    if D > 0:
        x1 = (-b + np.sqrt(D)) / (2*a)
        x2 = (-b - np.sqrt(D)) / (2*a)
        return (x1, x2)
    elif D == 0:
        x = -b / (2*a)
        return (x,)
    else:
        real = -b / (2*a)
        imag = np.sqrt(-D) / (2*a)
        return (complex(real, imag), complex(real, -imag))

# Cubic equation solver: ax^3 + bx^2 + cx + d = 0
def solve_cubic(a, b, c, d, A):
    coeffs = [a, b, c, d]
    roots = np.roots(coeffs)

    # Note: Although this equation is cubic, its zeros (roots) change for different values of A and beta.
    # For each combination of A and beta, the cubic equation produces a new set of roots.
    # This means the equation does not have fixed zeros—its solutions depend on the parameters, allowing it to model or match different values, such as the zeros of the Riemann zeta function.
    return [complex(r.real+(A/2), r.imag) for r in roots]

# Find a zero of the Riemann zeta function on the critical line (0 < Im(s) < 50)
def find_zeta_zero(start=14, end=30):
    # Riemann zeta function on the critical line: s = 0.5 + it
    def zeta_critical(t):
        return np.real(zeta(0.5 + 1j*t))
    zero = brentq(zeta_critical, start, end)
    return 0.5 + 1j*zero

if __name__ == "__main__":
    print("Quadratic equation: 1x^2 + -3x + 2 = 0")
    print("Roots:", solve_quadratic(1, -3, 2))

    print("\nCubic equation: 1x^3 + -6x^2 + 11x + -6 = 0")
    print("Roots:", solve_cubic(1, -6, 11, -6,0))

    print("\nFinding a zero of the Riemann zeta function on the critical line...")
    #zero = find_zeta_zero()
    zero = find_zeta_zero(21,22)
    print("Zero found at s =", zero)

    print("\n--- PDF-based Equations ---")
    #for A in np.arange(16.6274544422428, 16.62745444224281, 0.00000000000001):
    for A in np.arange( 24.5891777027,  24.5891777033, 0.0000000001):
        print(f"\nA = {A}")
        print("Quadratic roots (x^2 - x + A(A-1) = 0):", quadratic_roots_from_A(A))
        print("Cubic roots (x^3 - x^2 + x - (A^3-A^2+A) = 0):", cubic_roots_from_A(A))

    # Example for distribution cubic equation with beta
    A = 2
    beta = 1
    print(f"\nDistribution cubic equation roots for A={A}, beta={beta}:")
    print("Roots:", cubic_distribution_roots(A, beta))

    # Example for quadratic distribution equation
    print(f"\nQuadratic distribution equation roots for beta={beta}:")
    print("Roots:", quadratic_distribution_roots(beta))
