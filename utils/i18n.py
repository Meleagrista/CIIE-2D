traducciones = {
    'es': {
        'play': 'JUGAR',
        'settings': 'OPCIONES',
        'credits': 'CREDITOS',
        'exit': 'SALIR',
        'menu music': 'MUSICA MENU',
        'controls': 'CONTROLES',
        'return': 'VOLVER',
        'arrows': 'FLECHAS',
        'language': 'IDIOMA',
        'pick up key': 'Pulsa <ESPACIO> para coger la llave',
        'find exit': 'Tienes que encontrar la salida',
        'find key': 'Tienes que encontrar la llave',
        '1': "Contornos Inmersivos, Interactivos y de Entretenimiento",
        '2': "Grado en Ingenieria Informática",
        '3': "Universidade da Coruña",
        '4': "Autores:",
        '5': "Martín do Río Rico",
        '6': "Yago Fernández Rego",
        '7': "David García Ramallal",
        '8': "Pelayo Vieites Pérez",
        'resume': 'CONTINUAR',
        'restart': 'REINICIAR',
        'main menu': 'MENU PRINCIPAL',
        'next level': 'SIGUIENTE NIVEL'
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
        'find key': 'You need to find the key',
        '1': "Immersive, Interactive, and Entertainment Environments",
        '2': "Degree in Computer Engineering",
        '3': "University of A Coruña",
        '4': "Authors:",
        '5': "Martín do Río Rico",
        '6': "Yago Fernández Rego",
        '7': "David García Ramallal",
        '8': "Pelayo Vieites Pérez",
        'resume': 'RESUME',
        'restart': 'RESTART',
        'main menu': 'MAIN MENU',
        'next level': 'NEXT LEVEL'
    }
}


def get_translation(idioma, texto):
    return traducciones[idioma][texto.lower()]
