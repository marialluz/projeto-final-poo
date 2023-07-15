import tkinter as tk
from typing import List
from model import Imagem
from view import ImagemView
from model import BDImagens

class ImagemController:
    def __init__(self, bd: BDImagens, view: ImagemView):
        self.imagens:List[Imagem] = []
        self._bd = bd
        self.view:ImagemView = view

    def inicializa(self):
        self._configura()
    
    def executa(self):
        self.view._root.mainloop()

    def _configura(self):
        self.view.botoes['Buscar']['command'] = self.buscar_imagem
        self.view.botoes['Redefinir']['command'] = self.redefinir_busca

    
    def buscar_imagem(self):
        dataInicio = self.view._entryDataInicial.get_date()
        dataFim = self.view._entryDataFinal.get_date()
        cidade = self.view._entryCidade.get()
        pais = self.view._entryPais.get()


        print(dataInicio)
        print(dataFim)
        print(cidade)
        print(pais)

        imagens_encontradas = []

        # Filtrar imagens pela data
        if dataInicio and dataFim:
            imagens_encontradas = self._bd.busca_por_data(dataInicio, dataFim)

        if cidade:
            imagens_encontradas = [self._bd.busca_por_cidade(cidade)]

        if pais:
            imagens_encontradas = [self._bd.busca_por_pais(pais)]

        # Atualizar a exibição das imagens encontradas na view
        self.view.atualizar_lista_imagens(imagens_encontradas)

        print(imagens_encontradas)


        
    def redefinir_busca(self):
        self.view._listaImagens.delete(0, tk.END)
        for imagem in self._bd.imagens.todas():
            self.view._listaImagens.insert(tk.END, imagem.nome)
    
        