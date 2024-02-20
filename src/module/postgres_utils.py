import typer
import os

from rich import print


CACHE_PATH = f"{os.getcwd()}/.cache"


def choices():
    print("[bold yellow]Welcome to Postgres CLI, what do you want to do?")
    print("[bold]1. Dump database")
    print("[bold]2. Restore database")
    option = typer.prompt("Select an option")

    if option == "1":
        dump()
    elif option == "2":
        restore()


def dump():
    print("[bold yellow]We dump your database in a file stored in the cache folder")
    print("[bold yellow]Please provide the following information:")

    db_name = typer.prompt("Database name?", "", type=str)

    os.system(f"pg_dump '{db_name}' > '{CACHE_PATH}/{db_name}.sql'")
    print("[bold green]Database dumped successfully")


def restore():
    print("[bold yellow]We will restore your database from a file stored in the cache folder")
    print("[bold yellow]Please provide the following information:")

    db_name = typer.prompt("Database name?", "", type=str)

    os.system(f"psql -d '{db_name}' -f '{CACHE_PATH}/{db_name}.sql'")
    print("[bold green]Database restored successfully")
