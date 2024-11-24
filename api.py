from flask import Flask, jsonify
import os
import shutil
import subprocess
import glob
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/generate_patient_bundle', methods=['POST'])
def generate_patient_bundle():
    try:
        print("Starting bundle generation process...")

        # 1. Delete contents of output folder
        if os.path.exists('./output'):
            print("Deleting existing output directory...")
            shutil.rmtree('./output')
        os.makedirs('./output/fhir')
        print("Output directory prepared.")

        # 2. Run Synthea jar with current date as seed
        current_date = datetime.now().strftime('%Y%m%d')
        command = f'java -Xms1g -Xmx4g -XX:+UseParallelGC -jar synthea-with-dependencies.jar -c synthea.properties -p 1 -r {current_date} --exporter.fhir.use_us_core_ig=false --exporter.hospital.fhir.export=false --exporter.practitioner.fhir.export=false'
        print(f"Running Synthea with command: {command}")

        process = subprocess.run(command.split(), 
                               capture_output=True,
                               text=True)
        
        if process.returncode != 0:
            print("Synthea generation failed.")
            print(f"Error details: {process.stderr}")
            return jsonify({
                'error': 'Synthea generation failed',
                'details': process.stderr
            }), 500
        
        print("Synthea generation completed successfully.")

        # 3. Find and read the Bundle JSON file
        fhir_files = glob.glob('./output/fhir/*.json')
        print(f"Found {len(fhir_files)} FHIR JSON files.")

        for file_path in fhir_files:
            # Skip files that start with 'hospital' or 'practitioner'
            if file_path.startswith('./output/fhir/hospital') or file_path.startswith('./output/fhir/practitioner'):
                continue

            with open(file_path, 'r') as f:
                data = json.load(f)
                if data.get('resourceType') == 'Bundle':
                    print(f"Bundle resource found in file: {file_path}")
                    return jsonify(data)
        
        print("No Bundle resource found in output.")
        return jsonify({
            'error': 'No Bundle resource found in output'
        }), 404

    except Exception as e:
        print("An internal server error occurred.")
        print(f"Error details: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@app.route('/generate_patient', methods=['POST'])
def generate_patient():
    try:
        print("Starting patient generation process...")

        # 1. Delete contents of output folder
        if os.path.exists('./output'):
            print("Deleting existing output directory...")
            shutil.rmtree('./output')
        os.makedirs('./output/fhir')
        print("Output directory prepared.")

        # 2. Run Synthea jar with current date as seed
        current_date = datetime.now().strftime('%Y%m%d')
        command = f'java -Xms1g -Xmx4g -XX:+UseParallelGC -jar synthea-with-dependencies.jar -c synthea.properties -p 1 -r {current_date} --exporter.fhir.use_us_core_ig=false --exporter.hospital.fhir.export=false --exporter.practitioner.fhir.export=false'
        print(f"Running Synthea with command: {command}")

        process = subprocess.run(command.split(), 
                               capture_output=True,
                               text=True)
        
        if process.returncode != 0:
            print("Synthea generation failed.")
            print(f"Error details: {process.stderr}")
            return jsonify({
                'error': 'Synthea generation failed',
                'details': process.stderr
            }), 500
        
        print("Synthea generation completed successfully.")

        # 3. Find and read the Bundle JSON file
        fhir_files = glob.glob('./output/fhir/*.json')
        print(f"Found {len(fhir_files)} FHIR JSON files.")

        for file_path in fhir_files:
            # Skip files that start with 'hospital' or 'practitioner'
            if file_path.startswith('./output/fhir/hospital') or file_path.startswith('./output/fhir/practitioner'):
                continue

            with open(file_path, 'r') as f:
                data = json.load(f)
                if data.get('resourceType') == 'Bundle':
                    print(f"Bundle resource found in file: {file_path}")
                    for entry in data.get('entry', []):
                        resource = entry.get('resource', {})
                        if resource.get('resourceType') == 'Patient':
                            print("Patient resource extracted.")
                            return jsonify(resource)
        
        print("No Patient resource found in bundle.")
        return jsonify({
            'error': 'No Patient resource found in bundle'
        }), 404

    except Exception as e:
        print("An internal server error occurred.")
        print(f"Error details: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 