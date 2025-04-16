from setuptools import find_packages, setup

package_name = 'mapping_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='avalor',
    maintainer_email='youremail@example.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'udp_service_bridge = mapping_bridge.udp_service_bridge:main',
            'send_udp = mapping_bridge.send_udp:main',
        ],
    },
)
