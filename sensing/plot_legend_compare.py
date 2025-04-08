import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Custom legend elements using Line2D for better control of border
legend_elements = [
    Line2D([0], [0], marker='s', color='black', label='Detected Boxes',
           markerfacecolor='red', markersize=15, linewidth=0),
    Line2D([0], [0], marker='s', color='black', label='Ground Truth Boxes',
           markerfacecolor='white', markersize=15, linewidth=0)
]

# Create the legend figure
legend_fig = plt.figure(figsize=(6, 0.5))
legend = legend_fig.legend(handles=legend_elements,
                           loc='center',
                           fontsize=20,
                           frameon=False,
                           ncol=2)

# White background
legend_fig.patch.set_facecolor('white')

# Save the figure
legend_fig.savefig('figs/legend_compare.pdf',
                   format='pdf',
                   bbox_inches='tight')