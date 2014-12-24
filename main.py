# -*- coding: utf-8 -*-

from __future__ import unicode_literals



# intersection ligne et plan :
# http://geomalgorithms.com/a05-_intersect-1.html
# http://mathworld.wolfram.com/CrossProduct.html

# transformation d'un point cliqué à l'écran en rayon.
# http://myweb.lmu.edu/dondi/share/cg/unproject-explained.pdf

import math
import itertools

import pyglet
pgl = pyglet.gl

# Disable error checking for increased performance
#pyglet.options['debug_gl'] = False


win = pyglet.window.Window(
    fullscreen=False, vsync=False, resizable=True,
    height=600, width=600)

class Vector3D(object):

    # TODO : trouver une putain de classe vecteur toute faite.
    # Je vais pas me faire chier à tout recoder.

    def __init__(self, x, y, z):
        # TODO : transformer en float.
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "".join((
            "vect :",
            " x:", str(self.x),
            " y:", str(self.y),
            " z:", str(self.z),
        ))

    def normify(self):
        current_norm = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        self.x /= current_norm
        self.y /= current_norm
        self.z /= current_norm

    def cross_product(self, v_other):

        u1 = self.x
        u2 = self.y
        u3 = self.z
        v1 = v_other.x
        v2 = v_other.y
        v3 = v_other.z

        prod_x = u2*v3 - u3*v2
        prod_y = u3*v1 - u1*v3
        prod_z = u1*v2 - u2*v1

        # http://en.wikipedia.org/wiki/Cross_product
        return Vector3D(prod_x, prod_y, prod_z)

# TODO : mettre ça dans des tests unitaires.
test_normify = Vector3D(1.0, 2.0, 3.0)
print "test_normify: ", test_normify
test_normify.normify()
print "test_normify normé: ", test_normify

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
        print "up : ", self.v_up
        print "left : ", self.v_front.cross_product(self.v_up)

    def _refresh_vfront(self):
        self.v_front = Vector3D(-self.x, -self.y, -self.z)
        self.v_front.normify()

    def _get_back_to_sphere(self):
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

cam = Camera()


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
print "h_second_sqr", h_second_sqr
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
#icosahedron_list_vertices = list(itertools.chain.from_iterable(icosahedron_list_coord))


icosahedron_list_colors = (
    # haut
    1.0, 1.0, 1.0,
    # couronne du haut
    0.7, 0.7, 0.7,
    0.0, 0.7, 0.0,
    0.7, 0.7, 0.7,
    0.0, 0.7, 0.0,
    0.0, 0.7, 0.7,
    # couronne du bas
    0.3, 0.3, 0.3,
    0.0, 0.3, 0.0,
    0.3, 0.3, 0.3,
    0.0, 0.3, 0.0,
    0.0, 0.3, 0.3,
    # bas
    0.1, 0.1, 0.1,
)

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
    return itertools.imap(None, *([ iter(iterator) ] * count))

solid_vertices = vector(pgl.GLfloat, *list_plane_vertices)
solid_colors = vector(pgl.GLfloat, *list_plane_colors)
#solid_vertices = (GLfloat * len(list_plane_vertices))(*list_plane_vertices)
#solid_colors = (GLfloat * len(list_plane_colors))(*list_plane_colors)


@win.event
def on_resize(width, height):
    pgl.glViewport(0, 0, width, height)
    pgl.glMatrixMode(pgl.GL_PROJECTION)
    pgl.glLoadIdentity()
    # TODO : width/height
    pgl.gluPerspective(40.0, 1.0, 1.0, 40.0)
    return pyglet.event.EVENT_HANDLED

@win.event
def on_draw():

    pgl.glClearColor(0.0, 0.0, 0.0, 1)
    pgl.glClear(pgl.GL_COLOR_BUFFER_BIT | pgl.GL_DEPTH_BUFFER_BIT)

    pgl.glMatrixMode(pgl.GL_MODELVIEW)
    pgl.glLoadIdentity()
    pgl.gluLookAt(cam.x * 15, cam.y * 15, cam.z * 15,   0, 0, 0,   cam.v_up.x, cam.v_up.y, cam.v_up.z)
    pgl.glScalef(3.0, 3.0, 3.0)

    pgl.glEnableClientState(pgl.GL_VERTEX_ARRAY)
    pgl.glEnableClientState(pgl.GL_COLOR_ARRAY)

    pgl.glColorPointer(3, pgl.GL_FLOAT, 0, solid_colors)
    pgl.glVertexPointer(3, pgl.GL_FLOAT, 0, solid_vertices)
    # glDrawElements(
    #     GL_TRIANGLES, len(solid_index_for_planes),
    #     GL_UNSIGNED_INT, solid_index_for_planes)

    # Attention au dernier param ! On n'indique pas le nombre d'élément du tableau, mais le nombre d'objets qu'on veut dessiner.
    # C'est pas comme glDrawElements.
    pgl.glDrawArrays(pgl.GL_TRIANGLES, 0, len(solid_vertices) // 3)

    pgl.glDisableClientState(pgl.GL_COLOR_ARRAY)
    pgl.glDisableClientState(pgl.GL_VERTEX_ARRAY)

@win.event
def on_key_press(symbol, modifiers):
    # TODO : dict avec un vecteur de déplacement ou autre chose.
    if symbol == pyglet.window.key.RIGHT:
        cam.delta_x = 0.05
    elif symbol == pyglet.window.key.LEFT:
        cam.delta_x = -0.05
    if symbol == pyglet.window.key.UP:
        cam.delta_y = -0.05
    elif symbol == pyglet.window.key.DOWN:
        cam.delta_y = 0.05

@win.event
def on_key_release(symbol, modifiers):
    if symbol in (pyglet.window.key.RIGHT, pyglet.window.key.LEFT):
        cam.delta_x = 0.0
    if symbol in (pyglet.window.key.UP, pyglet.window.key.DOWN):
        cam.delta_y = 0.0

def update(dt):
    if cam.delta_x != 0.0:
        cam.slide_lateral(cam.delta_x)
    if cam.delta_y != 0.0:
        cam.slide_longitudinal(cam.delta_y)

pgl.glEnable(pgl.GL_DEPTH_TEST)

# Diminuer le 0.01 pour avoir une animation plus rapide.
pyglet.clock.schedule_interval(update, 0.01)
pyglet.app.run()
