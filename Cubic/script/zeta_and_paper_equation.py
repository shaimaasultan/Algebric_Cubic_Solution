import numpy as np
from scipy.optimize import brentq
from scipy.special import zeta

# Find a zero of the Riemann zeta function on the critical line (0 < Im(s) < 50)
def find_zeta_zero_scipy(start=14, end=30):
    # Riemann zeta function on the critical line: s = 0.5 + it
    def zeta_critical(t):
        return np.real(zeta(0.5 + 1j*t))
    zero = brentq(zeta_critical, start, end)
    return 0.5 + 1j*zero

# From the paper: Distribution Cubic Equation Solution and Zeta Function
# Equation: x^3 - (2A-1)x^2 + (A^2-2A+1)x - (A^3-A^2+A)*beta = 0
# For a given A and beta, solve for x (roots)
def cubic_distribution_roots(A, beta):
    a = 1
    b = -(1*A-1)
    c = (A**2 - 2*A + 1)
    d = -(A**3 - A**2 + A) * beta
    roots = np.roots([a, b, c, d])
    return roots

if __name__ == "__main__":
    print("Finding a zero of the Riemann zeta function on the critical line using scipy...")
    zero = find_zeta_zero_scipy()
    print("Zero found at s =", zero)


    # Try a range of A and beta values to see if any root matches the imaginary part of the zeta zero
    im_zero = round(np.imag(zero),5)
    rel_zero = np.real(zero)
    atol = 0.1
    print(f"\nTrying to match the imaginary part of the zeta zero: {im_zero:.6f},real part: {rel_zero:.6f}  ")
    found = False
    for A in np.arange(0, 21, 0.001):
        for beta in np.arange(0, 1, 0.001):
            roots = cubic_distribution_roots(A, beta)
            #print(f"A={A}, beta={beta:.2f}, roots={roots} , real part of roots={np.real(roots)}, imag part of roots={np.imag(roots)}    ")
            # Check if any root (real or imaginary part) is close to im_zero
            for r in roots:
                if round(np.imag(r),5)== im_zero +atol or round(np.imag(r),5)== im_zero -atol:
                    print(f"A={A:2f}, beta={beta:.2f}, root={r} matches zeta zero imag part {im_zero:.6f}")
                    found = True
                if  round(np.real(r),5)== rel_zero :
                    print(f"A={A:2f}, beta={beta:.2f}, root={r} matches zeta zero real part {rel_zero:.6f}")
                    found = True
    if not found:
        print("No close match found in the tested range.")
