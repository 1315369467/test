import matplotlib.pyplot as plt
import numpy as np

# Extract data from the table
M_values = [2, 5, 10, 20, 30, 50]
M_scores = [69.55, 70.80, 71.13, 71.24, 71.29, 71.35]

alpha_values = [0, 0.2, 0.5, 0.7, 0.9, 1.0]
alpha_scores = [66.01, 69.73, 71.18, 71.35, 70.90, 70.51]

lambda_values = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
lambda_scores = [71.20, 71.28, 71.35, 71.30, 71.03, 70.85]

beta_values = [0, 0.2, 0.5, 1.0, 1.5, 2.0]
beta_scores = [66.02, 70.70, 71.35, 71.27, 71.23, 71.20]

# Create a 2x2 subplot layout
fig, axs = plt.subplots(2, 2, figsize=(10, 8))
# fig.suptitle('Performance Comparison of Different Parameters', fontsize=16)

# Function to add values on top of bars
# 使用 annotate 添加顶部数值，固定偏移量（单位：points）
def add_values(ax, scores, offset_points=5):
    for i, score in enumerate(scores):
        ax.annotate(f'{score:.2f}',
                    xy=(i, score),
                    xytext=(0, offset_points),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=12)

# Plot histogram for parameter M
bars1 = axs[0, 0].bar(range(len(M_values)), M_scores)
axs[0, 0].set_title('Effect of Hyper-parameter M')
# axs[0, 0].set_xlabel('M value')
axs[0, 0].set_ylabel('Performance Score')
axs[0, 0].set_xticks(range(len(M_values)))
axs[0, 0].set_xticklabels(M_values)
axs[0, 0].set_ylim(69, 72)
add_values(axs[0, 0], M_scores)

# Plot histogram for parameter alpha
bars2 = axs[0, 1].bar(range(len(alpha_values)), alpha_scores)
axs[0, 1].set_title('Effect of Hyper-parameter α')
# axs[0, 1].set_xlabel('α value')
axs[0, 1].set_ylabel('Performance Score')
axs[0, 1].set_xticks(range(len(alpha_values)))
axs[0, 1].set_xticklabels(alpha_values)
axs[0, 1].set_ylim(65, 73)
add_values(axs[0, 1], alpha_scores)

# Plot histogram for parameter lambda
bars3 = axs[1, 0].bar(range(len(lambda_values)), lambda_scores)
axs[1, 0].set_title('Effect of Hyper-parameter λ')
# axs[1, 0].set_xlabel('λ value')
axs[1, 0].set_ylabel('Performance Score')
axs[1, 0].set_xticks(range(len(lambda_values)))
axs[1, 0].set_xticklabels(lambda_values)
axs[1, 0].set_ylim(70.5, 71.6)
add_values(axs[1, 0], lambda_scores)

# Plot histogram for parameter beta
bars4 = axs[1, 1].bar(range(len(beta_values)), beta_scores)
axs[1, 1].set_title('Effect of Hyper-parameter β')
# axs[1, 1].set_xlabel('β value')
axs[1, 1].set_ylabel('Performance Score')
axs[1, 1].set_xticks(range(len(beta_values)))
axs[1, 1].set_xticklabels(beta_values)
axs[1, 1].set_ylim(65, 73)
add_values(axs[1, 1], beta_scores)


# Adjust layout
# plt.tight_layout(rect=[0, 0, 1, 0.96])

# Display the chart
plt.show()