import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.special import zeta
import math

# Find the nth zero of the Riemann zeta function on the critical line using scipy

def find_zeta_zero_scipy1(start, end, S=-1):
    def zeta_critical(t, S):
        return np.real(zeta(0.5 + 1j * t * S))
    zero = brentq(zeta_critical, start, end, args=(S,))
    return 0.5 + 1j * zero * S

def find_zeta_zero_scipy(start, end):
    def f(t):
        s = 0.5 + 1j*t
        z = zeta(s)
        return float((z.real**2 + z.imag**2))  # |zeta|^2

    res = minimize_scalar(f, bracket=(start, end))
    return 0.5 + 1j*res.x

# Distribution cubic equation from the paper
def cubic_distribution_roots2(A, beta):
    a = 1
    b = -(3 * A - 1)
    c = (A ** 2 - 3* A + 1)
    d = -(A ** 3 - A ** 2 + A +(3/(1 * beta))) * beta  #d is cubic in A
    #print(f"cubic coefficients: a={a}, b={b}, c={c}, d={d}")
    roots = np.roots([a, b, c, d])
    return roots

def cubic_distribution_roots(A, beta):
    a = 0
    b = -(1 * A - 0)
    c = (A ** 2 - 1 * A + 0)
    d = -(A ** 3 - A ** 2 + A ) * beta  #d is cubic in A
    #print(f"cubic coefficients: a={a}, b={b}, c={c}, d={d}")
    roots = np.roots([a, b, c, d])
    return roots

def search_matching_roots(zeta_zero_imag, A_range, beta_range, tol=0.01):
    matches = []
    for A in A_range:
        for beta in beta_range:
            roots = cubic_distribution_roots(A, beta)
            for r in roots:
                if np.isclose(np.imag(r), zeta_zero_imag, atol=tol):
                    matches.append((A, beta, r))
    return matches

def zoom_search(zeta_zero_imag, A_range, beta_start, beta_end, initial_step, initial_tol, zoom_levels=2, zoom_factor=10):
    results = []
    beta_min, beta_max = beta_start, beta_end
    step = initial_step
    tol = initial_tol
    for level in range(zoom_levels):
        beta_range = np.arange(beta_min, beta_max, step)
        matches = search_matching_roots(zeta_zero_imag, A_range, beta_range, tol)
        if not matches:
            break
        # Find the best match (smallest difference)
        best = min(matches, key=lambda x: abs(np.imag(x[2]) - zeta_zero_imag))
        results.append((level, best, step, tol))
        # Zoom in around the best beta
        beta_center = best[1]
        beta_min = beta_center - step * zoom_factor
        beta_max = beta_center + step * zoom_factor
        step /= zoom_factor
        tol /= zoom_factor
    return results

if __name__ == "__main__":
    # Example: 2nd zeta zero
    interval = (21, 22)
    try:
        zeta_zero = find_zeta_zero_scipy(*interval)
    except Exception:
        zeta_zero = find_zeta_zero_scipy(*interval)
    zeta_zero_imag = np.imag(zeta_zero)
    print(f"Zeta zero found at s = {zeta_zero}")
    print(f"Imaginary part to match: {zeta_zero_imag:.6f}")

    A_range = np.arange(1, 10, 1)
    beta_start, beta_end = 10, 100
    initial_step = 0.01
    initial_tol = 0.001
    zoom_levels = 10
    zoom_factor = 10

    results = zoom_search(zeta_zero_imag, A_range, beta_start, beta_end, initial_step, initial_tol, zoom_levels, zoom_factor)
    for level, (A, beta, root), step, tol in results:
        print(f"Level {level+1}: A={A:.6f}, beta={beta:.8f}, root-(A/2)={root-(A/2)}, step={step}, tol={tol}")
