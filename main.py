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
        "--ip", help="The IP address of the server", type=str, default="localhost"
    )
    argparse.add_argument(
        "--timeout", help="The timeout for the server", type=int, default=60
    )
    

    args = argparse.parse_args()

    board = Board()
    gateway = Gateway(args.team, "GiulioJr", args.ip)

    if args.team == "WHITE":
        Agent(gateway, args.timeout, Color.WHITE, board, [25, 5, 8])
    else:
        Agent(gateway, args.timeout, Color.BLACK, board, [12,20,2])
