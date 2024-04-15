import argparse
import csv
import bisect
import struct


class Node:
    def __init__(self, dimension=2, partition_dimension=None, partition_value=None, points=None, capacity=0, domain=None, id=0):
        # Common properties
        self.partition_dimension = partition_dimension
        self.partition_value = partition_value
        self.left = None
        self.right = None
        # Leaf node specific properties
        self.points = points if points is not None else []
        self.capacity = capacity
        self.domain = domain
        self.state = None
        self.action = 0
        self.reward = 0.0
        self.dimension = dimension
        self.id = 0

    # def split(self, split_dim=0, median_value=0):
    #     if not self.points:
    #         return None
        
    #     # if len(points) <= self.leaf_capacity:
    #     #     return Node(points=points, capacity=self.leaf_capacity)
    #     left_points = [point for point in self.points if (point[split_dim] + point[split_dim + self.dim]) / 2 <= median_value]
    #     right_points = [point for point in self.points if (point[split_dim] + point[split_dim + self.dim]) / 2 > median_value]
        
    def get_state(self):
        # range & mask
        state = []
        for i in range(self.dimension):
            state.extend(self.float_to_bit_array(self.domain[i][0]))
            state.extend(self.float_to_bit_array(self.domain[i][1]))
            
        # for i in range(self.dimension):
        #     dim_candidate_partitions = candidate_partitions[i]
        #     dim_categorical_mask = [0] * (len(dim_candidate_partitions) + 1)
        #     split_vals = []
        #     for j in range(len(dim_candidate_partitions)):
        #         split_dim, split_val = dim_candidate_partitions[i]
        #         split_vals.append(split_val)
        #     split_vals.sort()

        #     for point in self.points:
        #         pos = bisect.bisect_left(split_vals, (point[i] + point[i + self.dimension]) / 2)
        #         dim_categorical_mask[pos] = 1
        #     state.extend(dim_categorical_mask)

        return state
        

    def float_to_bit_array(self, f):
        # Pack the floating point number into 4 bytes of binary data using big-endian format
        binary_string = struct.pack('>f', f)
        # Convert the binary data to an unsigned integer
        as_int = struct.unpack('>I', binary_string)[0]
        # Convert the integer to a 32-bit binary string
        bit_string = format(as_int, '032b')
        # Convert the binary string to an array of integers (0s and 1s)
        bit_array = [int(bit) for bit in bit_string]
        return bit_array

    def is_leaf(self):
        # A node is considered a leaf if it has no children and has a list of points
        return len(self.points) <= self.capacity


class QDTree:
    def __init__(self, leaf_capacity=2, dimension=2, query_rectangles=[]):
        self.root = None
        self.leaf_capacity = leaf_capacity  # Maximum number of points a leaf node can store
        self.dimension = dimension
        self.query_rectangles = query_rectangles


    def build(self, points, domain):
        self.root = Node(dimension=self.dimension, points=points, capacity=self.leaf_capacity, domain=domain)
        return self.root



def print_tree(node, depth=0):
    """Recursively print a simple representation of the KD tree, mainly for verification purposes."""
    if node is None:
        return
    indent = "  " * depth
    if node.is_leaf():
        print(f"{indent}Leaf({len(node.points)} points)")
    else:
        print(f"{indent}Node(dim={node.partition_dimension}, value={node.partition_value})")
    print_tree(node.left, depth + 1)
    print_tree(node.right, depth + 1)

def main(args):

    dataset = []
    with open(args.dataset_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            dataset.append([float(item) for item in row])
            dataset[-1].extend(dataset[-1])

    query_rectangles = []
    with open(args.queryset_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            query_rectangles.append([float(item) for item in row])
    
    # Build the KD tree
    tree = QDTree(leaf_capacity=args.leaf_capacity, dimension=args.dimension, query_rectangles=query_rectangles)  
    tree.build(dataset, query_rectangles)
    
    # Print the constructed KD tree
    print("KD Tree:")
    print_tree(tree.root)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate synthetic data.")
    parser.add_argument("-leaf_capacity", type=int, help="Number of data points in a leaf node.", required=False, default=100)
    parser.add_argument("-dimension", type=int, help="Number of dimensions.", required=False, default=2)
    # parser.add_argument("--distribution", type=str, help="Type of distribution (uniform, normal, skewed).", required=True)
    # parser.add_argument("--skewness", type=int, help="Skewness of skew data.", required=False)
    # parser.add_argument("--range", type=float, nargs=2, action='append', help="Range for each dimension. Repeat this argument for each dimension.", required=True)
    # parser.add_argument("--output", type=str, help="Output CSV file path.", required=True)
    parser.add_argument('-dataset_filename', help='data set', required=True, default='')
    parser.add_argument('-queryset_filename', help='query data', required=True, default='')
    args = parser.parse_args()

    main(args)


# python rl_baseline/Qdtree/qdtree.py -dataset_filename data/synthetic/dataset/data_100000_2_uniform_1.csv -queryset_filename range_1000_2_uniform_1_0.01x0.01.csv

