#!/usr/bin/env python3
#rosrun px4 formation_control.py
import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.srv import SetMode, CommandBool
import time

leader_pose = PoseStamped()
last_leader_position = None

def leader_pose_callback(data):
    global leader_pose, last_leader_position
    leader_pose = data

    if last_leader_position is None or (
        leader_pose.pose.position.x != last_leader_position.pose.position.x or
        leader_pose.pose.position.y != last_leader_position.pose.position.y or
        leader_pose.pose.position.z != last_leader_position.pose.position.z
    ):
        rospy.loginfo("UAV0当前位置: x: {:.2f}, y: {:.2f}, z: {:.2f}".format(
            leader_pose.pose.position.x, 
            leader_pose.pose.position.y, 
            leader_pose.pose.position.z
        ))
        last_leader_position = PoseStamped()
        last_leader_position.pose.position.x = leader_pose.pose.position.x
        last_leader_position.pose.position.y = leader_pose.pose.position.y
        last_leader_position.pose.position.z = leader_pose.pose.position.z

def set_mode(service, mode):
    try:
        service(base_mode=0, custom_mode=mode)
        rospy.loginfo("模式设置为 {}".format(mode))
    except rospy.ServiceException as e:
        rospy.logerr("设置模式失败: %s" % e)

def arm(service):
    try:
        service(True)
        rospy.loginfo("解锁成功")
    except rospy.ServiceException as e:
        rospy.logerr("解锁失败: %s" % e)

def main():
    rospy.init_node('formation_control', anonymous=True)

    # Subscribers
    rospy.Subscriber('/uav0/mavros/local_position/pose', PoseStamped, leader_pose_callback)

    # Publishers
    follower1_pub = rospy.Publisher('/uav1/mavros/setpoint_position/local', PoseStamped, queue_size=10)
    follower2_pub = rospy.Publisher('/uav2/mavros/setpoint_position/local', PoseStamped, queue_size=10)

    # Services
    rospy.wait_for_service('/uav1/mavros/set_mode')
    rospy.wait_for_service('/uav1/mavros/cmd/arming')
    rospy.wait_for_service('/uav2/mavros/set_mode')
    rospy.wait_for_service('/uav2/mavros/cmd/arming')

    set_mode_uav1 = rospy.ServiceProxy('/uav1/mavros/set_mode', SetMode)
    arm_uav1 = rospy.ServiceProxy('/uav1/mavros/cmd/arming', CommandBool)
    set_mode_uav2 = rospy.ServiceProxy('/uav2/mavros/set_mode', SetMode)
    arm_uav2 = rospy.ServiceProxy('/uav2/mavros/cmd/arming', CommandBool)

    rate = rospy.Rate(20)  # 20 Hz

    # Send a few setpoints before switching to OFFBOARD mode
    pose = PoseStamped()
    pose.pose.position.x = 0
    pose.pose.position.y = 0
    pose.pose.position.z = 2

    for _ in range(100):
        follower1_pub.publish(pose)
        follower2_pub.publish(pose)
        rate.sleep()

    # Set mode to OFFBOARD and arm
    set_mode(set_mode_uav1, 'OFFBOARD')
    set_mode(set_mode_uav2, 'OFFBOARD')

    arm(arm_uav1)
    arm(arm_uav2)

    while not rospy.is_shutdown():
        # Followers follow the leader with an offset
        follower1_pose = PoseStamped()
        follower1_pose.pose.position.x = leader_pose.pose.position.x - 2
        follower1_pose.pose.position.y = leader_pose.pose.position.y
        follower1_pose.pose.position.z = leader_pose.pose.position.z

        follower2_pose = PoseStamped()
        follower2_pose.pose.position.x = leader_pose.pose.position.x + 2
        follower2_pose.pose.position.y = leader_pose.pose.position.y
        follower2_pose.pose.position.z = leader_pose.pose.position.z

        follower1_pub.publish(follower1_pose)
        follower2_pub.publish(follower2_pose)

        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
