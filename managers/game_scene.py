
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        SCENE PROTOTYPE                                        #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class Scene:
    def __init__(self, manager):
        self.manager = manager

    def update(self, *args):
        raise NotImplemented("Not implemented here.")

    def events(self, *args):
        raise NotImplemented("Not implemented here.")

    def draw(self, screen):
        raise NotImplemented("Not implemented here.")
