from setuptools import setup, find_packages

package_name = 'republisher_py_pkg'
setup(
 name=package_name,
 version='0.0.0',
 #packages=[package_name],
 packages=find_packages(),
 data_files=[
     ('share/ament_index/resource_index/packages',
             ['resource/' + package_name]),
     ('share/' + package_name, ['package.xml']),
   ],
 install_requires=['setuptools',
                   'cv2',
                   'rospy',
                   'cv_bridge',
                   'sensor_msgs',
                   'camera_info_manager'],
 zip_safe=True,
 maintainer='TODO',
 maintainer_email='TODO',
 description='TODO: Package description',
 license='TODO: License declaration',
 tests_require=['pytest'],
 entry_points={
     'console_scripts': [
             'mono_node = republisher_py_pkg.mono_node:main'
     ],
   },
)