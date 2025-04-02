#include <rclcpp/rclcpp.hpp>
#include <px4_msgs/msg/vehicle_odometry.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <geometry_msgs/msg/transform_stamped.hpp>
#include <tf2_ros/transform_broadcaster.h>

class VehicleOdometryConverter : public rclcpp::Node
{
public:
    VehicleOdometryConverter()
        : Node("vehicle_odometry_converter")
    {
        // Set QoS profile to match the publisher's QoS
        rclcpp::QoS qos_profile = rclcpp::QoS(rclcpp::KeepLast(10)).reliability(RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT);

        subscription_ = this->create_subscription<px4_msgs::msg::VehicleOdometry>(
            "/fmu/out/vehicle_odometry", qos_profile,
            std::bind(&VehicleOdometryConverter::odometry_callback, this, std::placeholders::_1));

        odom_publisher_ = this->create_publisher<nav_msgs::msg::Odometry>("/odom", 10);
        tf_broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);
    }

private:
    void odometry_callback(const px4_msgs::msg::VehicleOdometry::SharedPtr msg)
    {
        nav_msgs::msg::Odometry odom_msg;
        odom_msg.header.stamp = this->get_clock()->now();
        odom_msg.header.frame_id = "odom";
        odom_msg.child_frame_id = "base_link";

        // Convert position from NED to ENU
        odom_msg.pose.pose.position.x = msg->position[1];
        odom_msg.pose.pose.position.y = msg->position[0];
        odom_msg.pose.pose.position.z = -msg->position[2];

        // Convert orientation from FRD to FLU (180-degree rotation around X-axis)
        odom_msg.pose.pose.orientation.w = msg->q[0];
        odom_msg.pose.pose.orientation.x = msg->q[1];
        odom_msg.pose.pose.orientation.y = -msg->q[2];
        odom_msg.pose.pose.orientation.z = -msg->q[3];

        odom_publisher_->publish(odom_msg);

        geometry_msgs::msg::TransformStamped transform_stamped;
        transform_stamped.header.stamp = this->get_clock()->now();//odom_msg.header.stamp;
        transform_stamped.header.frame_id = "odom";
        transform_stamped.child_frame_id = "base_link";
        transform_stamped.transform.translation.x = odom_msg.pose.pose.position.x;
        transform_stamped.transform.translation.y = odom_msg.pose.pose.position.y;
        transform_stamped.transform.translation.z = odom_msg.pose.pose.position.z;
        transform_stamped.transform.rotation = odom_msg.pose.pose.orientation;

        tf_broadcaster_->sendTransform(transform_stamped);
    }

    rclcpp::Subscription<px4_msgs::msg::VehicleOdometry>::SharedPtr subscription_;
    rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr odom_publisher_;
    std::shared_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<VehicleOdometryConverter>());
    rclcpp::shutdown();
    return 0;
}
