traducciones = {
    'es': {
        'play': 'JUGAR',
        'settings': 'CONFIGURACION',
        'credits': 'CREDITOS',
        'exit': 'SALIR',
        'menu music': 'MUSICA MENU',
        'controls': 'CONTROLES',
        'return': 'VOLVER',
        'arrows': 'FLECHAS',
        'language': 'IDIOMA',
        'pick up key': 'Pulsa <ESPACIO> para coger la llave',
        'find exit': 'Tienes que encontrar la salida',
        'find key': 'Tienes que encontrar la llave'
    },
    'en': {
        'play': 'PLAY',
        'settings': 'SETTINGS',
        'credits': 'CREDITS',
        'exit': 'EXIT',
        'menu music': 'MENU MUSIC',
        'controls': 'CONTROLS',
        'return': 'RETURN',
        'arrows': 'ARROWS',
        'language': 'LANGUAGE',
        'pick up key': 'Press <SPACE> to pick up the key',
        'find exit': 'You need to find the exit',
        'find key': 'You need to find the key'
    }
}


def get_translation(idioma, texto):
    return traducciones[idioma][texto.lower()]
