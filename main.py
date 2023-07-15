import tkinter as tk
from view import ImagemView
from controller import ImagemController
from model import BDImagens


def main():
    root = tk.Tk()
    view = ImagemView(root)

    # bd = BDImagens('./dataset1/index')
    # bd.processa()

    imagensController = ImagemController(BDImagens, view)

    imagensController.inicializa()
    imagensController.executa()

if __name__ == "__main__":
    main()