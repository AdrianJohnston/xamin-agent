import os
import subprocess
import typing as t
import typer
from pathlib import Path

app = typer.Typer()


@app.command()
def start(git_repo: str,
          command: str,
          checkout_dir: t.Optional[str] = '.',
          branch: t.Optional[str] = 'main',
          git_auth_token: t.Optional[str] = None,
          working_dir: t.Optional[str] = '.',
          verbose: t.Optional[bool] = False):
    """Starts a process in the desired git repo.
    
    Clones the git repo, with an optional auth token, optionally checkouts a
    desired branch, then runs the provded command.

    Args:
        git_repo (str): The https URI for the desired git repo to clone.
        command (str):  The 
        git_auth_token (t.Optional[str], optional): [description]. Defaults to None.
    """

    # Originally I was going to use GitPython, but as we only need
    # limited functionallity, and it leaks memory on long running
    # processes, it makes sense to reduce the number of libraries
    # required to start batch jobs.
    
    if verbose:
        print(f"Cloning: {git_repo}#{branch} to {checkout_dir}")
    
    output = subprocess.run(["git", "clone", "-b", branch, git_repo], capture_output=True, check=True)
    
    if verbose:    
        print(output.stderr)
        print(f"SUCCESS: {output.returncode}")
    
    if verbose:
        print(f"Changing working directory to -> {working_dir}")
    
    os.chdir(working_dir)
    if verbose:
        print(f"Current Working Directory: {os.getcwd()}")

    if verbose:
        print(f"Running Command: {command}")

    subprocess.run([command], shell=True, check=True)



if __name__ == "__main__":
    app()