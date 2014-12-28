# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

# intersection ligne et plan :
# http://geomalgorithms.com/a05-_intersect-1.html
# http://mathworld.wolfram.com/CrossProduct.html

# transformation d'un point cliqué à l'écran en rayon.
# http://myweb.lmu.edu/dondi/share/cg/unproject-explained.pdf

import pyglet
pgl = pyglet.gl

from vector3D import Vector3D
from camera import CameraAroundSphere

# Disable error checking for increased performance
#pyglet.options['debug_gl'] = False

# Plus cette valeur est petite, plus l'application sera rapide.
# (Si l'ordinateur est trop lent,
# ça ne sert à rien de mettre une valeur très faible).
PERIOD_GAME_CYCLE_SECONDS = 0.01

class WindowGeodeSweeper(pyglet.window.Window):

    # Diverses constantes, dont les valeurs ont été déterminées au feeling.

    # paramètres fovy, zNear, zFar.
    # Voir documentation de la fonction gluPerspective
    # https://www.opengl.org/sdk/docs/man2/xhtml/gluPerspective.xml
    FIELD_OF_VIEW_ANGLE_Y = 40.0
    Z_NEAR = 1.0
    Z_FAR = 40.0

    # Distance entre la caméra et le centre de l'espace O.
    # (La caméra se déplace sur une sphère centrée en O, de rayon DIST_CAM).
    DIST_CAM = 15

    # Facteur d'agrandissement des coordonnées de l'espace.
    SCALE_COORD = 3.0

    # Distance de déplacement orthogonal de la caméra, à chaque cycle.
    CAM_DELTA = 0.05

    def init_geode_sweeper(self, mesh):
        self.mesh = mesh
        self.cam = CameraAroundSphere()        
        pgl.glEnable(pgl.GL_DEPTH_TEST)        

    def on_resize(self, width, height):
        pgl.glViewport(0, 0, width, height)
        pgl.glMatrixMode(pgl.GL_PROJECTION)
        pgl.glLoadIdentity()
        if height != 0:
            pgl.gluPerspective(
                WindowGeodeSweeper.FIELD_OF_VIEW_ANGLE_Y,
                width / height,
                WindowGeodeSweeper.Z_NEAR,
                WindowGeodeSweeper.Z_FAR)
        return pyglet.event.EVENT_HANDLED

    def on_draw(self):

        pgl.glClearColor(0.0, 0.0, 0.0, 1)
        pgl.glClear(pgl.GL_COLOR_BUFFER_BIT | pgl.GL_DEPTH_BUFFER_BIT)

        pgl.glMatrixMode(pgl.GL_MODELVIEW)
        pgl.glLoadIdentity()
        pos_final = self.cam.pos * WindowGeodeSweeper.DIST_CAM
        pgl.gluLookAt(
            pos_final.x, pos_final.y, pos_final.z, 
            self.cam.lookat.x, self.cam.lookat.y, self.cam.lookat.z,
            self.cam.v_up.x, self.cam.v_up.y, self.cam.v_up.z)
        scale_coord = WindowGeodeSweeper.SCALE_COORD
        pgl.glScalef(scale_coord, scale_coord, scale_coord)

        pgl.glEnableClientState(pgl.GL_VERTEX_ARRAY)
        pgl.glEnableClientState(pgl.GL_COLOR_ARRAY)

        pgl.glColorPointer(3, pgl.GL_FLOAT, 0, self.mesh.glfloat_colors)
        pgl.glVertexPointer(3, pgl.GL_FLOAT, 0, self.mesh.glfloat_vertices)

        # Attention au dernier param !
        # On n'indique pas le nombre d'élément du tableau,
        # mais le nombre d'objets qu'on veut dessiner.
        # C'est pas comme la fonction glDrawElements.
        pgl.glDrawArrays(
            pgl.GL_TRIANGLES,
            0,
            len(self.mesh.glfloat_vertices) // 3)

        pgl.glDisableClientState(pgl.GL_COLOR_ARRAY)
        pgl.glDisableClientState(pgl.GL_VERTEX_ARRAY)

    def move_lat_right(self):
        self.cam.delta_lateral = WindowGeodeSweeper.CAM_DELTA
    def move_lat_left(self):
        self.cam.delta_lateral = -WindowGeodeSweeper.CAM_DELTA
    def move_longi_up(self):
        self.cam.delta_longitudinal = -WindowGeodeSweeper.CAM_DELTA
    def move_longi_down(self):
        self.cam.delta_longitudinal = WindowGeodeSweeper.CAM_DELTA

    def on_key_press(self, symbol, modifiers):
        function_from_key_pressed = {
            pyglet.window.key.RIGHT : self.move_lat_right,
            pyglet.window.key.LEFT : self.move_lat_left,
            pyglet.window.key.UP : self.move_longi_up,
            pyglet.window.key.DOWN : self.move_longi_down,
            pyglet.window.key.ESCAPE : self.close,
        }
        function_to_exec = function_from_key_pressed.get(symbol)
        if function_to_exec is not None:
            function_to_exec()

    def stop_move_lat(self):
        self.cam.delta_lateral = 0.0
    def stop_move_longi(self):
        self.cam.delta_longitudinal = 0.0

    def on_key_release(self, symbol, modifiers):
        function_from_key_released = {
            pyglet.window.key.RIGHT : self.stop_move_lat,
            pyglet.window.key.LEFT : self.stop_move_lat,
            pyglet.window.key.UP : self.stop_move_longi,
            pyglet.window.key.DOWN : self.stop_move_longi,
        }
        function_to_exec = function_from_key_released.get(symbol)
        if function_to_exec is not None:
            function_to_exec()

    def update(self, dt):
        self.cam.slide_with_deltas()


window_geode_sweeper = WindowGeodeSweeper(
    fullscreen=False, vsync=False, resizable=True,
    height=600, width=600)

