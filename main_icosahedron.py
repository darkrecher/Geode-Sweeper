# -*- coding: utf-8 -*-

"""
Initialisation et lancement d'une application pyglet WindowGeodeSweeper.
Affiche un icosaèdre blanc et vert.
"""

from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

import pyglet
pgl = pyglet.gl

import window_geode_sweeper
win = window_geode_sweeper.window_geode_sweeper
from mesh_builder import MeshRainbowCube, MeshIcosahedron


def main():
    mesh = MeshIcosahedron()
    win.init_geode_sweeper(mesh)

    pyglet.clock.schedule_interval(
        win.update,
        window_geode_sweeper.PERIOD_GAME_CYCLE_SECONDS)
    pyglet.app.run()

if __name__ == "__main__":
    main()

