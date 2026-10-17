import sys
from pathlib import Path

# Permite importar el paquete "playlist" que está en la raíz del proyecto
# (fuera de api/, para que Vercel no lo trate como una función más).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, Response, request

from playlist.channels import EPG, UA, AR, GL, GETCHANNELS
from playlist.generator import GENERATEM3U

app = Flask(__name__)


def RESPONDER(KODI: bool) -> Response:
    """Genera la lista M3U8 y la devuelve con las cabeceras originales."""
    BODY = GENERATEM3U(GETCHANNELS(), KODI, EPG, UA, AR, GL)

    return Response(
        BODY,
        content_type='application/vnd.apple.mpegurl; charset=utf-8',
        headers={
            'Content-Disposition': 'inline; filename="playlist.m3u8"',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
        },
    )


# Lista normal (VLC, etc.).
# También acepta ?kodi para mantener compatibilidad con el index.php original.
@app.route('/')
@app.route('/index.m3u8')
def DEFAULT_M3U():
    return RESPONDER('kodi' in request.args)


# Lista para Kodi.
@app.route('/kodi')
@app.route('/kodi.m3u8')
def KODI_M3U():
    return RESPONDER(True)


# IMPORTANTE para Vercel: NO usar app.run()
