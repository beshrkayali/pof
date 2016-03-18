import click
from pof import POFixer


@click.command()
@click.argument('po_input', required=True)
@click.argument('po_output', required=False)
@click.argument('tries', default=10, required=False)
def main(po_input, po_output, tries):
    """Fix syntax errors in po files."""
    click.echo('Processing: {}'.format(po_input))

    pof = POFixer(input_file=po_input,
                  output_file=po_output if po_output else po_input)

    for i in xrange(tries):
        if pof.check_errors():
            pof.fix_all()
        else:
            break

    pof.save()

    # If errors still exist print a report
    pof.print_errors()
