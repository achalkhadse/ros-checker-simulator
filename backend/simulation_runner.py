import os
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64

class SimulationRunner:
    def __init__(self):
        self.joint_positions = {
            'joint1': 0,
            'joint2': 0,
            'joint3': 0,
            'joint4': 0,
            'joint5': 0,
            'joint6': 0
        }
        self.cube_position = [0.5, 0.5, 0.0]  # Initial cube position
        self.target_position = [0.7, 0.3, 0.0]  # Target position
        self.success = False
        self.frames = []
    
    def run_simulation(self, file_path: str, report: dict) -> dict:
        """Run a simplified simulation of the robotic arm"""
        # Extract joint movements from the code (simplified)
        if file_path.endswith('.py'):
            self._extract_joint_movements_from_python(file_path)
        elif file_path.endswith('.cpp'):
            self._extract_joint_movements_from_cpp(file_path)
        
        # Generate simulation frames
        self._generate_frames()
        
        # Check if cube reached target
        distance = np.linalg.norm(np.array(self.cube_position[:2]) - np.array(self.target_position[:2]))
        self.success = distance < 0.1
        
        return {
            "success": self.success,
            "frames": self.frames,
            "joint_positions": self.joint_positions,
            "cube_position": self.cube_position,
            "target_position": self.target_position
        }
    
    def _extract_joint_movements_from_python(self, file_path: str):
        """Extract joint movements from Python code (simplified)"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Look for joint value assignments (simplified pattern matching)
        joint_assignments = {}
        for joint in self.joint_positions.keys():
            pattern = rf'{joint}[_\s]*value[s]*\s*=\s*([-\d.]+)'
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                joint_assignments[joint] = float(matches[-1])  # Take the last assignment
        
        # Update joint positions
        self.joint_positions.update(joint_assignments)
        
        # Simple forward kinematics to determine cube position (simplified)
        self._update_cube_position()
    
    def _extract_joint_movements_from_cpp(self, file_path: str):
        """Extract joint movements from C++ code (simplified)"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Look for joint value assignments (simplified pattern matching)
        joint_assignments = {}
        for joint in self.joint_positions.keys():
            pattern = rf'{joint}[_\s]*value[s]*\s*=\s*([-\d.]+)'
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                joint_assignments[joint] = float(matches[-1])  # Take the last assignment
        
        # Update joint positions
        self.joint_positions.update(joint_assignments)
        
        # Simple forward kinematics to determine cube position (simplified)
        self._update_cube_position()
    
    def _update_cube_position(self):
        """Update cube position based on joint angles (simplified forward kinematics)"""
        # This is a very simplified version - real forward kinematics would be more complex
        # Just using joint1 and joint2 for x and y positioning
        self.cube_position[0] = 0.5 + 0.2 * np.sin(self.joint_positions['joint1'])
        self.cube_position[1] = 0.5 + 0.2 * np.sin(self.joint_positions['joint2'])
    
    def _generate_frames(self):
        """Generate visualization frames for the simulation"""
        # Create a simple 2D visualization
        fig, ax = plt.subplots(figsize=(6, 6))
        
        # Plot robotic arm (simplified as lines)
        arm_length = 0.3
        x = [0, arm_length * np.cos(self.joint_positions['joint1']), 
             arm_length * np.cos(self.joint_positions['joint1']) + arm_length * np.cos(self.joint_positions['joint1'] + self.joint_positions['joint2'])]
        y = [0, arm_length * np.sin(self.joint_positions['joint1']), 
             arm_length * np.sin(self.joint_positions['joint1']) + arm_length * np.sin(self.joint_positions['joint1'] + self.joint_positions['joint2'])]
        
        ax.plot(x, y, 'o-', lw=3, color='blue')
        
        # Plot cube
        ax.plot(self.cube_position[0], self.cube_position[1], 's', markersize=10, color='green')
        
        # Plot target
        ax.plot(self.target_position[0], self.target_position[1], 'x', markersize=10, color='red')
        
        # Set axis limits
        ax.set_xlim(-0.5, 1.0)
        ax.set_ylim(-0.5, 1.0)
        ax.set_aspect('equal')
        ax.grid(True)
        ax.set_title('Robotic Arm Simulation')
        
        # Convert plot to base64 string
        canvas = FigureCanvas(fig)
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        self.frames.append(img_base64)