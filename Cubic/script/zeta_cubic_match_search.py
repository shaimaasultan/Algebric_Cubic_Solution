import numpy as np
from scipy.optimize import brentq
from scipy.special import zeta

# Find the nth zero of the Riemann zeta function on the critical line using scipy
def find_zeta_zero_scipy(start, end , S):
    def zeta_critical(t,S):
        return np.real(zeta(0.5 + 1j*t*S))
    zero = brentq(zeta_critical, start, end, args=(S,))
    return 0.5 + 1j*zero*S

# Distribution cubic equation from the paper
def cubic_distribution_roots(A, beta):
    a = 1
    b = -(2*A-1)
    c = (A**2 - 2*A + 1)
    d = -(A**3 - A**2 + A) * beta
    roots = np.roots([a, b, c, d])
    return roots

# Search for (A, beta) that matches the imaginary part of a zeta zero
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
    # Intervals for the first several nontrivial zeta zeros (approximate)
    intervals = [
        (14, 15),   # 1st zero
        # (21, 22),   # 2nd zero
        # (25, 26),   # 3rd zero
        # (29, 30),   # 4th zero
        # (32, 33),   # 5th zero
        # (37, 38),   # 6th zero
        # (40, 41),   # 7th zero
        # (43, 44),   # 8th zero
        # (48, 49),   # 9th zero
        # (52, 53),   # 10th zero
    ]

    # Search ranges (can be adjusted)
    A_range = np.arange(0, 100 , 1)
    beta_range = np.arange(0, 1, 0.0001)
    tol = 0.001
    for idx, (start, end) in enumerate(intervals, 1):
        print(f"\n=== Searching for matches to zeta zero #{idx} in interval ({start}, {end}) ===")
        try:
            try:
                zeta_zero = find_zeta_zero_scipy(start, end,1)
            except Exception as ve:
                zeta_zero = find_zeta_zero_scipy(start, end,-1)
        except Exception as e:
            print(f"Could not find zeta zero in interval ({start}, {end}): {e}")
            continue
        print(f"Zeta zero found at s = {zeta_zero}")
        zeta_zero_imag = np.imag(zeta_zero)
        print(f"Imaginary part to match: {zeta_zero_imag:.6f}")

        matches = search_matching_roots(zeta_zero_imag, A_range, beta_range, tol=tol)

        if matches:
            print("Matches found:")
            for A, beta, root in matches:
                print(f"A={A:.6f}, beta={beta:.6f}, root={root}")
        else:
            print("No matches found in the tested range.")
