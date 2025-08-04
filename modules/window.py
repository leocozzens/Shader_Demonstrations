import moderngl_window as mglw
from moderngl import VertexArray
from abc import abstractmethod

class Shaders:
    def __init__(self, **kwargs):
        self.shaderData = {}
        for key, value in kwargs.items():
            shaderFile = open(value, "r")
            self.shaderData[key] = shaderFile.read()
            shaderFile.close()
    def get_data(self) -> dict:
        return self.shaderData

class ProgramWindow(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (800, 600)
    resizable = True
    aspect_ratio = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prog = self.ctx.program(**self.get_shaders().get_data())
        self.texture = self.ctx.texture(self.wnd.size, 4)
        self.vao = self.get_vao()

    def on_resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, width, height)
        self.texture = self.ctx.texture(self.wnd.size, 4)

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys
        if key == keys.ESCAPE and action == keys.ACTION_PRESS:
            self.on_close()

    def on_close(self):
        if not self.wnd.is_closing:
            self.wnd.close()

    @abstractmethod
    def get_shaders(self) -> Shaders:
        pass
    @abstractmethod
    def empty_shaders(self):
        pass
    @abstractmethod
    def get_vao(self) -> VertexArray:
        pass
    @abstractmethod
    def on_render(self, time: float, frametime: float):
        pass