# Synthea API Wrapper
A Flask-based REST API wrapper for Synthea patient data generator.

## Prerequisites

- Python 3.7+
- Java Runtime Environment (JRE)
- Synthea with dependencies JAR file in the root directory (see [synthea-with-dependencies.md](/synthea-with-dependencies.md))


## Installation
1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```
2. Download synthea-with-dependencies.jar 
```bash
# Download Synthea
wget https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar

# and place it in this working directory

# Install Java (if needed)
sudo apt install openjdk-11-jre-headless
```
## 

## Running the API
```bash
# Run the API
python api.py
```

## Calling the API
```bash
# Generate a bundle (clears out previous bundle)
curl -X POST http://localhost:5000/generate_bundle

# Extract a patient (requires bundle to be generated first)
curl -X POST http://localhost:5000/generate_patient
```


## Project Status
🚧 In Development - Stage 3

## Development Stages

1. **Stage 1**: Generate a complete bundle for a single patient
2. **Stage 2**: Generate a complete bundle for a single patient with customizable input parameters
3. **Stage 3**: Generate a complete bundle to represent patient history, and extract only the demographic data. Return that via API.
4. **Stage 4**: (external downstream app) Then revert to LLM to generate the condition, encounter, treatment and medication resources. *(see Work in progress notes)*







## Input Parameters

- Date of generation / encounter
- Extent of encounter
- _(Additional parameters to be defined)_

## File Structure

- `fhir_samples/` - Sample FHIR data from [Synthea Sample Data (R4, Sept 2019)](https://synthetichealth.github.io/synthea-sample-data/downloads/synthea_sample_data_fhir_r4_sep2019.zip)
- `synthea/` - Java-based Synthea generator ([go to synthea-with-dependencies.md](/synthea/synthea-with-dependencies.md))


## References

- [Synthea Documentation](https://synthetichealth.github.io/synthea/)

## Work in progress notes:

Prompts:

patient
```
extract the patient resource from the following JSON file:
```

condition
```
now generate a condition resource  (a serious condition) with severity rating for this patient and reference the patient as appropriate. use FHIR R4 format
```

encounter
```
now generate an emergency encounter for 01-11-2024 for this patient, who has arrived in emergency via ambulance and reference the patient as appropriate.

The Hospital FHIR id 
   "resourceType": "Organization",
      "id": "6e193b4a-9a3d-3cac-854a-d89b9a8bf317",

use FHIR R4 format
```

treatment, medication and diagnosis
```
now generate resources to represent treatment, medication and diagnosis given during that encounter for this patient.
reference previous resources as appropriate.
use FHIR R4 format
```

free notes
```
now based on all of the above clinical activities for this patient, craft my a short set of bullet points as narrative of his journey
```