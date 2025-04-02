#include "rclcpp/rclcpp.hpp"
#include "px4_msgs/msg/vehicle_odometry.hpp"
#include "nav_msgs/msg/odometry.hpp"

class VehicleOdometryToNavOdometryRemapper : public rclcpp::Node
{
public:
    VehicleOdometryToNavOdometryRemapper()
        : Node("vehicle_odometry_to_nav_odometry_remapper")
    {
        rclcpp::QoS qos(rclcpp::KeepLast(1));
        qos.best_effort();

        vehicle_odometry_sub_ = this->create_subscription<px4_msgs::msg::VehicleOdometry>(
            "/fmu/out/vehicle_odometry",
            qos,
            std::bind(&VehicleOdometryToNavOdometryRemapper::vehicleOdometryCallback, this, std::placeholders::_1)
        );

        nav_odometry_pub_ = this->create_publisher<nav_msgs::msg::Odometry>("/odometry", qos);
        odom_msg_.header.frame_id = "odom";
        odom_msg_.child_frame_id = "base_link";
    }

private:
    void vehicleOdometryCallback(const std::shared_ptr<const px4_msgs::msg::VehicleOdometry>& msg)
    {
        odom_msg_.header.stamp = rclcpp::Time(msg->timestamp, RCL_ROS_TIME);
        odom_msg_.pose.pose.position.x = msg->position[0];
        odom_msg_.pose.pose.position.y = msg->position[1];
        odom_msg_.pose.pose.position.z = msg->position[2];
        nav_odometry_pub_->publish(odom_msg_);
    }

    rclcpp::Subscription<px4_msgs::msg::VehicleOdometry>::SharedPtr vehicle_odometry_sub_;
    rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr nav_odometry_pub_;
    nav_msgs::msg::Odometry odom_msg_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<VehicleOdometryToNavOdometryRemapper>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
