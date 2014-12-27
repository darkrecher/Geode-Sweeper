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

    def init_geode_sweeper(self, mesh):
        self.mesh = mesh
        self.cam = CameraAroundSphere()
        pgl.glEnable(pgl.GL_DEPTH_TEST)

    def on_resize(self, width, height):
        pgl.glViewport(0, 0, width, height)
        pgl.glMatrixMode(pgl.GL_PROJECTION)
        pgl.glLoadIdentity()
        # TODO : width/height
        pgl.gluPerspective(40.0, 1.0, 1.0, 40.0)
        return pyglet.event.EVENT_HANDLED

    def on_draw(self):

        pgl.glClearColor(0.0, 0.0, 0.0, 1)
        pgl.glClear(pgl.GL_COLOR_BUFFER_BIT | pgl.GL_DEPTH_BUFFER_BIT)

        pgl.glMatrixMode(pgl.GL_MODELVIEW)
        pgl.glLoadIdentity()
        pgl.gluLookAt(
            self.cam.pos.x * 15, self.cam.pos.y * 15, self.cam.pos.z * 15,
            self.cam.lookat.x, self.cam.lookat.y, self.cam.lookat.z,
            self.cam.v_up.x, self.cam.v_up.y, self.cam.v_up.z)
        pgl.glScalef(3.0, 3.0, 3.0)

        pgl.glEnableClientState(pgl.GL_VERTEX_ARRAY)
        pgl.glEnableClientState(pgl.GL_COLOR_ARRAY)

        pgl.glColorPointer(3, pgl.GL_FLOAT, 0, self.mesh.glfloat_colors)
        pgl.glVertexPointer(3, pgl.GL_FLOAT, 0, self.mesh.glfloat_vertices)
        # pgl.glDrawElements(
        #     pgl.GL_TRIANGLES, len(solid_index_for_planes),
        #     pgl.GL_UNSIGNED_INT, solid_index_for_planes)

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

    def on_key_press(self, symbol, modifiers):
        # TODO : dict touche -> fonction.
        if symbol == pyglet.window.key.RIGHT:
            self.cam.delta_lateral = 0.05
        elif symbol == pyglet.window.key.LEFT:
            self.cam.delta_lateral = -0.05
        if symbol == pyglet.window.key.UP:
            self.cam.delta_longitudinal = -0.05
        elif symbol == pyglet.window.key.DOWN:
            self.cam.delta_longitudinal = 0.05
        elif symbol == pyglet.window.key.ESCAPE:
            self.close()

    def on_key_release(self, symbol, modifiers):
        if symbol in (pyglet.window.key.RIGHT, pyglet.window.key.LEFT):
            self.cam.delta_lateral = 0.0
        if symbol in (pyglet.window.key.UP, pyglet.window.key.DOWN):
            self.cam.delta_longitudinal = 0.0

    def update(self, dt):
        self.cam.slide_with_deltas()


window_geode_sweeper = WindowGeodeSweeper(
    fullscreen=False, vsync=False, resizable=True,
    height=600, width=600)

