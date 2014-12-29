# -*- coding: utf-8 -*-

"""
Module contenant des classe Mesh.
Un Mesh permet de définir un objet 3D. (faces, coordonnées, couleurs)

La classe de base Mesh est dérivée en deux classes :
MeshRainbowCube et MeshIcosahedron.

Ces 3 classes définissent chacune un objet 3D spécifique.

Une classe Mesh doit contenir deux variables membres :
glfloat_vertices et glfloat_colors.
Ces deux variables sont des arrays ctype contenant des floats.
Les deux arrays doivent avoir le même nombre d'éléments. Ce nombre doit être
un multiple de 9.

Pour glfloat_vertices : un paquet de 9 valeurs correspond aux coordonnées
X, Y, Z de 3 points dans l'espace.
X1, Y1, Z1, X2, Y2, Z2, X3, Y3, Z3.
Ces 3 points définissent un triangle dans l'espace : une face de l'objet 3D.

Pour glfloat_colors : un paquet de 9 valeurs correspond à 3 couleurs RGB.
R1, G1, B1, R2, G2, B2, R3, G3, B3.
Chacune de ces 3 couleurs est à associer avec chacun des 3 points du triangle
correspondant dans glfloat_vertices.

Ces 3 couleurs permettent de savoir comment colorer la face de l'objet 3D.

Si les couleurs des 3 points sont égales, le triangle est de couleur unie.
Sinon, le triangle est dessiné avec un dégradé de couleur.
"""

from __future__ import (unicode_literals, absolute_import,
                        print_function, division)
import itertools
import math
import pyglet
pgl = pyglet.gl

from bat_belt import ctype_array, group2


class Mesh(object):
    """
    Mesh de base.
    Définit un objet 3D vide, n'ayant aucune face.
    les arrays glfloat_vertices et glfloat_colors contiennent 0 éléments.
    (Ce qui est une multiple de 9, hahaha).
    """
    def __init__(self):
        self.glfloat_vertices = ctype_array(pgl.GLfloat, *[])
        self.glfloat_colors = ctype_array(pgl.GLfloat, *[])


class MeshRainbowCube(Mesh):
    """
    Un cube "rainbow", avec des dégradés de couleur.
    Le cube est centré en (0, 0, 0), et fait 2 de côté.
    Les faces du cube sont perpendiculaires aux axes X, Y et Z.

    On associe toujours la même couleur à un sommet du cube,
    quel que soit la face d'appartenance.

    Chaque face du cube est composé de 2 triangles collés ensemble,
    qui forment un carré.
    Pour un triangle donné, les 3 couleurs de ses 3 sommets sont différentes.
    C'est ce qui fait les dégradés.
    """

    def __init__(self):

        # Coordonnées des 8 sommets du cube.
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

        # Couleurs des 8 sommets du cube.
        # (Listées dans le même ordre que coords_cube).
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

        # Index des sommets. Les éléments de cette liste sont à prendre par
        # paquet de 4. Chaque paquet définit une face du cube.
        # Chaque élément de cette liste est un index dans
        # coords_cube et colors_cube, permettant d'associer un sommet et sa
        # couleur à une face.
        indexes_vertex_cube = (
            0, 1, 2, 3, # front face
            0, 4, 5, 1, # top face
            4, 0, 3, 7, # right face
            1, 5, 6, 2, # left face
            3, 2, 6, 7, # bottom face
            4, 7, 6, 5, # back face
        )

        # Construction de glfloat_vertices et glfloat_colors à partir des
        # 3 listes ci-dessus.
        indexes_vertex_cube_grouped_by_plane = group2(indexes_vertex_cube, 4)
        # Pour chaque face, on doit faire 2 triangles.
        # grouping_plane_to_triangles défnit les index des sommets
        # de ces triangles, à prendre dans un paquet de 4 coordonnées.
        # 0, 1, 2 = le premier triangle.
        # 0, 2, 3 = le deuxième.
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
    """
    Un icosaèdre blanc au-dessus, vert clair au milieu, vert foncé en dessous.
    L'icosaèdre est posé sur un de ses sommets, et non pas une de ses arêtes.

    Les sommets et les faces sont organisés comme suit :
     - Un seul sommet tout en haut.
     - Un peu en dessous, 5 sommets répartis en pentagone. (pentagone_up)
     - On prend 2 sommets adjacents du pentagone, et le sommet du haut,
       pour créer une face.
       De cette manière, on crée 5 faces, appelée la couronne du haut.
     - Encore un peu en dessous, 5 autres sommets : pentagone_down.
       Mais ce second pentagone est tourné d'un dixième de tour par rapport
       au premier. Les points des deux pentagones ne sont donc pas
       les uns au-dessus au-dessus des autres.
     - On prend 2 sommets adjacents du pentagone du haut et un sommet du
       pentagone du bas pour créer une face.
       De cette manière, on crée 5 autres faces, appelées : le premier
       groupe de triangle de la bande du milieu.
     - On prend un sommet du pentagone du haut et 2 sommets adjacents du
       pentagone du bas pour créer une face.
       De cette manière, on crée 5 autres faces : le second groupe de
       triangle de la bande du milieu.
     - Tout en dessous, un dernier sommet.
     - On prend 2 sommets adjacents du pentagone du bas, et le sommet du bas,
       pour créer une face.
       De cette manière, on crée 5 dernières faces, appelée la couronne du bas.

    Chaque face est unie (les 3 points du triangle d'une face ont la même
    couleur). Un sommet n'a pas forcément la même couleur selon la face à
    laquelle on l'associe.
    Les faces de la couronne du haut sont gris clair.
    Les faces des deux groupes de triangles de la bande du milieu sont
    vert clair.
    Les faces de la couronne du bas sont vert foncé.
    """

    def __init__(self):

        # Calcul de l'altitude des sommets et des pentagones.
        # Je ne sais plus exactement comment j'ai calculé ça.
        # TODO : retrouver les shémas que j'avais fait au brouillon,
        # expliquer les calculs, et mettre tout ça comme doc du repository.
        h_prime_sqr = math.sin(math.pi/10.0) * math.sin((3.0*math.pi)/10.0)
        h_prime = math.sqrt(h_prime_sqr)
        h_second_sqr = 1.0 - (0.25 / (math.sin(math.pi/5)) ** 2)
        h_second = math.sqrt(h_second_sqr)

        # Liste de 5 tuples de 3 valeurs (x, y, z).
        # Coordonnées du pentagone du haut.
        pentagone_up = [
            (
                math.cos((k * math.pi) / 5),
                -h_prime,
                math.sin((k * math.pi) / 5))
            for k in (0, 2, 4, 6, 8)
        ]

        # Liste de 5 tuples de 3 valeurs (x, y, z).
        # Coordonnées du pentagone du bas.
        pentagone_down = [
            (
                math.cos((k * math.pi) / 5),
                +h_prime,
                math.sin((k * math.pi) / 5))
            for k in (1, 3, 5, 7, 9)
        ]

        # Liste de toutes les coordonnées des sommets
        # de l'icosaèdre, dans l'ordre du haut vers le bas.
        coords_icosahedron = list(itertools.chain(
            [ (0.0, -h_prime - h_second, 0.0) ], # sommet unique du haut.
            pentagone_up, # les 5 sommets du pentagone du haut.
            pentagone_down, # les 5 sommets du pentagone du bas.
            [ (0.0, +h_prime + h_second, 0.0) ] # sommet unique du bas.
        ))

        # Liste, dont chaque élément est constitué des infos suivantes :
        # - Un premier tuple de 3 entiers. Définit 3 index dans
        #   la liste coords_icosahedron, permettant de récupérer 3 sommets
        #   pour obtenir un triangle constituant une face de l'icosaèdre.
        # - Un second tuple de 3 floats. Définit la couleurs RGB de la face
        #   de l'icosaèdre. (C'est à dire la couleur des 3 sommets de
        #   l'icosaèdre, pour cette face).
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

        # Construction de glfloat_vertices et glfloat_colors à partir de
        # coords_icosahedron et indexes_vertex_and_colors_icosahedron.
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

