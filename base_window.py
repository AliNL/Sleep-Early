from appJar import gui


class Window(object):
    def __init__(self):
        self.app = gui("护肝宝", "500x300")
        self.app.setFont(14)
        self.app.setGuiPadding(50, 50)
        self.app.setInPadding(5, 5)
        self.app.setSticky("ew")
