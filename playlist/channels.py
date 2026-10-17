"""
|--------------------------------------------------------------------------
| CONFIGURACIÓN Y DATOS (conversión de index_channels.php)
|--------------------------------------------------------------------------
| Aquí solo van datos. La lógica está en generator.py y external.py.
|
| Valores PHP -> Python:  FALSE -> False | TRUE -> True | NULL -> None
|
| Para agregar un canal: copia un bloque { ... } dentro de GETCHANNELS().
| Solo NAME y URL son obligatorios; el resto es opcional.
"""

from playlist.external import GETEXTERNALITEM

# --------------------------------------------------------------------------
# EPG
# --------------------------------------------------------------------------
EPG = 'https://raw.githubusercontent.com/Puticastillo/EPGCL/refs/heads/main/smithers/guia-de-programacion.xml,https://www.open-epg.com/files/uruguay2.xml,https://www.open-epg.com/files/argentina.xml'

# --------------------------------------------------------------------------
# PÁGINA EXTERNA (direcciones que cambian)
#
# EXTERNAL        -> URL de la página HTML que contiene el array JavaScript:
#                        var mt = [ { cdn: "...", token: "..." }, ];
#                    Si se deja vacía (''), no se consulta nada.
# EXTERNAL_CACHE  -> segundos que se reutiliza la respuesta antes de volver
#                    a consultar la página (0 = consultar en cada petición).
# CDN_DEFAULT     -> CDN de respaldo si la página no responde y todavía no
#                    hay ninguna respuesta válida guardada. '' = sin respaldo
#                    (los canales que usan CDN se omiten de la lista).
# --------------------------------------------------------------------------
EXTERNAL = 'https://bestleague.life/tok.html'
EXTERNAL_CACHE = 60
CDN_DEFAULT = ''

# --------------------------------------------------------------------------
# USER-AGENTS DISPONIBLES
#
# Se cuentan desde 1:
#
#   'AGENT': 1  -> UA[0]
#   'AGENT': 2  -> UA[1]
#   'AGENT': 'Android 9.0'  -> texto literal
#
# Si AGENT es inválido, vacío, False, None, 0, etc.,
# se utiliza SIEMPRE el primer User-Agent:
#
#   UA[0] = Firefox
# --------------------------------------------------------------------------
UA = [
	'Firefox',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
	'AivAndroidPlayer/1.0 (AndroidDevice)',
	'dgo/4.48.0 (Android; Android 7.1.2; Asus; ASUS_Z01QD) ExoPlayer/2.19.1'
]

# --------------------------------------------------------------------------
# REFERER / ORIGIN DISPONIBLES
#
# Se cuentan desde 1 para seleccionar una entrada de AR:
#
#   'REFERER': 2  -> Directivas VLC:  http-referrer y http-origin.
#   'ORIGIN':  4  -> Kodi:            stream_headers referer y origin.
#
# También aceptan una URL literal: 'REFERER': 'https://sitio.com/'
#
# Ambos parámetros aplican el valor elegido tanto a Referer como a Origin.
# Añade aquí las URLs que necesites; las entradas vacías no generan headers.
# --------------------------------------------------------------------------
AR = [
	'https://portal.app.flow.com.ar',
	'https://www.izzigo.tv/'

]

# --------------------------------------------------------------------------
# COOKIE
# Opcional por canal. Solamente un STRING activa la Cookie:
#
#   'COOKIE': 'valor=1; num=0'   -> Cookie con valor
#   'COOKIE': ''                 -> Cookie presente pero vacía
#   'COOKIE': False / None / 0   -> sin Cookie
#   'COOKIE': True / 4 / lista   -> sin Cookie
#
# Una Cookie vacía se utiliza tanto para VLC como para Kodi y genera
# explícitamente http-cookie= / Cookie=.
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# DRM (opcional por canal)
#
#   'KEY': 'KID:KEY'              -> una clave ClearKey
#   'KEY': 'KID:KEY,KID2:KEY2'    -> varias claves
#   'KEY': None / False / ''      -> sin DRM
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# GROUP LABELS
#
# 'GROUP': 7        -> GL[6] ('PELICULAS')
# 'GROUP': 'Otro'   -> texto literal
# 'GROUP': True     -> 'General'
# 'GROUP': False / None / ausente -> sin group-title
# --------------------------------------------------------------------------
GL = [
    'LOCALES',          # 1
    'NACIONALES',       # 2
    'NOTICIAS',         # 3
    'DEPORTES',         # 4
    'FUTBOL PREMIUM',   # 5
    'LPF PLAY',         # 6
    'PELICULAS',        # 7
    'CINE PREMIUM',     # 8
    'DOCUMENTALES',     # 9
    'ESTILO DE VIDA',   # 10
    'MUSICA',           # 11
    'INTERNACIONAL',    # 12
]


# --------------------------------------------------------------------------
# CANALES
#
# Es una función (y no una lista fija) para que se evalúe en CADA petición:
# así la consulta a la página externa y la elección al azar se repiten,
# en vez de quedar "congeladas" mientras Vercel mantiene la instancia activa.
# --------------------------------------------------------------------------
def GETCHANNELS() -> list:

    # ----------------------------------------------------------------------
    # Equivalente al JavaScript:
    #
    #   var randomIndex = Math.floor(Math.random() * mt.length);
    #   var selected = mt[randomIndex];
    #   CDN = selected.cdn;
    #
    # Solo se consideran los elementos con 'cdn' no vacío.
    # ----------------------------------------------------------------------
    SELECTED = GETEXTERNALITEM(EXTERNAL, EXTERNAL_CACHE, REQUIRED='cdn') or {}

    CDN = SELECTED.get('cdn', CDN_DEFAULT)
    TOKEN = SELECTED.get('token', '')
    URL = 'https://' + CDN + '.cvattv.com.ar/' + TOKEN;

    return [

        # ------------------------------------------------------------------
        # EJEMPLO con CDN externo (descomentar y adaptar).
        # Si CDN está vacío, 'URL' queda en None y el canal se omite solo.
        # TOKEN también está disponible, por ejemplo:
        #   CDN + '/live/playlist.m3u8?token=' + TOKEN
        # ------------------------------------------------------------------
        # {
        #     'NAME':  'CANAL CON CDN',
        #     'GROUP': 7,
        #     'URL':   CDN + '/live/playlist.m3u8' if CDN else None,
        # },



# ------------------------------------------------------------------
# PELICULAS
# ------------------------------------------------------------------

{
	'NAME'  : 'BAYRES',
	'ID'    : False,
	'GROUP' : 7,
	'ICON'  : 'logo/Bayres_1.png',
	'URL'   : 'https://streaming01.mikrolive.tv/bayrestv/live/playlist.m3u8',
	'KEY'   : None,
	'AGENT' : 2,

},
	
{
	'NAME'  : 'COSMOS',
	'GROUP' : 7,
	'ICON'  : 'logo/Cosmos_1.png',
	'URL'   : 'https://tv.mediacp.eu:19360/cosmos/cosmos.m3u8'
},

{
	'NAME'  : 'SONY CINE',
	'GROUP' : 7,
	'ICON'  : 'logo/SonyCine_1.png',
	'URL'   : 'https://a-cdn.klowdtv.com/live1/cine_720p/playlist.m3u8'
},

{
	'NAME'  : 'GOLDEN EDGE',
	'ID'    : 'Golden Edge.ar',
	'GROUP' : 7,
	'ICON'  : 'logo/GoldenEdge_1.png',
	'URL'   : 'https://live-pv-ta.amazon.fastly-edge.com/iad-nitro/live/clients/dash/enc/xv3tnoayi8/out/v1/46aaaeb778de4cd39893d88a7f93b05a/cenc.mpd',
	'KEY'    : 'ae4cbc34d4b1645f6c7b26410dde7b58:647478cd3bd0dfb3e820249296c23096',
	'REFERER': 'https://www.primevideo.com/',
	'AGENT'  : 2,
},

{
	'NAME'  : 'GOLDEN PLUS',
	'ID'    : 'GOLDEN PLUS',
	'GROUP' : 7,
	'ICON'  : 'logo/GoldenPlus_1.png',
	'URL'   : 'https://live-pv-ta.amazon.fastly-edge.com/iad-nitro/live/clients/dash/enc/o09knwldwh/out/v1/15f9f74c888e4fdd9815ea94635ae4db/cenc.mpd',
	'KEY'    : 'ed5849d33e07606d6118d7fb26b90cd0:63670e57e70353ca526fb07a8d7ddb7b',
	'REFERER': 'https://www.primevideo.com/',
	'AGENT'  : 2,
},

{
	'NAME'  : 'GOLDEN PREMIER',
	'ID'    : 'GOLDEN PREMIER',
	'GROUP' : 7,
	'ICON'  : 'logo/GoldenPremier_1.png',
	'URL'   : 'https://live-pv-ta.amazon.fastly-edge.com/gru-nitro/live/clients/dash/enc/1pyrprmguo/out/v1/e63748f718754f6ca76df9ce757b10f5/cenc.mpd',
	'KEY'    : 'b39fdb1efc89fa2b791bdce8428c3e09:1941081db257b29643c95783d3a2c5cd',
	'REFERER': 'https://www.primevideo.com/',
	'AGENT'  : 2,
},

{
	'NAME'  : 'GOLDEN',
	'ID'    : 'Golden.ar',
	'GROUP' : 7,
	'ICON'  : 'logo/Golden_1.png',
	'URL'   : URL + '/live/c6eds/Golden/SA_Live_dash_enc/Golden.mpd',
	'KEY'    : 'f6cd784e5b53208261dd81a345908400:b125fd77d7d88752dc045e57edcf9943',
	'ORIGIN' : 1,
},

{
	'NAME'  : 'CINECANAL',
	'ID'    : 'Cinecanal HD.uy',
	'GROUP' : 7,
	'ICON'  : 'logo/CineCanal.png',
	'URL'   : URL + '/live/c3eds/CinecanalHD/SA_Live_dash_enc/CinecanalHD.mpd',
	'KEY'    : '98b31a0a125d81ef4c9caf1683f55444:7ec3df0771fe86c9f405765ce9fb5204',
	'ORIGIN' : 1,
},

{
	'NAME'  : 'CINEMAX',
	'ID'    : 'Cinemax HD.uy',
	'GROUP' : 7,
	'ICON'  : 'logo/Cinemax.png',
	'URL'   : URL + '/live/c6eds/Cinemax/SA_Live_dash_enc/Cinemax.mpd',
	'KEY'    : 'fd84db183866916b15366b4852e68da8:1201b1f0ed299a46ddffabb5c8553793',
	'ORIGIN' : 1,
},

{
	'NAME'  : 'STUDIO',
	'ID'    : 'Studio Universal HD.uy',
	'GROUP' : 7,
	'ICON'  : 'logo/Studio.png',
	'URL'   : URL + '/live/c6eds/Studio_Universal/SA_Live_dash_enc/Studio_Universal.mpd',
	'KEY'    : 'dbe5d9ce01740076fdc95cbc0253b9ee:d8a8ef434bffae80e45e203f6f7f4988',
	'ORIGIN' : 1,
},

{
	'NAME'  : 'AMC',
	'ID'    : 'AMC HD.uy',
	'GROUP' : 7,
	'ICON'  : 'logo/Amc.png',
	'URL'   : URL + '/live/c3eds/AMC/SA_Live_dash_enc/AMC.mpd',
	'KEY'    : '30ffe7a2776537e8cec7020d783536f9:7b4f323576ac85d8938f5bebc245131c',
	'ORIGIN' : 1,
},

{
	'NAME'  : 'TNT',
	'ID'    : 'TNT.ar',
	'GROUP' : 7,
	'ICON'  : 'logo/Tnt.png',
	'URL'   : URL + '/live/c3eds/TNT_HD_Arg/SA_Live_dash_enc/TNT_HD_Arg.mpd',
	'KEY'    : '61d9873e1f281cd0223acce773cc08b0:3dda0d89ece37c244ed8cb7e90153555',
	'ORIGIN' : 1,
},

{
	'NAME'  : 'SPACE',
	'ID'    : 'Space HD.uy',
	'GROUP' : 7,
	'ICON'  : 'logo/Space.png',
	'URL'   : URL + '/live/c3eds/Space/SA_Live_dash_enc/Space.mpd',
	'KEY'    : '32684b675439d127a5ab1e07b2a57242:e169f625df475d6d1c014cca1a52a251',
	'ORIGIN' : 1,
},

{
	'NAME'  : 'SONY MOVIES',
	'ID'    : 'Sony Movies.uy',
	'GROUP' : 7,
	'ICON'  : 'logo/SonyMovies_1.png',
	'URL'   : URL + '/live/c7eds/Sony_Movies/SA_Live_dash_enc/Sony_Movies.mpd',
	'KEY'    : 'f76233e56d5102867c2bc5418871ad07:16b38f0f7a797b3bb87983ebf5879814',
	'ORIGIN' : 1,
},

{
	'NAME'  : 'FX',
	'ID'    : 'FX.ar',
	'GROUP' : 7,
	'ICON'  : 'logo/Fx.png',
	'URL'   : URL + '/live/c3eds/FXHD/SA_Live_dash_enc/FXHD.mpd',
	'KEY'    : '78a17258be5ca72ec3bc362aeb976816:31c188361f6431cf4dfb5c176870b4e9',
	'ORIGIN' : 1,
},

{
	'NAME'  : 'DHE',
	'ID'    : 'DHE.ar',
	'GROUP' : 7,
	'ICON'  : 'logo/Dhe.png',
	'URL'   : URL + '/live/c7eds/DHE/SA_Live_dash_enc/DHE.mpd',
	'KEY'    : '7650ddfb5362bb721625873d246b71cc:51c2839183b1f5056d94fe0b75e44662',
	'ORIGIN' : 1,
},

{
	'NAME'  : 'EUROPA',
	'ID'    : 'Europa Europa HD.uy',
	'GROUP' : 7,
	'ICON'  : 'logo/Europa.png',
	'URL'   : URL + '/live/c6eds/Europa_Europa/SA_Live_dash_enc/Europa_Europa.mpd',
	'KEY'    : '8bd459a9144057b023f993e54e27775e:02a88246e1dc82d2aea02d131f3312e2',
	'ORIGIN' : 1,
},



# ------------------------------------------------------------------
# LOCALES
# ------------------------------------------------------------------
	
{
	'NAME'   : '4 JUJUY',
	'ICON'   : 'logo/C4Juy.png',
	'GROUP'  : 1,
	'URL'    : 'https://5cd577a3dd8ec.streamlock.net/CANAL4/smil:CANAL4.smil/playlist.m3u8',
	'ORIGIN' : 'https://canal4jujuy.elcuatro.com'
},

{
	'NAME'  : '7 JUJUY',
	'ICON'  : 'logo/C7Juy.png',
	'GROUP' : 1,
	'URL'   : 'https://stream.arcast.live/canal7jujuy/ngrp:canal7jujuy_all/playlist.m3u8'
},

{
	'NAME'   : 'MULTIVISION',
	'ICON'   : 'logo/mv.png',
	'GROUP'  : 1,
	'URL'    : 'https://videostream.shockmedia.com.ar/hls/multivisionfederal/multivisionfederal.m3u8',
	'ORIGIN' : 'https://multivision.tv'
},

{
	'NAME'   : 'EL 10 SALTA',
	'ICON'   : 'logo/C10Sal_1.png',
	'GROUP'  : 1,
	'URL'    : 'https://el10tvstream.digitalnoa.com.ar/memfs/accd8bcb-61b0-416b-bf02-0245cb8267f6.m3u8',
	'ORIGIN' : 'https://el10tvstream.digitalnoa.com.ar/'
},

{
	'NAME'   : '11 SALTA',
	'ICON'   : 'logo/TVLitoral.png',
	'GROUP'  : 1,
	'URL'    : 'https://kickpy.vercel.app/play/eloncetv/index.m3u8',
	'REFERER': 'https://kick.com/'
},

{
	'NAME'  : '7 SALTA',
	'ICON'  : 'logo/C7Sal.png',
	'GROUP' : 'LOCALES',
	'URL'   : 'https://vivo.solumedia.com:19360/canal7salta/canal7salta.m3u8'
},

{
	'NAME'   : 'MILENIUM',
	'ICON'   : 'logo/Milenium.png',
	'GROUP'  : 1,
	'URL'    : 'https://milenium.alfasocialmedia.com.ar/live/milenium/index.m3u8',
	'ORIGIN' : 'https://mileniumtv.com.ar'
},

{
	'NAME'   : 'NEOX SALTA',
	'ICON'   : 'logo/Milenium.png',
	'GROUP'  : 1,
	'URL'    : 'https://tv.streamcasthd.com:3031/live/neoxtvlive.m3u8',
	'ORIGIN' : 'https://sonicaargentina.com.ar'
},

{
	'NAME'   : 'ORBE 21',
	'ICON'   : 'logo/Orbe.png',
	'GROUP'  : 1,
	'URL'    : 'https://stream.arcast.net:4443/canal21/ngrp:canal21_all/playlist.m3u8',
	'REFERER': 'https://arcast.net/'
},

{
	'NAME'   : 'EWTN',
	'ICON'   : 'logo/EWTN_1.png',
	'GROUP'  : 1,
	'URL'    : 'https://cdn3.wowza.com/1/SmVrQmZCUXZhVDgz/b3J3MFJv/hls/live/playlist.m3u8',
	'REFERER': 'https://www.ewtn.com'
},



# ------------------------------------------------------------------
# NOTICIAS
# ------------------------------------------------------------------

{
	'NAME'   : 'A24 LOCAL',
	'ID'     : 'A24.ar',
	'ICON'   : 'logo/A24_1.png',
	'GROUP'  : 3,
	'URL'    : 'https://g3.vxral-hor.transport.edge-access.net/a15/ngrp:a24-100056_all/Playlist.m3u8?sense=true',
	'REFERER': 'https://vmf.edge-apps.net',
	'AGENT'  : 'iPhone;Chrome'
},

{
	'NAME'   : 'TN LOCAL',
	'ID'     : 'TN.ar',
	'ICON'   : 'logo/TN_1.png',
	'GROUP'  : 3,
	'COOKIE' : '',
	'URL'    : 'https://live-01-01-tn.vodgc.net/TN_DAI_Beta/index_TN_DAI_Beta_1080.m3u8',
	'REFERER': 'https://tn.com.ar/',
	'AGENT'  : 1
},

{
	'NAME'   : 'PERFIL LOCAL',
	'ID'     : 'Perfil.ar',
	'ICON'   : 'logo/Perfil_1.png',
	'GROUP'  : 3,
	'URL'    : 'https://unlimited1-saopaulo.dps.live/perfiltv/perfiltv.smil/playlist.m3u8',
	'REFERER': 'https://rudo.video',
},

{
	'NAME'   : 'DW LOCAL',
	'ID'     : 'DWEspanol.de',
	'ICON'   : 'logo/DW.png',
	'GROUP'  : 3,
	'URL'    : 'https://dwamdstream104.akamaized.net/hls/live/2015530/dwstream104/index.m3u8',
	'REFERER': 'https://www.dw.com',
},

{
	'NAME'   : 'RT LOCAL',
	'ID'     : 'RTenEspanol.ru',
	'ICON'   : 'logo/Rt.png',
	'GROUP'  : 3,
	'URL'    : 'https://rt-esp.rttv.com/dvr/rtesp/playlist.m3u8',
	'REFERER': 'https://actualidad-rt.com',
},

{
	'NAME'   : 'LN',
	'ID'     : 'LaNacion+.ar',
	'ICON'   : 'logo/LN.png',
	'GROUP'  : 3,
	'URL'    : URL + '/live/c7eds/La_Nacion/SA_Live_dash_enc/La_Nacion.mpd',
	'KEY'    : '3561945a15a88603aee20ea15c605d6c:7a1676bb6cc6cbb328f41626d8084594',
	'ORIGIN' : 1
},

{
	'NAME'   : 'C5N',
	'ID'     : 'C5N.ar',
	'ICON'   : 'logo/C5N_1.png',
	'GROUP'  : 3,
	'URL'    : URL + '/live/c7eds/C5N/SA_Live_dash_enc/C5N.mpd',
	'KEY'    : 'ef98ad3a4a5b9f6edae885e8bf450d3c:861873c6c69eb66df0afc3034a02a796',
	'ORIGIN' : 1
},

{
	'NAME'   : 'AR12',
	'ID'     : 'Ar12.ar',
	'ICON'   : 'logo/Ar12_1.png',
	'GROUP'  : 3,
	'URL'    : URL + '/live/c7eds/Investigacion_Periodistica/SA_Live_dash_enc/Investigacion_Periodistica.mpd',
	'KEY'    : '723d8d918d61cee1f708ec849b6498a2:b4b48cfccc1cddcc73bc7a7df46cb531',
	'ORIGIN' : 1
},

{
	'NAME'   : 'CRONICA',
	'ID'     : 'CronicaTV.ar',
	'ICON'   : 'logo/Cronica2.png',
	'GROUP'  : 3,
	'URL'    : URL + '/live/c7eds/CronicaTV/SA_Live_dash_enc/CronicaTV.mpd',
	'KEY'    : '33ded37fefaa6c3d6878e0d555dfaffd:9e024c10af20f240a1ea35b94d147f28',
	'ORIGIN' : 1
},

{
	'NAME'   : 'PERFIL',
	'ID'     : 'Perfil.ar',
	'ICON'   : 'logo/Perfil.png',
	'GROUP'  : 3,
	'URL'    : URL + '/live/c7eds/Canal_Economico/SA_Live_dash_enc/Canal_Economico.mpd',
	'KEY'    : '2bbbc95ef2db831cab99b3bc29f96e14:f3755517e66c2bf8af9e7dda33a7c9ab',
	'ORIGIN' : 1
},

{
	'NAME'   : 'A24',
	'ID'     : 'A24.ar',
	'ICON'   : 'logo/A24.png',
	'GROUP'  : 3,
	'URL'    : URL + '/live/c7eds/America24/SA_Live_dash_enc/America24.mpd',
	'KEY'    : '71133ea8e1941323a21acb5090c5c469:f46178e47581d410008a505eeed759fe',
	'ORIGIN' : 1
},

{
	'NAME'   : 'TN',
	'ID'     : 'TN.ar',
	'ICON'   : 'logo/TN.png',
	'GROUP'  : 3,
	'URL'    : URL + '/live/c7eds/TodoNoticias/SA_Live_dash_enc/TodoNoticias.mpd',
	'KEY'    : '775d4113d76beac8231e92ed732e27d6:0854a56be655bfa9055ef0e4980f4674',
	'ORIGIN' : 1
},

{
	'NAME'   : 'DNEWS',
	'ID'     : 'DNews.ar',
	'ICON'   : 'logo/DNews_1.png',
	'GROUP'  : 3,
	'URL'    : URL + '/live/c7eds/DNews/SA_Live_dash_enc/DNews.mpd',
	'KEY'    : '5dcaeaa309c8d828c7731c7877158a92:423e96f5f1199b026cbab4a7521e0591',
	'ORIGIN' : 1
},



# ------------------------------------------------------------------
# MUSICA
# ------------------------------------------------------------------

{
	'NAME'   : 'MUSIC TOP',
	'ID'     : 'MusicTop.ar',
	'ICON'   : 'logo/Musictop.png',
	'GROUP'  : 11,
	'URL'    : 'https://g1.proy-hor.transport.edge-access.net/a01/ngrp:musictop-100188_all/Playlist.m3u8?sense=true',
	'REFERER': 'https://vmf.edge-apps.net',
},

{
	'NAME'   : 'MTV CLASSIC',
	'ID'     : 'MTVClassic.us@East',
	'ICON'   : 'logo/MTVClassic-1.png',
	'GROUP'  : 11,
	'URL'    : 'https://jmp2.uk/plu-66a11a21a79dea0008aa90ca.m3u8',
	'REFERER': 'https://pluto.tv',
},

{
	'NAME'   : 'RADIOCITY',
	'ICON'   : 'logo/RadioCityJuy.png',
	'GROUP'  : 11,
	'URL'    : 'https://5cd577a3dd8ec.streamlock.net/CANAL4P/_definst_/stream/playlist.m3u8',
	'ORIGIN' : 'https://www.radiocityfm.com'
},

{
	'NAME'   : 'RADIOFIESTA',
	'ICON'   : 'https://www.radiofiestafm.com.ar/images/header-rf-logo.png',
	'GROUP'  : 11,
	'URL'    : 'https://5cd577a3dd8ec.streamlock.net/RADIOFIESTA/_definst_/stream/playlist.m3u8',
	'ORIGIN' : 'https://www.radiofiestafm.com.ar'
},

{
	'NAME'   : 'POWER',
	'ID'     : 'RadioPowerPinamar',
	'ICON'   : 'logo/RadioPower_1.png',
	'GROUP'  : 11,
	'URL'    : 'https://live2.tensila.com/1-1-1.power-tv/hls/live/mystream.m3u8',
	'REFERER': 'https://www.radiopower.com.ar/',
},

{
	'NAME'   : 'LN +MUSICA',
	'ID'     : 'LaNacionPlus.ar',
	'ICON'   : 'https://masmusica.lanacion.com.ar/assets/img/logo-masmusica.png',
	'GROUP'  : 11,
	'URL'    : 'https://twitchpy.vercel.app/play/lanacionmusica/index.m3u8',
	'REFERER': 'https://www.twitch.tv'
},

{
	'NAME'   : 'ROCK & POP',
	'ID'     : 'RockAndPop.ar',
	'ICON'   : 'logo/FMRock&Pop.png',
	'GROUP'  : 11,
	'URL'    : 'https://twitchpy.vercel.app/play/fmrockandpop/index.m3u8',
	'REFERER': 'https://www.twitch.tv'
},

{
	'NAME'   : 'LA 100',
	'ID'     : 'La100.ar@SD',
	'ICON'   : 'logo/FM100.png',
	'GROUP'  : 11,
	'URL'    : 'https://mdstrm.com/live-stream-playlist/68b74fd1d6512526f1f7c75a.m3u8',
},

{
	'NAME'   : 'HTV',
	'ID'     : 'HTV.ar',
	'ICON'   : 'logo/HTV.png',
	'GROUP'  : 11,
	'URL'    : URL + '/live/c6eds/HTV/SA_Live_dash_enc/HTV.mpd',
	'KEY'    : '3d29ee7a67ff04156c6cb56b90cb5d0e:95139c5421574247ced3d0a10d3bbe12',
	'ORIGIN' : 1
},

{
	'NAME'   : 'CM',
	'ID'     : 'CanaldelaMusica.ar',
	'ICON'   : 'logo/CM.png',
	'GROUP'  : 11,
	'URL'    : URL + '/live/c6eds/CM/SA_Live_dash_enc/CM.mpd',
	'KEY'    : 'eb0b25b83dfe576856ca30ff55e6dfd6:30380b34a4de53bc0b3edcf9f2c6abe2',
	'ORIGIN' : 1
},

{
	'NAME'   : 'TIERRAMIA',
	'ID'     : 'TierraMiaTV.ar',
	'ICON'   : 'logo/Tierramia.png',
	'GROUP'  : 11,
	'URL'    : 'https://g4.vxral-hor.transport.edge-access.net/a06/ngrp:tierramiatv-100188_all/Playlist.m3u8?sense=true',
	'REFERER': 'https://vmf.edge-apps.net',
},



# ------------------------------------------------------------------
# NACIONALES
# ------------------------------------------------------------------

{
	'NAME'   : 'AMERICA LOCAL',
	'ID'     : 'America.uy',
	'ICON'   : 'logo/America_1.png?v=2',
	'GROUP'  : 2,
	'URL'    : 'https://prepublish.f.qaotic.net/a07/americahls-100056/playlist_720p.m3u8',
	'AGENT'  : 'Android;Chrome'
},

{
	'NAME'   : 'EL TRECE LOCAL',
	'ID'     : 'ElTrece.ar',
	'ICON'   : 'logo/ElTrece_1.png?v=1',
	'GROUP'  : 2,
	'URL'    : 'https://live-01-02-eltrece.vodgc.net/eltrecetv/index.m3u8',
	'URL2'    : 'https://livetrx01.vodgc.net/eltrecetv/index.m3u8',
	'REFERER': 'https://vodgc.net'
},

{
	'NAME'   : 'NET LOCAL',
	'ID'     : 'Net TV.ar',
	'ICON'   : 'logo/NetTV_1.png?v=1',
	'GROUP'  : 2,
	'URL'    : 'https://unlimited1-saopaulo.dps.live/nettv/nettv.smil/playlist.m3u8',
	'URL2'    : 'https://unlimited1-buenosaires.dps.live/nettv/nettv.smil/playlist.m3u8',
	'REFERER': 'https://rudo.video'
},

{
	'NAME'   : 'TELEFE',
	'ID'     : 'Telefe.ar',
	'ICON'   : 'logo/Telefe.png?v=1',
	'GROUP'  : 2,
	'URL'    : URL + '/live/c6eds/TelefeHD/SA_Live_dash_enc/TelefeHD.mpd',
	'KEY'    : '69d08ad795092fc59dbdfb194424dd92:a73948b44e9292eede50c0c654301860',
	'ORIGIN' : 1
},

{
	'NAME'   : 'TELEFE FHD',
	'ID'     : 'Telefe.ar',
	'ICON'   : 'logo/Telefe_3.png?v=1',
	'GROUP'  : 2,
	'URL'    : URL + '/live/c6eds/TelefeHD/SA_Live_dash_enc_wl/TelefeHD.mpd',
	'KEY'    : '69d08ad795092fc59dbdfb194424dd92:a73948b44e9292eede50c0c654301860',
	'ORIGIN' : 1
},

{
	'NAME'   : 'TELEFE INTERNACIONAL',
	'ID'     : 'Telefe HD.uy',
	'ICON'   : 'logo/Telefe_4.png?v=1',
	'GROUP'  : 2,
	'URL'    : URL + '/live/c4eds/Telefe_Internacional/SA_Live_dash_enc_wl/Telefe_Internacional.mpd',
	'KEY'    : '2a3fd5e0c53eab2a7ff19e101888c3fb:e16cb312b80a063ab346bdc8baf93464',
	'ORIGIN' : 1
},


{
	'NAME'   : 'AMERICA',
	'ID'     : 'America.uy',
	'ICON'   : 'logo/America.png?v=1',
	'GROUP'  : 2,
	'URL'    : URL + '/live/c3eds/AmericaTV/SA_Live_dash_enc/AmericaTV.mpd',
	'KEY'    : '3d7afc43dab940d699b61466b245369f:712b5165ff990156e6c9e580b0b4df59',
	'ORIGIN' : 1
},

{
	'NAME'   : 'EL TRECE',
	'ID'     : 'ElTrece.ar',
	'ICON'   : 'logo/ElTrece.png?v=1',
	'GROUP'  : 2,
	'URL'    : URL + '/live/c3eds/ArtearHD/SA_Live_dash_enc/ArtearHD.mpd',
	'KEY'    : '4aa8ec10f92b212c0cbaaa8e0591b468:17985aeaac30e62e6dad45f4df84cc2c',
	'ORIGIN' : 1
},

{
	'NAME'   : 'EL TRECE INTERNACIONAL',
	'ID'     : 'Canal 13 (Satelital).ar',
	'ICON'   : 'logo/ElTrece_4.png?v=1',
	'GROUP'  : 2,
	'URL'    : URL + '/live/c6eds/Artear_Internacional/SA_Live_dash_enc/Artear_Internacional.mpd',
	'KEY'    : 'c5f7b491a191048931aaaf0314558bc7:6477522b434cad2020b5fb4d055720b0',
	'ORIGIN' : 1
},

{
	'NAME'   : 'EL NUEVE',
	'ID'     : '0916',
	'ICON'   : 'logo/ElNueve_1.png',
	'GROUP'  : 2,
	'URL'    : URL + '/live/c3eds/Canal9/SA_Live_dash_enc/Canal9.mpd',
	'KEY'    : '3ddf62bf44e68f06a6adb810199df713:2ace15b4ffbe70940fdf04cf97e114e7',
	'ORIGIN' : 1
},

{
	'NAME'   : 'ALPHA',
	'ID'     : 'AlphaTv.ar',
	'ICON'   : 'logo/Alpha.png',
	'GROUP'  : 2,
	'URL'    : URL + '/live/c7eds/BravoTV/SA_Live_dash_enc/BravoTV.mpd',
	'KEY'    : 'd67ea3430c0dd019e820535765268109:7d7bf2d1b5f4c7c97138a1b9b98e0675',
	'ORIGIN' : 1
},

{
	'NAME'   : 'NET',
	'ID'     : 'Net TV.ar',
	'ICON'   : 'logo/NetTV.png?v=1',
	'GROUP'  : 2,
	'URL'    : URL + '/live/c6eds/Net_TV/SA_Live_dash_enc/Net_TV.mpd',
	'KEY'    : '42803fd8c2cff83bfca0e64931c42d2b:728caae294e864b66aabe753c72df05e',
	'ORIGIN' : 1
},

{
	'NAME'   : 'CIUDAD',
	'ID'     : 'Canal de la Ciudad.ar',
	'ICON'   : 'logo/CanalCiudad.png',
	'GROUP'  : 2,
	'URL'    : URL + '/live/c6eds/Canal_de_la_ciudad/SA_Live_dash_enc/Canal_de_la_ciudad.mpd',
	'KEY'    : '8700e5c6a3528f38f878a1720ab8a5d4:dd4d69622cd92dfe429229925c6a0a75',
	'ORIGIN' : 1
},

{
	'NAME'   : 'MAGAZINE',
	'ID'     : 'Ciudad Magazine.ar',
	'ICON'   : 'logo/Magazine.png',
	'GROUP'  : 2,
	'URL'    : URL + '/live/c3eds/Magazine/SA_Live_dash_enc//Magazine.mpd',
	'KEY'    : '36bc52ea68831dbbec6a9529bc81a9e8:39858817235ad0c15640dbde56f87d78',
	'ORIGIN' : 1
},




# ------------------------------------------------------------------
# DEPORTES
# ------------------------------------------------------------------

{
	'NAME'   : 'TYC SPORTS 24',
	'ID'     : 'TyC 24',
	'ICON'   : 'logo/TYCSports_1.png',
	'GROUP'  : 4,
	'COOKIE' : '',
	'URL'    : 'https://live-04-11-tyc24.vodgc.net/tyc24/index.m3u8',
	'REFERER': 'https://play.tycsports.com/',
	'AGENT'  : 2
},

{
	'NAME'   : 'TYC SPORTS FAN',
	'ID'     : 'TyC Sports Fan',
	'ICON'   : 'logo/TYCSports_1.png',
	'GROUP'  : 4,
	'COOKIE' : '',
	'URL'    : 'https://streams2.sofast.tv/ptnr-hispasat/title-TYC-SPORTS-LATMA/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/18a85327-6b17-4d41-8c2f-41ff8511c1dd/sofastplayout/2f7c083c-a970-4cd4-a634-0b56fed45495/manifest.m3u8',
	'REFERER' : 'https://play.tycsports.com/',
	'AGENT'  : 2
},

{
	'NAME'   : 'PELEAS',
	'ICON'   : 'logo/PlutoPeleas-1.png',
	'GROUP'  : 4,
	'URL'    : 'https://jmp2.uk/plu-5e98b0447665f200078caded.m3u8?plu=2',
},

{
	'NAME'   : 'DSPORTS LOCAL',
	'ID'     : 'DSports HD.uy',
	'ICON'   : 'logo/DSports1_1.png',
	'GROUP'  : 4,
	'URL'    : 'https://1cf44b5bdec84b56bd4ec71e0cbf33de.mediatailor.us-east-1.amazonaws.com/v1/dash/dffceb859a31f14d0ed059ef6b4e2e4d850e60b1/live_1057/1057_DIRECTV_SPORTS_ARG_DASH/manifest.mpd',
	'KEY'    : '13129171e9303da3a31dd7b583f7f41c:dc4844c309c47baf996f267cda324d61',
	'REFERER': 'https://android_mobile.directvgo.com/',
	'AGENT'  : 4,	
},

{
	'NAME'   : 'DSPORTS 2 LOCAL',
	'ID'     : 'DSports 2 HD.uy',
	'ICON'   : 'logo/DSports2_1.png',
	'GROUP'  : 4,
	'URL'    : 'https://46925e69ccf445e09667cb17c8bb4f2c.mediatailor.us-east-1.amazonaws.com/v1/dash/dffceb859a31f14d0ed059ef6b4e2e4d850e60b1/live_1065/1065_DIRECTV_SPORTS_OCC_2_DASH/manifest.mpd',
	'KEY'    : '054e17b9b99e3e0aa1e022d238635d35:4cc211af8468e321973787bb61f55db4',
	'REFERER': 'https://android_mobile.directvgo.com/',
	'AGENT'  : 4,	
},

{
	'NAME'   : 'DSPORTS + LOCAL',
	'ID'     : 'DSports + HD.uy',
	'ICON'   : 'logo/DSports3_1.png',
	'GROUP'  : 4,
	'URL'    : 'https://b5cce558f58c4843a8264d282ebce3ec.mediatailor.us-east-1.amazonaws.com/v1/dash/dffceb859a31f14d0ed059ef6b4e2e4d850e60b1/live_1071/1071_DIRECTV_SPORTS_HD_DASH/manifest.mpd',
	'KEY'    : '7dbd6af5e0e530919642f53f4b9af775:48d7040d3c5edf52115fd0b2ede3bdb0',
	'REFERER': 'https://android_mobile.directvgo.com/',
	'AGENT'  : 4,	
},

{
	'NAME'   : 'TYC SPORTS',
	'ID'     : '0409',
	'ICON'   : 'logo/TYCSports_2.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c7eds/TyCSport/SA_Live_dash_enc/TyCSport.mpd',
	'KEY'    : '0b1e6825350fa1bc0032f8f36287e006:11fc540a4539d18f91cd403a5ed42284',
	'ORIGIN' : 1
},

{
	'NAME'   : 'TYC SPORTS FHD',
	'ID'     : 'TyCSports.ar',
	'ICON'   : 'logo/TYCSports_2.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c7eds/TyCSport/SA_Live_dash_enc_wl/TyCSport.mpd',
	'KEY'    : '0b1e6825350fa1bc0032f8f36287e006:11fc540a4539d18f91cd403a5ed42284',
	'ORIGIN' : 1
},

{
	'NAME'   : 'TYC SPORTS INTERNACIONAL',
	'ID'     : 'TyC Sports HD.uy',
	'ICON'   : 'logo/TYCSports_2.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c3eds/TyC_Internacional/SA_Live_dash_enc/TyC_Internacional.mpd',
	'KEY'    : 'e7880e1b0d50ca324646b9d73d781e1f:2bef2d7912ee52310d421c1d7756d072',
	'ORIGIN' : 1
},

{
	'NAME'   : 'TNT SPORTS',
	'ID'     : '0404',
	'ICON'   : 'logo/TntSports_1.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c6eds/TNT_Sports_HD/SA_Live_dash_enc/TNT_Sports_HD.mpd',
	'KEY'    : '9fb56301bc7687baf0b1a61def9a007a:947d2294ba67256827e8e97f267e71e0',
	'ORIGIN' : 1
},

{
	'NAME'   : 'TNT SPORTS FHD',
	'ID'     : 'TNTSportsPremium.ar',
	'ICON'   : 'logo/TntSports_2.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c6eds/TNT_Sports_HD/SA_Live_dash_enc_wl/TNT_Sports_HD.mpd',
	'KEY'    : '9fb56301bc7687baf0b1a61def9a007a:947d2294ba67256827e8e97f267e71e0',
	'ORIGIN' : 1
},

{
	'NAME'   : 'ESPN PREMIUM',
	'ID'     : '1418',
	'ICON'   : 'logo/EspnPremium_1.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c7eds/Fox_Sports_Premiun_HD/SA_Live_dash_enc/Fox_Sports_Premiun_HD.mpd',
	'KEY'    : 'c502892e037a9f34827147b2b24e42cf:2531bd34bec6c0e8fa4e07aedb261ade',
	'ORIGIN' : 1
},

{
	'NAME'   : 'ESPN PREMIUM FHD',
	'ID'     : 'EspnPremium.ar',
	'ICON'   : 'logo/EspnPremium_2.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c7eds/Fox_Sports_Premiun_HD/SA_Live_dash_enc_wl/Fox_Sports_Premiun_HD.mpd',
	'KEY'    : 'c502892e037a9f34827147b2b24e42cf:2531bd34bec6c0e8fa4e07aedb261ade',
	'ORIGIN' : 1
},

{
	'NAME'   : 'ESPN',
	'ID'     : 'Espn.ar',
	'ICON'   : 'logo/Espn1_1.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c3eds/ESPN2HD/SA_Live_dash_enc/ESPN2HD.mpd',
	'KEY'    : 'd079ffa3757e8335611fc48be6ba47ff:05059d1cb21b6708a55e9c26fb38e2f3',
	'ORIGIN' : 1
},

{
	'NAME'   : 'ESPN 2',
	'ID'     : '1412',
	'ICON'   : 'logo/Espn2_1.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c6eds/ESPN2_Arg/SA_Live_dash_enc/ESPN2_Arg.mpd',
	'KEY'    : 'e6eab53cf8ea962b999c59c298596a65:10c103ae76f99620d66fa75f2c03302a',
	'ORIGIN' : 1
},

{
	'NAME'   : 'ESPN 3',
	'ID'     : '2413',
	'ICON'   : 'logo/Espn3_1.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c3eds/ESPN3/SA_Live_dash_enc/ESPN3.mpd',
	'KEY'    : 'deeed0f44c6b45e064f4d5064486e821:bf89ceeb93564ddc603ba6afd8c9266a',
	'ORIGIN' : 1
},

{
	'NAME'   : 'ESPN 4',
	'ID'     : '0414',
	'ICON'   : 'logo/Espn4_1.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c3eds/ESPNHD/SA_Live_dash_enc/ESPNHD.mpd',
	'KEY'    : 'd02981e6faeacef49c90fdb053ab641d:645e13624e933841b1ea35cda1b55bd1',
	'ORIGIN' : 1
},

{
	'NAME'   : 'ESPN 5',
	'ID'     : 'ESPN 5 HD.uy',
	'ICON'   : 'logo/Espn5_1.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c7eds/ESPN4/SA_Live_dash_enc/ESPN4.mpd',
	'KEY'    : 'cf626de3cadd9bfaf0b85c06aafd2cd0:bc2aa7d9e6354e4979ee62b0ec5595c5',
	'ORIGIN' : 1
},

{
	'NAME'   : 'ESPN 6',
	'ID'     : '0416',
	'ICON'   : 'logo/Espn6_1.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c7eds/FoxSports3_UY/SA_Live_dash_enc/FoxSports3_UY.mpd',
	'KEY'    : 'fdac9b45f19959b848f498c8efe15d12:c2a6e7acabc370ef792ffacc5e2610a9',
	'ORIGIN' : 1
},

{
	'NAME'   : 'ESPN 7',
	'ID'     : '0417',
	'ICON'   : 'logo/Espn7_1.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c7eds/FoxSports2_UY/SA_Live_dash_enc/FoxSports2_UY.mpd',
	'KEY'    : 'fdac9b45f19959b848f498c8efe15d12:c2a6e7acabc370ef792ffacc5e2610a9',
	'ORIGIN' : 1
},

{
	'NAME'   : 'ESPN UY',
	'ID'     : 'ESPN HD.uy',
	'ICON'   : 'logo/Espn1.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c4eds/ESPN_UY/SA_Live_dash_enc/ESPN_UY.mpd',
	'KEY'    : 'e95fe84b9f73e6655fde711d5c896056:267a0e514deb984803bec43cc607c4cb',
	'ORIGIN' : 1
},

{
	'NAME'   : 'ESPN 2 UY',
	'ID'     : 'ESPN 2 HD.uy',
	'ICON'   : 'logo/Espn2.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c4eds/ESPN2_UY/SA_Live_dash_enc/ESPN2_UY.mpd',
	'KEY'    : '3f2e12c72e1a011be0569fbd9ca486ab:1273deabb3c043560fe264dd2b1690f1',
	'ORIGIN' : 1
},

{
	'NAME'   : 'ESPN 3 UY',
	'ID'     : 'ESPN 3 HD.uy',
	'ICON'   : 'logo/Espn3.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c7eds/ESPN3_Uy-Py/SA_Live_dash_enc/ESPN3_Uy-Py.mpd',
	'KEY'    : '3b302c8ed3781696208bc346d9397554:ee35be47515d781f56b72b78c7e9c7b5',
	'ORIGIN' : 1
},

{
	'NAME'   : 'ESPN PY',
	'ID'     : 'ESPN HD.uy',
	'ICON'   : 'logo/Espn1_2.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c4eds/ESPN2_PY/SA_Live_dash_enc/ESPN2_PY.mpd',
	'KEY'    : '88003c992a67f3221dc4502fcf4a8086:dade5af67461fdacecb721dbbb500fb1',
	'ORIGIN' : 'https://portal.app.flow.com.py/'
},

{
	'NAME'   : 'FOX SPORTS',
	'ID'     : '1436',
	'ICON'   : 'logo/FoxSports1.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c3eds/FoxSports/SA_Live_dash_enc/FoxSports.mpd',
	'KEY'    : '37730b00a5f92084c47a8129e84559f3:a2e20a45a057ff4e7c0bc2ad49e6f3e5',
	'ORIGIN' : 1
},

{
	'NAME'   : 'FOX SPORTS 2',
	'ID'     : '1437',
	'ICON'   : 'logo/FoxSports2.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c3eds/FoxSports2HD/SA_Live_dash_enc/FoxSports2HD.mpd',
	'KEY'    : '1b0ab680ef94a1842185fa78a830cbd7:23129ab5572aeda7607c920655c0dbea',
	'ORIGIN' : 1
},

{
	'NAME'   : 'FOX SPORTS 3',
	'ID'     : '1438',
	'ICON'   : 'logo/FoxSports3.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c3eds/FoxSports3HD/SA_Live_dash_enc/FoxSports3HD.mpd',
	'KEY'    : '4629bd0ae30c0e72af111fb948fada1c:7864154c679e769e7f164ba083c8fad3',
	'ORIGIN' : 1
},

{
	'NAME'   : 'DSPORTS',
	'ID'     : '1431',
	'ICON'   : 'logo/DSports1.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c3eds/DSports_1/SA_Live_dash_enc/DSports_1.mpd',
	'KEY'    : '86d19904429f78baf98cf1fd481c430e:5229197732a9a3e109264b272bd782f2',
	'ORIGIN' : 1
},

{
	'NAME'   : 'DSPORTS FHD',
	'ID'     : '1431',
	'ICON'   : 'logo/DSports1.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c3eds/DSports_1/SA_Live_dash_enc_wl/DSports_1.mpd',
	'KEY'    : '86d19904429f78baf98cf1fd481c430e:5229197732a9a3e109264b272bd782f2',
	'ORIGIN' : 1
},

{
	'NAME'   : 'DSPORTS 2',
	'ID'     : '1431',
	'ICON'   : 'logo/DSports2.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c3eds/DSports_2/SA_Live_dash_enc/DSports_2.mpd',
	'KEY'    : '33848c262a3cc8c0eb8b34cdb9691f04:fd8e52ad745cec9e62263928a10f3abd',
	'ORIGIN' : 1
},

{
	'NAME'   : 'DSPORTS 2 FHD',
	'ID'     : '1431',
	'ICON'   : 'logo/DSports2.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c3eds/DSports_2/SA_Live_dash_enc_wl/DSports_2.mpd',
	'KEY'    : '33848c262a3cc8c0eb8b34cdb9691f04:fd8e52ad745cec9e62263928a10f3abd',
	'ORIGIN' : 1
},


{
	'NAME'   : 'DSPORTS UY',
	'ID'     : 'DSports HD.uy',
	'ICON'   : 'logo/DSports1_2.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c7eds/Dsports_UY/SA_Live_dash_enc/Dsports_UY.mpd',
	'KEY'    : '9768d634efd3139386b907405e0a70cc:f02c61e5952a3079f629e2f705b02cc6',
	'ORIGIN' : 1
},

{
	'NAME'   : 'DSPORTS 2 UY',
	'ID'     : 'Dsports 2 HD.uy',
	'ICON'   : 'logo/DSports2_2.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c7eds/Dsports2_UY/SA_Live_dash_enc_wl/Dsports2_UY.mpd',
	'KEY'    : 'df41365cbe65033f4e57f4b7bafafbf3:62c11f75b6836e1defe480d8a9775320',
	'ORIGIN' : 1
},

{
	'NAME'   : 'DSPORTS + UY',
	'ID'     : 'Dsports + HD.uy',
	'ICON'   : 'logo/DSports3_2.png',
	'GROUP'  : 4,
	'URL'    : URL + '/live/c7eds/Dsports_Plus_UY/SA_Live_dash_enc/Dsports_Plus_UY.mpd',
	'KEY'    : 'fc51b58e664b610663329079722d98b3:3a444d28d15313665b305bb99c0e4c82',
	'ORIGIN' : 1
},


# ------------------------------------------------------------------
# DOCUMENTALES
# ------------------------------------------------------------------

{
	'NAME'   : 'LOVE THE PLANET',
	'ICON'   : 'logo/LovePlanet_1.png',
	'GROUP'  : 9,
	'URL'    : 'https://jmp2.uk/stvp-ESBC4700002TD?sam=1',
},

{
	'NAME'   : 'LOVE NATURE',
	'ID'     : 'LoveNature.es',
	'ICON'   : 'logo/LoveNature_1.png',
	'GROUP'  : 9,
	'URL'    : 'https://jmp2.uk/rok-03a419fc4dff59b39b176d9f76b09e38.m3u8',
},

{
	'NAME'   : 'SALVAJE',
	'ICON'   : 'logo/PlutoNaturaleza.png',
	'GROUP'  : 9,
	'URL'    : 'https://jmp2.uk/rok-098bce44be895630a3e437516fe70853.m3u8',
},

{
	'NAME'   : 'DISCOVERY',
	'ID'     : 'Discovery HD.uy',
	'ICON'   : 'logo/Discovery_1.png',
	'GROUP'  : 9,
	'URL'    : URL + '/live/c3eds/DiscoveryHD/SA_Live_dash_enc/DiscoveryHD.mpd',
	'KEY'    : 'f55aec775d92cea41ea0f80b8615495a:8927f326931c6a5af38d0cd7cd744338',
	'ORIGIN' : 1
},

{
	'NAME'   : 'THEATER',
	'ID'     : 'Discovery Theater.ar',
	'ICON'   : 'logo/Theater.png',
	'GROUP'  : 9,
	'URL'    : URL + '/live/c6eds/Theater_HD/SA_Live_dash_enc/Theater_HD.mpd',
	'KEY'    : 'e76e0dd95f2187770a6fa9f72d7600f5:bcab30dad55228fcd0a89a534b7b4f04',
	'ORIGIN' : 1
},

{
	'NAME'   : 'HEALTH',
	'ID'     : 'DiscoveryHomeAndHealth.ar',
	'ICON'   : 'logo/H&H.png',
	'GROUP'  : 9,
	'URL'    : URL + '/live/c3eds/DiscoveryHomeHealthHD/SA_Live_dash_enc/DiscoveryHomeHealthHD.mpd',
	'KEY'    : '6e2bc2b3c9464c407af6d0559bb5e1ea:43ec5e698b6f60a0f41d604909a25186',
	'ORIGIN' : 1
},

{
	'NAME'   : 'SCIENCE',
	'ID'     : 'Discovery Science.ar',
	'ICON'   : 'logo/Science_1.png',
	'GROUP'  : 9,
	'URL'    : URL + '/live/c6eds/Discovery_Science/SA_Live_dash_enc/Discovery_Science.mpd',
	'KEY'    : 'c9fcd9709b38058ca2c90b83e81bc039:fb736e65c2a7248987e58a2a7e6d49a6',
	'ORIGIN' : 1
},

{
	'NAME'   : 'HISTORY',
	'ID'     : 'History HD.uy',
	'ICON'   : 'logo/History_1.png',
	'GROUP'  : 9,
	'URL'    : URL + '/live/c7eds/HistoryHD/SA_Live_dash_enc/HistoryHD.mpd',
	'KEY'    : 'b10e48eb0c9940015e28dfe7637b48fa:4df252f95de70923b736f3f659821cb7',
	'ORIGIN' : 1
},

{
	'NAME'   : 'HISTORY 2',
	'ID'     : 'History 2 HD.uy',
	'ICON'   : 'logo/History2_1.png',
	'GROUP'  : 9,
	'URL'    : URL + '/live/c6eds/History_2/SA_Live_dash_enc/History_2.mpd',
	'KEY'    : '6e08ea85cdbf5d3d2089d5e9a5349d8c:ccdb13d6d47775894452a0629c986b67',
	'ORIGIN' : 1
},

{
	'NAME'   : 'NATGEO',
	'ID'     : 'National Geographic HD.uy',
	'ICON'   : 'logo/Natgeo_1.png',
	'GROUP'  : 9,
	'URL'    : URL + '/live/c3eds/NatGeoHD/SA_Live_dash_enc/NatGeoHD.mpd',
	'KEY'    : '73735c1740464c99cca3ffb450c15811:b9241d083c902fa615e4f780081ae926',
	'ORIGIN' : 1
},




# ------------------------------------------------------------------
# CINE PREMIUM
# ------------------------------------------------------------------

{
	'NAME'   : 'UNIVERSAL CINEMA MX',
	'ID'     : 'Universal Cinema.uy',
	'ICON'   : 'logo/UnivCinema_1.png',
	'GROUP'  : 8,
	'URL'    : 'https://unipluslivedash.akamaized.net/universalcinemat0/manifest.mpd',
	'KEY'    : '693c14512fe754679776b9352fa84fa2:5c04eb44db6dfabcbb73be28408e831d,47b9ccb70c5c512f9195712d11923df6:8a7dba41bad7d0f2a9ebecd3eaf9c2ff,e97732b12ed754588cd3e01e3e6ea7ee:494c340693c70e21b4490c2ec6430627',
	'AGENT'  : 2
},

{
	'NAME'   : 'UNIVERSAL PREMIERE MX',
	'ID'     : 'Universal Premiere.uy',
	'ICON'   : 'logo/UnivPremiere_1.png',
	'GROUP'  : 8,
	'URL'    : 'https://unipluslivedash.akamaized.net/universalpremiert0/manifest.mpd',
	'KEY'    : '4518f2fc410a5327b26a26e8c0cebd17:16da291229b2b68ded5419cc35339beb,3ef088eaf6685839a1d77c9bc89b1e20:68c8566c7cb4400fac63d0abe8eea6d4,2528892552c65b5399017c2f2a194ab7:fc87001860c95eb094c2dd5fc2d2e2bd',
	'AGENT'  : 2
},

{
	'NAME'   : 'HBO',
	'ID'     : 'HBO HD.uy',
	'ICON'   : 'logo/Hbo_1.png',
	'GROUP'  : 8,
	'URL'    : URL + '/live/c4eds/HBOHD/SA_Live_dash_enc_wl/HBOHD.mpd',
	'KEY'    : 'b059cdbfc787a32f57fbcb6e52dbc0a0:50648d7806624eb8d53fb2aecc8b1af1',
	'ORIGIN' : 1
},

{
	'NAME'   : 'HBO 2',
	'ID'     : 'HBO 2 HD.uy',
	'ICON'   : 'logo/Hbo2_1.png',
	'GROUP'  : 8,
	'URL'    : URL + '/live/c6eds/HBO_2/SA_Live_dash_enc/HBO_2.mpd',
	'KEY'    : '91bd6f829d06498c21e212acf1c5fa07:148a358284689e40b22074c244c535da',
	'ORIGIN' : 1
},

{
	'NAME'   : 'HBO PLUS',
	'ID'     : 'HBO Plus HD.uy',
	'ICON'   : 'logo/HboPlus_1.png',
	'GROUP'  : 8,
	'URL'    : URL + '/live/c6eds/HBO_Plus/SA_Live_dash_enc/HBO_Plus.mpd',
	'KEY'    : 'c1c780647a98d46c3e5867cf204d129a:006d44f02be55c28f34b9106d79a82a9',
	'ORIGIN' : 1
},

{
	'NAME'   : 'HBO FAMILY',
	'ID'     : 'HBO Family.uy',
	'ICON'   : 'logo/HboFamily_1.png',
	'GROUP'  : 8,
	'URL'    : URL + '/live/c6eds/HBO_Family/SA_Live_dash_enc/HBO_Family.mpd',
	'KEY'    : '9768f423e5121ded23637f54245506a2:abd28dce83c82d26d5953b416db0e52a',
	'ORIGIN' : 1
},

{
	'NAME'   : 'HBO MUNDI',
	'ID'     : 'HBO Mundi HD.uy',
	'ICON'   : 'logo/HboMundi_1.png',
	'GROUP'  : 8,
	'URL'    : URL + '/live/c6eds/HBO_Mundi/SA_Live_dash_enc/HBO_Mundi.mpd',
	'KEY'    : '56fc145492109590d82cf8f60c55d4f5:c713241579436e0d5fe2480b6eb7b1fd',
	'ORIGIN' : 1
},

{
	'NAME'   : 'HBO SIGNATURE',
	'ID'     : 'HBO Signature HD.uy',
	'ICON'   : 'logo/HboSignature_1.png',
	'GROUP'  : 8,
	'URL'    : URL + '/live/c6eds/HBO_Signature/SA_Live_dash_enc/HBO_Signature.mpd',
	'KEY'    : '4918d3bf399a237e8ee065eb3ebf7327:747179296ae370e9b8746a09904b5385',
	'ORIGIN' : 1
},

{
	'NAME'   : 'HBO SIGNATURE FHD',
	'ID'     : 'HBO Signature',
	'ICON'   : 'logo/HboSignature_1.png',
	'GROUP'  : 8,
	'URL'    : URL + '/live/c6eds/HBO_Signature/SA_Live_dash_enc_wl/HBO_Signature.mpd',
	'KEY'    : '4918d3bf399a237e8ee065eb3ebf7327:747179296ae370e9b8746a09904b5385',
	'ORIGIN' : 1
},

{
	'NAME'   : 'HBO POP',
	'ID'     : 'HBO POP HD.uy',
	'ICON'   : 'logo/HboPop_1.png',
	'GROUP'  : 8,
	'URL'    : URL + '/live/c7eds/HBO_POP/SA_Live_dash_enc/HBO_POP.mpd',
	'KEY'    : '782be6aa05e2e53f1f0769ac21335975:bc54efe24ebc6127dee264704cdd543b',
	'ORIGIN' : 1
},

{
	'NAME'   : 'HBO XTREME',
	'ID'     : 'HBO Xtreme HD.uy',
	'ICON'   : 'logo/HboXtreme_1.png',
	'GROUP'  : 8,
	'URL'    : URL + '/live/c6eds/HBO_Extreme/SA_Live_dash_enc/HBO_Extreme.mpd',
	'KEY'    : 'b1c518c4859b1eac1ac409dd7a712155:d9ae29d636e14074da10360765ee4cb5',
	'ORIGIN' : 1
},

{
	'NAME'   : 'UNIVERSAL TV',
	'ID'     : 'Universal HD.uy',
	'ICON'   : 'logo/Universal.png',
	'GROUP'  : 8,
	'URL'    : URL + '/live/c6eds/Universal_Channel_HD/SA_Live_dash_enc/Universal_Channel_HD.mpd',
	'KEY'    : 'e0bb7db70deee6be9b881a5bd1af6453:88c72f8626a9d7a9ca222fed62e1e6af',
	'ORIGIN' : 1
},

{
	'NAME'   : 'UNIVERSAL PREMIERE',
	'ID'     : 'Universal Premiere.uy',
	'ICON'   : 'logo/UnivPremiere_1.png',
	'GROUP'  : 8,
	'URL'    : URL + '/live/c6eds/Universal_Premiere/SA_Live_dash_enc/Universal_Premiere.mpd',
	'KEY'    : '909eb7589305cd00e1b6827fadd74411:43a9e55701369434df4892240d9741c2',
	'ORIGIN' : 1
},


# ------------------------------------------------------------------
# INTERNACIONAL
# ------------------------------------------------------------------

{
	'NAME'   : 'MALAGA',
	'ICON'   : 'logo/Malaga-2.png',
	'GROUP'  : 12,
	'URL'    : 'https://canalmalaga-tv-live.flumotion.com/playlist.m3u8',
	'REFERER': 'https://www.canalmalaga.es/'
},

{
	'NAME'   : 'LATINA',
	'ICON'   : 'logo/Latina.png',
	'GROUP'  : 12,
	'URL'    : 'https://origin.dpsgo.com/ssai/event/oYQGDqEGTmGdHE_fz9oLlg/master.m3u8',
	'REFERER': 'https://www.latina.pe'
},





]  # END.
