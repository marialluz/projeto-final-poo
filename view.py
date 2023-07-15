import tkinter as tk
from tkinter import ttk
from typing import Dict
import tkintermapview as tkmv
from PIL import Image, ImageTk
from tkcalendar import DateEntry


class ImagemView:
    def __init__(self, root: tk.Tk):
        self._root = root
        self.botoes: Dict[str, tk.Button] = {}
        self._inicializa_gui()

    def _inicializa_gui(self):
        cor_botao = "#914275" 
        cor_fundo = "#cfa1c4"
        self._root.configure(bg=cor_fundo)

        self._root.title('Mapa de Fotos')
        self._root.geometry('1200x600')

        self._frameMapa = tk.Frame(self._root, bg=cor_fundo)
        self._frameMapa.pack(side=tk.LEFT)

        self._frameInterface = tk.Frame(self._root, bg=cor_fundo)
        self._frameInterface.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._frameBusca = tk.Frame(self._frameInterface, bg=cor_fundo)
        self._frameBusca.pack(padx=10, pady=10)

        self._frameInfoImagem = tk.Frame(self._frameInterface, bg=cor_fundo)
        self._frameInfoImagem.pack(padx=20, pady=10, anchor="w")

        self._frameWave = tk.Frame(self._frameInterface, bg=cor_fundo)
        self._frameWave.pack(anchor="sw")

        map = tkmv.TkinterMapView(self._frameMapa, width=600, height=800, corner_radius=0)
        map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        map.set_address('ECT UFRN') # centraliza mapa na ECT/UFRN
        map.set_zoom(15)
        map.pack(expand=True)
        map.set_marker(-5.843428, -35.199286, text='ECT/UFRN', )


        lupaImg = Image.open("./assets/lupaIcon.png")
        self._lupaIcon = ImageTk.PhotoImage(lupaImg.resize((20, 20)), name="lupaIcon")
        self._labelLupa = tk.Label(self._frameBusca, image=self._lupaIcon, bg=cor_fundo)
        self._labelLupa.grid(row=0, column=0, sticky="w", pady=5)

        self._labelTituloUm = tk.Label(self._frameBusca, text="Busca por imagem: ", bg=cor_fundo, font=("Times New Roman", 14, "bold"), foreground=cor_botao)
        self._labelTituloUm.grid(row=0, column=1, sticky="w", pady=5)

        self._labelDataInicial = tk.Label(self._frameBusca, text="Data Inicial: ", bg=cor_fundo)
        self._labelDataInicial.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self._entryDataInicial = DateEntry(self._frameBusca, selectmode = 'day', year = 2023, month = 7, day = 13, background = cor_botao, borderwidth = 2, relief = "flat", format = 'MM/dd/yyyy', locale='pt_BR')
        self._entryDataInicial.grid(row=1, column=1, padx=5, pady=5)

        self._labelDataFinal = tk.Label(self._frameBusca, text="Data Final: ", bg=cor_fundo)
        self._labelDataFinal.grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self._entryDataFinal = DateEntry(self._frameBusca, selectmode = 'day', year = 2023, month = 7, day = 18, background = cor_botao, borderwidth = 2, relief = "flat", format = 'MM/dd/yyyy', locale='pt_BR')
        self._entryDataFinal.grid(row=1, column=3, padx=5, pady=5)

        self._labelCidade = tk.Label(self._frameBusca, text="Cidade: ", bg=cor_fundo)
        self._labelCidade.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self._entryCidade = tk.Entry(self._frameBusca)
        self._entryCidade.grid(row=2, column=1, padx=5, pady=5)

        self._labelPais = tk.Label(self._frameBusca, text="País: ", bg=cor_fundo)
        self._labelPais.grid(row=2, column=2, sticky="w", padx=5, pady=5)
        self._entryPais = tk.Entry(self._frameBusca)
        self._entryPais.grid(row=2, column=3, padx=5, pady=5)

        self.botoes['Buscar'] = tk.Button(self._frameBusca, text="Buscar", bg=cor_botao, foreground='white')
        self.botoes['Buscar'].grid(row=3, column=0, padx=5, pady=5, columnspan=2, sticky="e")

        self.botoes['Redefinir'] = tk.Button(self._frameBusca, text="Redefinir", bg=cor_botao, foreground='white')
        self.botoes['Redefinir'].grid(row=3, column=2, padx=5, pady=5, columnspan=2, sticky="w")


        imageIcon = Image.open("./assets/imageIcon.png")
        self._imageIcon = ImageTk.PhotoImage(imageIcon.resize((20, 20)), name="imageIcon")
        self._labelImage = tk.Label(self._frameInfoImagem, image=self._imageIcon, bg=cor_fundo)
        self._labelImage.grid(row=0, column=0, sticky="w", pady=5)

        self._labelTituloDois = tk.Label(self._frameInfoImagem, text="Imagem: ", bg=cor_fundo, font=("Times New Roman", 14, "bold"), foreground=cor_botao)
        self._labelTituloDois.grid(row=0, column=1, sticky="w")

        self._labelNomeImagem = tk.Label(self._frameInfoImagem, text="Nome:", bg=cor_fundo)
        self._labelNomeImagem.grid(row=1, column=0, sticky="w")

        self._labelDataImagem = tk.Label(self._frameInfoImagem, text="Data:", bg=cor_fundo)
        self._labelDataImagem.grid(row=2, column=0, sticky="w")

        self._labelCoordenadasImagem = tk.Label(self._frameInfoImagem, text="Coordenadas:", bg=cor_fundo)
        self._labelCoordenadasImagem.grid(row=3, column=0, sticky="w")

        self._labelCidadeImagem = tk.Label(self._frameInfoImagem, text="Cidade:", bg=cor_fundo)
        self._labelCidadeImagem.grid(row=4, column=0, sticky="w")

        self._labelPaisImagem = tk.Label(self._frameInfoImagem, text="País:", bg=cor_fundo)
        self._labelPaisImagem.grid(row=5, column=0, sticky="w")

        waveImg = Image.open("./assets/wave3.png")
        self._waveImage = ImageTk.PhotoImage(waveImg.resize((800, 300)), name="waveImage")
        self._labelWave = tk.Label(self._frameWave, image=self._waveImage, bg=cor_fundo)
        self._labelWave.grid(row=2, column=0, sticky="s", columnspan=2, pady=5, rowspan=2)

        self._frameInterface.grid_rowconfigure(0, weight=1)
        self._frameInterface.grid_columnconfigure(0, weight=1)

