from moderngl import VertexArray
import modules.window as wnd
import modules.utils as util

class NewWindow(wnd.ProgramWindow):
    title = "Template #1 - Skeleton"
    shaderFolder = "shaders/"
    shaderPaths = {
        "vertex_shader":   "vert.glsl",
        "fragment_shader": "frag.glsl"
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_shaders(self) -> wnd.Shaders:
        for key, value in self.shaderPaths.items():
            self.shaderPaths[key] = util.add_abs_path(__file__, self.shaderFolder + value)
        return wnd.Shaders(**self.shaderPaths)
    def get_vao(self) -> VertexArray:
        return self.ctx.vertex_array(self.prog, [])
    def on_render(self, time: float, frametime: float):
        self.ctx.clear(0.0, 0.0, 0.1)