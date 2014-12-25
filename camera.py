# -*- coding: utf-8 -*-

"""
"""

from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

from vector3D import Vector3D


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

    def _refresh_vfront(self):
        self.v_front = Vector3D(-self.x, -self.y, -self.z)
        self.v_front.normify()

    def _get_back_to_sphere(self):
        # TODO : c'est pas plus simple de définir directement les xyz à -v_front ?
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


if __name__ == "__main__":
    
    # tests unitaires.
    cam = Camera()
    print("up : ", cam.v_up)
    print("left : ", cam.v_front.cross_product(cam.v_up))

        
