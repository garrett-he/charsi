import click

from charsi import __version__


def print_version(ctx: click.Context, _, value: bool):
    if not value or ctx.resilient_parsing:
        return

    click.echo(__version__)
    ctx.exit()


@click.command()
@click.option('--version', help='Show version information.', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def cli():
    """A command-line tool to help game modders build string resources for Diablo II: Resurrected."""


if __name__ == '__main__':
    cli()
