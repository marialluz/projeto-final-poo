from PIL.ExifTags import TAGS, GPSTAGS

'''
Obtém as tags relacionadas a Geolocalização (GPS) da imagem a partir dos metadados EXIF.

Parâmetros:
    exif: dicionário contendo metadados EXIF da imagem

Retorna:
    dicionário contendo informações de latitude e longitude
'''
def getGeotagging(exif):
    if not exif:
        raise ValueError("A imagem não possui metadados EXIF")

    geotagging = {}
    for (key, val) in exif.items():
        tag = TAGS.get(key, key)
        if tag == "GPSInfo":
            for (i, val) in val.items():
                sub_tag = GPSTAGS.get(i, i)
                geotagging[sub_tag] = val

    return geotagging

'''
Converte valores de graus, minutos e segundos para graus decimais.

Parâmetros:
    value (tuple): tupla contendo valores de graus, minutos e segundos

Retorna:
    float: valor em graus decimais
'''
def convertToDegrees(value):
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)

'''
Obtém as informações da latitude e longitude da imagem.

Parâmetros:
    geotags: dicionário contendo informações sobre a GeoLocalização da imagem

Retorna:
    tuple: tupla contendo latitude e longitude da imagem
'''
def getLatLon(geotags):
    if not geotags:
        raise ValueError("Não foi possível obter latitude e longitude")

    lat = geotags.get("GPSLatitude")
    lat_ref = geotags.get("GPSLatitudeRef")
    lon = geotags.get("GPSLongitude")
    lon_ref = geotags.get("GPSLongitudeRef")

    if lat and lat_ref and lon and lon_ref:
        
        lat_val = convertToDegrees(lat)
        lon_val = convertToDegrees(lon)

        if lat_ref != "N":
            lat_val = -lat_val
        if lon_ref != "E":
            lon_val = -lon_val
        return (lat_val, lon_val)
    else:
        raise ValueError("Não foi possível obter latitude e longitude")

def getImageDateTime(exif):
    if exif:
        for tag, value in exif.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == "DateTimeOriginal":
                return value

    return None