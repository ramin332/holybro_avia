#include "rclcpp/rclcpp.hpp"
#include "px4_msgs/msg/sensor_gps.hpp"
#include "sensor_msgs/msg/nav_sat_fix.hpp"

class SensorGpsToNavSatFixRemapper : public rclcpp::Node
{
public:
    SensorGpsToNavSatFixRemapper()
        : Node("sensor_gps_to_nav_sat_fix_remapper")
    {
        rclcpp::QoS qos(rclcpp::KeepLast(1));
        qos.best_effort();

        sensor_gps_sub_ = this->create_subscription<px4_msgs::msg::SensorGps>(
            "/fmu/out/vehicle_gps_position",
            qos,
            std::bind(&SensorGpsToNavSatFixRemapper::sensorGpsCallback, this, std::placeholders::_1)
        );

        nav_sat_fix_pub_ = this->create_publisher<sensor_msgs::msg::NavSatFix>("/gps/fix", qos);
        nav_sat_fix_msg_.header.frame_id = "gps_link";
    }

private:
    void sensorGpsCallback(const std::shared_ptr<const px4_msgs::msg::SensorGps>& msg)
    {
        nav_sat_fix_msg_.header.stamp = this->get_clock()->now();
        nav_sat_fix_msg_.latitude = msg->latitude_deg;
        nav_sat_fix_msg_.longitude = msg->longitude_deg;
        nav_sat_fix_msg_.altitude = msg->altitude_msl_m;
        nav_sat_fix_pub_->publish(nav_sat_fix_msg_);
    }

    rclcpp::Subscription<px4_msgs::msg::SensorGps>::SharedPtr sensor_gps_sub_;
    rclcpp::Publisher<sensor_msgs::msg::NavSatFix>::SharedPtr nav_sat_fix_pub_;
    sensor_msgs::msg::NavSatFix nav_sat_fix_msg_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SensorGpsToNavSatFixRemapper>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
