from gateway import Gateway
from agent import Agent
import argparse


if __name__ == "__main__":
    argparse = argparse.ArgumentParser()

    argparse.add_argument(
        "--team",
        help="The color of the player: WHITE or BLACK",
        type=str.upper,
        choices=["WHITE", "BLACK"],
        required=True,
    ),
    argparse.add_argument(
        "--name", help="The name of the player", type=str, default="VikingAI"
    )
    argparse.add_argument(
        "--ip", help="The IP address of the server", type=str, default="localhost"
    )
    argparse.add_argument(
        "--timeout", help="The timeout for the server", type=int, default=60
    )
    args = argparse.parse_args()

    gateway = Gateway(args.team, args.name, args.timeout, args.ip)
    Agent(gateway)
