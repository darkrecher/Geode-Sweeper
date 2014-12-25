# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, absolute_import,
                        print_function, division)
import itertools
import math
import pyglet
pgl = pyglet.gl

from bat_belt import ctype_array, group2


class Mesh(object):

    def __init__(self):
        self.glfloat_vertices = ctype_array(pgl.GLfloat, *[])
        self.glfloat_colors = ctype_array(pgl.GLfloat, *[])


class MeshRainbowCube(Mesh):

    def __init__(self):

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

        self.glfloat_vertices = ctype_array(pgl.GLfloat, *mesh_vertices)
        self.glfloat_colors = ctype_array(pgl.GLfloat, *mesh_colors)
    

class MeshIcosahedron(Mesh):

    def __init__(self):
            
        h_prime_sqr = math.sin(math.pi/10.0) * math.sin((3.0*math.pi)/10.0)
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

        self.glfloat_vertices = ctype_array(pgl.GLfloat, *mesh_vertices)
        self.glfloat_colors = ctype_array(pgl.GLfloat, *mesh_colors)
