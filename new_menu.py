import pygame
import time
from pygame.locals import *
from ui.director import *
from ui.escena import *
from ui.gestorRecursos import *
from gamemanager import GameManager
from utils.enums import Controls as Ctl
from utils.constants import *

movement_option = Ctl.WASD

# -------------------------------------------------
# Clase abstracta ElementoGUI

class ElementoGUI:
    def __init__(self, pantalla, rectangulo):
        self.pantalla = pantalla
        self.rect = rectangulo

    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony

    def posicionEnElemento(self, posicion):
        (posicionx, posiciony) = posicion
        if (posicionx>=self.rect.left) and (posicionx<=self.rect.right) and (posiciony>=self.rect.top) and (posiciony<=self.rect.bottom):
            return True
        else:
            return False

    def dibujar(self):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")
    def accion(self):
        raise NotImplemented("Tiene que implementar el metodo accion.")


# -------------------------------------------------
# Clase Boton y los distintos botones

class Boton(ElementoGUI):
    def __init__(self, pantalla, nombreImagen, posicion):
        # Se carga la imagen del boton
        self.imagen = GestorRecursos.CargarImagen(nombreImagen,-1)
        self.imagen = pygame.transform.scale(self.imagen, (20, 20))
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class BotonJugar(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'controller.png', (500,50))
    def accion(self):
        self.pantalla.menu.ejecutarJuego()

class BotonConfiguracion(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'config.png', (500,90))
    def accion(self):
        self.pantalla.menu.mostrarPantallaConfiguracion()

class BotonCreditos(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'corona.png', (500,130))
    def accion(self):
        self.pantalla.menu.mostrarPantallaCreditos()

class BotonSalir(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'exit.png', (500,170))
    def accion(self):
        self.pantalla.menu.salirPrograma()
        
class BotonVolverMenuInicial(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'return_pixel3.png', (520,160))
    def accion(self):
        self.pantalla.menu.mostrarPantallaInicial()

class BotonSwitch(Boton):
    def __init__(self, pantalla, nombreImagen1, nombreImagen2, posicion, estado_inicial):
        # Se cargan las imagenes del boton
        self.imagen1 = GestorRecursos.CargarImagen(nombreImagen1,-1)
        self.imagen1 = pygame.transform.scale(self.imagen1, (50, 50))
        self.imagen2 = GestorRecursos.CargarImagen(nombreImagen2,-1)
        self.imagen2 = pygame.transform.scale(self.imagen2, (50, 50))
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        ElementoGUI.__init__(self, pantalla, self.imagen1.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
        # Estado inicial
        self.estado = estado_inicial
        self.imagen = self.imagen2

class SwitchVolumen(BotonSwitch):
    def __init__(self, pantalla):
        BotonSwitch.__init__(self, pantalla, 'switch_off.jpg', "switch_on.png", (500,90), "On")
    def accion(self):
        # Cambiar el estado del interruptor
        if self.estado == 'Off':
            pygame.mixer.music.set_volume(1.0)  # Max volume
            self.estado = 'On'
            self.imagen = self.imagen2
        else:
            pygame.mixer.music.set_volume(0.0)  # Mute
            self.estado = 'Off'
            self.imagen = self.imagen1

class SwitchControles(BotonSwitch):
    def __init__(self, pantalla):
        BotonSwitch.__init__(self, pantalla, 'arrows.png', "wasd.png", (500,130), "WASD")
    def accion(self):
        global movement_option
        # Cambiar el estado del interruptor
        if self.estado == 'Arrows':
            movement_option = Ctl.WASD
            self.estado = 'WASD'
            self.imagen = self.imagen2
        else:
            movement_option = Ctl.Arrows
            self.estado = 'Arrows'
            self.imagen = self.imagen1
# -------------------------------------------------
# Clase TextoGUI y los distintos textos

class TextoGUI(ElementoGUI):
    def __init__(self, pantalla, fuente, color, texto, posicion):
        # Se crea la imagen del texto
        self.imagen = fuente.render(texto, True, color)
        # Se llama al método de la clase padre con el rectángulo que ocupa el texto
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class TextoJugar(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font('assets\pixel.regular.ttf', 20)
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), 'PLAY', (530, 55))
    def accion(self):
        self.pantalla.menu.ejecutarJuego()

class TextoConfiguracion(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font('assets\pixel.regular.ttf', 20)
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), 'SETTINGS', (530, 95))
    def accion(self):
        self.pantalla.menu.mostrarPantallaConfiguracion()

class TextoCreditos(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font('assets\pixel.regular.ttf', 20)
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), 'CREDITS', (530, 135))
    def accion(self):
        self.pantalla.menu.mostrarPantallaCreditos()

class TextoSalir(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font('assets\pixel.regular.ttf', 20)
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), 'EXIT', (530, 175))
    def accion(self):
        self.pantalla.menu.salirPrograma()

class TextoTituloMenuPrincipal(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font('assets\pixel.regular.ttf', 50)
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), 'GAME TITLE', (50, 100))
    def accion(self):
        pass

class TextoVolverMenuPrincipal(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font('assets\pixel.regular.ttf', 20)
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), 'RETURN', (560, 160))
    def accion(self):
        self.pantalla.menu.mostrarPantallaInicial()

class TextoMusicaMenu(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font('assets\pixel.regular.ttf', 20)
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), 'MENU MUSIC', (560, 80))
    def accion(self):
        pass

class TextoArrowsWASDMenu(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font('assets\pixel.regular.ttf', 20)
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), 'CONTROLS', (560, 120))
    def accion(self):
        pass

class TextoContenidoCreditos(ElementoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font('assets\pixel.regular.ttf', 20)
        self.textos = []
        self.textos.append(TextoGUI(pantalla, fuente, (0, 0, 0), "Contornos Inmersivos, Interactivos e de Entretemento", (40, 100)))
        self.textos.append(TextoGUI(pantalla, fuente, (0, 0, 0), "Grao en Enxeneria Informatica", (40, 130)))
        self.textos.append(TextoGUI(pantalla, fuente, (0, 0, 0), "UDC", (40, 160)))
        self.textos.append(TextoGUI(pantalla, fuente, (0, 0, 0), "Authors:", (40, 190)))
        self.textos.append(TextoGUI(pantalla, fuente, (0, 0, 0), "- Martin do Rio Rico", (50, 220)))
        self.textos.append(TextoGUI(pantalla, fuente, (0, 0, 0), "- Yago Fernandez Rego", (50, 250)))
        self.textos.append(TextoGUI(pantalla, fuente, (0, 0, 0), "- David Garcia Ramallal:", (50, 280)))
        self.textos.append(TextoGUI(pantalla, fuente, (0, 0, 0), "- Pelayo Vieites Perez", (50, 310)))
        

    def dibujar(self, pantalla):
        for texto in self.textos:
            texto.dibujar(pantalla)

    def accion(self):
        pass

# -------------------------------------------------
# Clase PantallaGUI y las distintas pantallas

class PantallaGUI:
    def __init__(self, menu, nombreImagen):
        self.menu = menu
        # Se carga la imagen de fondo
        self.imagen = GestorRecursos.CargarImagen(nombreImagen)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        # Se tiene una lista de elementos GUI
        self.elementosGUI = []

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == MOUSEBUTTONDOWN:
                self.elementoClic = None
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        self.elementoClic = elemento
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        if (elemento == self.elementoClic):
                            elemento.accion()

    def dibujar(self, pantalla):
        # Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        # Después los botones
        for elemento in self.elementosGUI:
            elemento.dibujar(pantalla)

class PantallaInicialGUI(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'desert-pixel-placeholder.png')
        # Creamos los botones y los metemos en la lista
        botonJugar = BotonJugar(self)
        botonConfiguracion = BotonConfiguracion(self)
        botonCreditos = BotonCreditos(self)
        botonSalir = BotonSalir(self)
        self.elementosGUI.append(botonJugar)
        self.elementosGUI.append(botonConfiguracion)
        self.elementosGUI.append(botonCreditos)
        self.elementosGUI.append(botonSalir)
        # Creamos el texto y lo metemos en la lista
        textoJugar = TextoJugar(self)
        textoConfiguracion = TextoConfiguracion(self)
        textoCreditos = TextoCreditos(self)
        textoSalir = TextoSalir(self)
        textoTitulo = TextoTituloMenuPrincipal(self)
        self.elementosGUI.append(textoJugar)
        self.elementosGUI.append(textoConfiguracion)
        self.elementosGUI.append(textoCreditos)
        self.elementosGUI.append(textoSalir)
        self.elementosGUI.append(textoTitulo)

class PantallaConfiguracionGUI(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'desert-pixel-placeholder.png')
        # Creamos los botones y los metemos en la lista
        switchVolumen = SwitchVolumen(self)
        switchControles = SwitchControles(self)
        botonVolverAtras = BotonVolverMenuInicial(self)
        self.elementosGUI.append(switchControles)
        self.elementosGUI.append(switchVolumen)
        self.elementosGUI.append(botonVolverAtras)
        # Creamos el texto y lo metemos en la lista
        textoVolumen = TextoMusicaMenu(self)
        textoArrowsWASD = TextoArrowsWASDMenu(self)
        textVolverAtras = TextoVolverMenuPrincipal(self)
        self.elementosGUI.append(textoVolumen)
        self.elementosGUI.append(textoArrowsWASD)
        self.elementosGUI.append(textVolverAtras)


class PantallaCreditosGUI(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'desert-pixel-placeholder.png')
        # Creamos los botones y los metemos en la lista
        botonVolverAtras = BotonVolverMenuInicial(self)
        self.elementosGUI.append(botonVolverAtras)
        # Creamos el texto y lo metemos en la lista
        textoCreditos = TextoContenidoCreditos(self)
        textVolverAtras = TextoVolverMenuPrincipal(self)
        self.elementosGUI.append(textoCreditos)
        self.elementosGUI.append(textVolverAtras)
        

# -------------------------------------------------
# Clase Menu, la escena en sí

class Menu(Escena):

    def __init__(self, director):
        # Llamamos al constructor de la clase padre
        Escena.__init__(self, director)
        # Creamos la lista de pantallas
        self.listaPantallas = []
        # Creamos las pantallas que vamos a tener
        #   y las metemos en la lista
        self.listaPantallas.append(PantallaInicialGUI(self))
        self.listaPantallas.append(PantallaConfiguracionGUI(self))
        self.listaPantallas.append(PantallaCreditosGUI(self))
        # En que pantalla estamos actualmente
        self.mostrarPantallaInicial()

    def update(self, *args):
        return

    def eventos(self, lista_eventos):
        # Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    self.salirPrograma()
            elif evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def dibujar(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)

    #--------------------------------------
    # Metodos propios del menu

    def salirPrograma(self):
        self.director.salirPrograma()

    def ejecutarJuego(self):
        global movement_option
        pygame.mixer.music.stop()
        game = GameManager(mov_opt=movement_option)
        game.run()

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0

    def mostrarPantallaConfiguracion(self):
        self.pantallaActual = 1

    def mostrarPantallaCreditos(self):
        self.pantallaActual = 2
        
    # Function for the Splash Screen
    def splash_screen(self, screen, wait_seconds):
        # Get user screen size
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        # Loads the image
        splash_image = pygame.image.load("assets\splash_screen_placeholder.jpeg")
        splash_image = pygame.transform.scale(splash_image, (screen_width, screen_height))

        # Draws the splash screen image
        screen.blit(splash_image, (0, 0))

        # Updates the screen
        pygame.display.flip()

        # Waits until the user interacts (or the time ends)
        start_time = time.time()
        running = True
        while running and time.time() - start_time < wait_seconds:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = False

            # Limits to 60fps
            pygame.time.delay(1000 // 60)       
        
if __name__ == '__main__':

    # Inicializamos la libreria de pygame
    pygame.init()
    # Creamos el director
    director = Director()
    # Creamos la escena con la pantalla inicial
    escena = Menu(director)
    # Le decimos al director que apile esta escena
    director.apilarEscena(escena)
    # Inicialize the music mixer
    pygame.mixer.init()
    # Loads and reproduce music 
    pygame.mixer.music.load('assets/fall-from-grace.mp3')   #HAY QUE METER EL COPYRIGHT EN CREDITOS
    pygame.mixer.music.play(-1)  # -1 to infinity music
    # Ejecutamos la Splash Screen
    escena.splash_screen(director.screen, 10)
    # Y ejecutamos el juego
    director.ejecutar()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()