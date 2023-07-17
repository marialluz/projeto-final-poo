import tkinter as tk
from typing import List
from model import Imagem
from view import ImagemView
from model import BDImagens


class ImagemController:
    def __init__(self, bd: BDImagens, view: ImagemView):
        self.imagens: List[Imagem] = []
        self._bd = bd
        self.view: ImagemView = view

    def executa(self):
        self.view._root.mainloop()

    def configura(self):
        self.view.botoes['Buscar']['command'] = self.buscar_imagem
        self.view.botoes['Redefinir']['command'] = self.redefinir_busca

    def buscar_imagem(self):
        dataInicio = self.view.getDataInicial()
        dataFim = self.view.getDataFinal()
        cidade = self.view.getCidade()
        pais = self.view.getPais()
        filtrandoPor = self.view.getFiltrandoPor()
        filtrandoPorData = self.view.getFiltrandoPorData()

        imagens_encontradas = []
        # Filtrar imagens pela data
        if filtrandoPorData and dataInicio and dataFim:
            imagens_encontradas = self._bd.busca_por_data(dataInicio, dataFim)

        if filtrandoPor == "cidade" and cidade:
            imagens_encontradas = self._bd.busca_por_cidade(cidade)

        if filtrandoPor == "pais" and pais:
            imagens_encontradas = self._bd.busca_por_pais(pais)

        # Atualizar a exibição das imagens encontradas na view
        self.view.atualizar_lista_imagens(imagens_encontradas)

    def redefinir_busca(self):
        self.view.atualizar_lista_imagens(self._bd.imagens)
        self.view.redefinirCamposBusca()
