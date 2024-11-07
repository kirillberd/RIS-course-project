import requests
import click
from pathlib import Path

@click.group()
def cli():...

@cli.command()
@click.argument("namespace", type=str)
@click.argument("host", type=str)
@click.argument("credpath", type=str)
@click.argument("vault_token", type=str)
@click.argument("env_file", type=Path)
def vault_env(
        namespace,
        host,
        credpath,
        vault_token,
        env_file
):
    request_string = f"http://{host}/v1/{namespace}/{credpath}"
    resp = requests.request("GET", request_string, headers={"X-Vault-Token": vault_token})
    dotenv_vars = resp.json().get("data")
    with open(env_file, "a") as file:
        for key, secret in dotenv_vars.items():
            file.write(f"{key}={secret}\n")

if __name__ == "__main__":
    cli()