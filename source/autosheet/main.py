import sys

import wx

from autosheet.app.Window import Window
from autosheet.utils import constants, strings


def main():
    """
    Main function to run the application
    """
    if "--debug" in sys.argv:
        constants.DEBUG = True

    app = wx.App(redirect=False, useBestVisual=True)
    window = Window(strings.APP_NAME, constants.WINDOW_SIZE)
    window.Center()
    window.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
