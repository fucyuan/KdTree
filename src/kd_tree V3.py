import numpy as np
import matplotlib.pyplot as plt

class Node:
    """
    KD-Tree 节点类
    """
    def __init__(self, axis=None, value=None, left=None, right=None, point_indices=None):
        self.axis = axis  # 当前分割轴
        self.value = value  # 分割平面位置
        self.left = left  # 左子树
        self.right = right  # 右子树
        self.point_indices = point_indices  # 当前节点包含的点

class ResultSet:
    """
    存储最近邻结果的类
    """
    def __init__(self, k):
        self.k = k
        self.distances = []  # 最近邻的距离
        self.indices = []  # 最近邻的索引

    def add_point(self, distance, index):
        """
        添加点到结果集
        """
        if len(self.distances) < self.k:
            self.distances.append(distance)
            self.indices.append(index)
        else:
            # 如果结果集满了，替换掉最远的点
            max_idx = np.argmax(self.distances)
            if distance < self.distances[max_idx]:
                self.distances[max_idx] = distance
                self.indices[max_idx] = index

    def worst_dist(self):
        """
        返回结果集中最远的距离
        """
        if not self.distances:
            return float('inf')
        return max(self.distances)

def knn_search(node, points, query, result_set):
    """
    递归实现 k 最近邻搜索
    """
    if node is None:
        return

    # 如果是叶节点，比较叶节点中的所有点
    if node.value is None:
        for idx in node.point_indices:
            distance = np.linalg.norm(np.array(points[idx]) - np.array(query))
            result_set.add_point(distance, idx)
        return

    # 判断查询点在左子树还是右子树
    if query[node.axis] <= node.value:
        first, second = node.left, node.right
    else:
        first, second = node.right, node.left

    # 优先搜索与查询点同侧的子树
    knn_search(first, points, query, result_set)

    # 检查分割平面，决定是否需要搜索另一侧子树
    if abs(query[node.axis] - node.value) < result_set.worst_dist():
        knn_search(second, points, query, result_set)

def kdtree_recursive_build(points, point_indices, axis=0, leaf_size=1, plot_range=None, ax=None):
    """
    递归构建 KD-Tree，并包含可视化功能。
    """
    if len(point_indices) <= leaf_size:
        return Node(axis=axis, value=None, left=None, right=None, point_indices=point_indices)

    # 根据分割轴排序
    point_indices_sorted = sorted(point_indices, key=lambda idx: points[idx][axis])

    # 计算分割线的位置（中位数）
    median_idx = len(point_indices_sorted) // 2
    median_value = points[point_indices_sorted[median_idx]][axis]

    # 递归构造左右子树
    left_child = kdtree_recursive_build(
        points, point_indices_sorted[:median_idx], (axis + 1) % len(points[0]), leaf_size, plot_range, ax)
    right_child = kdtree_recursive_build(
        points, point_indices_sorted[median_idx + 1:], (axis + 1) % len(points[0]), leaf_size, plot_range, ax)

    # 创建节点
    return Node(axis=axis, value=median_value, left=left_child, right=right_child, point_indices=None)

# 示例点
points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (6, 3), (1, 9), (3, 8)]
point_indices = list(range(len(points)))

# 构建 KD-Tree
kd_tree = kdtree_recursive_build(points, point_indices)

# 查询点
query_point = (6, 4)

# 最近邻搜索
k = 2
result_set = ResultSet(k)
knn_search(kd_tree, points, query_point, result_set)

# 输出结果
print(f"Query Point: {query_point}")
print("Nearest Neighbors:")
for dist, idx in zip(result_set.distances, result_set.indices):
    print(f"Point: {points[idx]}, Distance: {dist}")
