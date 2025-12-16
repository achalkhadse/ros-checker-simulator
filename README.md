ROS Code Checker and Simulation Tool for Windows:

A simplified tool for checking ROS/ROS2 code and running basic simulations on Windows 11.


Features:

- Code validation for ROS/ROS2 Python and C++ nodes
- Syntax checking and basic safety analysis
- Simple robotic arm simulation visualization
- Web-based interface for easy use

Installation
1. Clone this repository
2. Install dependencies:
pip install -r requirements.txt
3. Run the application:
python app.py
4. Open your browser and go to `http://127.0.0.1:5000`

## Usage

1. Upload a Python (.py), C++ (.cpp), or ZIP file containing a ROS package
2. View the code check results
3. Run the simulation to see how the robotic arm moves
4. Check if the cube reaches the target position

## Limitations

- This is a simplified version adapted for Windows
- Simulation uses 2D visualization instead of Gazebo or CoppeliaSim
- Code checking is basic and may not catch all issues
- Only supports simple joint movements

## System Requirements

- Windows 11
- Python 3.8+
- Flask and other dependencies listed in requirements.txt


How to Run on Windows 11
1. Install Python 3.8 or higher from the official Python website
2. Install Git if you haven't already
3. Clone or download this repository
4. Open Command Prompt or PowerShell
5. Navigate to the project directory
6. Create a virtual environment (recommended):
python -m venv venv
venv\Scripts\activate
7. Install dependencies:
pip install -r requirements.txt
8. Run the application:
python app.py
9. Open your web browser and go to http://127.0.0.1:5000