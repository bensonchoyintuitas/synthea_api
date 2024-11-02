# Synthea Patient Generator

## Reference Documentation
For detailed information, visit the [Synthea Wiki Basic Setup Guide](https://github.com/synthetichealth/synthea/wiki/Basic-Setup-and-Running)

## Getting Started

### Installation
```bash
# Download Synthea
wget https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar

# and place it in this working directory

# Install Java (if needed)
sudo apt install openjdk-11-jre-headless
```

### Basic Usage
```bash
# Generate 10 patients with seed 123
java -jar synthea-with-dependencies.jar --exporter.fhir.use_us_core_ig true -p 10 -s 123

# Generate 1000 patients with random seed and reference date
java -jar synthea-with-dependencies.jar --exporter.fhir.use_us_core_ig true -p 1000 -s $((RANDOM % 100)) -r 20240315

# Generate 1 patient with current date and custom config
java -jar synthea-with-dependencies.jar --exporter.fhir.use_us_core_ig true -p 1 -c synthea.properties -r $(date +%Y%m%d)

java -jar synthea-with-dependencies.jar  -c synthea.properties -p 1 -r $(date +%Y%m%d)
```

## Command Line Options

### Common Examples
- Show help message:
  ```bash
  java -jar synthea-with-dependencies.jar -h
  ```

- Generate by location:
  ```bash
  # All cities in Massachusetts
  java -jar synthea-with-dependencies.jar Massachusetts
  
  # Specific city (Juneau, Alaska)
  java -jar synthea-with-dependencies.jar Alaska Juneau
  ```

- Control population characteristics:
  ```bash
  # Set specific seed (reproducible results)
  java -jar synthea-with-dependencies.jar -s 12345
  
  # Generate 1000 patients
  java -jar synthea-with-dependencies.jar -p 1000
  
  # Age range 30-40 years
  java -jar synthea-with-dependencies.jar -a 30-40
  
  # Only female patients
  java -jar synthea-with-dependencies.jar -g F
  ```

- Combined parameters:
  ```bash
  # Seattle, WA with seed 987
  java -jar synthea-with-dependencies.jar -s 987 Washington Seattle
  
  # 100 patients in Salt Lake City with seed 21
  java -jar synthea-with-dependencies.jar -s 21 -p 100 Utah "Salt Lake City"
  ```

### FHIR Export Options
```bash
# Export using US Core R4 Implementation Guide profiles
java -jar synthea-with-dependencies.jar --exporter.fhir.use_us_core_ig true
```