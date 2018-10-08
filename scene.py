class Scene:
    """Game scene template."""

    def __init__(self, director):
        self.director = director

    def keydown(self, key):
        pass

    def keyup(self, key):
        pass

    def mousebuttondown(self, button, position):
        pass

    def reset(self):
        pass

    def update(self):
        pass

    def render(self):
        pass
