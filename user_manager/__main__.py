import os
import sys
import click
import uvicorn

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)


@click.command()
@click.argument("action", type=click.STRING, required=False)
def main(action: str):
    if action == "run":
        uvicorn.run(
            app="server:app",
            host="127.0.0.1",
            port=5656,
            workers=1,
        )


if __name__ == "__main__":
    main()
