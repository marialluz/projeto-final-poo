'''
Módulo imagem.

Contém classes para manipular
imagens georreferenciadas (com informação de GPS)

Authors: Alice Maria
         Maria Eduarda
'''

from datetime import datetime
from PIL import Image
import PIL.ImageFile
from PIL.ExifTags import TAGS, GPSTAGS
from typing import List, Tuple
import tkintermapview as tkmv


def converte_graus_para_decimais(tup: Tuple[int, int, int], ref: str) -> float:
    '''
    Função utilitária: converte coordenadas de
    graus, minutos e segundos (tupla) para
    decimais (float).
    '''

    if ref.upper() in ('N', 'E'):
        s = 1
    elif ref.upper() in ('S', 'W'):
        s = -1

    return s*(tup[0] + float(tup[1]/60) + float(tup[2]/3600))

# Utilize herança ou composição com o objeto
# retornado pelo método de classe "abre"
class Imagem:
    '''
    Representa uma imagem
    (classe principal do programa).
    '''

    def __init__(self, nome):
        '''
        Inicializa um objeto imagem
        a partir do nome do seu arquivo.
        '''
        self._nome = nome.rsplit('/')[-1] # nome do arquivo da imagem
        self._data = None # data de captura da imagem
        self._lat = None # latitude da captura da imagem
        self._lon = None # longitude da captura da imagem
        self._cidade = None # cidade da captura da imagem
        self._pais = None # país da captura da imagem
        self._img = self.abre(nome)
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
        tup_lat = None
        tup_lon = None
        ref_lat = None
        ref_lon = None

        for c, v in self._img._getexif().items():
            if TAGS[c] == 'GPSInfo':
                for gps_cod, gps_dado in v.items():
                    if GPSTAGS[gps_cod] == 'GPSLatitude':
                        tup_lat = gps_dado
                    if GPSTAGS[gps_cod] == 'GPSLongitude':
                        tup_lon = gps_dado
                    if GPSTAGS[gps_cod] == 'GPSLatitudeRef':
                        ref_lat = gps_dado
                    if GPSTAGS[gps_cod] == 'GPSLongitudeRef':
                        ref_lon = gps_dado

                self._lat = converte_graus_para_decimais(tup_lat, ref_lat)
                self._lon = converte_graus_para_decimais(tup_lon, ref_lon)

                self._cidade = tkmv.convert_coordinates_to_city(self._lat, self._lon)
                self._pais = tkmv.convert_coordinates_to_country(self._lat, self._lon)

            if TAGS[c] == 'DateTime':
                self._data = datetime.strptime(v, '%Y:%m:%d %H:%M:%S')

    @staticmethod
    def abre(nome: str) -> PIL.ImageFile:
        '''
        Abre imagem a partir de
        arquivo com o nome
        fornecido.
        Retorna objeto imagem
        aberto.
        '''
        img = Image.open(nome)
        return img

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
        return self._img.width

    @property
    def altura(self) -> int:
        '''
        Retorna a altura da imagem.
        '''
        return self._img.height

    @property
    def tamanho(self) -> Tuple[int, int]:
        '''
        Retorna o tamanho da imagem
        (tupla largura x altura).
        '''
        return self._img.size

    @property
    def data(self) -> datetime:
        '''
        Retorna a data em que a imagem
        foi capturada (objeto da classe datetime).
        '''
        return self._data

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

    def imprime_info(self) -> None:
        '''
        Imprime informações sobre
        a imagem.
        '''
        print("Nome: ", self._nome)
        print("Data de captura: ", self._data)
        print("Latitude: ", self._lat)
        print("Longitude: ", self._lon)
        print("Altura: ", self.altura)
        print("Largura: ", self.largura)
        print("Tamanho: ", self.tamanho)

    def redimensiona(self, nv_lar: float, nv_alt: float) -> None:
        '''
        Altera as dimensões do objeto imagem para
        que ele possua novo tamanho dado por
        nv_lar x nv_alt.
        '''
        novo_tamanho = (int(nv_lar), int(nv_alt))
        self._img.resize(size=novo_tamanho)
        self._img.save(self._nome)

class BDImagens:
    '''
    Representa um banco de dados de
    imagens geoespaciais
    (classe de busca do programa).
    '''

    imagens: List[Imagem] = []

    def __init__(self, idx):
        self._idx = idx
        

    def processa(self) -> None:
        with open(self._idx, 'r') as file:
            for line in file:
                nome = line.strip()
                print(f'Processando {nome}...')
                imagem = Imagem(nome)
                self.imagens.append(imagem)

    @property
    def tamanho(self) -> int:
        '''
        Retorna a quantidade de imagem
        no banco de dados.
        '''
        return len(BDImagens.imagens)

    def todas(self) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens abertas
        no banco de dados.
        '''
        return BDImagens.imagens

    def busca_por_nome(self, texto: str) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados
        cujo nome contenha o texto passado
        como parâmetro.
        '''
        imagens_encontradas = []
        for imagem in BDImagens.imagens:
            if texto.lower() in imagem.nome.lower():
                imagens_encontradas.append(imagem)
        return imagens_encontradas

    @staticmethod
    def busca_por_data(dini: datetime.date, dfim: datetime.date) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados
        cuja data de captura encontra-se entre
        dini (data inicial) e dfim (data final).
        '''
        imagens_encontradas = []
        for imagem in BDImagens.imagens:
            if dini <= imagem.data.date <= dfim:
                imagens_encontradas.append(imagem)     
        return imagens_encontradas
    
    @staticmethod
    def busca_por_cidade(cidade: str) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados
        cuja cidade de captura é cidade.
        '''
        imagens_encontradas = []
        for imagem in BDImagens.imagens:
            if cidade.lower() in imagem._cidade.lower():
                imagens_encontradas.append(imagem)
        return imagens_encontradas

    @staticmethod
    def busca_por_pais(pais: str) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados
        cujo país de captura é pais.
        '''
        imagens_encontradas = []
        for imagem in BDImagens.imagens:
            if pais.lower() in imagem._pais.lower():
                imagens_encontradas.append(imagem)
        return imagens_encontradas

# def main():

#     bd = BDImagens('dataset1/index')
#     bd.processa()

#     # Mostra as informações de todas as imagens do banco de dados
#     print('Imagens do Banco de Dados:')
#     for img in bd.todas():
#         img.imprime_info()

#     # Mostra os nomes das imagens que possuam texto no seu nome
#     texto = '06'
#     for img in bd.busca_por_nome(texto):
#         print(img.nome)

#     # Mostra as datas das imagens capturadas entre d1 e d2
#     d1 = datetime(2021, 1, 1)
#     d2 = datetime(2023, 1, 1)
#     for img in bd.busca_por_data(d1, d2):
#         print(img.data)

# if __name__ == '__main__':
#     main()



    # self._lat = None # latitude da captura da imagem
    # self._lon = None # longitude da captura da imagem
    # self._cidade = None # cidade da captura da imagem
    # self._pais = None # país da captura da imagem