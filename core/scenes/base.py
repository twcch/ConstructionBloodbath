class BaseScene:
    def __init__(self, app):
        self.app = app
    def enter(self):
        pass
    def exit(self):
        pass
    def handle_event(self, event):
        pass
    def update(self, dt: float):
        pass
    def draw(self, surface):
        pass
