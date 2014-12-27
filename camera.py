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
        # TODO : addition/multiplication de Vector3D
        self.v_front = Vector3D(-self.pos.x, -self.pos.y, -self.pos.z)
        self.v_front.normify()

    def _get_back_to_sphere(self):
        # TODO : addition/multiplication de Vector3D
        self.pos = Vector3D(-self.v_front.x, -self.v_front.y, -self.v_front.z)

    def _slide_lateral(self, dist):
        # TODO : addition/multiplication de Vector3D
        self.pos.x += self.v_left.x * dist
        self.pos.y += self.v_left.y * dist
        self.pos.z += self.v_left.z * dist
        self._refresh_vfront()
        self._get_back_to_sphere()
        self.v_left = self.v_front.cross_product(self.v_up)

    def _slide_longitudinal(self, dist):
        # TODO : addition/multiplication de Vector3D
        self.pos.x += self.v_up.x * dist
        self.pos.y += self.v_up.y * dist
        self.pos.z += self.v_up.z * dist
        self._refresh_vfront()
        self._get_back_to_sphere()
        self.v_up = self.v_left.cross_product(self.v_front)

    def slide_with_deltas(self):
        if self.delta_lateral != 0.0:
            self._slide_lateral(self.delta_lateral)
        if self.delta_longitudinal != 0.0:
            self._slide_longitudinal(self.delta_longitudinal)
        

if __name__ == "__main__":
    
    # tests unitaires.
    cam = CameraAroundSphere()
    print("up : ", cam.v_up)
    print("left : ", cam.v_front.cross_product(cam.v_up))

