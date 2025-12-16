import os
import zipfile
import tempfile
import shutil

def handle_upload(file):
    """Handle uploaded file, extract if ZIP, return file path and temp directory"""
    temp_dir = tempfile.mkdtemp()
    
    if file.filename.endswith('.zip'):
        # Extract ZIP file
        zip_path = os.path.join(temp_dir, 'upload.zip')
        file.save(zip_path)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find main Python or C++ file
        main_file = None
        for root, _, files in os.walk(temp_dir):
            for f in files:
                if f.endswith('.py') or f.endswith('.cpp'):
                    main_file = os.path.join(root, f)
                    break
            if main_file:
                break
        
        return main_file, temp_dir
    else:
        # Single file upload
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)
        return file_path, temp_dir

def cleanup_temp_dir(temp_dir):
    """Clean up temporary directory"""
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)