#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math

class DIYLaserFilter(Node):
    def __init__(self):
        super().__init__('diy_laser_filter')
        
        # Subscribe to the noisy raw data
        self.subscription = self.create_subscription(
            LaserScan, '/scan_front_raw', self.scan_callback, 10)
            
        # Publish the clean data
        self.publisher = self.create_publisher(LaserScan, '/scan_front_filtered', 10)
        
        self.get_logger().info("Enhanced Laser Filter Started - Targets salt-and-pepper noise.")

    def median_filter(self, ranges, window_size=5):
        """Apply median filter to reduce salt-and-pepper noise."""
        half_window = window_size // 2
        filtered = list(ranges)
        
        for i in range(half_window, len(ranges) - half_window):
            # Get neighborhood
            neighborhood = []
            for j in range(i - half_window, i + half_window + 1):
                if not math.isinf(ranges[j]) and not math.isnan(ranges[j]):
                    neighborhood.append(ranges[j])
            
            if neighborhood:
                neighborhood.sort()
                filtered[i] = neighborhood[len(neighborhood) // 2]
            else:
                filtered[i] = float('inf')
        
        return filtered

    def aggressive_outlier_removal(self, ranges, threshold=0.08):
        """
        Remove outliers that differ significantly from neighbors.
        Uses a wider window (7 points) for better isolation detection.
        """
        filtered_ranges = list(ranges)
        
        for i in range(3, len(filtered_ranges) - 3):
            r_curr = filtered_ranges[i]
            
            if math.isinf(r_curr) or math.isnan(r_curr):
                continue
            
            # Get valid neighbors in a 7-point window
            neighbors = []
            for j in range(i - 3, i + 4):
                if j != i and not math.isinf(filtered_ranges[j]) and not math.isnan(filtered_ranges[j]):
                    neighbors.append(filtered_ranges[j])
            
            if not neighbors:
                continue
            
            # Calculate average of valid neighbors
            avg_neighbor = sum(neighbors) / len(neighbors)
            
            # If current point deviates significantly from neighbor average, mark as noise
            if abs(r_curr - avg_neighbor) > threshold:
                filtered_ranges[i] = float('inf')
        
        return filtered_ranges

    def edge_preserving_smooth(self, ranges, window_size=5, edge_threshold=0.2):
        """
        Smooth ranges while preserving edges (transitions between near and far objects).
        Uses moving average but preserves sharp discontinuities.
        """
        half_window = window_size // 2
        smoothed = list(ranges)
        
        for i in range(half_window, len(ranges) - half_window):
            if math.isinf(ranges[i]) or math.isnan(ranges[i]):
                continue
            
            # Get valid neighbors
            valid_neighbors = []
            for j in range(i - half_window, i + half_window + 1):
                if not math.isinf(ranges[j]) and not math.isnan(ranges[j]):
                    valid_neighbors.append(ranges[j])
            
            if len(valid_neighbors) < 3:
                continue
            
            # Check if we're at an edge (large difference between neighbors)
            min_neighbor = min(valid_neighbors)
            max_neighbor = max(valid_neighbors)
            is_edge = (max_neighbor - min_neighbor) > edge_threshold
            
            # Only smooth if not at an edge
            if not is_edge:
                smoothed[i] = sum(valid_neighbors) / len(valid_neighbors)
        
        return smoothed

    def scan_callback(self, msg):
        filtered_msg = msg
        filtered_ranges = list(msg.ranges)
        
        # Apply multiple filtering passes for aggressive noise reduction
        # Pass 1: Median filter (excellent for salt-and-pepper noise)
        filtered_ranges = self.median_filter(filtered_ranges, window_size=5)
        
        # Pass 2: Aggressive outlier removal
        filtered_ranges = self.aggressive_outlier_removal(filtered_ranges, threshold=0.08)
        
        # Pass 3: Edge-preserving smoothing
        filtered_ranges = self.edge_preserving_smooth(filtered_ranges, window_size=5, edge_threshold=0.15)
        
        # Pass 4: Final outlier sweep to catch remaining noise
        filtered_ranges = self.aggressive_outlier_removal(filtered_ranges, threshold=0.10)
        
        filtered_msg.ranges = filtered_ranges
        self.publisher.publish(filtered_msg)

def main(args=None):
    rclpy.init(args=args)
    node = DIYLaserFilter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()