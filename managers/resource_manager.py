import os
import pygame
from pygame.locals import *


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        RESOURCE MANAGER                                       #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class ResourceManager(object):
    resources = {}

    @classmethod
    def load_image(cls, name: str, color_key: int = None):
        if name in cls.resources:
            return cls.resources[name]
        else:
            full_name = os.path.join(name)
            try:
                image = pygame.image.load(full_name)
            except pygame.error as e:
                print('Cannot load image:', full_name)
                raise SystemExit(e)

            image = image.convert()

            if color_key is not None:
                if color_key == -1:
                    color_key = image.get_at((0, 0))
                image.set_colorkey(color_key, RLEACCEL)

            cls.resources[name] = image

            return image

    @classmethod
    def load_coordinates(cls, name):
        if name in cls.resources:
            return cls.resources[name]
        else:
            full_name = os.path.join('managers/deprecated_images', name)  # TODO: Check if this works
            path_file = open(full_name, 'r')

            data = path_file.read()
            path_file.close()

            cls.resources[name] = data

            return data
