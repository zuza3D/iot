from tkinter import *

from controller.controller import Controller
from model import init_db

if __name__ == '__main__':
    init_db()

    controller = Controller()
