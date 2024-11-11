import matplotlib.pyplot as plt
import numpy as np

# Data
exponents = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Exponents for 2^0, 2^1, 2^2, 2^3, 2^4...
exponents_2 = [0, 1, 2, 3, 4, 5, 6]  # Exponents for 2^0, 2^1, 2^2, 2^3, 2^4...
num_cb = [1,2,4,8,16,32,64,128,256,512,1024]
num_cb_2 = [1,2,4,8,16,32,64]


y = [99.18, 197.74, 353.92, 630.88, 1068.16, 1585.92, 2118.40, 2336.48, 2498.28, 2575.68, 2611.20]  # y-axis values
y_std_mcs10 = [1.711, 6.522, 16.852, 32.512, 95.952, 128.192, 59.3036, 52.48, 48.128, 34.304, 39.936]
y_time_min = [9.477693, 9.503077, 9.906154, 11.272307, 11.952308, 17.733076, 23.936924, 48.983078, 92.739227, 181.490768,354.923859]
y_time_max = [15.363846, 19.18, 18.852308, 22.753845, 22.978462, 33.098461, 45.796925, 63.697693, 119.980003, 212.691544, 443.728455]



y2 = [202.52, 390.50, 770.08, 1430.64, 2438.88, 3789.12, 3988.92, 4573.12, 4932.32, 5064.68, 5200.32]
y_std_17 =[2.854, 11.974, 15.92, 39.928, 65.248, 61.024, 104.231, 124.416, 95.488, 80.384, 69.632]
y2_time_min = [9.385385, 9.552308, 9.815385, 10.555385, 12.37, 16.144615, 28.7460001, 50.773846, 94.160767, 182.461533, 361.106934]
y2_time_max = [13.565385, 19.308462, 13.88, 14.416924, 23.031538, 24.401539, 43.735386, 70.480003, 121.414612, 236.235382, 439.690002]


time = [10.1013, 10.3578, 10.6632, 12.0027, 14.6575, 19.1482, 32.1900] 

y3 = 4224 * np.array([1,2,4,8,16,32,64]) / np.array(time)
y_std_28 =[3.409, 3.933, 4.679, 16.402, 10.344, 4.296, 3.192]
y_std_28 = np.array([1,2,4,8,16,32,64]) * np.array(y_std_28)
y3_time_min = [9.98, 10.164616, 10.46, 11.175385, 13.46077, 17.992308, 29.717691]
y3_time_max = [13.416154, 13.133077, 20.374615, 15.491538, 23.438461, 22.585384, 41.315384]

# Calculate the upper and lower bounds for the shaded area
y_upper = 968 * np.array(num_cb) / np.array(y_time_min)
y_lower = 968 * np.array(num_cb) / np.array(y_time_max)
y2_upper = 1936 * np.array(num_cb) / np.array(y2_time_min)
y2_lower = 1936 * np.array(num_cb) / np.array(y2_time_max)
y3_upper = 4224 * np.array(num_cb_2) / np.array(y3_time_min)
y3_lower = 4224 * np.array(num_cb_2) / np.array(y3_time_max)

# scale from Mbps to Gbps
y = np.array(y) / 1000
y_upper = np.array(y_upper) / 1000
y_lower = np.array(y_lower) / 1000
y2 = np.array(y2) / 1000
y2_upper = np.array(y2_upper) / 1000
y2_lower = np.array(y2_lower) / 1000
y3 = np.array(y3) / 1000
y3_upper = np.array(y3_upper) / 1000
y3_lower = np.array(y3_lower) / 1000

# Create an array for the x-axis labels with superscript notation
x_labels = [f'$2^{exp}$' if exp != 10 else '$2^{10}$' for exp in exponents]
x_ticks = exponents # [2**exp for exp in exponents]
x_ticks_2 = exponents_2 # [2**exp for exp in exponents_2]

# Creating the plot
fig, ax = plt.subplots(figsize=(6, 5))

# Plot with lines and shaded standard deviation
ax.plot(x_ticks, y, '-o', markersize=10, linewidth=3, label="$K_{cb} = 968$", color="tab:blue")
ax.fill_between(x_ticks, y_lower, y_upper, color="tab:blue", alpha=0.3)

ax.plot(x_ticks, y2, '-^', markersize=10, linewidth=3, label="$K_{cb} = $1,936", color="tab:orange")
ax.fill_between(x_ticks, y2_lower, y2_upper, color="tab:orange", alpha=0.3)

ax.plot(x_ticks_2, y3, '-s', markersize=10, linewidth=3, label="$K_{cb} =$4,224", color="tab:green")
ax.fill_between(x_ticks_2, y3_lower, y3_upper, color="tab:green", alpha=0.3)

ax.grid(color='grey', linestyle='--', linewidth=0.5)

# Adding title and labels
ax.set_xlabel("Number of Code Blocks", fontsize=24)
ax.set_ylabel("Throughput (Gbps)", fontsize=24)
ax.set_ylim([0, 9])
# ax.set_xscale('log', base=2)
# ax.set_xlim(0.5, 2**11)
ax.set_xticks(x_ticks)
ax.set_xticks(exponents)
ax.set_xticklabels(x_labels, fontsize=20)
ax.set_xticklabels(x_labels, fontsize=20)
ax.set_yticks(np.arange(0, 10, 1))
ax.set_yticklabels(ax.get_yticks(), fontsize=20)

# ax.set_title('Silicom', fontsize=28)
ax.legend(fontsize=15, loc="upper left")

# Save the plot
plt.savefig("../fig/mcs10_17_28_enq.pdf", bbox_inches='tight')
