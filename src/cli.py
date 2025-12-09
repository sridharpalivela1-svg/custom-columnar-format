import click
from writer import write_custom_columns

@click.command()
@click.argument("input_file")
@click.argument("output_file")
@click.argument("columns", nargs=-1)
def cli(input_file, output_file, columns):
    """
    Example:
    python -m cli input.csv output.csv id name value
    """
    write_custom_columns(input_file, output_file, columns)
    click.echo(f"Created {output_file} with columns: {', '.join(columns)}")

if __name__ == "__main__":
    cli()
