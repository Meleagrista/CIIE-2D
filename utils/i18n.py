class i18n:
    def __init__(self):
        self.traducciones = {
            'es': {
                'play': 'JUGAR',
                'settings': 'CONFIGURACION',
                'credits': 'CREDITOS',
                'exit': 'SALIR',
                'menu music': 'MUSICA MENU',
                'controls': 'CONTROLES',
                'return': 'VOLVER',
                'arrows': 'FLECHAS',
                'language': 'IDIOMA'
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
                'language': 'LANGUAGE'

            }
        }

    def translate(self, idioma, texto):
        return self.traducciones.get(idioma, {}).get(texto, texto)