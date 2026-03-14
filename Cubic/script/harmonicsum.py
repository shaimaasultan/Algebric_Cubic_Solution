import numpy as np
from scipy.optimize import brentq
from scipy.special import zeta

def find_zeta_zeros(t_min, t_max, N, S=1, step=0.1):
    zeros = []
    t = t_min
    found = 0
    while t < t_max and found < N:
        try:
            f1 = np.real(zeta(0.5 + 1j * t * S))
            f2 = np.real(zeta(0.5 + 1j * (t + step) * S))
            if f1 * f2 < 0:
                zero = brentq(lambda tau: np.real(zeta(0.5 + 1j * tau * S)), t, t + step)
                zeros.append(0.5 + 1j * zero * S)
                found += 1
                t += step  # skip ahead to avoid double-counting
            t += step
        except Exception:
            t += step
    return zeros

def cubic_distribution_roots(A, beta):
    a = 1
    b = -(2*A-1)
    c = (A**2 - 2*A + 1)
    d = -(A**3 - A**2 + A) * beta
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

if __name__ == "__main__":
    # Parameters
    t_min = 14
    t_max = 60
    N_zeros = 10
    A_range = np.arange(1, 21, 1)
    beta_range = np.linspace(10, 100, 181)
    tol = 0.05

    zeros = find_zeta_zeros(t_min, t_max, N_zeros, S=1, step=0.01)
    for idx, zeta_zero in enumerate(zeros, 1):
        print(f"\n=== Zeta zero #{idx} at s = {zeta_zero} ===")
        zeta_zero_imag = np.imag(zeta_zero)
        print(f"Imaginary part to match: {zeta_zero_imag:.6f}")

        matches = search_matching_roots(zeta_zero_imag, A_range, beta_range, tol=tol)

        if matches:
            print("Matches found:")
            for A, beta, root in matches:
                print(f"A={A:.2f}, beta={beta:.2f}, root={root}")
        else:
            print("No matches found in the tested range.")