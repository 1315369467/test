import matplotlib.pyplot as plt
import numpy as np

# Data from the ResNet-12 table
methods = ['LR+ICI', 'iLPC', 'protoLP', 'Ours']
labels = ['mini 1-shot', 'mini 5-shot', 'tiered 1-shot', 'tiered 5-shot']
data_resnet = {
    'mini 1-shot': [67.57, 70.99, 72.21, 73.72],
    'mini 5-shot': [79.07, 81.06, 81.48, 82.50],
    'tiered 1-shot': [83.32, 85.04, 85.22, 86.83],
    'tiered 5-shot': [89.06, 89.58, 89.65, 90.80]
}

x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars


SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

fig, axs = plt.subplots(1, 2, figsize=(10, 4))

# ResNet-12 Plot
rects1_resnet = axs[0].bar(x - 1.5*width, [data_resnet[label][0] for label in labels], width, label=methods[0])
rects2_resnet = axs[0].bar(x - 0.5*width, [data_resnet[label][1] for label in labels], width, label=methods[1])
rects3_resnet = axs[0].bar(x + 0.5*width, [data_resnet[label][2] for label in labels], width, label=methods[2])
rects4_resnet = axs[0].bar(x + 1.5*width, [data_resnet[label][3] for label in labels], width, label=methods[3])

# axs[0].set_xlabel('Settings')
axs[0].set_ylabel('Accuracy Mean (%)')
axs[0].set_title('Semi-supervised FSL setting (ResNet-12)')
axs[0].set_xticks(x)
axs[0].set_xticklabels(labels)
axs[0].set_ylim(65, 93)
axs[0].legend()

for rect in [rects1_resnet, rects2_resnet, rects3_resnet, rects4_resnet]:
    for r in rect:
        height = r.get_height()
        axs[0].annotate(f'{height:.1f}',
                        xy=(r.get_x() + r.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=6)


methods = ['LR+ICI', 'iLPC', 'protoLP', 'Ours']
labels = ['mini 1-shot', 'mini 5-shot', 'tiered 1-shot', 'tiered 5-shot']

data_wrn = {
    'mini 1-shot': [81.31, 83.58, 84.25, 85.18],
    'mini 5-shot': [88.53, 89.68, 89.48, 90.35],
    'tiered 1-shot': [88.48, 89.35, 90.10, 90.69],
    'tiered 5-shot': [92.03, 92.61, 92.49, 93.32]
}
# WRN-28-10 Plot
rects1_wrn = axs[1].bar(x - 1.5*width, [data_wrn[label][0] for label in labels], width, label=methods[0])
rects2_wrn = axs[1].bar(x - 0.5*width, [data_wrn[label][1] for label in labels], width, label=methods[1])
rects3_wrn = axs[1].bar(x + 0.5*width, [data_wrn[label][2] for label in labels], width, label=methods[2])
rects4_wrn = axs[1].bar(x + 1.5*width, [data_wrn[label][3] for label in labels], width, label=methods[3])

# axs[1].set_xlabel('Settings')
axs[1].set_ylabel('Accuracy Mean (%)')
axs[1].set_title('Semi-supervised FSL setting (WRN-28-10)')
axs[1].set_xticks(x)
axs[1].set_xticklabels(labels)
axs[1].set_ylim(80, 95)
axs[1].legend()

for rect in [rects1_wrn, rects2_wrn, rects3_wrn, rects4_wrn]:
    for r in rect:
        height = r.get_height()
        axs[1].annotate(f'{height:.1f}',
                        xy=(r.get_x() + r.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=6)

fig.tight_layout()

plt.show()
