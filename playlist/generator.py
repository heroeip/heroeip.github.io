"""
|--------------------------------------------------------------------------
| LIBRERÍA GENERADORA DE LISTAS M3U8
|--------------------------------------------------------------------------
| Conversión de index.php. Aquí vive SOLO la lógica; los datos (canales,
| User-Agents, referers, grupos, EPG) están en channels.py.
|
| Se conserva la convención original: funciones y variables en MAYÚSCULAS.
"""

from __future__ import annotations

import json
from typing import Any, Optional
from urllib.parse import quote


"""
|--------------------------------------------------------------------------
| UTILIDADES
|--------------------------------------------------------------------------
"""


def ESENTERO(VALUE: Any) -> bool:
    """
    En Python, bool es subclase de int (True == 1, False == 0).
    En PHP is_int(true) es false, así que hay que excluir los bool
    explícitamente para mantener el mismo comportamiento.
    """
    return isinstance(VALUE, int) and not isinstance(VALUE, bool)


def STRINGVALUE(VALUE: Any) -> Optional[str]:
    """
    Devuelve un string válido o None.

    Una cadena vacía, o compuesta solamente por espacios, se considera
    inválida.
    """
    if not isinstance(VALUE, str):
        return None

    if VALUE.strip() == '':
        return None

    return VALUE


def GETCOOKIE(VALUE: Any) -> Optional[str]:
    """
    COOKIE

    A diferencia de STRINGVALUE(), una cadena vacía ES un valor válido
    para COOKIE. Esto permite distinguir entre:

      ausencia / None / False / 0 / True / números / listas -> sin Cookie
      'COOKIE': ''                                          -> Cookie vacía
      'COOKIE': 'valor=1'                                   -> Cookie con valor

    Solamente los valores de tipo str activan la directiva Cookie.
    """
    if isinstance(VALUE, str):
        return VALUE

    return None


def ARRAYINDEX1BASED(VALUE: Any, ARRAY: list) -> Optional[str]:
    """
    Obtiene un elemento de una lista usando numeración humana:

      1 -> índice 0
      2 -> índice 1
      3 -> índice 2

    Solamente acepta enteros positivos.
    """
    if not ESENTERO(VALUE) or VALUE < 1:
        return None

    INDEX = VALUE - 1

    if INDEX >= len(ARRAY):
        return None

    return STRINGVALUE(ARRAY[INDEX])


"""
|--------------------------------------------------------------------------
| REFERER / ORIGIN
|--------------------------------------------------------------------------
| Ambos parámetros aceptan una referencia 1-based a la lista AR o una URL
| literal. REFERER genera opciones compatibles con VLC; ORIGIN genera
| propiedades stream_headers compatibles con Kodi/InputStream Adaptive.
| En ambos casos, el valor seleccionado se aplica a Referer y Origin.
"""


def GETHEADERVALUE(VALUE: Any, AR: list) -> Optional[str]:
    if ESENTERO(VALUE):
        if VALUE <= 0:
            return None
        return ARRAYINDEX1BASED(VALUE, AR)

    if isinstance(VALUE, str):
        return STRINGVALUE(VALUE)

    return None


"""
|--------------------------------------------------------------------------
| USER-AGENT
|--------------------------------------------------------------------------
|
| SIEMPRE existe un User-Agent.
|
| Válidos:
|
| ausencia / None / False / 0 / "" / valor inválido  -> UA[0] (Firefox)
|
| 1 -> UA[0]
| 2 -> UA[1]
| 3 -> UA[2]
|
| "Android 9.0"  -> "Android 9.0"
|
| True, 234, 1.5, listas, etc.  -> UA[0]
"""


def GETUA(VALUE: Any, UA: list) -> str:
    # String no vacío: se utiliza exactamente lo indicado.
    if isinstance(VALUE, str):
        VALUE = VALUE.strip()

        if VALUE != '':
            return VALUE

        return UA[0]

    # Entero positivo: referencia a la lista con numeración 1-based.
    if ESENTERO(VALUE) and VALUE > 0:
        RESULT = ARRAYINDEX1BASED(VALUE, UA)

        if RESULT is not None:
            return RESULT

        return UA[0]

    # False, None, 0, True, negativos, floats, listas, etc.
    # Todo cae al modo a prueba de fallos.
    return UA[0]


"""
|--------------------------------------------------------------------------
| GROUP
|--------------------------------------------------------------------------
|
| 1, 2, 3...                  -> GL[0], GL[1], GL[2]... (numeración humana)
| string no vacío             -> grupo indicado directamente
| True                        -> General
| False / None / 0 / ausencia -> sin group-title
| entero positivo fuera de GL -> sin group-title
| otros tipos inválidos       -> sin group-title
"""


def GETGROUP(VALUE: Any, GL: list) -> Optional[str]:
    # True significa explícitamente el grupo General.
    # (Debe evaluarse antes que los enteros: True es un int en Python.)
    if VALUE is True:
        return 'General'

    # False y None significan que no pertenece a ningún grupo.
    if VALUE is False or VALUE is None:
        return None

    # Entero positivo: GROUP 4 equivale a GL[3].
    if ESENTERO(VALUE):
        return ARRAYINDEX1BASED(VALUE, GL)

    # String no vacío: se utiliza literalmente como nombre del grupo.
    if isinstance(VALUE, str):
        return STRINGVALUE(VALUE)

    return None


"""
|--------------------------------------------------------------------------
| LICENSE KEY
|--------------------------------------------------------------------------
| Formato único: KID:KEY,KID2:KEY2
| Se eliminan comillas dobles accidentales.
"""


def PARSELICENSEKEY(KEY: str) -> dict:
    KEY = KEY.replace('"', '').strip()
    RESULT: dict = {}

    for PAIR in KEY.split(','):
        PARTS = PAIR.strip().split(':', 1)

        if len(PARTS) != 2:
            continue

        KID = PARTS[0].strip()
        KEYVALUE = PARTS[1].strip()

        if KID != '' and KEYVALUE != '':
            RESULT[KID] = KEYVALUE

    return RESULT


"""
|--------------------------------------------------------------------------
| DRM
|--------------------------------------------------------------------------
|
| KEY solamente activa DRM si es un string no vacío.
|
| False / None / 0 / True / números / listas  -> sin DRM
|
| Devuelve una lista de líneas (vacía si no hay DRM).
"""


def DRM(CHANNEL: dict, KODI: bool) -> list[str]:
    KEY = STRINGVALUE(CHANNEL.get('KEY'))

    if KEY is None:
        return []

    KEYS = PARSELICENSEKEY(KEY)

    if not KEYS:
        return []

    if KODI:
        PAIRS = [KID + ':' + KEYVALUE for KID, KEYVALUE in KEYS.items()]

        return [
            '#KODIPROP:inputstream=inputstream.adaptive',
            '#KODIPROP:inputstream.adaptive.drm_legacy=org.w3.clearkey|'
            + ','.join(PAIRS),
        ]

    if len(KEYS) == 1:
        KID, KEYVALUE = next(iter(KEYS.items()))
        LICENSE = KID + ':' + KEYVALUE
    else:
        # Sin espacios, igual que json_encode() de PHP.
        LICENSE = json.dumps(KEYS, separators=(',', ':'))

    return [
        '#KODIPROP:inputstream.adaptive.license_type=clearkey',
        '#KODIPROP:inputstream.adaptive.license_key=' + LICENSE,
    ]


"""
|--------------------------------------------------------------------------
| KODI URL
|--------------------------------------------------------------------------
|
| Kodi recibe los headers dentro de la URL (URL|Header=valor&Header=valor).
| Solamente se agregan los que realmente existen.
|
| Referer y Origin se emiten como directivas en EXT; no se duplican aquí.
"""


def KODIURL(URL: str, AGENT: str, COOKIE: Optional[str]) -> str:
    PARAMS = []

    # User-Agent siempre existe.
    # quote(..., safe='') equivale a rawurlencode() de PHP.
    PARAMS.append('User-Agent=' + quote(AGENT, safe=''))

    if COOKIE is not None:
        PARAMS.append('http-cookie=' + quote(COOKIE, safe=''))

    return URL + '|' + '&'.join(PARAMS)


"""
|--------------------------------------------------------------------------
| EXT
|--------------------------------------------------------------------------
|
| Construye el bloque de información de un canal.
| Devuelve None si el canal es inválido (sin NAME o sin URL).
"""


def EXT(
    CHANNEL: dict,
    KODI: bool,
    UA: list,
    AR: list,
    GL: list,
) -> Optional[str]:

    # NAME y URL son obligatorios.
    NAME = STRINGVALUE(CHANNEL.get('NAME'))
    if NAME is None:
        return None

    URL = STRINGVALUE(CHANNEL.get('URL'))
    if URL is None:
        return None

    # Opcionales.
    GROUP = GETGROUP(CHANNEL.get('GROUP'), GL)
    ID = STRINGVALUE(CHANNEL.get('ID'))
    ICON = STRINGVALUE(CHANNEL.get('ICON'))

    # REFERER: formato VLC (#EXTVLCOPT).
    # ORIGIN: formato moderno Kodi/InputStream Adaptive (#KODIPROP).
    REFERER = GETHEADERVALUE(CHANNEL.get('REFERER'), AR)
    ORIGIN = GETHEADERVALUE(CHANNEL.get('ORIGIN'), AR)

    # AGENT: siempre termina teniendo un valor.
    AGENT = GETUA(CHANNEL.get('AGENT'), UA)

    # COOKIE: solamente se utiliza si el valor es de tipo str.
    # Una cadena vacía ('') es válida y genera explícitamente
    # http-cookie= / Cookie=.
    COOKIE = GETCOOKIE(CHANNEL.get('COOKIE'))

    # Primera línea EXTINF.
    EXTINF = '#EXTINF:-1'

    if ID is not None:
        EXTINF += ' tvg-id="' + ID + '"'

    if ICON is not None:
        EXTINF += ' tvg-logo="' + ICON + '"'

    if GROUP is not None:
        EXTINF += ' group-title="' + GROUP + '"'

    EXTINF += ',' + NAME

    LINES = [EXTINF]

    # User-Agent + opciones VLC obligatorias (SIEMPRE salen).
    LINES.append('#EXTVLCOPT:network-caching=1000')
    LINES.append('#EXTVLCOPT:http-user-agent=' + AGENT)
    LINES.append('#EXTVLCOPT:http-reconnect=true')

    # COOKIE (VLC).
    if COOKIE is not None:
        LINES.append('#EXTVLCOPT:http-cookie=' + COOKIE)

    # COOKIE para Kodi: header de stream, además del http-cookie
    # que se agrega a la URL mediante KODIURL().
    if KODI and COOKIE is not None:
        LINES.append('#KODIPROP:inputstream.adaptive.stream_headers=cookie=' + COOKIE)

    # Compatibilidad de encabezados (se mantienen independientes para
    # poder elegir el formato por canal):
    # - REFERER => directivas VLC http-referrer y http-origin.
    # - ORIGIN  => propiedades Kodi stream_headers referer y origin.
    if REFERER is not None:
        LINES.append('#EXTVLCOPT:http-referrer=' + REFERER)
        LINES.append('#EXTVLCOPT:http-origin=' + REFERER)

    if ORIGIN is not None:
        LINES.append('#KODIPROP:inputstream.adaptive.stream_headers=referer=' + ORIGIN)
        LINES.append('#KODIPROP:inputstream.adaptive.stream_headers=origin=' + ORIGIN)

    # DRM.
    LINES.extend(DRM(CHANNEL, KODI))

    # URL.
    if KODI:
        LINES.append(KODIURL(URL, AGENT, COOKIE))
    else:
        LINES.append(URL)

    return '\n'.join(LINES)


"""
|--------------------------------------------------------------------------
| GENERADOR M3U
|--------------------------------------------------------------------------
"""


def GENERATEM3U(
    CHANNELS: list,
    KODI: bool,
    EPG: str,
    UA: list,
    AR: list,
    GL: list,
) -> str:

    # Primera etiqueta: #EXTM3U url-tvg=...
    OUTPUT = '#EXTM3U url-tvg="' + EPG + '"\n\n'

    BLOCKS = []

    for CHANNEL in CHANNELS:
        if not isinstance(CHANNEL, dict):
            continue

        BLOCK = EXT(CHANNEL, KODI, UA, AR, GL)

        # Canal inválido: simplemente se ignora.
        if BLOCK is None:
            continue

        BLOCKS.append(BLOCK)

    # Línea en blanco entre canales.
    return OUTPUT + '\n\n'.join(BLOCKS) + '\n'
