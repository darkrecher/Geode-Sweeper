# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

import pyglet
pgl = pyglet.gl

import window_geode_sweeper
win = window_geode_sweeper.window_geode_sweeper
PERIOD_GAME_CYCLE_SECONDS = window_geode_sweeper.PERIOD_GAME_CYCLE_SECONDS
from mesh_builder import MeshRainbowCube, MeshIcosahedron

mesh = MeshRainbowCube()
win.init_geode_sweeper(mesh)

pyglet.clock.schedule_interval(win.update, PERIOD_GAME_CYCLE_SECONDS)
pyglet.app.run()

