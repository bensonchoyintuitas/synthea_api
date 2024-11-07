from flask import Flask, jsonify
import subprocess
import os
import json
import shutil
from datetime import datetime
import glob

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_patient():
    try:
        # 1. Delete contents of output folder
        if os.path.exists('./output'):
            shutil.rmtree('./output')
            os.makedirs('./output/fhir')
        
        # 2. Run Synthea jar with current date as seed
        current_date = datetime.now().strftime('%Y%m%d')
        command = f'java -jar synthea-with-dependencies.jar -c synthea.properties -p 1 -r {current_date}'
        
        process = subprocess.run(command.split(), 
                               capture_output=True,
                               text=True)
        
        if process.returncode != 0:
            return jsonify({
                'error': 'Synthea generation failed',
                'details': process.stderr
            }), 500
        
        # 3. Find and read the Bundle JSON file
        fhir_files = glob.glob('./output/fhir/*.json')
        
        for file_path in fhir_files:
            with open(file_path, 'r') as f:
                data = json.load(f)
                if data.get('resourceType') == 'Bundle':
                    return jsonify(data)
        
        return jsonify({
            'error': 'No Bundle resource found in output'
        }), 404

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 