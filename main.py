from core.game import Game

if __name__ == "__main__":
    game = Game(1000, 800, "Space rush!", 60, mobs_count=10, lives=3)

    game.start()
