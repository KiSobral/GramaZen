import time

from coordinates import Coordinates
from gui import Gui


if __name__ == "__main__":
    time.sleep(0.1)
    gui = Gui(Coordinates())
    while True:
        gui.main()
