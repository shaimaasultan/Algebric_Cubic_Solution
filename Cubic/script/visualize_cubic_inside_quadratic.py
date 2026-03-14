import numpy as np
import matplotlib.pyplot as plt

# Quadratic with cubic-in-A constant term
def cubic_inside_quadratic_roots(A, beta):
    a = 0
    b = -A
    c = A**2 - A
    d = -(A**3 - A**2 + A) * beta
    # Quadratic: bx^2 + cx + d = 0
    # Ignore a=0, so roots are for bx^2 + cx + d = 0
    roots = np.roots([b, c, d])
    return roots

if __name__ == "__main__":
    beta = 1.0  # You can vary this
    A_values = np.linspace(0.1, 30, 300)
    real_parts = []
    imag_parts = []
    for A in A_values:
        roots = cubic_inside_quadratic_roots(A, beta)
        real_parts.append([np.real(r) for r in roots])
        imag_parts.append([np.imag(r) for r in roots])
    real_parts = np.array(real_parts)
    imag_parts = np.array(imag_parts)


    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title('Real parts of roots vs A')
    plt.plot(A_values, real_parts[:, 0], label='Root 1')
    plt.plot(A_values, real_parts[:, 1], label='Root 2')
    plt.plot(A_values, A_values/2, 'k--', label='A/2 (reference)')
    plt.plot(A_values, A_values/2 - 0.5, 'r:', label='A/2 - 0.5 (offset)')
    plt.xlabel('A')
    plt.ylabel('Real part')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.title('Imaginary parts of roots vs A')
    plt.plot(A_values, imag_parts[:, 0], label='Root 1')
    plt.plot(A_values, imag_parts[:, 1], label='Root 2')
    plt.xlabel('A')
    plt.ylabel('Imaginary part')
    plt.legend()

    plt.tight_layout()
    plt.show()
