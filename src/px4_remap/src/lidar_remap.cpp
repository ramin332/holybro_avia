#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
class LivoxLidarToLidarRemapper : public rclcpp::Node
{
public:
  LivoxLidarToLidarRemapper()
  : Node("livox_lidar_to_lidar_remapper", rclcpp::NodeOptions().parameter_overrides({rclcpp::Parameter("use_sim_time", true)}))
  {
    // Use a QoS profile that guarantees message delivery.
    rclcpp::QoS qos(rclcpp::KeepLast(1));
    qos.reliable();
    // Subscription to the /livox/lidar topic
    livox_lidar_sub_ = this->create_subscription<sensor_msgs::msg::PointCloud2>(
      "/livox/lidar", qos,
      std::bind(&LivoxLidarToLidarRemapper::livoxLidarCallback, this, std::placeholders::_1)
    );
    // Publisher for the /lidar topic (with sim time stamps)
    lidar_pub_ = this->create_publisher<sensor_msgs::msg::PointCloud2>("/lidar", qos);
  }
private:
  void livoxLidarCallback(const std::shared_ptr<const sensor_msgs::msg::PointCloud2>& msg)
  {
    // Always use the current ROS (sim) time
    auto sim_time = this->get_clock()->now();
  
    // Create a new message, overriding the header timestamp with sim time
    sensor_msgs::msg::PointCloud2 lidar_msg = *msg;
    lidar_msg.header.stamp = sim_time;
    lidar_msg.header.frame_id = "lidar_link";
    // Publish the corrected message
    lidar_pub_->publish(lidar_msg);
  }
  rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr livox_lidar_sub_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr lidar_pub_;
};
int main(int argc, char *argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<LivoxLidarToLidarRemapper>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}