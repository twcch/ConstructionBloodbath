class SceneManager:
    def __init__(self):
        self._scenes = {}
        self.current = None

    def register(self, name: str, scene):
        self._scenes[name] = scene

    def change(self, name: str):
        if self.current and hasattr(self.current, 'exit'):
            self.current.exit()
        self.current = self._scenes[name]
        if hasattr(self.current, 'enter'):
            self.current.enter()
