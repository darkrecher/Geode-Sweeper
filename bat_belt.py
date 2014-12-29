# -*- coding: utf-8 -*-

"""
    Module contenant quelques fonctions de base.
"""

from __future__ import (unicode_literals, absolute_import,
                        print_function, division)
import itertools


def ctype_array(gl_type, *args):
    """
    Fonction utile avec la libraire pyglet
    (mais pourrait servir à d'autres occasions).
    Renvoie un tableau à une dimension contenant des variables ctype.

    :Example:
    >>> import pyglet
    >>> ctype_array_floats = ctype_array(pyglet.gl.GLfloat, 0.5, 1.0, 1.5)
    >>> ctype_array_floats
    <bat_belt.c_float_Array_3 object at 0x01DDDF30>
    >>> ctype_array_floats[0]
    0.5

    :param gl_type: type des données du tableau. GLfloat, GLuint, ...
    :param *args: valeurs float. Données à mettre dans le tableau de ctype.
    """
    return (gl_type*len(args))(*args)

def group2(iterator, count):
    """
    Regroupe par paquet.
    Construit des tuples de "count" elements,
    à partir de ce qui sort de iterator.
    Ne renvoit pas la fin de l'itérateur
    si ça ne tombe pas juste par rapport à "count"

    :Example:
    >>> iter_group2 = bat_belt.group2(range(5, 15), 4)
    >>> iter_group2
    <itertools.imap object at 0x018D85F0>
    >>> list(iter_group2)
    [(5, 6, 7, 8), (9, 10, 11, 12)]
    # On ne récupère pas 13 et 14.
    """
    return itertools.imap(None, *([ iter(iterator) ] * count))

