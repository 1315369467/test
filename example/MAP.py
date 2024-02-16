import numpy as np
from scipy.stats import norm


def map_estimate(data, prior_mean, prior_variance, prior_mean_variance, prior_variance_alpha, prior_variance_beta):
    """
    计算给定数据和先验假设的均值和方差的MAP估计值。

    :param data: 观测数据列表或NumPy数组。
    :param prior_mean: 均值的先验分布的均值。
    :param prior_variance: 均值的先验分布的方差。
    :param prior_mean_variance: 均值先验均值的方差。
    :param prior_variance_alpha: 方差的先验分布的α参数（逆Gamma分布）。
    :param prior_variance_beta: 方差的先验分布的β参数（逆Gamma分布）。
    :return: 均值和方差的MAP估计值。
    """
    n = len(data)
    data_mean = np.mean(data)
    data_variance = np.var(data)

    # MAP估计均值
    map_mean_numerator = (prior_mean_variance / prior_variance * prior_mean) + (n * data_mean)
    map_mean_denominator = (prior_mean_variance / prior_variance) + n
    map_mean = map_mean_numerator / map_mean_denominator

    # MAP估计方差
    alpha_post = prior_variance_alpha + n / 2
    beta_post = prior_variance_beta + 0.5 * np.sum((data - data_mean) ** 2) + (
                n * prior_mean_variance * (data_mean - prior_mean) ** 2) / (
                            2 * (n * prior_mean_variance + prior_variance))
    map_variance = beta_post / (alpha_post + 1)

    return map_mean, map_variance


# 示例用法
data = np.random.normal(5, 2, 100)  # 样本数据
prior_mean = 0  # 均值的先验分布的均值
prior_variance = 10  # 均值的先验分布的方差
prior_mean_variance = 1  # 先验均值的方差
prior_variance_alpha = 2  # 方差的先验分布的α参数
prior_variance_beta = 2  # 方差的先验分布的β参数

map_mean, map_variance = map_estimate(data, prior_mean, prior_variance, prior_mean_variance, prior_variance_alpha,
                                      prior_variance_beta)
print(f"MAP估计均值: {map_mean}")
print(f"MAP估计方差: {map_variance}")

