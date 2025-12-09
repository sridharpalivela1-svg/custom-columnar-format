import csv

def write_custom_columns(input_file, output_file, columns):
    """
    Writes only selected columns from input CSV to output CSV.
    :param input_file: Path to input CSV
    :param output_file: Path to output CSV
    :param columns: List of column names to keep
    """
    with open(input_file, mode="r", newline="") as infile:
        reader = csv.DictReader(infile)
        selected_rows = [{col: row[col] for col in columns if col in row} for row in reader]

    with open(output_file, mode="w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(selected_rows)
