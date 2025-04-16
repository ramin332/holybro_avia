#!/usr/bin/env python3

import socket
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class UDPToServiceNode(Node):
    def __init__(self):
        super().__init__('udp_to_service_node')
        self.client = self.create_client(SetBool, 'start_slam')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for start_slam service...')

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 5000))
        self.sock.setblocking(False)

        self.timer = self.create_timer(0.1, self.check_udp)

    def check_udp(self):
        try:
            data, _ = self.sock.recvfrom(1024)
            msg = data.decode('utf-8').strip()
            self.get_logger().info(f"Raw UDP: {repr(msg)} len={len(msg)}")
            self.get_logger().info(f"Received UDP message: {msg}")

            req = SetBool.Request()
            req.data = msg.lower() == 'true'
            self.get_logger().info(f"Sending to service with data={req.data}")  
            future = self.client.call_async(req)

            def callback(fut):
                if fut.result() is not None:
                    self.get_logger().info('Service call succeeded')
                else:
                    self.get_logger().warn('Service call failed')

            future.add_done_callback(callback)

        except BlockingIOError:
            pass

def main(args=None):
    rclpy.init(args=args)
    node = UDPToServiceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
