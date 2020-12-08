from utils.obj_reader import obj_reader
import ipyvolume as ipv
import pythreejs as p3js
import ipywidgets as widgets


class Display:
    def __init__(self, scene_path):
        self.figure = ipv.figure(width=800,height=600)
        self.control = p3js.OrbitControls(controlling=self.figure.camera)
        self.control.autoRotate = True
        self.control.autoRotateSpeed = 0.1
        self.figure.render_continuous = True
        # TODO[x]: Prepare Scene
        self.scene = None
        self.make_scene()

    # TODO[x]: Render Scene
    @staticmethod
    def show():
        ipv.show()

    def make_scene(self, scene_path):
        vertices, triangles = obj_reader(scene_path)
        x = vertices[:, 0]
        y = vertices[:, 1]
        z = vertices[:, 2]
        self.scene = self.ipv.plot_trisuft(x,y,z, triangles=triangles, color='#06d6a0')
        return

    def zoom_button(self):
        def zoom(zoom):
            self.figure.camera.zoom = zoom
            return zoom
        print("Zoom in/out")
        widgets.interact(zoom, zoom=widgets.IntSlider(min=1, max=20, step=1, value=self.figure.camera.zoom))
        return
