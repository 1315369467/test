import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def visualize_model_predictions(image_path, predictions, uncertainties, true_label, top_k=5):
    """
    Visualize predictions from different models including uncertainties

    Args:
        image_path: Path to the input image
        predictions: Dict with keys 'CLIP', 'Aux1', 'Aux2', 'Fusion' containing prediction arrays
        uncertainties: Dict with same keys containing uncertainty values
        true_label: Ground truth class index
        top_k: Number of top classes to show
    """
    # Set style
    plt.style.use('seaborn')

    # Create figure with subplots
    fig = plt.figure(figsize=(15, 10))
    gs = plt.GridSpec(2, 2, figure=fig)

    # Load and show the image
    img = plt.imread(image_path)
    ax_img = fig.add_subplot(gs[0, 0])
    ax_img.imshow(img)
    ax_img.axis('off')
    ax_img.set_title('Input Image', pad=10)

    # Plot predictions for each model
    models = ['CLIP', 'Aux1', 'Aux2', 'Fusion']
    colors = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c']

    # Get top k classes across all models
    all_preds = np.concatenate([predictions[m] for m in models])
    top_classes = np.unique(np.argsort(-all_preds)[:, :top_k].flatten())

    # Create bar plots
    for idx, model in enumerate(models):
        ax = fig.add_subplot(gs[idx // 2, 1 if idx % 2 else 0])

        # Get predictions and uncertainties
        preds = predictions[model][0][top_classes]
        uncer = uncertainties[model][0][top_classes]

        # Create bars
        x = np.arange(len(top_classes))
        bars = ax.bar(x, preds, color=colors[idx], alpha=0.6)

        # Add error bars for uncertainty
        ax.errorbar(x, preds, yerr=uncer, fmt='none', color='gray', capsize=5)

        # Customize plot
        ax.set_title(f'{model} Predictions', pad=10)
        ax.set_xticks(x)
        ax.set_xticklabels([f'Class {i}' for i in top_classes], rotation=45)
        ax.set_ylim(0, 1.2)

        # Highlight true class
        if true_label in top_classes:
            true_idx = np.where(top_classes == true_label)[0][0]
            bars[true_idx].set_color('gold')
            bars[true_idx].set_alpha(1.0)

    # Add legend
    legend_elements = [
        Patch(facecolor='gold', label='True Class'),
        Patch(facecolor='gray', alpha=0.3, label='Uncertainty')
    ]
    fig.legend(handles=legend_elements, loc='center right')

    # Adjust layout
    plt.tight_layout()
    return fig


# Example usage
def create_example_visualization():
    # Sample data (replace with real predictions)
    num_classes = 10
    models = ['CLIP', 'Aux1', 'Aux2', 'Fusion']
    predictions = {
        model: np.random.dirichlet(np.ones(num_classes), size=1)
        for model in models
    }
    uncertainties = {
        model: np.random.uniform(0, 0.1, size=(1, num_classes))
        for model in models
    }

    # Create visualization
    fig = visualize_model_predictions(
        image_path='sample_image.jpg',
        predictions=predictions,
        uncertainties=uncertainties,
        true_label=3,
        top_k=5
    )

    return fig


# Function to process real model outputs
def process_model_outputs(clip_output, aux1_output, aux2_output, fusion_output):
    """
    Process raw model outputs to get predictions and uncertainties

    Args:
        *_output: Model logits/probabilities (shape: batch_size x num_classes)
    Returns:
        predictions: Dict of normalized probabilities
        uncertainties: Dict of uncertainties computed using Kurtosis
    """

    def compute_uncertainty(logits):
        # Compute normalized Kurtosis as uncertainty measure
        mean = np.mean(logits, axis=1, keepdims=True)
        std = np.std(logits, axis=1, keepdims=True)
        kurtosis = np.mean(((logits - mean) / std) ** 4, axis=1, keepdims=True)
        return 1 / kurtosis  # Higher kurtosis = lower uncertainty

    # Convert logits to probabilities
    def softmax(x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

    predictions = {
        'CLIP': softmax(clip_output),
        'Aux1': softmax(aux1_output),
        'Aux2': softmax(aux2_output),
        'Fusion': softmax(fusion_output)
    }

    uncertainties = {
        'CLIP': compute_uncertainty(clip_output),
        'Aux1': compute_uncertainty(aux1_output),
        'Aux2': compute_uncertainty(aux2_output),
        'Fusion': compute_uncertainty(fusion_output)
    }

    return predictions, uncertainties

# 处理模型输出
predictions, uncertainties = process_model_outputs(
    clip_output,
    aux1_output,
    aux2_output,
    fusion_output
)

# 创建可视化
fig = visualize_model_predictions(
    image_path='path_to_image.jpg',
    predictions=predictions,
    uncertainties=uncertainties,
    true_label=true_class,
    top_k=5
)

# 保存图片
fig.savefig('predictions_visualization.png', dpi=300, bbox_inches='tight')