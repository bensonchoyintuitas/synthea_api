# Synthea API

A REST API that generates FHIR resources from Synthea data. The API enables generation of patient FHIR resources based on specified input parameters.

## Development Stages

1. **Stage 1**: Generate a complete bundle for a single patient
2. **Stage 2**: Generate a complete bundle for a single patient with customizable input parameters

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
