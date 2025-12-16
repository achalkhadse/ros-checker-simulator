import json
from datetime import datetime

def generate_text_report(check_report: dict, sim_report: dict = None) -> str:
    """Generate a text report from the check and simulation results"""
    report = []
    report.append("=" * 50)
    report.append("ROS Code Checker Report")
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 50)
    
    # Errors
    if check_report["errors"]:
        report.append("\nERRORS:")
        for error in check_report["errors"]:
            report.append(f"  - {error}")
    else:
        report.append("\nNo syntax errors found.")
    
    # Warnings
    if check_report["warnings"]:
        report.append("\nWARNINGS:")
        for warning in check_report["warnings"]:
            report.append(f"  - {warning}")
    
    # ROS Elements
    report.append("\nROS Elements Found:")
    report.append(f"  - init_node: {'Yes' if check_report['ros_elements']['init_node'] else 'No'}")
    
    if check_report["ros_elements"]["publishers"]:
        report.append(f"  - Publishers: {len(check_report['ros_elements']['publishers'])}")
        for pub in check_report["ros_elements"]["publishers"]:
            report.append(f"    * {pub['variable']} -> {pub['topic']}")
    
    if check_report["ros_elements"]["subscribers"]:
        report.append(f"  - Subscribers: {len(check_report['ros_elements']['subscribers'])}")
        for sub in check_report["ros_elements"]["subscribers"]:
            report.append(f"    * {sub}")
    
    if check_report["ros_elements"]["services"]:
        report.append(f"  - Services: {len(check_report['ros_elements']['services'])}")
        for svc in check_report["ros_elements"]["services"]:
            report.append(f"    * {svc['variable']} -> {svc['service']}")
    
    # Safety Issues
    if check_report["safety_issues"]:
        report.append("\nSafety Issues:")
        for issue in check_report["safety_issues"]:
            report.append(f"  - {issue}")
    
    # Simulation Results
    if sim_report:
        report.append("\nSimulation Results:")
        report.append(f"  - Success: {'Yes' if sim_report['success'] else 'No'}")
        report.append(f"  - Final Joint Positions:")
        for joint, value in sim_report["joint_positions"].items():
            report.append(f"    * {joint}: {value:.2f} rad")
        report.append(f"  - Final Cube Position: [{sim_report['cube_position'][0]:.2f}, {sim_report['cube_position'][1]:.2f}, {sim_report['cube_position'][2]:.2f}]")
        report.append(f"  - Target Position: [{sim_report['target_position'][0]:.2f}, {sim_report['target_position'][1]:.2f}, {sim_report['target_position'][2]:.2f}]")
    
    return "\n".join(report)

def generate_json_report(check_report: dict, sim_report: dict = None) -> str:
    """Generate a JSON report from the check and simulation results"""
    full_report = {
        "timestamp": datetime.now().isoformat(),
        "check_report": check_report,
        "simulation_report": sim_report
    }
    return json.dumps(full_report, indent=2)