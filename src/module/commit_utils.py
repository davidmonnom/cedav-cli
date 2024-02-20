import typer
import g4f

from rich import print
from git import Repo

from .cache_utils import read_json_configuration, write_json_configuration


def choices():
    print("[bold yellow]Welcome to Odoo CLI, what do you want to do?")
    print("[bold]1. Run commit utils")
    print("[bold]2. Initialize configuration")
    option = typer.prompt("Select an option")

    if option == "1":
        run()
    elif option == "2":
        init()


def run(style="original"):
    configuration = read_json_configuration("cedav-cli-commit.json")
    repo = Repo(configuration.get("repo_path"))

    diff = repo.git.diff()
    reason = typer.prompt("Reason for the commit?", type=str)

    print("[bold yellow]What's the style of the commit message?")
    print("[bold]1. Original")
    print("[bold]2. Odoo")
    style = typer.prompt("Select an option")
    if style == "1":
        style = "original"
    elif style == "2":
        style = "odoo"

    # Check if there is some diff
    if not diff:
        print("[bold red]There is no diff to commit")
        return

    prompt = f"""
        Create a commit message with what's the behavior before the change,
        what's the behavior after the change, and the reason for the change.

        Rules:
        - The commit should follow the {style} style.
        - The commit should never contains code snippet.
        - The commit should never contains diff itself.
        - The commit should never contains any link or URL.
        - The commit should have 2 paragraphs, one for the behavior before the change,
        and one for the behavior after the change.

        Information about the changes:
        - Here is the diff: {diff}
        - Here is the reason: {reason}
    """

    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo_16k_0613,
        messages=[{"role": "user", "content": prompt}],
    )

    print("[bold green]Commit message created successfully:")
    print(response)


def init():
    print("[bold yellow]We will initialize the configuration file")
    print("[bold yellow]Please provide the following information:")

    configuration = read_json_configuration("cedav-cli-commit.json") or ""
    repo_path = typer.prompt("Repository path?", configuration.get("repo_path") or "", type=str)

    result =write_json_configuration("cedav-cli-commit.json", {
        "repo_path": repo_path,
    })

    if not result:
        print("[bold red]Error creating configuration file")
        return False

    print("[bold green]Configuration file created successfully")
