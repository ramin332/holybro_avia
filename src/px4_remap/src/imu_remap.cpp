#include "rclcpp/rclcpp.hpp"
#include "px4_msgs/msg/sensor_combined.hpp"
#include "sensor_msgs/msg/imu.hpp"

class SensorCombinedToImuRemapper : public rclcpp::Node
{
public:
    SensorCombinedToImuRemapper()
        : Node("sensor_combined_to_imu_remapper")
    {
        rclcpp::QoS qos(rclcpp::KeepLast(1));
        qos.best_effort();

        sensor_combined_sub_ = this->create_subscription<px4_msgs::msg::SensorCombined>(
            "/fmu/out/sensor_combined",
            qos,
            std::bind(&SensorCombinedToImuRemapper::sensorCombinedCallback, this, std::placeholders::_1)
        );

        imu_pub_ = this->create_publisher<sensor_msgs::msg::Imu>("/imu/data", qos);
        imu_msg_.header.frame_id = "imu_link";
        imu_msg_.orientation_covariance[0] = -1;
        imu_msg_.orientation_covariance[4] = -1;
        imu_msg_.orientation_covariance[8] = -1;
    }

private:
    void sensorCombinedCallback(const std::shared_ptr<const px4_msgs::msg::SensorCombined>& msg)
    {
        imu_msg_.header.stamp = rclcpp::Time(msg->timestamp, RCL_ROS_TIME);
        imu_msg_.linear_acceleration.x = msg->accelerometer_m_s2[0];
        imu_msg_.linear_acceleration.y = msg->accelerometer_m_s2[1];
        imu_msg_.linear_acceleration.z = msg->accelerometer_m_s2[2];
        imu_msg_.angular_velocity.x = msg->gyro_rad[0];
        imu_msg_.angular_velocity.y = msg->gyro_rad[1];
        imu_msg_.angular_velocity.z = msg->gyro_rad[2];
        imu_pub_->publish(imu_msg_);
    }

    rclcpp::Subscription<px4_msgs::msg::SensorCombined>::SharedPtr sensor_combined_sub_;
    rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr imu_pub_;
    sensor_msgs::msg::Imu imu_msg_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SensorCombinedToImuRemapper>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
