import typer
import os

from rich import print
from git import Repo
from .cache_utils import read_json_configuration, write_json_configuration


CACHE_PATH = f"{os.path.dirname(__file__)}/../../.cache"


def choices():
    print("[bold yellow]Welcome to Odoo CLI, what do you want to do?")
    print("[bold]1. Run Odoo server")
    print("[bold]2. Initialize configuration")
    print("[bold]3. Change version")
    print("[bold]4. Pull latest changes")
    print("[bold]5. Drop database")
    option = typer.prompt("Select an option")

    if option == "1":
        run()
    elif option == "2":
        init()
    elif option == "3":
        version()
    elif option == "4":
        pull()
    elif option == "5":
        dropdb()


def init():
    print("[bold yellow]We will initialize the configuration file")
    print("[bold yellow]Please provide the following information:")

    configuration = read_json_configuration("cedav-cli-odoo.json")
    enterprise_path = typer.prompt("Odoo enterprise path?", configuration.get("enterprise_path") or "", type=str)
    community_path = typer.prompt("Odoo community path?", configuration.get("community_path") or "", type=str)
    port = typer.prompt("Port to run Odoo server?", configuration.get("port") or 8069, type=int)
    configuration_file_path = typer.prompt("Where is the odoo.conf file?", configuration.get("configuration_file_path") or "", type=str)

    result = write_json_configuration("cedav-cli-odoo.json", {
        "enterprise_path": enterprise_path,
        "community_path": community_path,
        "port": port,
        "configuration_file_path": configuration_file_path
    })

    if not result:
        print("[bold red]Error creating configuration file")
        return False

    print("[bold green]Configuration file created successfully")


def version():
    print("[bold yellow]We will change the Odoo version and drop the database")
    print("[bold yellow]Please provide the following information:")

    configuration = read_json_configuration("cedav-cli-odoo.json")
    target_version = typer.prompt("Target Odoo version?", configuration.get("target_version") or "", type=str)

    enterprise_repo = Repo(configuration.get("enterprise_path"))
    community_repo = Repo(configuration.get("community_path"))

    try:
        enterprise_repo.git.checkout(target_version)
        print(f"[bold green]Enterprise version updated successfully to {target_version}")
        community_repo.git.checkout(target_version)
        print(f"[bold green]Community version updated successfully to {target_version}")
        dropdb()
    except:
        print("[bold red]Error updating versions")
        return False
    print("[bold green]Odoo version updated successfully")



def pull():
    print("[bold yellow]We will pull the latest changes from the Odoo repositories")

    configuration = read_json_configuration("cedav-cli-odoo.json")
    enterprise_repo = Repo(configuration.get("enterprise_path"))
    community_repo = Repo(configuration.get("community_path"))

    try:
        enterprise_repo.remotes.origin.pull()
        print("[bold green]Enterprise repository updated successfully")
        community_repo.remotes.origin.pull()
        print("[bold green]Community repository updated successfully")
    except:
        print("[bold red]Error updating repositories")
        return False
    print("[bold green]Repositories updated successfully")


def dropdb():
    print("[bold yellow]We will drop the Odoo database")
    print(f"[bold red]Warning this script will delete the database file in {CACHE_PATH}/odoo.db[/bold red]")

    confirm = typer.prompt("Are you sure you want to continue? (yes/no)")
    if confirm == "yes":
        os.system(f"rm -r -f {CACHE_PATH}/odoo.db")


def run():
    """Run the Odoo server"""

    # Load configuration
    configuration = read_json_configuration("cedav-cli-odoo.json")
    if not configuration:
        print("[bold red]Error reading configuration file[/bold red]")
        return False

    community_path = configuration.get("community_path")
    enterprise_path = configuration.get("enterprise_path")
    port = configuration.get("port")
    configuration_file_path = configuration.get("configuration_file_path")

    try:
        # Verify enterprise path exists (optional)
        enterprise_path_check = os.path.exists(enterprise_path)
        if not enterprise_path_check:
            print(f"[bold yellow]Enterprise path not provided[/bold yellow]")

        # Verify community path exists
        community_path_check = os.path.exists(community_path)
        if not community_path_check:
            print(f"[bold red]Community path not found ({community_path})[/bold red]")
            return False

        # Verify Odoo configuration file exists
        configuration_file_path_check = os.path.exists(configuration_file_path)
        if not configuration_file_path_check:
            print(f"[bold red]Odoo configuration file not found ({configuration_file_path})[/bold red]")
            return False

        # Verify odoo-bin binary exists
        odoo_bin = os.path.isfile(f"{community_path}/odoo-bin")
        if not odoo_bin:
            print(f"[bold red]odoo-bin binary not found[/bold red]")
            return False

        # Verify odoo-bin binary is executable
        odoo_bin = os.access(f"{community_path}/odoo-bin", os.X_OK)
        if not odoo_bin:
            print(f"[bold red]odoo-bin binary is not executable[/bold red]")
            return False
    except:
        print("[bold red]Error verifying paths[/bold red]")
        print(f"[bold yellow]   Community path: {community_path}[/bold yellow]")
        print(f"[bold yellow]   Enterprise path: {enterprise_path}[/bold yellow]")
        print(f"[bold yellow]   Configuration file path: {configuration_file_path}[/bold yellow]")

        update_config_file = typer.prompt("Do you want to update the configuration file? (yes/no)")
        if update_config_file == "yes":
            init()

        return False

    # Launch Odoo server
    # Verify if cache db exist:
    args = "-i point_of_sale"
    if os.path.exists(f"{CACHE_PATH}/odoo.db"):
        args = ""

    print(f"Launching Odoo server on port {port}")
    os.system(f"{community_path}/odoo-bin --addons-path={community_path}/addons,{community_path}/odoo/addons,{enterprise_path} -d {CACHE_PATH}/odoo.db -p {port} {args}")
