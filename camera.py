# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

from vector3D import Vector3D


class CameraAroundSphere(object):

    """
    Une caméra se déplaçant sur une sphère de centre O (0, 0, 0) et de rayon 1.
    La caméra regarde toujours dans la direction du centre O.
    L'orientation de la caméra ne change jamais (le haut de la caméra est vers
    le point (x=0, y= -infini, z=0).

    Le déplacement sur la sphère est fait un peu à l'arrache. On ne donne pas
    des angles de déplacements (teta, phi en coordonnées polaires). On donne
    une "distance orthogonale latérale/longitudinale".

    Actions effectuées lors d'un déplacement :
     - On décale le point de vue selon un axe tangeant à la sphère, et une
       distance donnée.
     - Par conséquent, le point de vue n'est plus sur la sphère.
     - On ramène à l'arrache le point de vue sur la sphère, en choisissant
       le point de la sphère qui est sur le segment [O, point de vue]
     - Le prochain déplacement se fera le long d'un autre axe tangeant,
       puisqu'on fait partir ces axes du nouveau point de vue.

    Le déplacement latéral et le longitudinal se font selon le même principe,
    la seule différence, c'est le choix initial de l'axe tangeant.

    Variables membres intéressantes :

    pos : Vector3D. Position du point de vue, situé sur la sphère.
    lookat : Vector3D. Point vers lequel regarde la caméra.
        En fait c'est toujours le point O

    v_front : Vector3D. Vecteur normé, donnant la direction vers laquelle
        regarde la caméra.
    v_left : Vector3D. Vecteur normé, donnant la direction du côté gauche
        de la caméra.
    v_up : Vector3D. Vecteur normé, donnant la direction du haut de la caméra.

    delta_lateral : float. distance pour le dépl. orthogonal latéral.
    delta_longitunal : float. distance pour le dépl. orthogonal longitunal.

    Pour effectuer un déplacement :
     - Affecter une valeur non nulle à delta_lateral et/ou delta_longitunal.
     - Exécuter la fonction slide_with_deltas().
     - Les variables pos, v_front, v_left et v_up seront alors mises à jour.
    """

    def __init__(self):
        self.pos = Vector3D(0.0, 0.0, -1.0)
        self.lookat = Vector3D(0.0, 0.0, 0.0)
        self.v_front = Vector3D(0.0, 0.0, 1.0)
        self.v_left = Vector3D(1.0, 0.0, 0.0)
        self.v_up = self.v_left.cross_product(self.v_front)
        self.delta_lateral = 0.0
        self.delta_longitudinal = 0.0

    def _refresh_vfront(self):
        """
        Recalcule v_front, en fonction de la nouvelle position.
        Re-norme le vecteur v_front (longueur = 1).
        """
        self.v_front = -self.pos
        self.v_front.normify()

    def _get_back_to_sphere(self):
        """
        Replace le point pos sur la sphère.
        Cette fonction doit être exécuter uniquement quand v_front est normé.
        (Exécuter refresh_vfront au préalable).
        """
        self.pos = -self.v_front

    def _slide_lateral(self, dist):
        """
        Effectue un déplacement orthogonal latéral d'une distance de "dist".
        """
        self.pos += self.v_left * dist
        self._refresh_vfront()
        self._get_back_to_sphere()
        self.v_left = self.v_front.cross_product(self.v_up)

    def _slide_longitudinal(self, dist):
        """
        Effectue un déplacement orthogonal longitunal d'une distance de "dist".
        """
        self.pos += self.v_up * dist
        self._refresh_vfront()
        self._get_back_to_sphere()
        self.v_up = self.v_left.cross_product(self.v_front)

    def slide_with_deltas(self):
        """
        Effectue deux déplacement orthogonaux, selon les valeurs des
        variables membres delta_lateral et delta_longitudinal.
        """
        if self.delta_lateral != 0.0:
            self._slide_lateral(self.delta_lateral)
        if self.delta_longitudinal != 0.0:
            self._slide_longitudinal(self.delta_longitudinal)


def main():
    """
    Tests unitaires (pas exhaustif du tout).
    """
    cam = CameraAroundSphere()
    print("up : ", cam.v_up)
    print("left : ", cam.v_front.cross_product(cam.v_up))

if __name__ == "__main__":
    main()

