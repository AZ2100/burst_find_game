import matplotlib
matplotlib.use("TkAgg")
import game_player

data_path = "game_data"

if __name__ == "__main__":
    game_player.GamePlayer(data_path)
