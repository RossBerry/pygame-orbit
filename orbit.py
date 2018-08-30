import math
import sys
import types
import pygame as pg


# Constants 
CAPTION = "Orbiting & Rotating Planets"
SCREEN_SIZE = (1280, 1024)
BLACK     = (   0,   0,   0)
BLUE      = (  44, 176, 218)
COLOR_KEY = ( 255,   0, 255)
BACKGROUND_COLOR = BLACK
SELECT_COLOR = BLUE

class Planet(pg.sprite.Sprite):
    """Planet that can rotate and orbit around another object or location."""
    def __init__(self, orbit_a, orbit_r, orbit_s, rot_s, sel_r, image):
        pg.sprite.Sprite.__init__(self)
        self.loc = screen_rect.center
        self.orbit_c = self.loc
        self.orbit_a = orbit_a
        self.orbit_r = orbit_r
        self.orbit_s = orbit_s
        self.image = pg.image.load(image).convert()
        self.image.set_colorkey(COLOR_KEY)
        self.rect = self.image.get_rect()
        self.rot_a = 0
        self.rot_s = rot_s
        self.sel = False
        self.sel_r = sel_r
        # add planet to planets sprite group
        planets.add(self)
        
    def rotate(self):
        # Rotate planet image.
        if self.rot_a > 360:
            self.rot_a = 0
        self.rot_image = pg.transform.rotate(self.image, self.rot_a)
        self.rect = self.rot_image.get_rect(center=self.rect.center)
        self.rot_a += self.rot_s * 0.5

    def orbit(self):
        # Orbit planet around orbit_c at speed orbit_s and radius orbit_r
        self.rect.centerx = (
            self.orbit_r * math.sin(
                self.orbit_a) + self.orbit_c[0])
        self.rect.centery = (
            self.orbit_r * math.cos(
                self.orbit_a) + self.orbit_c[1])
        self.orbit_a += self.orbit_s
        self.loc = self.rect.center

    def update(self):
        # Update planet's location.
        self.orbit()
        self.rotate()
                
    def draw_selection(self, surface):
        # Draw selection shapes if planet selected.
        if self.sel == True:
            pg.draw.circle(
                surface, SELECT_COLOR, self.loc, self.sel_r)
            pg.draw.line(
                surface, SELECT_COLOR, self.loc, self.orbit_c, 4)

    def draw(self, surface):
        # Draw rotated planet at updated position.
        surface.blit(self.rot_image, self.rect)
        
        
class Universe(object):
    """Universe in which we can place planets."""
    def __init__(self):
        # create planets
        self.star = Planet(
            0, 0, 0, -0.5, 0, "star.png")
        self.planet = Planet(
            0, 300, 0.01, -1, 30, "blue_planet.png")
        self.moon1 = Planet(
            0, 75, -0.05, 3, 10, "small_moon.png")
        self.moon2 = Planet(
            90, 100, 0.05, -3, 17, "big_moon.png")
        self.moon3 = Planet(
            180, 125, -0.01, 3, 10, "small_moon.png")
        self.moon4 = Planet(
            45, 200, 0.02, -3, 17, "big_moon.png")
        self.moon5 = Planet(
            45, 50, 0.1, -3, 10, "small_moon.png")
    
    def event_loop(self):
        # check for pygame events
        for event in pg.event.get():
                # end main loop if pygame window closed
                if event.type == pg.QUIT:
                    self.done = True  
                elif event.type == pg.MOUSEBUTTONDOWN \
                     and event.button == 1: 
                    self.pos = pg.mouse.get_pos()
                    for planet in planets.sprites():
                        # select planet if clicked with left mouse button
                        if planet.rect.collidepoint(self.pos):
                            if planet.sel == False:
                                planet.sel = True
                            else:
                                planet.sel = False
                            
    def update(self):
        # update orbit center of all planets
        self.planet.orbit_c = self.star.loc
        self.moon1.orbit_c = self.planet.loc
        self.moon2.orbit_c = self.planet.loc
        self.moon3.orbit_c = self.planet.loc
        self.moon4.orbit_c = self.planet.loc
        self.moon5.orbit_c = self.moon4.loc
        # update rotation and location of all planets
        for planet in planets.sprites():
            planet.update()
        
    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        # draw selection shapes for all selected planets
        for planet in planets.sprites():
            planet.draw_selection(screen)
        # draw all planets
        for planet in planets.sprites():
            planet.draw(screen)
        # draw a circle at current mouse position
        self.mouse_pos = pg.mouse.get_pos() 
        self.cursor = pg.draw.circle(
            screen, SELECT_COLOR, self.mouse_pos, 10)
        pg.display.flip()
        
    def main(self):
        self.done = False
        # main loop
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            clock.tick(30)
            
        
if __name__ == "__main__":
    pg.init()
    clock = pg.time.Clock()
    pg.display.set_caption(CAPTION)
    planets = pg.sprite.Group()
    screen = pg.display.set_mode(SCREEN_SIZE)
    screen_rect = screen.get_rect()
    pg.mouse.set_visible(False)
    game = Universe()
    game.main()
    pg.quit()
    sys.exit()
