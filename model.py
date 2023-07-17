'''
Módulo imagem.

Contém classes para manipular
imagens georreferenciadas (com informação de GPS)

Authors: Alice Maria
         Maria Eduarda
'''

from datetime import datetime
from PIL import Image
from typing import List, Tuple
import tkintermapview as tkmv
from utils import getGeotagging, getLatLon, getImageDateTime

# Utilize herança ou composição com o objeto
# retornado pelo método de classe "abre"
class Imagem:
    '''
    Representa uma imagem
    (classe principal do programa).
    '''
    def __init__(self, caminhoImagem: str):
        '''
        Inicializa um objeto imagem
        a partir do nome do seu arquivo.
        '''
        self._nome = caminhoImagem.rsplit('/')[-1] # nome do arquivo da imagem
        self._data = None # data de captura da imagem
        self._lat = None # latitude da captura da imagem
        self._lon = None # longitude da captura da imagem
        self._cidade = None # cidade da captura da imagem
        self._pais = None # país da captura da imagem
        self._arquivo = Image.open(caminhoImagem)
        self._processa_EXIF()

    def __repr__(self) -> str:
        '''
        Retorna representação de uma imagem
        em forma de str.
        '''
        return self._nome

    def _processa_EXIF(self) -> None:
        '''
        Processa metadados EXIF contidos no arquivo da imagem
        para extrair informações de data e local de captura.

        Atribui valores aos atributos de instância correspondentes
        à latitude, longitude e data de captura.
        '''
        exif_data = self._arquivo._getexif()

        try:
            geotags = getGeotagging(exif_data)
        except:
            print(f"Erro ao processar geotags da imagem {self._nome}")
        
        try:
            lat_lon = getLatLon(geotags)
            self._lat = lat_lon[0]
            self._lon = lat_lon[1]
        except:
            print(f"Erro ao processar latitude e longitude da imagem {self._nome}")
            self._lat = -5.843139132505788 
            self._lon = -35.199263651980374
        
        try:
            date_time = getImageDateTime(exif_data)
            self._data = datetime.strptime(date_time, '%Y:%m:%d %H:%M:%S').date()
        except:
            print(f"Imagem {self._nome} não possui data de captura")
            self._data = datetime.now().date()

    @property
    def nome(self) -> str:
        '''
        Retorna o nome do arquivo
        da imagem.
        '''
        return self._nome

    @property
    def largura(self) -> int:
        '''
        Retorna a largura da imagem.
        '''
        return self._arquivo.width

    @property
    def altura(self) -> int:
        '''
        Retorna a altura da imagem.
        '''
        return self._arquivo.height

    @property
    def tamanho(self) -> Tuple[int, int]:
        '''
        Retorna o tamanho da imagem
        (tupla largura x altura).
        '''
        return self._arquivo.size

    @property
    def data(self) -> datetime:
        '''
        Retorna a data em que a imagem
        foi capturada (objeto da classe datetime).
        '''
        return self._data

    def getDataFormatada(self) -> str:
        '''
        Retorna a data em que a imagem
        foi capturada (str no formato dd/mm/aaaa).
        '''
        return self._data.strftime("%d/%m/%Y")

    @property
    def latitude(self) -> float:
        '''
        Retorna a latitude (em decimais)
        em que a imagem foi capturada
        '''
        return self._lat

    @property
    def longitude(self) -> float:
        '''
        Retorna a longitude (em decimais)
        em que a imagem foi capturada
        '''
        return self._lon
    
    @property
    def cidade(self) -> str:
        if self._cidade is None:
            cidadeEncontrada = tkmv.convert_coordinates_to_city(self.latitude, self.longitude)
            if cidadeEncontrada is None:
                self._cidade = "Sem cidade"
            else:
                self._cidade = cidadeEncontrada
        
        return self._cidade
    
    @property
    def pais(self) -> str:
        if self._pais is None:
            self._pais = tkmv.convert_coordinates_to_country(self.latitude, self.longitude)
        
        return self._pais

    @property
    def arquivo(self) -> Image.Image:
        '''
        Retorna o objeto Image
        correspondente à imagem.
        '''
        return self._arquivo

    def imprime_info(self) -> None:
        '''
        Imprime informações sobre
        a imagem.
        '''
        print("Nome: ", self.nome)
        print("Data de captura: ", self.data)
        print("Latitude: ", self.latitude)
        print("Longitude: ", self.longitude)
        print("Altura: ", self.altura)
        print("Largura: ", self.largura)
        print("Tamanho: ", self.tamanho)
        print("Cidade: ", self.cidade)
        print("País: ", self.pais)

    def redimensiona(self, nv_lar: float, nv_alt: float) -> None:
        '''
        Altera as dimensões do objeto imagem para
        que ele possua novo tamanho dado por
        nv_lar x nv_alt.
        '''
        novo_tamanho = (int(nv_lar), int(nv_alt))
        self._arquivo.resize(size=novo_tamanho)
        self._arquivo.save(self._nome)

class BDImagens:
    '''
    Representa um banco de dados de
    imagens geoespaciais
    (classe de busca do programa).
    '''

    def __init__(self, idx):
        self.imagens: List[Imagem] = []
        self._idx = idx
        self._processaImagens()
        

    def _processaImagens(self) -> None:
        with open(self._idx, 'r') as file:
            for line in file:
                nome = line.strip()
                imagem = Imagem(nome)
                self.imagens.append(imagem)

    @property
    def tamanho(self) -> int:
        '''
        Retorna a quantidade de imagem
        no banco de dados.
        '''
        return len(self.imagens)

    def todas(self) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens abertas
        no banco de dados.
        '''
        return self.imagens

    def busca_por_nome(self, texto: str) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados
        cujo nome contenha o texto passado
        como parâmetro.
        '''
        imagens_encontradas = []
        for imagem in self.imagens:
            if texto.lower() in imagem.nome.lower():
                imagens_encontradas.append(imagem)
        return imagens_encontradas
    
    def busca_por_data(self, dini: datetime.date, dfim: datetime.date, cidadeBusca: str = None, paisBusca: str = None) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados
        cuja data de captura encontra-se entre
        dini (data inicial) e dfim (data final), filtrando por cidade ou país caso seja passado como parâmetro.
        '''
        imagens_encontradas = []
        for imagem in self.imagens:
            if dini <= imagem.data <= dfim:
                if cidadeBusca is not None and cidadeBusca.lower() in imagem.cidade.lower():
                    imagens_encontradas.append(imagem)
                elif paisBusca is not None and paisBusca.lower() in imagem.pais.lower():
                    imagens_encontradas.append(imagem)
                else:
                    imagens_encontradas.append(imagem)
        return imagens_encontradas
        
    
    def busca_por_cidade(self, cidade: str) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados
        cuja cidade de captura é cidade.
        '''
        imagens_encontradas = []
        for imagem in self.imagens:
            if cidade.lower() in imagem.cidade.lower():
                imagens_encontradas.append(imagem)
        return imagens_encontradas

    def busca_por_pais(self, pais: str) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados
        cujo país de captura é pais.
        '''
        imagens_encontradas = []
        for imagem in self.imagens:
            if pais.lower() in imagem.pais.lower():
                imagens_encontradas.append(imagem)
        return imagens_encontradas
