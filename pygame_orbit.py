"""
pygame_orbit.py

Objects in the scene are loaded from an input file
that must be passed in as an argument. See example input
file 'scene'.

The planets and moons can be selected, which will
highlight them in blue and also draw a line between
them and the object they are orbiting.

Author: Kenneth Berry
"""

import math
import sys
import types
import pygame as pg


# Constants
INPUT_FILE = sys.argv[1]
CAPTION = "Orbiting & Rotating Planets"
SCREEN_SIZE = (1280, 1024)
BLACK     = (   0,   0,   0)
BLUE      = (  44, 176, 218)
COLOR_KEY = ( 255,   0, 255)
BACKGROUND_COLOR = BLACK
SELECT_COLOR = BLUE


class Planet(pg.sprite.Sprite):
    """Planet that can rotate and orbit a
    round another object or location."""
    def __init__(self, orbit_a, orbit_r, orbit_s, rot_s, sel_r, image, parent):
        pg.sprite.Sprite.__init__(self)
        self.loc = screen_rect.center
        self.orbit_c = self.loc       # orbit center
        self.orbit_a = int(orbit_a)   # orbit angle
        self.orbit_r = int(orbit_r)   # orbit radius
        self.orbit_s = float(orbit_s) # orbit speed
        image_filename = "./images/" + image
        print(image_filename)
        self.image = pg.image.load(image_filename).convert()
        self.parent = parent.rstrip()
        self.image.set_colorkey(COLOR_KEY)
        self.rect = self.image.get_rect()
        self.rot_a = 0                # rotation angle
        self.rot_s = float(rot_s)     # rotation speed
        self.sel = False              # selection flag
        self.sel_r = int(sel_r)       # selection radius
        # add planet to planets sprite group
        sprites.add(self)
        
    def rotate(self):
        """Rotate planet image."""
        if self.rot_a > 360:
            self.rot_a = 0
        self.rot_image = pg.transform.rotate(self.image, self.rot_a)
        self.rect = self.rot_image.get_rect(center=self.rect.center)
        self.rot_a += self.rot_s * 0.5

    def orbit(self):
        """Orbit planet around orbit_c at speed orbit_s and radius orbit_r."""
        self.rect.centerx = (
            self.orbit_r * math.sin(
                self.orbit_a) + self.orbit_c[0])
        self.rect.centery = (
            self.orbit_r * math.cos(
                self.orbit_a) + self.orbit_c[1])
        self.orbit_a += self.orbit_s
        self.loc = self.rect.center

    def update(self):
        """Update planet's location."""
        self.orbit()
        self.rotate()
                
    def draw_selection(self, surface):
        """Draw selection shapes if planet selected."""
        if self.sel == True:
            pg.draw.circle(
                surface, SELECT_COLOR, self.loc, self.sel_r)
            pg.draw.line(
                surface, SELECT_COLOR, self.loc, self.orbit_c, 4)

    def draw(self, surface):
        """Draw rotated planet at updated position."""
        surface.blit(self.rot_image, self.rect)
        
        
class Universe(object):
    """Universe in which to place planets."""
    def __init__(self):
        # create planets
        self.load_input()

    def load_input(self):
        first_line = True
        count = 0
        with open(INPUT_FILE, "r") as file:
            for line in file:
                if (first_line):
                    first_line = False
                    count = int(line)
                    continue
                if (count > 0):
                    line_list = line.split(" ")
                    new_planet = Planet(
                        line_list[0],
                        line_list[1],
                        line_list[2],
                        line_list[3],
                        line_list[4],
                        line_list[5],
                        line_list[6])
                    planets.append(new_planet)
                    count -= 1

    def event_loop(self):
        """Check for pygame events."""
        for event in pg.event.get():
                # end main loop if pygame window closed
                if event.type == pg.QUIT:
                    self.done = True  
                elif event.type == pg.MOUSEBUTTONDOWN \
                     and event.button == 1: 
                    self.pos = pg.mouse.get_pos()
                    for planet in sprites.sprites():
                        # select planet if clicked with left mouse button
                        if planet.rect.collidepoint(self.pos):
                            if planet.sel == False:
                                planet.sel = True
                            else:
                                planet.sel = False
                            
    def update(self):
        """Update orbit center of all planets."""
        for planet in planets:
            if (planet.parent != "*"):
                planet.orbit_c = planets[int(planet.parent)].loc
        # update rotation and location of all planets
        for planet in sprites.sprites():
            planet.update()
        
    def draw(self):
        """Draw the scene."""
        screen.fill(BACKGROUND_COLOR)
        # draw selection shapes for all selected planets
        for planet in sprites.sprites():
            planet.draw_selection(screen)
        # draw all planets
        for planet in sprites.sprites():
            planet.draw(screen)
        # draw a circle at current mouse position
        self.mouse_pos = pg.mouse.get_pos()
        self.cursor = pg.draw.circle(
            screen, SELECT_COLOR, self.mouse_pos, 10)
        pg.display.flip()
        
    def main(self):
        """Main game loop."""
        self.done = False
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            clock.tick(30)


if __name__ == "__main__":
    pg.init()
    clock = pg.time.Clock()
    pg.display.set_caption(CAPTION)
    sprites = pg.sprite.Group()
    planets = []
    screen = pg.display.set_mode(SCREEN_SIZE)
    screen_rect = screen.get_rect()
    pg.mouse.set_visible(False)
    game = Universe()
    game.main()
    pg.quit()
    sys.exit()
