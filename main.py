# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, absolute_import,
                        print_function, division)


# intersection ligne et plan :
# http://geomalgorithms.com/a05-_intersect-1.html
# http://mathworld.wolfram.com/CrossProduct.html

# transformation d'un point cliqué à l'écran en rayon.
# http://myweb.lmu.edu/dondi/share/cg/unproject-explained.pdf

import math
import itertools

import pyglet
pgl = pyglet.gl

from bat_belt import ctype_array, group2
from vector3D import Vector3D
from camera import Camera

# Disable error checking for increased performance
#pyglet.options['debug_gl'] = False

def build_mesh_rainbow_cube():

    coords_cube = (
        (1, 1, 1), 
        (-1, 1, 1), 
        (-1, -1, 1), 
        (1, -1, 1), 
        (1, 1, -1), 
        (-1, 1, -1), 
        (-1, -1, -1), 
        (1, -1, -1), 
    )

    colors_cube = (
        (1.0, 1.0, 1.0),
        (1.0, 1.0, 0.2),
        (1.0, 0.2, 0.2),
        (1.0, 0.2, 1.0),
        (0.2, 1.0, 1.0),
        (0.2, 1.0, 0.2),
        (0.2, 0.2, 0.2),
        (0.2, 0.2, 1.0),
    )

    indexes_vertex_cube = (
        0, 1, 2, 3, # front face
        0, 4, 5, 1, # top face
        4, 0, 3, 7, # right face
        1, 5, 6, 2, # left face
        3, 2, 6, 7, # bottom face
        4, 7, 6, 5, # back face
    )

    indexes_vertex_cube_grouped_by_plane = group2(indexes_vertex_cube, 4)
    grouping_plane_to_triangles = (0, 1, 2, 0, 2, 3)    
    mesh_vertices = []
    mesh_colors = []
    for indexes_one_plane in indexes_vertex_cube_grouped_by_plane:
        indexes_grouped_by_triangles = (
            indexes_one_plane[grouping_modification]
            for grouping_modification
            in grouping_plane_to_triangles)
        for one_index in indexes_grouped_by_triangles:
            coords_vertex = coords_cube[one_index]
            mesh_vertices.extend(coords_vertex)
            color = colors_cube[one_index]
            mesh_colors.extend(color)

    mesh_glfloat_vertices = ctype_array(pgl.GLfloat, *mesh_vertices)
    mesh_glfloat_colors = ctype_array(pgl.GLfloat, *mesh_colors)
    return mesh_glfloat_vertices, mesh_glfloat_colors
    

def build_mesh_icosahedron():
    
    h_prime_sqr = math.sin(math.pi / 10.0) * math.sin((3.0 * math.pi) / 10.0)
    h_prime = math.sqrt(h_prime_sqr)
    h_second_sqr = 1.0 - (0.25 / (math.sin(math.pi/5)) ** 2)
    h_second = math.sqrt(h_second_sqr)

    coords_crown_up = [
        (
            math.cos((k * math.pi) / 5),
            -h_prime,
            math.sin((k * math.pi) / 5))
        for k in (0, 2, 4, 6, 8)
    ]

    coords_crown_down = [
        (
            math.cos((k * math.pi) / 5),
            +h_prime,
            math.sin((k * math.pi) / 5))
        for k in (1, 3, 5, 7, 9)
    ]

    coords_icosahedron = list(itertools.chain(
        [ (0.0, -h_prime - h_second, 0.0) ],
        coords_crown_up,
        coords_crown_down,
        [ (0.0, +h_prime + h_second, 0.0) ]))

    indexes_vertex_and_colors_icosahedron = (
        # couronne du haut
        ((0, 1, 2),   (1.0, 1.0, 1.0, )),
        ((0, 2, 3),   (0.9, 0.9, 0.9, )),
        ((0, 3, 4),   (0.8, 0.8, 0.8, )),
        ((0, 4, 5),   (0.7, 0.7, 0.7, )),
        ((0, 5, 1),   (0.9, 0.9, 0.9, )),
        # bande du milieu (triangle groupe 1)
        ((1, 2, 6),   (0.7, 1.0, 0.7, )),
        ((2, 3, 7),   (0.6, 1.0, 0.6, )),
        ((3, 4, 8),   (0.5, 1.0, 0.5, )),
        ((4, 5, 9),   (0.4, 1.0, 0.4, )),
        ((5, 1, 10),  (0.6, 1.0, 0.6, )),
        # bande du milieu (triangle groupe 2)
        ((6, 7, 2),   (0.3, 1.0, 0.3, )),
        ((7, 8, 3),   (0.2, 1.0, 0.2, )),
        ((8, 9, 4),   (0.1, 1.0, 0.1, )),
        ((9, 10, 5),  (0.0, 1.0, 0.0, )),
        ((10, 6, 1),  (0.2, 1.0, 0.2, )),
        # couronne du bas
        ((11, 6, 7),  (0.0, 0.9, 0.0, )),
        ((11, 7, 8),  (0.0, 0.8, 0.0, )),
        ((11, 8, 9),  (0.0, 0.7, 0.0, )),
        ((11, 9, 10), (0.0, 0.6, 0.0, )),
        ((11, 10, 6), (0.0, 0.8, 0.0, )),
    )

    mesh_vertices = []
    mesh_colors = []
    for indexes, color in indexes_vertex_and_colors_icosahedron:
        for one_index in indexes:
            coords_one_vertex = coords_icosahedron[one_index]
            mesh_vertices.extend(coords_one_vertex)
        for _ in range(3):
            mesh_colors.extend(color)

    mesh_glfloat_vertices = ctype_array(pgl.GLfloat, *mesh_vertices)
    mesh_glfloat_colors = ctype_array(pgl.GLfloat, *mesh_colors)
    return mesh_glfloat_vertices, mesh_glfloat_colors


class WindowGeodeSweeper(pyglet.window.Window):

    def init_geode_sweeper(self, mesh_glfloat_vertices, mesh_glfloat_colors):
        self.mesh_glfloat_vertices = mesh_glfloat_vertices
        self.mesh_glfloat_colors = mesh_glfloat_colors
        self.cam = Camera()

    def on_resize(self, width, height):
        pgl.glViewport(0, 0, width, height)
        pgl.glMatrixMode(pgl.GL_PROJECTION)
        pgl.glLoadIdentity()
        # TODO : width/height
        pgl.gluPerspective(40.0, 1.0, 1.0, 40.0)
        return pyglet.event.EVENT_HANDLED

    def on_draw(self):

        # TODO : on n'a besoin de le faire qu'une fois au début, ça.
        pgl.glEnable(pgl.GL_DEPTH_TEST)

        pgl.glClearColor(0.0, 0.0, 0.0, 1)
        pgl.glClear(pgl.GL_COLOR_BUFFER_BIT | pgl.GL_DEPTH_BUFFER_BIT)

        pgl.glMatrixMode(pgl.GL_MODELVIEW)
        pgl.glLoadIdentity()
        pgl.gluLookAt(
            self.cam.x * 15, self.cam.y * 15, self.cam.z * 15,
            0, 0, 0,
            self.cam.v_up.x, self.cam.v_up.y, self.cam.v_up.z)
        pgl.glScalef(3.0, 3.0, 3.0)

        pgl.glEnableClientState(pgl.GL_VERTEX_ARRAY)
        pgl.glEnableClientState(pgl.GL_COLOR_ARRAY)

        pgl.glColorPointer(3, pgl.GL_FLOAT, 0, self.mesh_glfloat_colors)
        pgl.glVertexPointer(3, pgl.GL_FLOAT, 0, self.mesh_glfloat_vertices)
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
            len(self.mesh_glfloat_vertices) // 3)

        pgl.glDisableClientState(pgl.GL_COLOR_ARRAY)
        pgl.glDisableClientState(pgl.GL_VERTEX_ARRAY)

    def on_key_press(self, symbol, modifiers):
        # TODO : dict touche -> fonction.
        if symbol == pyglet.window.key.RIGHT:
            self.cam.delta_x = 0.05
        elif symbol == pyglet.window.key.LEFT:
            self.cam.delta_x = -0.05
        if symbol == pyglet.window.key.UP:
            self.cam.delta_y = -0.05
        elif symbol == pyglet.window.key.DOWN:
            self.cam.delta_y = 0.05
        elif symbol == pyglet.window.key.ESCAPE:
            self.close()

    def on_key_release(self, symbol, modifiers):
        if symbol in (pyglet.window.key.RIGHT, pyglet.window.key.LEFT):
            self.cam.delta_x = 0.0
        if symbol in (pyglet.window.key.UP, pyglet.window.key.DOWN):
            self.cam.delta_y = 0.0

    def update(self, dt):
        if self.cam.delta_x != 0.0:
            self.cam.slide_lateral(self.cam.delta_x)
        if self.cam.delta_y != 0.0:
            self.cam.slide_longitudinal(self.cam.delta_y)


windowGeodeSweeper = WindowGeodeSweeper(
    fullscreen=False, vsync=False, resizable=True,
    height=600, width=600)

mesh_glfloat_vertices, mesh_glfloat_colors = build_mesh_rainbow_cube()
#mesh_glfloat_vertices, mesh_glfloat_colors = build_mesh_icosahedron()
windowGeodeSweeper.init_geode_sweeper(
    mesh_glfloat_vertices,
    mesh_glfloat_colors)

# On peut diminuer le 0.01 pour avoir une animation plus rapide.
pyglet.clock.schedule_interval(windowGeodeSweeper.update, 0.01)
pyglet.app.run()
