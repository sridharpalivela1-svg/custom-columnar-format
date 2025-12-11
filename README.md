# Custom Columnar Format

This project implements a simple custom columnar storage format similar to Parquet/ORC.

## How to Run

### Install dependencies
pip install -r requirements.txt

### Write + Read Data
python example.py

This generates `output.ccf` and reads it back.

## Project Structure
src/columnar_writer.py  – Writes the format  
src/columnar_reader.py  – Reads the format  
example.py              – Example usage  
SPEC.md                 – Format documentation  
README.md               – Instructions  
