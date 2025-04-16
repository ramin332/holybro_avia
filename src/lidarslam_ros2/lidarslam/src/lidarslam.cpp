#include <rclcpp/rclcpp.hpp>
#include <std_srvs/srv/set_bool.hpp>
#include <scanmatcher/scanmatcher_component.h>
#include <graph_based_slam/graph_based_slam_component.h>

class SlamController : public rclcpp::Node {
  public:
    SlamController(rclcpp::executors::MultiThreadedExecutor &exec,
                   std::shared_ptr<graphslam::ScanMatcherComponent> sm,
                   std::shared_ptr<graphslam::GraphBasedSlamComponent> gbs)
      : Node("slam_controller"), exec_(exec), sm_(sm), gbs_(gbs)
    {
      service_ = this->create_service<std_srvs::srv::SetBool>(
        "start_slam",
        std::bind(&SlamController::handle_service, this, std::placeholders::_1, std::placeholders::_2));
      
    }
  
  private:
    void handle_service(
      const std::shared_ptr<std_srvs::srv::SetBool::Request> request,
      std::shared_ptr<std_srvs::srv::SetBool::Response> response)
    {
      RCLCPP_INFO(get_logger(), "Received request: data=%s", request->data ? "true" : "false");
    
      if (request->data == slam_enabled_) {
        RCLCPP_INFO(get_logger(), "SLAM state unchanged. Ignoring request.");
        response->success = true;
        return;
      }
    
      if (request->data) {
        RCLCPP_INFO(get_logger(), "Enabling SLAM nodes.");
        exec_.add_node(sm_);
        exec_.add_node(gbs_);
        slam_enabled_ = true;
      } 
      else {
        RCLCPP_INFO(get_logger(), "Disabling SLAM. Saving map first...");
        auto client = this->create_client<std_srvs::srv::Empty>("map_save");
        if (client->wait_for_service(std::chrono::seconds(2))) {
          auto map_save_request = std::make_shared<std_srvs::srv::Empty::Request>();
          auto future = client->async_send_request(map_save_request);
          RCLCPP_INFO(this->get_logger(), "Map save service requested.");
          rclcpp::sleep_for(std::chrono::milliseconds(2000));
        } else {
          RCLCPP_WARN(get_logger(), "map_save service not available.");
        }
        exec_.remove_node(sm_);
        exec_.remove_node(gbs_);
        slam_enabled_ = false;
      }
    
      response->success = true;
    }
  
    rclcpp::Service<std_srvs::srv::SetBool>::SharedPtr service_;
    rclcpp::executors::MultiThreadedExecutor &exec_;
    std::shared_ptr<graphslam::ScanMatcherComponent> sm_;
    std::shared_ptr<graphslam::GraphBasedSlamComponent> gbs_;
    bool slam_enabled_ = false;  
  };

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::NodeOptions options;
  options.use_intra_process_comms(true);
  rclcpp::executors::MultiThreadedExecutor exec;

  auto scanmatcher = std::make_shared<graphslam::ScanMatcherComponent>(options);
  auto graphslam = std::make_shared<graphslam::GraphBasedSlamComponent>(options);
  auto controller = std::make_shared<SlamController>(exec, scanmatcher, graphslam);

  exec.add_node(controller);  
  // exec.add_node(scanmatcher);
  // exec.add_node(graphslam);
  exec.spin();

  rclcpp::shutdown();
  return 0;
}