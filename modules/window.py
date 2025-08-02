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
    # TODO: Add resize callback

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prog = self.ctx.program(**self.get_shaders().get_data())
        self.texture = self.ctx.texture(self.wnd.size, 4)
        self.vao = self.get_vao()

    @abstractmethod
    def get_shaders(self) -> Shaders:
        pass
    @abstractmethod
    def get_vao(self) -> VertexArray:
        pass
    @abstractmethod
    def on_render(self, time: float, frametime: float):
        pass