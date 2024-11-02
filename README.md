# Synthea API

A REST API that generates FHIR resources from Synthea data. The API enables generation of patient FHIR resources based on specified input parameters.

## Development Stages

1. **Stage 1**: Generate a complete bundle for a single patient
2. **Stage 2**: Generate a complete bundle for a single patient with customizable input parameters
3. **Stage 3**: Generate a complete bundle to represent patient history, and extract only the demographic data. Then revert to LLM to generate the condition, encounter, treatment and medication resources. *(see Work in progress notes)*

## Project Status

🚧 In Development

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