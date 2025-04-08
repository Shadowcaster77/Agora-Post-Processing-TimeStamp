import matplotlib.pyplot as plt

# Marker styles and corresponding labels
legend_items = [
    {"marker": None, "linestyle": "--", "color": "red", "label": "0.375 msec"},
    {"marker": "o", "color": "orange", "label": r"$\theta(1,1|1,1)$"},
    {"marker": "s", "color": "orange", "label": r"$\theta(C,0|C,0)$"},
    {"marker": "D", "color": "green",  "label": r"$\theta(C\!-\!1,1|C,1)$"},
    {"marker": "^", "color": "red",    "label": r"$\theta(C\!-\!1,1|C,2)$"},
    {"marker": "P", "color": "purple", "label": r"$\theta(C\!-\!1,1|C,3)$"},
    {"marker": "X", "color": "brown",  "label": r"$\theta(C\!-\!1,1|C,4)$"},
    {"marker": "v", "color": "pink",   "label": r"$\theta(C,C|C,C)$"},
]

# Create a figure for the legend only
fig, ax = plt.subplots(figsize=(10, 1))
ax.axis("off")  # Hide axes

# Create dummy handles for legend
handles = []
for item in legend_items:
    if item["marker"] is None:
        # Dashed line for the first entry
        handle, = ax.plot([], [], linestyle=item["linestyle"],
                          color=item["color"], label=item["label"],
                          linewidth=2)
    else:
        # Marker entries
        handle = ax.scatter([], [], marker=item["marker"], color=item["color"],
                            label=item["label"], s=100)
    handles.append(handle)

# Draw the legend
legend = ax.legend(handles=handles, loc="center", ncol=len(legend_items)/2,
                   fontsize=14, frameon=False)

# Save the figure
plt.savefig("figs/legend_only_plot.pdf", bbox_inches="tight")
