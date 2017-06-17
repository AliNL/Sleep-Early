from appJar import gui


class Window(object):
    def __init__(self, app=None):
        if app:
            self.app = app
        else:
            self.app = gui("护肝宝")
        self.app.setFont(14)
        self.app.setGuiPadding(50, 50)
        self.app.setInPadding(5, 5)
        self.app.setSticky("ew")
        self.app.disableWarnings()
