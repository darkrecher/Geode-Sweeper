# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

import itertools

def ctype_array(gl_type, *args):
    """
        renvoie un tableau à une dimension contenant des variables ctype.
        gl_type : type des données du tableau : GLfloat, GLuint, ...
        args : donnée du tableau à convertir en ctype.
    """
    return (gl_type*len(args))(*args)

def group2(iterator, count):
    """
    Prend ce qui sort de iterator, et en fait des paquets de "count" elements.
    """
    return itertools.imap(None, *([ iter(iterator) ] * count))
