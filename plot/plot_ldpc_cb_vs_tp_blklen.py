import matplotlib.pyplot as plt
import numpy as np

mcs = list(range(29))

mcs_new = list(range(24))

cb_length = [176, 220, 286, 352, 440, 572, 660, 792, 880, 968, 968, 1144, 1320,
             1408, 1584, 1760, 1936,1936, 2112, 2288, 2464, 2816, 2816, 3168,
             3520, 3520, 3872, 3872, 4224]
cb_length_new = [176, 220, 286, 352, 440, 572, 660, 792, 880, 968, 968, 1144,
                 1320, 1408, 1584, 1760, 1936,1936, 2112, 2288, 2464, 2816,
                 2816, 3168]

y = [8.3215, 6.0509, 5.9016, 6.0813, 6.0422, 13.0408, 12.1526, 12.3927, 12.3715,
     12.3911, 13.7148, 12.7409, 12.7674, 12.6592, 12.9244, 12.9035, 13.1053,
     13.2673, 13.3313, 13.5377, 13.5699, 13.8477, 13.7339, 14.0075, 14.2170,
     14.1827, 14.4384, 14.4373, 15.6146]
# y-a,xis values
y_tp = np.array(cb_length)*16 / np.array(y)
y_std = [0.509, 0.517, 0.184, 0.533, 0.516, 0.457, 0.380, 0.346, 0.327, 0.333,
         0.401, 0.341, 0.397, 0.333, 0.348, 0.398, 0.362, 0.376, 0.450, 0.379,
         0.414, 0.442, 0.444, 0.429, 0.467, 0.425, 0.472, 0.495, 0.649]

# y_std = np.array(cb_length)*16 / np.array(y_std)


y2 = [25.4136, 25.5123, 14.8861, 33.6098, 24.9462, 22.1637, 22.0116, 30.1583,
      30.9799, 30.2756, 22.9968, 30.4408, 23.7605, 30.8903, 23.8429, 30.5404,
      30.5359, 31.0620, 30.4530, 30.5735, 30.5627, 31.0922, 31.4741, 31.6777,
      31.9933, 31.2648, 31.9846, 32.4049, 32.5355]

y_tp_2 = np.array(cb_length)*64 / np.array(y2)
y_std_2 =[1.059, 1.081, 1.152, 1.763, 0.786, 1.010, 0.347, 0.826, 1.095, 0.972,
          0.506, 0.804, 0.542, 0.879, 0.394, 1.025, 0.828, 0.811, 0.754, 0.773,
          0.845, 0.824, 0.839, 0.838, 0.829, 0.800, 0.805, 0.910, 0.876]


y3 = [52.4967, 50.2012, 80.6944, 52.1784, 77.6836, 100.7217, 100.8020, 98.2381,
      98.5405, 97.9270, 99.1245, 99.5134, 99.5350, 98.6500, 99.6782, 99.3596,
      99.9782, 100.7760, 100.8428, 100.5464, 102.7395, 100.2825, 100.4271,
      100.1482]
y_tp_3 = np.array(cb_length_new)*256 / np.array(y3)
y_std_3 =[]

 # corresponding standard deviation values


# Calculate the upper and lower bounds for the shaded area
# y_upper = np.array(y) + np.array(y_std)
# y_lower = np.array(y) - np.array(y_std)
y_lower = np.array([
    17.096924, 11.478461, 11.146923, 14.032308, 11.293077, 17.916924, 18.77,
    17.023077, 20.046154, 16.24, 19.174616, 16.218462, 22.584616, 21.258461,
    18.214615, 16.681538, 16.433077, 16.895384, 25.323847, 17.165384, 19.927692,
    24.146154, 17.780769, 18.206923, 18.358461, 16.37077, 18.530001, 27.496923,
    22.844616])
y_upper = np.array([
    7.626154, 5.683077, 5.679231, 5.680769, 5.692307, 12.006923, 11.527692,
    11.736154, 11.700769, 11.72, 13.299231, 11.987692, 11.993846, 11.936153,
    12.115385, 12.092308, 12.271539, 12.41, 12.473846, 12.600769, 12.614615,
    12.803846, 12.808461, 12.942307, 13.126154, 13.088462, 13.278461, 13.293077,
    14.657692])
y_upper = np.array(cb_length)*16 / y_upper
y_lower = np.array(cb_length)*16 / y_lower

# y_upper_2 = np.array(y2) + np.array(y_std_2)
# y_lower_2 = np.array(y2) - np.array(y_std_2)
y_lower_2 = np.array([
    35.453075, 34.291538, 48.092308, 33.02, 31.964615, 33.30846, 31.732307,
    40.466923, 41.833076, 50.198463, 29.653076, 38.752308, 31.596153, 43.868462,
    29.833076, 39.368462, 38.994614, 37.39077, 38.119999, 44.053078, 38.705383,
    40.978462, 51.934616, 40.98, 38.241539, 36.426922, 37.24231, 52.202309,
    46.213844])
y_upper_2 = np.array([
    23.071539, 22.875385, 14.223077, 14.280769, 22.904615, 20.924616, 21.113846,
    27.861538, 28.498461, 27.863846, 22.100769, 28.056923, 22.690769, 28.591539,
    22.860769, 28.085384, 27.952307, 28.746923, 28.406923, 28.445385, 28.400768,
    28.801538, 29.091539, 29.225384, 29.788462, 28.831539, 29.693846, 30.044615,
    29.984615])
y_upper_2 = np.array(cb_length)*64 / y_upper_2
y_lower_2 = np.array(cb_length)*64 / y_lower_2
# y2_upper = np.array(y2) + np.array(y_std_17)
# y2_lower = np.array(y2) - np.array(y_std_17)
# y3_upper = np.array(y3) + np.array(y_std_28)
# y3_lower = np.array(y3) - np.array(y_std_28)


y_lower_3 = np.array([
    108.957695, 66.245384, 83.212311, 84.732307, 85.593849, 150.975388,
    122.658463, 111.540001, 154.83461, 114.262306, 111.863075, 109.543846,
    113.21846, 155.598465, 118.396927, 119.695381, 145.827698, 158.830765,
    114.083847, 143.360001, 115.28231, 145.158463, 110.016922, 152.0])
y_upper_3 = np.array([
    49.189232, 48.983845, 48.824615, 48.752308, 48.807693, 93.680771, 92.806923,
    92.604614, 94.246155, 93.775383, 94.224617, 95.006157, 93.563843, 92.28154,
    94.06308, 94.873077, 93.203079, 94.393074, 94.343079, 92.756157, 96.811539,
    94.293076, 94.076157, 93.580772])
y_upper_3 = np.array(cb_length_new)*256 / y_upper_3
y_lower_3 = np.array(cb_length_new)*256 / y_lower_3

# Convert from Mbps to Gbps
y_tp = np.array(y_tp) / 1000
y_upper = np.array(y_upper) / 1000
y_lower = np.array(y_lower) / 1000
y_tp_2 = np.array(y_tp_2) / 1000
y_upper_2 = np.array(y_upper_2) / 1000
y_lower_2 = np.array(y_lower_2) / 1000
y_tp_3 = np.array(y_tp_3) / 1000
y_upper_3 = np.array(y_upper_3) / 1000
y_lower_3 = np.array(y_lower_3) / 1000


# Creating the plot
fig, ax = plt.subplots(figsize=(6, 5))

# Plot with lines and shaded standard deviation
ax.plot(cb_length, y_tp, '-o', markersize=8, linewidth=3, label="NUM_CB = 16", color="tab:blue")
ax.fill_between(cb_length, y_lower, y_upper, color="tab:blue", alpha=0.3)

ax.plot(cb_length, y_tp_2, '-^', markersize=8, linewidth=3, label="NUM_CB = 64", color="tab:orange")
ax.fill_between(cb_length, y_lower_2, y_upper_2, color="tab:orange", alpha=0.3)

ax.plot(cb_length_new, y_tp_3, '-s', markersize=8, linewidth=3, label="NUM_CB = 256", color="tab:green")
ax.fill_between(cb_length_new, y_lower_3, y_upper_3, color="tab:green", alpha=0.3)


ax.grid(color='grey', linestyle='--', linewidth=0.5)

# Adding title and labels
ax.set_xlabel("$K_{cb}$", fontsize=24)
ax.set_ylabel("Throughput (Gbps)", fontsize=24)
ax.set_ylim([0, 9])
plt.xlim(0, 4600)
plt.xticks([0, 1000, 2000, 3000, 4224], fontsize=20)

# ax.set_xticks(fontsize=20)
# ax.set_xticklabels(fontsize=20)
ax.set_yticks(np.arange(0, 10, 1))
ax.set_yticklabels(ax.get_yticks(), fontsize=20)
# ax.set_title('Silicom', fontsize=28)
ax.legend(fontsize=15, loc="upper left")

# Save the plot
plt.savefig("../fig/mcs_vs_tp_blklen.pdf", bbox_inches='tight')

