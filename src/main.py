"""Entry point for Doodle Jump."""

from src.controllers.game_controller import GameController


def main() -> None:
    GameController().run()


if __name__ == "__main__":
    main()
