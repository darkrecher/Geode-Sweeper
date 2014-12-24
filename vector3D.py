# -*- coding: utf-8 -*-

"""
Définit un vecteur dans un espace en 3 dimensions.
Avec quelques fonctions de base : normage; produit en croix.
Les fonctions de base-base (addition, multiplication) ne sont pas présentes.
Vous avez été prévenu.
"""

from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

import math

                        
class Vector3D(object):

    # TODO : trouver une putain de classe vecteur toute faite.
    # Je vais pas me faire chier à tout recoder.

    def __init__(self, x, y, z):
        # TODO : convertir en float.
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

        
if __name__ == "__main__":
    # TODO : mettre ça dans des tests unitaires.
    test_normify = Vector3D(1.0, 2.0, 3.0)
    print("test_normify: ", test_normify)
    test_normify.normify()
    print("test_normify normé: ", test_normify)

    
