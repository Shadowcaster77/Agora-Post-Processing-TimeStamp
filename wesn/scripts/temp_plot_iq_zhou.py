import numpy as np
import matplotlib.pyplot as plt

# Load the CSV exported from Armadillo
# Shape is (2, N): row 0 = real, row 1 = imag
# data = np.loadtxt("../../savannah_wesn/wesn_output_frame_0_sym_0_ant_0.csv",
#                   delimiter=",")
data = np.loadtxt(
    "../../../wesn_ref/Windowed-ESN-for-MIMO-OFDM/data/"
    "Tx_data_freq_symbols_2D.txt",
    dtype=complex)

re = data.real
im = data.imag

print("Data shape:", data.shape)

plt.figure()
plt.scatter(re, im, s=5)  # s = marker size

plt.xlim(-2, 2)
plt.ylim(-2, 2)

plt.xlabel("In-phase (I)")
plt.ylabel("Quadrature (Q)")
plt.title("Constellation Diagram")
plt.gca().set_aspect("equal", adjustable="box")
plt.grid(True)

plt.tight_layout()
plt.savefig("temp_plot_iq_zhou.png", bbox_inches='tight', dpi=100)
