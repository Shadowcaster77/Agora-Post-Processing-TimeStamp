import numpy as np
import matplotlib.pyplot as plt

path = "../../../savannah_wesn/data/"

# Load the CSV exported from Armadillo
# Shape is (2, N): row 0 = real, row 1 = imag
data = np.loadtxt(
    path + "wesn_output_frame_0_sym_0_ant_0.csv",
    delimiter=",")

re = data[0, :]
im = data[1, :]

data = np.loadtxt(
    path + "wesn_output_frame_0_sym_0_ant_1.csv",
    delimiter=",")

re = np.concatenate((re, data[0, :]))
im = np.concatenate((im, data[1, :]))

for symbol_idx in range(1, 2):
    for ant_idx in range(2):
        data = np.loadtxt(
            path + f"wesn_output_frame_0_sym_{symbol_idx}_ant_{ant_idx}.csv",
            delimiter=",")

        re = np.concatenate((re, data[0, :]))
        im = np.concatenate((im, data[1, :]))

plt.figure()
plt.scatter(re, im, s=5)  # s = marker size

print("Total points plotted:", len(re))

plt.xlim(-2, 2)
plt.ylim(-2, 2)

plt.xlabel("In-phase (I)")
plt.ylabel("Quadrature (Q)")
plt.title("Constellation Diagram")
plt.gca().set_aspect("equal", adjustable="box")
plt.grid(True)

plt.tight_layout()
plt.savefig("temp_plot_iq_bulk.png", bbox_inches='tight', dpi=100)