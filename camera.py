# -*- coding: utf-8 -*-

"""
"""

from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

from vector3D import Vector3D


class CameraAroundSphere(object):

    def __init__(self):
        self.pos = Vector3D(0.0, 0.0, -1.0)
        self.lookat = Vector3D(0.0, 0.0, 0.0)
        self.v_front = Vector3D(0.0, 0.0, 1.0)
        self.v_left = Vector3D(1.0, 0.0, 0.0)
        self.v_up = self.v_left.cross_product(self.v_front)
        self.delta_lateral = 0.0
        self.delta_longitudinal = 0.0        

    def _refresh_vfront(self):
        self.v_front = -self.pos
        self.v_front.normify()

    def _get_back_to_sphere(self):
        self.pos = -self.v_front

    def _slide_lateral(self, dist):
        self.pos += self.v_left * dist
        self._refresh_vfront()
        self._get_back_to_sphere()
        self.v_left = self.v_front.cross_product(self.v_up)

    def _slide_longitudinal(self, dist):
        self.pos += self.v_up * dist
        self._refresh_vfront()
        self._get_back_to_sphere()
        self.v_up = self.v_left.cross_product(self.v_front)

    def slide_with_deltas(self):
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

