import numpy as np
from zoom_search import find_zeta_zero_scipy, zoom_search

if __name__ == "__main__":
    # Intervals for the first several nontrivial zeta zeros (approximate)
    intervals = [
        (14, 15),   # 1st zero
        (21, 22),   # 2nd zero
        (25, 26),   # 3rd zero
        (29, 30),   # 4th zero
        (32, 33),   # 5th zero
        (37, 38),   # 6th zero
        (40, 41),   # 7th zero
        (43, 44),   # 8th zero
        (48, 49),   # 9th zero
        (52, 53),   # 10th zero
    ]

    A_range = np.arange(1, 22, 1)
    beta_start, beta_end = 10, 100
    initial_step = 0.01
    initial_tol = 0.001
    zoom_levels = 10
    zoom_factor = 10

    for idx, interval in enumerate(intervals, 1):
        print(f"\n=== Zeta zero #{idx} in interval {interval} ===")
        zeta_zero = None
        for S in [1, -1]:
            try:
                zeta_zero = find_zeta_zero_scipy(*interval)
                break
            except Exception as e:
                last_error = e
        if zeta_zero is None:
            print(f"Could not find zeta zero in interval {interval}: {last_error}")
            continue
        zeta_zero_imag = np.imag(zeta_zero)
        print(f"Zeta zero found at s = {zeta_zero}")
        print(f"Imaginary part to match: {zeta_zero_imag:.6f}")

        results = zoom_search(zeta_zero_imag, A_range, beta_start, beta_end, initial_step, initial_tol, zoom_levels, zoom_factor)
        for level, (A, beta, root), step, tol in results:
            print(f"Level {level+1}: A={A:.6f}, beta={beta:.8f}, root={root-(A/2)}, step={step}, tol={tol}")
        if results:
            best_level, (A, beta, root), step, tol = results[-1]
            print(f"Best match for zero #{idx}: A={A:.6f}, beta={beta:.8f}, root={root-(A/2)}")
        else:
            print(f"No match found for zero #{idx} in interval {interval}")
