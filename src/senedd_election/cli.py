from typer import Exit, Option, Typer

from .db import create_db, drop_db
from .scrape import scrape as _scrape
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


@interface.command()
def scrape(
    reset: bool = Option(False, "--reset", help="Drop existing data in the database"),
):
    """Scrape data and save to a local SQLite DB"""
    # Safe to call repeatedly - will not overwrite already existing tables
    create_db()

    if reset:
        drop_db()

    create_db()

    _scrape()


def cli():
    """Run the CLI tool"""

    interface()
