# -*- coding: utf-8 -*-

from pygameframework import Game
from pygameframework import GridWindow
from pygameframework import Color
from pygameframework import AsciiTileSheet
from pygameframework import Coordinate
from pygameframework import Direction
from pygameframework import Sprite
import sys

class ActorMap(object):
    def __init__(self, width, height):
        self._actor = dict()
        self._coordinate = dict()

    def pickup(self, coordinate):
        actor = self._actor[coordinate]
        del self._actor[coordinate]
        del self._coordinate[actor]
        return actor

    def actor(self, coordinate):
        if coordinate in self._actor:
            return self._actor[coordinate]
        return None

    def put(self, coordinate, actor):
        self._actor[coordinate] = actor
        self._coordinate[actor] = coordinate

    def render(self, screen):
        for pos, actor in self._actor.items():
            actor.render(pos, screen)

    def moved_position(self, actor, direction):
        c = self._coordinate[actor]
        return c + direction

    def move_actor(self, actor, direction):
        c = self._coordinate[actor]
        self.put(c+direction, self.pickup(c))

class Actor(object):
    def __init__(self, graphic):
        self._graphic = graphic

    def render(self, position, screen):
        screen.draw(position, self._graphic)

class WalkDemo(Game):
    POSITION = Coordinate(0, 0)
    GRID_SIZE = Coordinate(10, 18)
    def __init__(self):
        Game.__init__(self)
        self._window = None
        self._actor = None
        self._map = ActorMap(80, 20)

    def initialize(self):
        tile_sheet = AsciiTileSheet().initialize('Courier New', 18)
        self._actor = Actor(tile_sheet.get_tile('@', Color.LIME))
        self._map.put(Coordinate(1, 1), self._actor)
        self._map.put(Coordinate(1, 2),
                Actor(tile_sheet.get_tile('@', Color.AQUA)))
        self._map.put(Coordinate(2, 2),
                Actor(tile_sheet.get_tile('@', Color.OLIVE)))
    
    def update(self):
        down_keys =  self._controllers[0].pressed_keys()
        if 'left' in down_keys: self._walk(Direction.LEFT)
        if 'down' in down_keys: self._walk(Direction.DOWN)
        if 'up' in down_keys: self._walk(Direction.UP)
        if 'right' in down_keys: self._walk(Direction.RIGHT)

        down_keys =  self._keyboard.pressed_keys()
        if ord('h') in down_keys: self._walk(Direction.LEFT)
        if ord('j') in down_keys: self._walk(Direction.DOWN)
        if ord('k') in down_keys: self._walk(Direction.UP)
        if ord('l') in down_keys: self._walk(Direction.RIGHT)

    def set_screen(self, screen):
        self._screen = screen
        self._window = GridWindow(screen, self.POSITION, self.GRID_SIZE)

    def render(self):
        self._screen.fill()
        self._map.render(self._window)

    def _walk(self, direction):
        pos = self._map.moved_position(self._actor, direction)
        if self._map.actor(pos): return
        self._map.move_actor(self._actor, direction)

if __name__ == '__main__':
    from pygameframework.framework import GameRunner
    CONTROLLER_NUM = 4
    demo = WalkDemo()
    runner = GameRunner(demo)\
        .initialize_system()\
        .initialize_screen(640, 480, 16)\
        .initialize_controller(CONTROLLER_NUM, 'config.ini')\
        .set_font('Courier New', 18)\
        .set_fps(24)\
        .set_caption('WalkDemo')
    runner.run()
