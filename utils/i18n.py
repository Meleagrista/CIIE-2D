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
        'credit text': "Contornos Inmersivos, Interactivos y de Entretenimiento\n"
                       "Grado en Ingenieria Informática\n"
                       "Universidade da Coruña\n"
                       "Autores:\n"
                       "  - Martín do Río Rico\n"
                       "  - Yago Fernández Rego\n"
                       "  - David García Ramallal\n"
                       "  - Pelayo Vieites Pérez",
        'resume': 'CONTINUAR',
        'restart': 'REINICIAR',
        'main menu': 'MENU PRINCIPAL'
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
        'credit text': "Contornos Inmersivos, Interactivos e de Entretenimiento\n"
                       "Informatics engineering\n"
                       "Universidade da Coruña\n"
                       "Authors:\n"
                       "  - Martín do Río Rico\n"
                       "  - Yago Fernández Rego\n"
                       "  - David García Ramallal\n"
                       "  - Pelayo Vieites Pérez",
        'resume': 'RESUME',
        'restart': 'RESTART',
        'main menu': 'MAIN MENU'
    }
}


def get_translation(idioma, texto):
    return traducciones[idioma][texto.lower()]
