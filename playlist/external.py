"""
|--------------------------------------------------------------------------
| DATOS EXTERNOS (página HTML fuera de Vercel)
|--------------------------------------------------------------------------
| Consulta una página HTML, extrae de ella un array de JavaScript como:
|
|     var mt = [
|       {
|         cdn: "https://...",
|         token: "abc"
|       },
|     ];
|
| y lo convierte en una lista de diccionarios de Python:
|
|     [{'cdn': 'https://...', 'token': 'abc'}]
|
| Características:
|   - Usa cloudscraper (evita bloqueos de Cloudflare).
|   - Caché en memoria (TTL) para no consultar la página en cada petición.
|   - Si la consulta falla, usa la última lista válida (si existe).
|   - Nunca lanza excepciones hacia afuera: en el peor caso devuelve None.
"""

from __future__ import annotations

import random
import re
import sys
import time
from typing import Optional

# --------------------------------------------------------------------------
# SCRAPER (se crea una sola vez, la primera vez que se necesita)
# --------------------------------------------------------------------------
_SCRAPER = None


def GETSCRAPER():
    global _SCRAPER

    if _SCRAPER is None:
        import cloudscraper

        _SCRAPER = cloudscraper.create_scraper(
            browser={'custom': 'okhttp/4.9.2'}
        )

    return _SCRAPER


def FETCHHTML(URL: str, TIMEOUT: int = 7) -> str:
    """
    Descarga el HTML. El timeout es corto a propósito: las funciones de
    Vercel tienen un tiempo máximo de ejecución (10 s en el plan gratuito).
    """
    RESPONSE = GETSCRAPER().get(URL, timeout=TIMEOUT)
    RESPONSE.raise_for_status()
    return RESPONSE.text


# --------------------------------------------------------------------------
# PARSER: array JavaScript -> lista de diccionarios
# --------------------------------------------------------------------------
_RE_BLOCKCOMMENT = re.compile(r'/\*.*?\*/', re.DOTALL)
_RE_LINECOMMENT = re.compile(r'(?m)^\s*//.*$')
_RE_OBJECT = re.compile(r'\{(.*?)\}', re.DOTALL)
_RE_PAIR = re.compile(
    r'''["']?([A-Za-z_$][\w$]*)["']?\s*:\s*'''
    r'''(?:"((?:[^"\\]|\\.)*)"|'((?:[^'\\]|\\.)*)')'''
)


def PARSEJSARRAY(HTML: str, VARNAME: str = 'mt') -> list[dict]:
    """
    Busca  var/let/const VARNAME = [ {...}, {...} ];  dentro del HTML.

    Acepta:
      - claves con o sin comillas      ( cdn: "x"  /  "cdn": "x" )
      - valores con comillas dobles o simples
      - coma final                     ( {...}, ]
      - comentarios de línea completa  ( // {cdn: "viejo"}, ) y /* ... */

    Devuelve [] si no encuentra el array.
    """
    MATCH = re.search(
        r'\b(?:var|let|const)\s+' + re.escape(VARNAME) + r'\s*=\s*\[(.*?)\]\s*;',
        HTML,
        re.DOTALL,
    )

    if MATCH is None:
        return []

    BODY = MATCH.group(1)
    BODY = _RE_BLOCKCOMMENT.sub('', BODY)
    BODY = _RE_LINECOMMENT.sub('', BODY)

    ITEMS = []

    for OBJ in _RE_OBJECT.finditer(BODY):
        ITEM = {}

        for PAIR in _RE_PAIR.finditer(OBJ.group(1)):
            KEY = PAIR.group(1)
            VALUE = PAIR.group(2) if PAIR.group(2) is not None else PAIR.group(3)
            # Quita los escapes de JavaScript (\/ -> /, \" -> ", etc.)
            ITEM[KEY] = re.sub(r'\\(.)', r'\1', VALUE)

        if ITEM:
            ITEMS.append(ITEM)

    return ITEMS


# --------------------------------------------------------------------------
# CACHÉ + SELECCIÓN
# --------------------------------------------------------------------------
_CACHE = {'URL': None, 'TIME': 0.0, 'ITEMS': []}


def GETEXTERNALITEMS(URL: str, TTL: int = 60, VARNAME: str = 'mt') -> list[dict]:
    """
    Devuelve la lista completa de elementos del array externo.

    TTL: segundos que se reutiliza el resultado antes de volver a consultar
         (0 = consultar siempre).
    """
    NOW = time.time()

    if _CACHE['URL'] == URL and (NOW - _CACHE['TIME']) < TTL:
        return _CACHE['ITEMS']

    try:
        ITEMS = PARSEJSARRAY(FETCHHTML(URL), VARNAME)

        if not ITEMS:
            raise ValueError("no se encontró el array '" + VARNAME + "' en el HTML")

        _CACHE.update(URL=URL, TIME=NOW, ITEMS=ITEMS)

    except Exception as ERROR:
        # Se imprime en el log de Vercel. Se conserva la última lista válida
        # (si es de la misma URL) y no se reintenta hasta que venza el TTL.
        print('[EXTERNAL] Error consultando ' + URL + ': ' + repr(ERROR), file=sys.stderr)

        if _CACHE['URL'] != URL:
            _CACHE['ITEMS'] = []

        _CACHE.update(URL=URL, TIME=NOW)

    return _CACHE['ITEMS']


def GETEXTERNALITEM(
    URL: str,
    TTL: int = 60,
    REQUIRED: Optional[str] = None,
    VARNAME: str = 'mt',
) -> Optional[dict]:
    """
    Equivalente a:

        var randomIndex = Math.floor(Math.random() * mt.length);
        var selected = mt[randomIndex];

    Devuelve un elemento al azar (dict) o None si no hay ninguno válido.

    REQUIRED: nombre de una clave que debe existir y no estar vacía
              (por ejemplo 'cdn'). Los elementos que no la cumplan se ignoran.
    """
    if not URL:
        return None

    ITEMS = GETEXTERNALITEMS(URL, TTL, VARNAME)

    if REQUIRED:
        ITEMS = [ITEM for ITEM in ITEMS if ITEM.get(REQUIRED, '').strip() != '']

    if not ITEMS:
        return None

    return random.choice(ITEMS)
