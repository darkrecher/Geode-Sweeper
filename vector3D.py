# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, absolute_import,
                        print_function, division)
import math


class Vector3D(object):

    """
    Définit un vecteur dans un espace en 3 dimensions.
    Avec quelques fonctions de base : normage, produit en croix.
    Les fonctions de base-base (add, multiply) ne sont pas présentes.
    Vous avez été prévenu.
    """

    # TODO : trouver une putain de classe vecteur toute faite.
    # Je vais pas me faire chier à tout recoder.

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        """
        Représentation du Vector3D.
        Écrit les valeurs des 3 coordonnées x, y, z.
        """
        return "".join((
            "<vector3D:",
            " x:", str(self.x),
            " y:", str(self.y),
            " z:", str(self.z),
            ">",
        ))

    def normify(self):
        """
        Modifie les coordonnées x, y, z, de façon à ce que la norme (longueur)
        du Vector3D soit égale à 1.
        Le sens et la direction du Vector3D ne sont pas modifiées.
        """
        current_norm = math.sqrt(sum((self.x ** 2, self.y ** 2, self.z ** 2)))
        self.x /= current_norm
        self.y /= current_norm
        self.z /= current_norm

    def cross_product(self, v_other):
        """
        Renvoit un nouveau Vector3D, correspondant au produit vectoriel
        (produit en croix) de ce Vector3D, et d'un second Vector3D (v_other).
        Pour une description de la méthode de calcul du produit en croix :
        http://en.wikipedia.org/wiki/Cross_product
        """
        u1, u2, u3 = self.x, self.y, self.z
        v1, v2, v3 = v_other.x, v_other.y, v_other.z

        prod_x = u2*v3 - u3*v2
        prod_y = u3*v1 - u1*v3
        prod_z = u1*v2 - u2*v1

        return Vector3D(prod_x, prod_y, prod_z)


def main():
    """
    Tests unitaires (pas exhaustif du tout).
    """
    test_normify = Vector3D(1.0, 2.0, 3.0)
    print("test_normify init : ", test_normify)
    test_normify.normify()
    print("test_normify normé : ", test_normify)
        
if __name__ == "__main__":
    main()

