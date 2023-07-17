import tkinter as tk
from typing import Dict, List
import tkintermapview as tkmv
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from model import Imagem

cor_botao = "#914275"
cor_fundo = "#cfa1c4"


class ImagemView:
    def __init__(self, root: tk.Tk, imagensIniciais: List[Imagem] = []):
        self._root = root
        self.botoes: Dict[str, tk.Button] = {}
        self._imagens = imagensIniciais
        self._indexImagemAtual = 0
        self.map: tkmv.TkinterMapView = None
        self._inicializa_gui()

    def _inicializa_gui(self):
        self._root.configure(bg=cor_fundo)

        self._root.title('Mapa de Fotos')
        self._root.geometry('1220x600')

        self._frameMapa = tk.Frame(self._root, bg=cor_fundo)
        self._frameMapa.pack(side=tk.LEFT)

        self._frameInterface = tk.Frame(self._root, bg=cor_fundo)
        self._frameInterface.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._frameBusca = tk.Frame(self._frameInterface, bg=cor_fundo)
        self._frameBusca.pack(padx=10, pady=10)

        self._frameInfoImagem = tk.Frame(self._frameInterface, bg=cor_fundo)
        self._frameInfoImagem.pack(padx=20, pady=10, anchor="w")

        self._frameGallery = tk.Frame(self._frameInfoImagem, bg=cor_fundo)
        self._frameGallery.grid(row=1, column=0, columnspan=2)

        self._frameImagemAtual = tk.Frame(self._frameInfoImagem, bg=cor_fundo)
        self._frameImagemAtual.grid(row=1, column=2, columnspan=2)

        self._frameWave = tk.Frame(self._frameInterface, bg=cor_fundo)
        self._frameWave.pack(anchor="sw")

        self.map = tkmv.TkinterMapView(
            self._frameMapa, width=600, height=800, corner_radius=0)
        self.map.set_tile_server(
            "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map.pack(expand=True)

        self._lupaIcon = ImageTk.PhotoImage(
            Image.open("./assets/lupaIcon.png").resize((20, 20)))
        self._labelLupa = tk.Label(
            self._frameBusca, image=self._lupaIcon, bg=cor_fundo)
        self._labelLupa.grid(row=0, column=0, sticky="w", pady=5)

        self._labelTituloUm = tk.Label(self._frameBusca, text="Busca por imagem: ", bg=cor_fundo, font=(
            "Times New Roman", 14, "bold"), foreground=cor_botao)
        self._labelTituloUm.grid(row=0, column=1, sticky="w", pady=5)

        self._labelFiltrarPor = tk.Label(
            self._frameBusca, text="Filtrar por: ", bg=cor_fundo)
        self._labelFiltrarPor.grid(row=1, column=0)

        self._checkPaisVar = tk.IntVar()
        self._checkPaisButton = tk.Checkbutton(
            self._frameBusca, text="País", bg=cor_fundo, variable=self._checkPaisVar, onvalue=1, offvalue=0, command=self.checkTipoBusca)
        self._checkPaisButton.grid(row=1, column=1)

        self._checkCidadeVar = tk.IntVar()
        self._checkCidadeButton = tk.Checkbutton(
            self._frameBusca, text="Cidade", bg=cor_fundo, variable=self._checkCidadeVar, onvalue=1, offvalue=0, command=self.checkTipoBusca)
        self._checkCidadeButton.grid(row=1, column=2)

        self._filtrarPorDataVar = tk.IntVar()
        self._filtrarPorDataButton = tk.Checkbutton(
            self._frameBusca, text="Data", bg=cor_fundo, variable=self._filtrarPorDataVar, onvalue=1, offvalue=0, command=self.checkFiltrarPorData)
        self._filtrarPorDataButton.grid(row=1, column=3)

        self._labelDataInicial = tk.Label(
            self._frameBusca, text="Data Inicial: ", bg=cor_fundo)
        self._labelDataInicial.grid(
            row=2, column=0, sticky="w", padx=5, pady=5)
        self._entryDataInicial = DateEntry(self._frameBusca, selectmode='day',
                                           background=cor_botao, borderwidth=2, relief="flat", format='MM/dd/yyyy', locale='pt_BR', state='disabled')
        self._entryDataInicial.grid(row=2, column=1, padx=5, pady=5)

        self._labelDataFinal = tk.Label(
            self._frameBusca, text="Data Final: ", bg=cor_fundo)
        self._labelDataFinal.grid(row=2, column=2, sticky="w", padx=5, pady=5)
        self._entryDataFinal = DateEntry(self._frameBusca, selectmode='day',
                                         background=cor_botao, borderwidth=2, relief="flat", format='MM/dd/yyyy', locale='pt_BR', state='disabled')
        self._entryDataFinal.grid(row=2, column=3, padx=5, pady=5)

        self._labelCidade = tk.Label(
            self._frameBusca, text="Cidade: ", bg=cor_fundo)
        self._labelCidade.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self._entryCidade = tk.Entry(self._frameBusca, state='disabled')
        self._entryCidade.grid(row=3, column=1, padx=5, pady=5)

        self._labelPais = tk.Label(
            self._frameBusca, text="País: ", bg=cor_fundo)
        self._labelPais.grid(row=3, column=2, sticky="w", padx=5, pady=5)
        self._entryPais = tk.Entry(self._frameBusca, state='disabled')
        self._entryPais.grid(row=3, column=3, padx=5, pady=5)

        self.botoes['Buscar'] = tk.Button(
            self._frameBusca, text="Buscar", bg=cor_botao, foreground='white')
        self.botoes['Buscar'].grid(
            row=4, column=0, padx=5, pady=5, columnspan=2, sticky="e")

        self.botoes['Redefinir'] = tk.Button(
            self._frameBusca, text="Redefinir", bg=cor_botao, foreground='white')
        self.botoes['Redefinir'].grid(
            row=4, column=2, padx=5, pady=5, columnspan=2, sticky="w")

        # self._imageIcon = ImageTk.PhotoImage(
        #     Image.open("./assets/imageIcon.png").resize((20, 20)))
        # self._labelImage = tk.Label(
        #     self._frameInfoImagem, image=self._imageIcon, bg=cor_fundo)
        # self._labelImage.grid(row=0, column=0, sticky="w", pady=5)

        self._labelTituloDois = tk.Label(self._frameGallery, text=f"Imagens ({len(self._imagens)}): ", bg=cor_fundo, font=(
            "Times New Roman", 14, "bold"), foreground=cor_botao)
        self._labelTituloDois.grid(row=0, column=0, sticky="w")

        self._imageLabel = tk.Label(
            self._frameGallery, text="Imagem: ", bg=cor_fundo)
        self._imageLabel.grid(row=1, column=0, columnspan=2, pady=5)

        self._prevButton = tk.Button(self._frameGallery, text="Anterior",
                                     bg=cor_botao, foreground='white', command=self.mostrarImagemAnterior)
        self._prevButton.grid(row=2, column=0)
        self._nextButton = tk.Button(self._frameGallery, text="Próxima",
                                     bg=cor_botao, foreground='white', command=self.mostrarProximaImagem)
        self._nextButton.grid(row=2, column=1)

        self._labelNomeImagemAtual = tk.Label(self._frameImagemAtual, text="Nome:", bg=cor_fundo)
        self._labelNomeImagemAtual.grid(row=0, column=0, sticky="w")

        self._labelDataImagemAtual = tk.Label(self._frameImagemAtual, text="Data:", bg=cor_fundo)
        self._labelDataImagemAtual.grid(row=1, column=0, sticky="w")

        self._labelLatImagemAtual = tk.Label(self._frameImagemAtual, text="Latitude:", bg=cor_fundo)
        self._labelLatImagemAtual.grid(row=2, column=0, sticky="w")
        self._labelLonImagemAtual = tk.Label(self._frameImagemAtual, text="Longitude:", bg=cor_fundo)
        self._labelLonImagemAtual.grid(row=3, column=0, sticky="w")

        self._labelCidadeImagemAtual = tk.Label(self._frameImagemAtual, text="Cidade:", bg=cor_fundo)
        self._labelCidadeImagemAtual.grid(row=4, column=0, sticky="w")

        self._labelPaisImagemAtual = tk.Label(self._frameImagemAtual, text="País:", bg=cor_fundo)
        self._labelPaisImagemAtual.grid(row=5, column=0, sticky="w")


        self._waveImage = ImageTk.PhotoImage(Image.open("./assets/wave3.png"))
        self._labelWave = tk.Label(
            self._frameWave, image=self._waveImage, bg=cor_fundo)
        self._labelWave.grid(row=3, column=0, sticky="s",
                             columnspan=2, pady=5, rowspan=2)

        self._frameInterface.grid_rowconfigure(0, weight=1)
        self._frameInterface.grid_columnconfigure(0, weight=1)

        self._mostrarImagemAtual()

    def _mostrarImagemAtual(self):
        img = self._imagens[self._indexImagemAtual]
        photo = ImageTk.PhotoImage(img.arquivo.resize((300, 300)))
        self._imageLabel.configure(image=photo)
        self._imageLabel.image = photo
        self._labelNomeImagemAtual.configure(text=f"Nome: {img.nome}")
        self._labelDataImagemAtual.configure(text=f"Data: {img.getDataFormatada()}")
        self._labelLatImagemAtual.configure(text=f"Latitude: {img.latitude}")
        self._labelLonImagemAtual.configure(text=f"Longitude: {img.longitude}")
        self._labelCidadeImagemAtual.configure(text=f"Cidade: {img.cidade}")
        self._labelPaisImagemAtual.configure(text=f"País: {img.pais}")
        self.atualizarMapa()

    def atualizarMapa(self):
        img = self.imagemAtual()
        address = f"{img.cidade}, {img.pais}"
        photo = ImageTk.PhotoImage(img.arquivo.resize((100, 100)))
        self.map.set_marker(
            img.latitude, img.longitude, text=address, image=photo
        )
        self.map.set_zoom(15)
        self.map.set_position(img.latitude, img.longitude)
    
    def mostrarProximaImagem(self):
        self._indexImagemAtual = (
            self._indexImagemAtual + 1) % len(self._imagens)
        self._mostrarImagemAtual()

    def mostrarImagemAnterior(self):
        self._indexImagemAtual = (
            self._indexImagemAtual - 1) % len(self._imagens)
        self._mostrarImagemAtual()

    def checkTipoBusca(self):
        if self._checkPaisVar.get() == 1:
            self._entryPais.config(state='normal')
            self._entryCidade.config(state='disabled')
            self._checkCidadeVar.set(0)
        elif self._checkCidadeVar.get() == 1:
            self._entryCidade.config(state='normal')
            self._entryPais.config(state='disabled')
            self._checkPaisVar.set(0)
        else:
            self._entryCidade.config(state='disabled')
            self._entryPais.config(state='disabled')

    def checkFiltrarPorData(self):
        if self._filtrarPorDataVar.get() == 1:
            self._entryDataInicial.config(state='normal')
            self._entryDataFinal.config(state='normal')
        else:
            self._entryDataInicial.config(state='disabled')
            self._entryDataFinal.config(state='disabled')

    def atualizar_lista_imagens(self, imagens):
        self._imagens = imagens
        self._indexImagemAtual = 0
        self._labelTituloDois.configure(
            text=f"Imagens ({len(self._imagens)}): ")
        self._mostrarImagemAtual()

    def imagemAtual(self):
        return self._imagens[self._indexImagemAtual]

    def getDataInicial(self):
        try:
            return self._entryDataInicial.get_date()
        except:
            return None

    def getDataFinal(self):
        try:
            return self._entryDataFinal.get_date()
        except:
            return None

    def getCidade(self):
        return self._entryCidade.get()

    def getPais(self):
        return self._entryPais.get()

    def getFiltrandoPor(self):
        if self._checkPaisVar.get() == 1:
            return "pais"
        elif self._checkCidadeVar.get() == 1:
            return "cidade"

    def getFiltrandoPorData(self):
        return self._filtrarPorDataVar.get()

    def redefinirCamposBusca(self):
        self._entryDataInicial.set_date(None)
        self._entryDataFinal.set_date(None)
        self._entryCidade.delete(0, tk.END)
        self._entryPais.delete(0, tk.END)
        self._checkCidadeVar.set(0)
        self._checkPaisVar.set(0)
        self._filtrarPorDataVar.set(0)
        self._entryDataInicial.config(state='disabled')
        self._entryDataFinal.config(state='disabled')
        self._entryCidade.config(state='disabled')
        self._entryPais.config(state='disabled')
