from moderngl import VertexArray
from modules.window import Shaders, ProgramWindow
import modules.utils as util

class GLWindow(ProgramWindow):
    title = "Template #2 - Basic"
    shaderFolder = "shaders/"
    shaderPaths = {
        "vertex_shader":   "vert.glsl",
        "fragment_shader": "frag.glsl"
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_shaders(self) -> Shaders:
        fullShaderPaths = {}
        for key, value in self.shaderPaths.items():
            fullShaderPaths[key] = util.add_abs_path(__file__, self.shaderFolder + value)
        return Shaders(**fullShaderPaths)
    def get_vao(self) -> VertexArray:
        return self.ctx.vertex_array(self.prog, [])
    def on_render(self, time: float, frametime: float):
        self.ctx.clear(0.0, 0.0, 0.1)
        self.vao.render(mode=self.ctx.TRIANGLES, vertices=3)