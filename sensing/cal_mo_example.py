################################################################################
# Visualize the MO results as an example using scipy and numpy.
#
# Author: Chung-Hsuan Tung
################################################################################

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import binary_dilation
from scipy.ndimage import binary_erosion
from scipy.ndimage import convolve

def plot_image(data, title):
    fig, ax = plt.subplots()
    ax.imshow(data, cmap='gray_r')
    max_val = data.max()
    min_val = data.min()
    mid_val = (max_val + min_val) / 2

    # Add text annotations
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            ax.text(j, i, str(data[i, j]),
                    ha='center',
                    va='center',
                    color='white' if data[i, j] > mid_val else 'black',
                    fontweight='bold')

    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    ax.set_xticklabels(np.arange(data.shape[1]))
    ax.set_yticklabels(np.arange(data.shape[0]))

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    plt.tight_layout()
    plt.savefig('figs/mo_example_' + title + '.png')
    plt.close()

# Example array
data = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

plot_image(data, 'input')

################################################################################
kernel = np.ones((3, 3), np.uint8)

# Dilation
dilated = binary_dilation(data, kernel)
dilated = dilated.astype(int)
plot_image(dilated, 'dilated')

# Erosion
eroded = binary_erosion(data, kernel)
eroded = eroded.astype(int)
plot_image(eroded, 'eroded')

# Opening
opened = binary_dilation(binary_erosion(data, kernel), kernel)
opened = opened.astype(int)
plot_image(opened, 'opened')

# Closing
closed = binary_erosion(binary_dilation(data, kernel), kernel)
closed = closed.astype(int)
plot_image(closed, 'closed')

# Convoluted
convoluted = convolve(data, kernel)
convoluted = convoluted.astype(int)
plot_image(convoluted, 'convoluted')
