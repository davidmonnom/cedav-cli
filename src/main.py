import typer
import sys

from module import odoo_utils
from module import postgres_utils
from module import commit_utils
from rich import print

app = typer.Typer()

def main():
    """
    This function is the main entry point for the CLI

    Odoo CLI: Allow you to start a server, initialize the configuration,
    change the version, pull the latest changes, and drop the database.

    Postgres CLI: Allow you to dump and restore a database.

    Commit CLI: Allow you to run commit utils and initialize the configuration.
    """

    print("[bold yellow]Hello, which CLI do you want to use?")
    print("[bold]1. Odoo")
    print("[bold]2. Postgres")
    print("[bold]3. Commit")
    print("[bold]4. Exit")
    option = typer.prompt("Select an option")

    if option == "1":
        odoo_cli()
    elif option == "2":
        postgres_cli()
    elif option == "3":
        commit_cli()
    elif option == "4":
        print("[bold green]Goodbye")


def postgres_cli():
    postgres_utils.choices()


def odoo_cli():
    odoo_utils.choices()


def commit_cli():
    commit_utils.choices()


if __name__ == "__main__":
    typer.run(main)
