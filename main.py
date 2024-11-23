from gateway import Gateway
from agent import Agent
import argparse
from board import Board, Color


if __name__ == "__main__":
    argparse = argparse.ArgumentParser()

    argparse.add_argument(
        "--team",
        help="The color of the player: WHITE or BLACK",
        type=str.upper,
        choices=["WHITE", "BLACK"],
        required=True,
    )
    argparse.add_argument(
        "--name", help="The name of the player", type=str, default="VikingAI"
    )
    argparse.add_argument(
        "--ip", help="The IP address of the server", type=str, default="localhost"
    )
    argparse.add_argument(
        "--timeout", help="The timeout for the server", type=int, default=60
    )
    argparse.add_argument(
        "--port", help="Port of the player", type=int, default=5800
    )
    argparse.add_argument(
        "--weights", help="Weights for player", nargs=3,type=int, default=5800
    )
    args = argparse.parse_args()

    board = Board()
    gateway = Gateway(args.team, args.name, args.ip, args.port)

    if args.team == "WHITE":
        Agent(gateway, args.timeout, Color.WHITE, board, args.weights)
    else:
        Agent(gateway, args.timeout, Color.BLACK, board, args.weights)
