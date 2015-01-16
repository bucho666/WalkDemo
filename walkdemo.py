# -*- coding: utf-8 -*-

from pygameframework import Game
from pygameframework import GridWindow
from pygameframework import Color
from pygameframework import AsciiTileSheet
from pygameframework import Coordinate
from pygameframework import Direction
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

    def coordinate_of(self, actor):
        try:
            return self._coordinate[actor]
        except KeyError:
            return None

    def put(self, coordinate, actor):
        self._actor[coordinate] = actor
        self._coordinate[actor] = coordinate

    def render(self, screen):
        for pos, actor in self._actor.items():
            actor.render(pos, screen)

    def to_coordinate(self, actor, direction):
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

class MapHandler(object):
    active_map = ActorMap(80, 20)

    def __init__(self):
        self._map = self.active_map

class PlayerHandler(MapHandler):
    def __init__(self, actor):
        MapHandler.__init__(self)
        self._actor = actor

    def initialize(self):
        x = 1
        while self._map.actor(Coordinate(x, 1)): x += 1
        self._map.put(Coordinate(x, 1), self._actor)
        return self

    def handle(self, controller, keyboard=None):
        down_keys =  controller.pressed_keys()
        if 'left' in down_keys: self._walk(Direction.LEFT)
        if 'down' in down_keys: self._walk(Direction.DOWN)
        if 'up' in down_keys: self._walk(Direction.UP)
        if 'right' in down_keys: self._walk(Direction.RIGHT)
        if 'start' in down_keys: self.initialize()
        if not keyboard: return
        down_keys =  keyboard.pressed_keys()
        if ord('h') in down_keys: self._walk(Direction.LEFT)
        if ord('j') in down_keys: self._walk(Direction.DOWN)
        if ord('k') in down_keys: self._walk(Direction.UP)
        if ord('l') in down_keys: self._walk(Direction.RIGHT)
        if ord('q') in down_keys: sys.exit()

    def _walk(self, direction):
        pos = self._map.to_coordinate(self._actor, direction)
        if self._map.actor(pos): return
        self._map.move_actor(self._actor, direction)

class WalkDemo(Game, MapHandler):
    POSITION = Coordinate(0, 0)
    GRID_SIZE = Coordinate(10, 18)
    MAX_PLAYER = 4
    PLAYER_COLOR = (Color.RED, Color.AQUA, Color.LIME, Color.YELLOW)
    def __init__(self):
        Game.__init__(self)
        MapHandler.__init__(self)
        self._window = None
        self._handlers = []

    def initialize(self):
        tile_sheet = AsciiTileSheet().initialize('Courier New', 18)
        for color in self.PLAYER_COLOR:
            actor = Actor(tile_sheet.get_tile('@', color))
            self._handlers.append(PlayerHandler(actor).initialize())

    def update(self):
        for handler, controller in zip(self._handlers, self._controllers):
            handler.handle(controller, self._keyboard)

    def set_screen(self, screen):
        self._screen = screen
        self._window = GridWindow(screen, self.POSITION, self.GRID_SIZE)

    def render(self):
        self._screen.fill()
        self._map.render(self._window)

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
