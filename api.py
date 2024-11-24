from flask import Flask, jsonify
import os
import shutil
import subprocess
import glob
import json
from datetime import datetime
import uuid
from threading import Lock
import tempfile

app = Flask(__name__)
file_operation_lock = Lock()

# Define base output directory
BASE_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output', 'fhir')

# Add a set to track used patient IDs with a lock
used_patient_ids = set()
patient_id_lock = Lock()

def get_temp_output_dir():
    """Create a unique subdirectory within the base output directory."""
    os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)
    unique_dir = f'synthea_{datetime.now().strftime("%Y%m%d")}_{uuid.uuid4().hex[:8]}'
    return os.path.join(BASE_OUTPUT_DIR, unique_dir)

def is_patient_used(patient_id):
    """Check if a patient ID has been used before."""
    with patient_id_lock:
        return patient_id in used_patient_ids

def mark_patient_used(patient_id):
    """Mark a patient ID as used."""
    with patient_id_lock:
        used_patient_ids.add(patient_id)

@app.route('/generate_patient_bundle', methods=['POST'])
def generate_patient_bundle():
    output_dir = get_temp_output_dir()
    try:
        print(f"Starting bundle generation process in {output_dir}...")
        os.makedirs(os.path.join(output_dir, 'fhir'))

        # Generate patient with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            current_date = datetime.now().strftime('%Y%m%d')
            command = (f'java -Xms1g -Xmx4g -XX:+UseParallelGC -jar synthea-with-dependencies.jar '
                      f'-c synthea.properties -p 1 -r {current_date} '
                      f'--exporter.baseDirectory={output_dir} '
                      f'--exporter.fhir.use_us_core_ig=false '
                      f'--exporter.hospital.fhir.export=false '
                      f'--exporter.practitioner.fhir.export=false')
            
            process = subprocess.run(command.split(), capture_output=True, text=True)
            
            if process.returncode != 0:
                print(f"Synthea generation failed: {process.stderr}")
                continue

            fhir_files = glob.glob(os.path.join(output_dir, 'fhir', '*.json'))
            
            for file_path in fhir_files:
                if os.path.basename(file_path).startswith(('hospital', 'practitioner')):
                    continue

                with open(file_path, 'r') as f:
                    bundle = json.load(f)
                    if bundle.get('resourceType') == 'Bundle':
                        # Extract patient and related resources
                        patient_resource = None
                        condition_resources = []
                        
                        for entry in bundle.get('entry', []):
                            resource = entry.get('resource', {})
                            if resource.get('resourceType') == 'Patient':
                                patient_resource = resource
                            elif resource.get('resourceType') == 'Condition':
                                condition_resources.append(resource)
                        
                        if patient_resource:
                            patient_id = patient_resource.get('id')
                            if patient_id and not is_patient_used(patient_id):
                                mark_patient_used(patient_id)
                                # Return both patient and related resources
                                return jsonify({
                                    'patient': patient_resource,
                                    'conditions': condition_resources,
                                    'bundle': bundle  # Include full bundle for reference
                                })

            print(f"Attempt {attempt + 1}: Generated patient was already used, retrying...")
            
        return jsonify({'error': 'Could not generate unique patient after retries'}), 503

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    
    finally:
        try:
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
        except Exception as e:
            print(f"Warning: Failed to clean up directory {output_dir}: {str(e)}")

@app.route('/cleanup_used_patients', methods=['POST'])
def cleanup_used_patients():
    """Clear the set of used patient IDs."""
    try:
        with patient_id_lock:
            count = len(used_patient_ids)
            used_patient_ids.clear()
            return jsonify({'message': f'Cleared {count} used patient IDs'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)
    app.run(debug=True, port=5001) 