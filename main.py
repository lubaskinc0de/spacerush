from core.game import Game

if __name__ == "__main__":
    game = Game(600, 500, "Space rush!", 60, mobs_count=6, lives=3)

    game.start()
