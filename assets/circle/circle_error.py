import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams["lines.linewidth"] = 2
matplotlib.rcParams["font.size"] = 14

if __name__ == "__main__":

    h0 = 4.0
    exact = np.pi * 10.0**2 * 0.25
    linear = np.array(
        (
            76.5366864730179,
            78.0361288064513,
            78.4137122636484,
            78.5082789238686,
            78.5316789749293,
            78.5377819511152,
        )
    )
    quadratic = np.array(
        (
            78.0361288064512,
            78.4137122636485,
            78.5082789238688,
            78.5319312733191,
            78.5377819511145,
            78.5393077396236,
        )
    )

    linear_error = exact - linear
    quadratic_error = exact - quadratic

    h = h0 * np.array([0.5**i for i in range(len(linear))])

    plt.figure()
    plt.loglog(h, linear_error, "-o", label="Linear")
    plt.loglog(h, quadratic_error, "-o", label="Quadratic")
    plt.loglog(
        h,
        h**2 * 0.5 * linear_error[0] / h[0],
        "-k",
        lw=1,
        label="$\\mathcal{O}(h^2)$",
    )
    plt.legend()
    plt.xlabel("h")
    plt.ylabel("Error")
    plt.title("Convergence of Circular Area from Gmsh")
    plt.tight_layout()
    plt.savefig("circle_error.png", dpi=600)

    plt.show()
