import matplotlib.pyplot as plt
import numpy as np

# Data
imbalance_coefficients = [1, 2, 3, 4]
TIM = [69.9, 70.7, 70.8, 71.0]
protoPL = [68.6, 73.4, 75.8, 77.3]
PUTM = [70.1, 73.2, 74.4, 75.1]
AM = [72.5, 73.4, 73.6, 73.9]
our = [71.8, 75.8, 77.2, 78.5]

# Set bar width and position
bar_width = 0.15
index = np.arange(len(imbalance_coefficients))

# Create the bar chart
fig, ax = plt.subplots(figsize=(5, 4))

bar1 = ax.bar(index - 2*bar_width, TIM, bar_width, label='α-TIM')
bar2 = ax.bar(index - bar_width, protoPL, bar_width, label='ProtoLP')
bar3 = ax.bar(index, PUTM, bar_width, label='PUTM')
bar4 = ax.bar(index + bar_width, AM, bar_width, label='AM')
bar5 = ax.bar(index + 2*bar_width, our, bar_width, label='SGMP')

# Add labels and title
plt.xlabel('Imbalance Level')
plt.ylabel('Mean Accuracy (%)')
plt.title('mini-ImageNet 5-way 1-shot')
ax.set_xticks(index)
ax.set_xticklabels(imbalance_coefficients)
ax.set_ylim([65, 80])
ax.legend()

# # Annotate the bars with values
# for bars in [bar1, bar2, bar3, bar4, bar5]:
#     for bar in bars:
#         yval = bar.get_height()
#         ax.text(bar.get_x() + bar.get_width()/2, yval + 0.2, round(yval, 1),
#                 ha='center', va='bottom', fontsize=8)

# Adjust layout
fig.tight_layout()

# Show the plot
plt.show()
