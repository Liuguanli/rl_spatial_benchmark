import random
import unittest
from qdtree_env import QdtreeEnv  # Make sure this import reflects your actual module and class structure

class TestQdtreeEnv(unittest.TestCase):
    def setUp(self):
        """Initialize the environment before each test."""
        self.env = QdtreeEnv(
            leaf_threshold=100,
            dataset_path='../../data/synthetic/dataset/data_100000_2_uniform_1.csv',  # Update this path to your dataset
            workload_path='../../data/synthetic/query/range_1000_2_uniform_1_0.01x0.01.csv',  # Update this path to your workload
            dimension=2,
            dump_dir=None,
            sampling_ratio=0.01,
            action_sampling_size=400,
            zero_obs=False
        )

    def test_initial_conditions(self):
        """Test initial setup conditions of the environment."""
        self.assertEqual(self.env.leaf_threshold, 100)
        self.assertIsNotNone(self.env.points)
        self.assertIsNotNone(self.env.query_rectangles)
        self.assertEqual(len(self.env.actions), 400)  # Adjust according to your setup

    def test_load_data(self):
        """Test the data loading mechanism."""
        points = self.env.load_data('../../data/synthetic/dataset/data_100000_2_uniform_1.csv')
        self.assertTrue(len(points) > 0)

    def test_load_workloads(self):
        """Test the workload loading mechanism."""
        workloads = self.env.load_workloads('../../data/synthetic/query/range_1000_2_uniform_1_0.01x0.01.csv')
        self.assertTrue(len(workloads) > 0)

    def test_action_generation(self):
        """Test action generation logic."""
        actions = self.env.gen_actions(is_sample=True, sample_size=100)
        self.assertEqual(len(actions), 100)

    def test_reset(self):
        """Test the reset functionality of the environment."""
        initial_state = self.env.reset()
        self.assertIsNotNone(initial_state)

    def test_step(self):
        """Test the step function."""
        self.env.reset()
        initial_state, _, _, _ = self.env.step(1)
        self.assertIsNotNone(initial_state)

    def test_integration(self):
        """Test a simple sequence of actions."""
        self.env.reset()
        for action in random.sample(self.env.actions, 10):
            state, reward, done, _ = self.env.step(1)
            self.assertFalse(done)  # Adjust based on expected behavior

        # Test completion
        self.env.node_queue = []
        _, _, done, _ = self.env.step(1)
        self.assertTrue(done)  # This assumes the last step completes the episode

# Run the tests
if __name__ == '__main__':
    unittest.main()

# python -m unittest rl_baseline/Qdtree/test_qdtree_env.py
