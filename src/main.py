import arcade
from game import Game
# [from <name>] import <name> [, <name>]* [as <name> [, <name>]* ]

# Run game here
def main():

    new_game = Game(640, 480, "Snake Game")
    arcade.run()


if __name__ == "__main__":
    main()