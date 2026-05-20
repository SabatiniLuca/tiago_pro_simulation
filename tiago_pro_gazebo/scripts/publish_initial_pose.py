#!/usr/bin/env python3
import rclpy
from geometry_msgs.msg import PoseWithCovarianceStamped, Pose, Point, Quaternion
import time

def main():
    rclpy.init()
    node = rclpy.create_node('initial_pose_publisher')
    publisher = node.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)
    
    time.sleep(5)  # Wait for robot to start
    
    pose_msg = PoseWithCovarianceStamped()
    pose_msg.header.frame_id = 'map'
    pose_msg.pose.pose.position = Point(x=0.0, y=1.85, z=0.03)
    pose_msg.pose.pose.orientation = Quaternion(x=0.0, y=0.0, z=-0.7071068, w=0.7071068)
    # 6x6 covariance matrix: [x, y, z, rot_x, rot_y, rot_z]
    covariance = [0.0] * 36
    covariance[0] = 0.25  # x variance
    covariance[7] = 0.25  # y variance
    covariance[35] = 0.06853891945200942  # yaw variance
    pose_msg.pose.covariance = covariance
    
    publisher.publish(pose_msg)
    time.sleep(10)  # Allow time for message to be published
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()