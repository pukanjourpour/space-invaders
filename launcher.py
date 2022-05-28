from view_pygame import ViewPyGame

class Launcher:
    def __init__(self):
        self.game = ViewPyGame()
        
    def run(self):
        self.game.run_game()

if __name__ == "__main__":
    launcher = Launcher()
    launcher.run()
