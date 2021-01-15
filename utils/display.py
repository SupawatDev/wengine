from utils.obj_reader import obj_reader
import ipyvolume as ipv
import pythreejs as p3js
import ipywidgets as widgets
import numpy as np

class Display:
    def __init__(self, scene_path):
        self.figure = ipv.figure(width=800,height=600)
        self.control = p3js.OrbitControls(controlling=self.figure.camera)
        self.control.autoRotate = True
        self.control.autoRotateSpeed = 0.1
        self.figure.render_continuous = True
        # TODO[x][x]: Prepare Scene
        self.scene = None
        self.scene_path = scene_path
        self.ues = None
        self.bss = None

    # TODO[x]: Render Scene
    @staticmethod
    def show():
        ipv.show()

    def make_scene(self):
        vertices, triangles = obj_reader(self.scene_path)
        x = vertices[:, 0]
        y = vertices[:, 1]
        z = vertices[:, 2]
        self.scene = ipv.plot_trisurf(x,y,z, triangles=triangles, color='#4cc9f0')
        return

    # TODO[]: Add UEs to the plot
    def add_ue(self, x_list, y_list, z_list):
        self.ues = ipv.scatter(np.array(x_list), np.array(y_list), np.array(z_list), size=1, color="#480ca8")
        return

    def add_bs(self, x_list, y_list, z_list):
        self.bss = ipv.scatter(np.array(x_list), np.array(y_list), np.array(z_list), size=1 ,color="#f72585")
        return

    def run(self, ues = None, bss=None):
        self.clear()
        self.figure = ipv.figure(width=800,height=600)
        self.control = p3js.OrbitControls(controlling=self.figure.camera)
        self.control.autoRotate = True
        self.control.autoRotateSpeed = 0.1
        self.figure.render_continuous = True
        ipv.style.use('minimal')
        ipv.xlim(-170, 170)
        ipv.zlim(-170, 170)
        ipv.ylim(-170, 170)
        if ues is not None:
            self.add_ue(ues[0], ues[1], ues[2])
        if bss is not None:
            self.add_bs(bss[0], bss[1], bss[2])
        self.make_scene()
        ipv.show()

    @staticmethod
    def clear():
        ipv.clear()

    def zoom_button(self):
        def zoom(zoom):
            self.figure.camera.zoom = zoom
            return zoom
        print("Zoom in/out")
        widgets.interact(zoom, zoom=widgets.IntSlider(min=1, max=20,
                                                      step=1, value=self.figure.camera.zoom))
        return
