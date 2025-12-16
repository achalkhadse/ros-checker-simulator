import os
import re
import ast
import json
import subprocess
from typing import Dict, List, Tuple

class ROSCodeChecker:
    def __init__(self):
        self.report = {
            "errors": [],
            "warnings": [],
            "ros_elements": {
                "publishers": [],
                "subscribers": [],
                "services": [],
                "init_node": False
            },
            "safety_issues": []
        }
    
    def check_file(self, file_path: str) -> Dict:
        """Main method to check the ROS code"""
        if file_path.endswith('.py'):
            self._check_python_file(file_path)
        elif file_path.endswith('.cpp'):
            self._check_cpp_file(file_path)
        
        # Check ROS package structure if in a package
        package_dir = os.path.dirname(file_path)
        self._check_package_structure(package_dir)
        
        return self.report
    
    def _check_python_file(self, file_path: str):
        """Check Python ROS code"""
        try:
            # Syntax check using ast
            with open(file_path, 'r') as f:
                content = f.read()
            
            try:
                ast.parse(content)
            except SyntaxError as e:
                self.report["errors"].append(f"Syntax error: {str(e)}")
                return
            
            # Check for ROS elements
            if 'rospy.init_node' in content:
                self.report["ros_elements"]["init_node"] = True
            
            # Find publishers
            publishers = re.findall(r'(\w+)\s*=\s*rospy\.Publisher\([\'"]([^\'"]+)[\'"]', content)
            for var_name, topic in publishers:
                self.report["ros_elements"]["publishers"].append({"variable": var_name, "topic": topic})
            
            # Find subscribers
            subscribers = re.findall(r'rospy\.Subscriber\([\'"]([^\'"]+)[\'"]', content)
            for topic in subscribers:
                self.report["ros_elements"]["subscribers"].append(topic)
            
            # Find services
            services = re.findall(r'(\w+)\s*=\s*rospy\.Service\([\'"]([^\'"]+)[\'"]', content)
            for var_name, service in services:
                self.report["ros_elements"]["services"].append({"variable": var_name, "service": service})
            
            # Basic safety checks
            self._check_python_safety(content)
            
        except Exception as e:
            self.report["errors"].append(f"Error checking Python file: {str(e)}")
    
    def _check_cpp_file(self, file_path: str):
        """Check C++ ROS code"""
        try:
            # Syntax check using g++ dry run
            result = subprocess.run(
                ['g++', '-fsyntax-only', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode != 0:
                self.report["errors"].append(f"C++ syntax error: {result.stderr}")
                return
            
            # Check for ROS elements
            with open(file_path, 'r') as f:
                content = f.read()
            
            if 'ros::init' in content:
                self.report["ros_elements"]["init_node"] = True
            
            # Find publishers
            publishers = re.findall(r'ros::Publisher\s+(\w+)\s*=\s*n\.advertise<[^>]+>\([\'"]([^\'"]+)[\'"]', content)
            for var_name, topic in publishers:
                self.report["ros_elements"]["publishers"].append({"variable": var_name, "topic": topic})
            
            # Find subscribers
            subscribers = re.findall(r'n\.subscribe<[^>]+>\([\'"]([^\'"]+)[\'"]', content)
            for topic in subscribers:
                self.report["ros_elements"]["subscribers"].append(topic)
            
            # Find services
            services = re.findall(r'ros::ServiceServer\s+(\w+)\s*=\s*n\.advertiseService\([\'"]([^\'"]+)[\'"]', content)
            for var_name, service in services:
                self.report["ros_elements"]["services"].append({"variable": var_name, "service": service})
            
            # Basic safety checks
            self._check_cpp_safety(content)
            
        except Exception as e:
            self.report["errors"].append(f"Error checking C++ file: {str(e)}")
    
    def _check_package_structure(self, package_dir: str):
        """Check if the directory contains a valid ROS package structure"""
        package_xml = os.path.join(package_dir, 'package.xml')
        cmake_lists = os.path.join(package_dir, 'CMakeLists.txt')
        setup_py = os.path.join(package_dir, 'setup.py')
        
        if not os.path.exists(package_xml):
            self.report["warnings"].append("package.xml not found. This might not be a valid ROS package.")
        
        if not os.path.exists(cmake_lists) and not os.path.exists(setup_py):
            self.report["warnings"].append("Neither CMakeLists.txt nor setup.py found. This might not be a valid ROS package.")
    
    def _check_python_safety(self, content: str):
        """Check for basic safety issues in Python code"""
        # Check for loops without sleep
        if re.search(r'while\s+True:.*?(?!rospy\.sleep|time\.sleep)', content, re.DOTALL):
            self.report["safety_issues"].append("Potential infinite loop without sleep detected")
        
        # Check for joint values that might be out of range
        joint_values = re.findall(r'joint[_\s]*(\w+)[_\s]*value[s]*\s*=\s*([-\d.]+)', content, re.IGNORECASE)
        for joint, value in joint_values:
            try:
                val = float(value)
                if abs(val) > 3.14:  # Assuming radians, most joints shouldn't exceed ±π
                    self.report["safety_issues"].append(f"Joint value {val} for {joint} might be out of safe range")
            except ValueError:
                pass
    
    def _check_cpp_safety(self, content: str):
        """Check for basic safety issues in C++ code"""
        # Check for loops without sleep
        if re.search(r'while\s*\(\s*true\s*\).*?(?!ros::Duration|ros::Rate)', content, re.DOTALL):
            self.report["safety_issues"].append("Potential infinite loop without sleep detected")
        
        # Check for joint values that might be out of range
        joint_values = re.findall(r'joint[_\s]*(\w+)[_\s]*value[s]*\s*=\s*([-\d.]+)', content, re.IGNORECASE)
        for joint, value in joint_values:
            try:
                val = float(value)
                if abs(val) > 3.14:  # Assuming radians, most joints shouldn't exceed ±π
                    self.report["safety_issues"].append(f"Joint value {val} for {joint} might be out of safe range")
            except ValueError:
                pass