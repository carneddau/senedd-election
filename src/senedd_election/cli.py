from typer import Exit, Option, Typer

from .settings import get_settings
from .utils import console, version

# Allow invocation without subcommand so --version option does not produce an error
interface = Typer(invoke_without_command=True, no_args_is_help=True)


@interface.callback()
def version_callback(
    print_version: bool = Option(False, "--version", "-v", is_eager=True),
):
    if print_version:
        console.print(version())
        raise Exit()


@interface.command()
def config():
    """Display configuration"""
    settings = get_settings()
    console.print(
        {
            "App data path": str(settings.user_data_dir),
        },
    )


def cli():
    """Run the CLI tool"""
    interface()
