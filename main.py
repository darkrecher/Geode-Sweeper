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

from vector3D import Vector3D

# Disable error checking for increased performance
#pyglet.options['debug_gl'] = False


class Camera(object):

    def __init__(self):

        self.delta_x = 0.0
        self.delta_y = 0.0

        self.x = 0.0
        self.y = 0.0
        self.z = -1.0

        self.v_front = Vector3D(0.0, 0.0, 1.0)
        self.v_left = Vector3D(1.0, 0.0, 0.0)
        self.v_up = self.v_left.cross_product(self.v_front)

        # TODO : mettre ça dans des tests unitaires.
        print("up : ", self.v_up)
        print("left : ", self.v_front.cross_product(self.v_up))

    def _refresh_vfront(self):
        self.v_front = Vector3D(-self.x, -self.y, -self.z)
        self.v_front.normify()

    def _get_back_to_sphere(self):
        # TODO : c'est pas plus simple de définir directement les xyz à -v_front ?
        v_pos_to_center = Vector3D(-self.x, -self.y, -self.z)
        v_pos_to_sphere = Vector3D(
            v_pos_to_center.x - self.v_front.x,
            v_pos_to_center.y - self.v_front.y,
            v_pos_to_center.z - self.v_front.z)
        self.x += v_pos_to_sphere.x
        self.y += v_pos_to_sphere.y
        self.z += v_pos_to_sphere.z

    def slide_lateral(self, dist):
        self.x += self.v_left.x * dist
        self.y += self.v_left.y * dist
        self.z += self.v_left.z * dist
        self._refresh_vfront()
        self._get_back_to_sphere()
        self.v_left = self.v_front.cross_product(self.v_up)

    def slide_longitudinal(self, dist):
        self.x += self.v_up.x * dist
        self.y += self.v_up.y * dist
        self.z += self.v_up.z * dist
        self._refresh_vfront()
        self._get_back_to_sphere()
        self.v_up = self.v_left.cross_product(self.v_front)



def vector(gl_type, *args):
    '''
        return a ctype array
        GLfloat
        GLuint
        ...
    '''
    return (gl_type*len(args))(*args)

cube_list_vertices = (
    1, 1, 1, #0
    -1, 1, 1, #1
    -1, -1, 1, #2
    1, -1, 1, #3
    1, 1, -1, #4
    -1, 1, -1, #5
    -1, -1, -1, #6
    1, -1, -1 #7
)

cube_list_colors = (
    1.0, 1.0, 1.0,
    1.0, 1.0, 0.2,
    1.0, 0.2, 0.2,
    1.0, 0.2, 1.0,
    0.2, 1.0, 1.0,
    0.2, 1.0, 0.2,
    0.2, 0.2, 0.2,
    0.2, 0.2, 1.0,
)

cube_list_index_for_planes = (
    0, 1, 2, 3, # front face
    0, 4, 5, 1, # top face
    4, 0, 3, 7, # right face
    1, 5, 6, 2, # left face
    3, 2, 6, 7, # bottom face
    4, 7, 6, 5, # back face
)

h_prime_sqr = math.sin(math.pi / 10.0) * math.sin((3.0 * math.pi) / 10.0)
h_prime = math.sqrt(h_prime_sqr)

h_second_sqr = 1.0 - (0.25 / (math.sin(math.pi/5)) ** 2)
print("h_second_sqr", h_second_sqr)
h_second = math.sqrt(h_second_sqr)

list_coord_crown_up = [
    (
        math.cos((k * math.pi) / 5),
        -h_prime,
        math.sin((k * math.pi) / 5))
    for k in (0, 2, 4, 6, 8)
]

list_coord_crown_down = [
    (
        math.cos((k * math.pi) / 5),
        +h_prime,
        math.sin((k * math.pi) / 5))
    for k in (1, 3, 5, 7, 9)
]

icosahedron_list_coord = [ (0.0, -h_prime - h_second, 0.0) ] + list_coord_crown_up + list_coord_crown_down + [ (0.0, +h_prime + h_second, 0.0) ]

icosahedron_list_index_vertices_and_colors = (
    # couronne du haut
    (0, 1, 2, 1.0, 1.0, 1.0, ),
    (0, 2, 3, 0.9, 0.9, 0.9, ),
    (0, 3, 4, 0.8, 0.8, 0.8, ),
    (0, 4, 5, 0.7, 0.7, 0.7, ),
    (0, 5, 1, 0.9, 0.9, 0.9, ),
    # bande du milieu (triangle groupe 1)
    (1, 2, 6,  0.7, 1.0, 0.7, ),
    (2, 3, 7,  0.6, 1.0, 0.6, ),
    (3, 4, 8,  0.5, 1.0, 0.5, ),
    (4, 5, 9,  0.4, 1.0, 0.4, ),
    (5, 1, 10, 0.6, 1.0, 0.6, ),
    # bande du milieu (triangle groupe 2)
    (6, 7, 2,  0.3, 1.0, 0.3, ),
    (7, 8, 3,  0.2, 1.0, 0.2, ),
    (8, 9, 4,  0.1, 1.0, 0.1, ),
    (9, 10, 5, 0.0, 1.0, 0.0, ),
    (10, 6, 1, 0.2, 1.0, 0.2, ),
    # couronne du bas
    (11, 6, 7,  0.0, 0.9, 0.0, ),
    (11, 7, 8,  0.0, 0.8, 0.0, ),
    (11, 8, 9,  0.0, 0.7, 0.0, ),
    (11, 9, 10, 0.0, 0.6, 0.0, ),
    (11, 10, 6, 0.0, 0.8, 0.0, ),
)

list_plane_vertices = []
list_plane_colors = []

for elem in icosahedron_list_index_vertices_and_colors:
    indexes = elem[0:3]
    color = elem[3:]
    for vertex_index in indexes:
        vertex = icosahedron_list_coord[vertex_index]
        for coord in vertex:
            list_plane_vertices.append(coord)
    for _ in range(3):
        for color_coord in color:
            list_plane_colors.append(color_coord)

# TODO : à mettre dans une bat belt ou quelque chose comme ça.
def group2(iterator, count):
    """
    Prend ce qui sort de iterator, et en Fait des paquets de "count" elements.
    """
    return itertools.imap(None, *([ iter(iterator) ] * count))

solid_vertices = vector(pgl.GLfloat, *list_plane_vertices)
solid_colors = vector(pgl.GLfloat, *list_plane_colors)
#solid_vertices = (GLfloat * len(list_plane_vertices))(*list_plane_vertices)
#solid_colors = (GLfloat * len(list_plane_colors))(*list_plane_colors)

class WindowGeodeSweeper(pyglet.window.Window):

    def init_geode_sweeper(self, solid_vertices, solid_colors):
        self.solid_vertices = solid_vertices
        self.solid_colors = solid_colors
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

        pgl.glColorPointer(3, pgl.GL_FLOAT, 0, self.solid_colors)
        pgl.glVertexPointer(3, pgl.GL_FLOAT, 0, self.solid_vertices)
        # pgl.glDrawElements(
        #     pgl.GL_TRIANGLES, len(solid_index_for_planes),
        #     pgl.GL_UNSIGNED_INT, solid_index_for_planes)

        # Attention au dernier param ! On n'indique pas le nombre d'élément du tableau, mais le nombre d'objets qu'on veut dessiner.
        # C'est pas comme glDrawElements.
        pgl.glDrawArrays(pgl.GL_TRIANGLES, 0, len(solid_vertices) // 3)

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

windowGeodeSweeper.init_geode_sweeper(solid_vertices, solid_colors)

# On peut diminuer le 0.01 pour avoir une animation plus rapide.
pyglet.clock.schedule_interval(windowGeodeSweeper.update, 0.01)
pyglet.app.run()
