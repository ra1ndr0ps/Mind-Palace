import click
import pathlib
from . import run_server
from . import run_webserver
from . import upload_thought


@click.group()
def main(**kwargs):
    pass


@main.command()
@click.argument('address')
@click.argument('user', type=int)
@click.argument('thought')
def upload(address, user, thought):
    try:
        ip, port = address.split(":")
        port = int(port)
        user_id = int(user)
        upload_thought((ip, port), user_id, thought)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


@main.command()
@click.argument('address')
@click.argument('data')
def start_server(address, data):
    try:
        ip, port = address.split(":")
        port = int(port)
        path = pathlib.Path(data)
        run_server((ip, port), path)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


@main.command()
@click.argument('address')
@click.argument('data_dir')
def start_webserver(address, data_dir):
    try:
        run_webserver(address, data_dir)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == "__main__":
    main()
