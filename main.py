import tkinter as tk
from view import ImagemView
from controller import ImagemController
from model import BDImagens


def main():
    root = tk.Tk()

    print("Iniciando o banco de imagens...")
    bd = BDImagens('./albuns-de-fotos/album-mariaLuz/index')

    print("Iniciando a view...")
    view = ImagemView(root, bd.imagens)

    print("Iniciando o controlador...")
    imagensController = ImagemController(bd, view)

    print("Configurando a aplicação...")
    imagensController.configura()
    print("Executando a aplicação...")
    imagensController.executa()

if __name__ == "__main__":
    main()
