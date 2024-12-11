# KD-Tree Implementation with k-Nearest Neighbors (k-NN) Search

## Overview
This project implements a KD-Tree data structure and a k-Nearest Neighbors (k-NN) search algorithm in C++. It allows efficient organization and querying of multi-dimensional points for tasks such as finding the closest neighbors to a given query point.

## Features
- **KD-Tree Construction**: Efficiently builds a KD-Tree from a given set of points.
- **k-NN Search**: Finds the k-nearest neighbors of a query point using the KD-Tree.
- **Leaf Node Handling**: Supports storing multiple points in leaf nodes for customizable granularity.
- **Distance Calculation**: Computes Euclidean distances between points for k-NN search.

## How It Works
1. **KD-Tree Construction**:
   - The tree is built recursively by splitting the points along alternating axes (x or y in 2D).
   - Points are sorted based on their coordinate values along the current axis.
   - Leaf nodes store indices of points when the number of points is below a specified threshold.

2. **k-NN Search**:
   - The algorithm navigates the KD-Tree recursively, visiting the subtree closer to the query point first.
   - The far subtree is searched only if the distance to the splitting plane is smaller than the distance to the current farthest neighbor.
   - A max heap is used to keep track of the k closest neighbors found so far.

## Code Structure
### Classes and Functions
- **`struct Point`**:
  - Represents a 2D point with `x` and `y` coordinates.

- **`class Node`**:
  - Represents a KD-Tree node, storing splitting axis, splitting value, left and right subtrees, and point indices for leaf nodes.

- **`struct Neighbor`**:
  - Stores distance and index of a neighboring point, used in k-NN search.

- **`class ResultSet`**:
  - Manages the result set of k-nearest neighbors using a max heap and ensures no duplicate points are added.

- **`double calculateDistance(const Point& a, const Point& b)`**:
  - Computes the Euclidean distance between two points.

- **`Node* kdtreeRecursiveBuild(const std::vector<Point>& points, const std::vector<int>& point_indices, int axis, int leaf_size)`**:
  - Recursively builds the KD-Tree.

- **`void knnSearch(Node* node, const std::vector<Point>& points, const Point& query, ResultSet& result_set)`**:
  - Recursively searches the KD-Tree for k-nearest neighbors of the query point.

## Usage
### Input
- A set of 2D points specified as a vector of `Point` structs.
- A query point specified as a `Point` struct.
- The desired number of neighbors, `k`.

### Output
- The coordinates and distances of the k-nearest neighbors to the query point.

### Example
```cpp
// Example points
std::vector<Point> points = {{2, 3}, {5, 4}, {9, 6}, {4, 7}, {8, 1}, {7, 2}, {6, 3}, {1, 9}, {3, 8}};

// Query point
Point query_point = {6, 4};

// Number of neighbors
int k = 3;

// Execute k-NN search
ResultSet result_set(k);
knnSearch(kd_tree, points, query_point, result_set);

// Output results
result_set.printResults(points);
```

### Sample Output
```
Query Point: (6, 4)
Nearest Neighbors:
Point: (5, 4), Distance: 1
Point: (6, 3), Distance: 1
Point: (7, 2), Distance: 2.23607
```

## Compilation and Execution
1. Save the code to a file, e.g., `kdtree_knn.cpp`.
2. Compile the code using a C++ compiler (e.g., g++):
   ```bash
   g++ -o kdtree_knn kdtree_knn.cpp
   ```
3. Run the compiled program:
   ```bash
   ./kdtree_knn
   ```

## Parameters
- **`leaf_size`**:
  - Defines the maximum number of points stored in leaf nodes. Adjust this to balance construction and query efficiency.

## Notes
- The implementation assumes 2D points but can be extended to higher dimensions with minimal modifications.
- The code uses a priority queue to manage the k-nearest neighbors efficiently.

## Limitations
- Memory usage may increase for large datasets due to the storage of point indices and heap management.
- Currently designed for static datasets. Dynamic insertion and deletion are not supported.

## License
This project is released under the MIT License.

