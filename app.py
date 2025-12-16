import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from backend.file_handler import handle_upload, cleanup_temp_dir
from backend.code_checker import ROSCodeChecker
from backend.simulation_runner import SimulationRunner
from backend.reports import generate_text_report, generate_json_report

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Handle file upload
    file_path, temp_dir = handle_upload(file)
    
    # Check the code
    checker = ROSCodeChecker()
    check_report = checker.check_file(file_path)
    
    # Generate reports
    text_report = generate_text_report(check_report)
    json_report = generate_json_report(check_report)
    
    # Store results in session or database (simplified: store in temp files)
    result_id = os.path.basename(temp_dir)
    
    with open(os.path.join(app.config['UPLOAD_FOLDER'], f"{result_id}_check.json"), 'w') as f:
        f.write(json_report)
    
    with open(os.path.join(app.config['UPLOAD_FOLDER'], f"{result_id}_report.txt"), 'w') as f:
        f.write(text_report)
    
    # Clean up temp directory but keep the main file
    cleanup_temp_dir(temp_dir)
    
    return jsonify({
        "result_id": result_id,
        "check_report": check_report,
        "text_report": text_report
    })

@app.route('/results/<result_id>')
def show_results(result_id):
    # Load check report
    check_report_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{result_id}_check.json")
    if not os.path.exists(check_report_path):
        return "Result not found", 404
    
    with open(check_report_path, 'r') as f:
        check_report = json.load(f)
    
    # Load text report
    report_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{result_id}_report.txt")
    with open(report_path, 'r') as f:
        text_report = f.read()
    
    return render_template('results.html', 
                          result_id=result_id,
                          check_report=check_report["check_report"],
                          text_report=text_report)

@app.route('/simulate/<result_id>', methods=['POST'])
def run_simulation(result_id):
    # Load check report
    check_report_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{result_id}_check.json")
    if not os.path.exists(check_report_path):
        return jsonify({"error": "Result not found"}), 404
    
    with open(check_report_path, 'r') as f:
        check_report = json.load(f)
    
    # Run simulation
    simulator = SimulationRunner()
    sim_report = simulator.run_simulation("", check_report["check_report"])  # File path not needed for simplified version
    
    # Update reports with simulation results
    text_report = generate_text_report(check_report["check_report"], sim_report)
    json_report = generate_json_report(check_report["check_report"], sim_report)
    
    # Save updated reports
    with open(os.path.join(app.config['UPLOAD_FOLDER'], f"{result_id}_sim.json"), 'w') as f:
        f.write(json_report)
    
    with open(os.path.join(app.config['UPLOAD_FOLDER'], f"{result_id}_sim_report.txt"), 'w') as f:
        f.write(text_report)
    
    return jsonify({
        "success": True,
        "sim_report": sim_report,
        "text_report": text_report
    })

@app.route('/simulation_results/<result_id>')
def show_simulation_results(result_id):
    # Load simulation report
    sim_report_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{result_id}_sim.json")
    if not os.path.exists(sim_report_path):
        return "Simulation result not found", 404
    
    with open(sim_report_path, 'r') as f:
        sim_report = json.load(f)
    
    # Load text report
    report_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{result_id}_sim_report.txt")
    with open(report_path, 'r') as f:
        text_report = f.read()
    
    return render_template('simulation_results.html',
                          result_id=result_id,
                          sim_report=sim_report["simulation_report"],
                          text_report=text_report)

if __name__ == '__main__':
    app.run(debug=True)