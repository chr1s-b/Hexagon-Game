# library version of 2dexample.py (2d ogl)
import sys, time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from textureandcolor import *
from math import pi, cos, sin, sqrt, floor
from random import randint

TITLE = "Hexagon!"
WIDTH, HEIGHT =800, 600
SPEED = 24
RADIUS = 60
SIZE = 10
SHRINK_SPEED = 0.7
THICKNESS = 10
ROTATION_SPEED = 0.15

def text(string, x, y, size, color=(0,0,0)):
    def linetext(text,x,y,size,color=(0,0,0)):
        @use_color(*color)
        def wrapper():
            glPushMatrix()
            glRotate(180,1,0,0)
            glTranslate(x,y,0)
            default = 120.
            glScale(size/default, size/default, size/default)
            for c in text:
                glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN,ord(c))
            glPopMatrix()
            return
        return wrapper()
    y = -y
    lines = string.split("\n")
    for i, line in enumerate(lines):
        offset = size+ (size + 10) * i
        linetext(line, x, y-offset, size, color=color)

class App:
    def __init__(self, title="My 2D OGL App"):
        self.title = title
        self.fps = 30.
        self.frame = 0
        return

    def create_window(self,width, height, fullscreen=False):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(width,height)
        glutCreateWindow(self.title.encode())
        self.width, self.height = width, height
        glEnable(GL_COLOR_MATERIAL)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
        glEnable (GL_BLEND)
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        return

class Player:
    def __init__(self,radius,size=50,color=(0,0,1)):
        self.radius = radius
        self.color = color
        self.angle = 0
        self.size=size
        return

    def display(self):
        self.angle = self.angle % 360
        glPushMatrix()
        glRotate(self.angle,0,0,1)
        glTranslate(self.radius, 0, 0)
        
        @use_color(*self.color)
        def circle(radius):
            triangleAmount = 24
            twicePi = 2 * pi
	
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(0,0)
            for i in range(triangleAmount+1):
                glVertex2f((radius * cos(i *  twicePi / triangleAmount)), 
                               (radius * sin(i * twicePi / triangleAmount)))
            glEnd()
            
        circle(self.size)
        glPopMatrix()

class Hexagon:
    thickness = THICKNESS
    color = (1,0,0)
    def __init__(self,radius):
        self.radius = radius
        self.slot =randint(0,5)
        return
    
    def display(self):
        #use cosine rule to calculate side_length
        self.side = sqrt(2*self.radius*self.radius - 2*self.radius*self.radius*cos(2*pi/6.))
        #draw a hexagon
        @use_color(*self.color)
        def hexagon():
            for i in range(0,5):
                a = (i + self.slot-1) * 60
                glPushMatrix()
                glRotate(a,0,0,1)
                glTranslate(self.radius, 0, 0)
                glRotate(30,0,0,1)
                glBegin(GL_QUADS)
                glVertex2f(0, 0)
                glVertex2f(self.thickness, -self.thickness/1.7)
                glVertex2f(self.thickness, self.side +self.thickness/1.7)
                glVertex2f(0, self.side)
                glEnd()
                glPopMatrix()
            return     
        hexagon()
        return

class Level:
    def __init__(self,player,shapes):
        self.player = player
        self.shapes = shapes
        self.gameover = False
        self.score = 0
        return

    def update(self,app):
        if self.gameover: return
        p = self.player
        hexagons = self.shapes
        # collisions
        for h in hexagons:
            if h.radius - p.radius < p.size + h.thickness/2 and h.radius - p.radius > 0:    # check distance
                if floor((p.angle +120)%360/60) != h.slot:                                  # check angle
                    self.gameover = True
                    return
            elif h.radius > p.radius: break
        # movement
        for h in hexagons:
            h.radius -= SHRINK_SPEED * (1+app.level.score/20.)
            if h.radius < h.thickness:
                hexagons.remove(h)
                hexagons.append(Hexagon(WIDTH))
                self.score += 1
        app.frame+=1
        return False

    def render(self):
        self.player.display()
        for s in self.shapes:
            s.display()
        return

def main():
    def draw():
        # clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glOrtho(0,WIDTH,HEIGHT,0,-1,1)
        
        # center matrix
        glPushMatrix()
        glTranslate(WIDTH/2, HEIGHT/2, 0)
        # slowly rotate
        glRotate(app.frame*ROTATION_SPEED,0,0,1)
        # update level
        app.level.update(app)
        # render level
        app.level.render()
        # uncenter matrix
        glPopMatrix()

        # display text
        glLineWidth(4)
        text("Score: {}".format(app.level.score), 4, 4, 24)
        
        # gameover state...
        if app.level.gameover:
            text("Game over!\nPress SPACE\nto play again", WIDTH/2-120, HEIGHT/2-48, 32)
        glutSwapBuffers()
        return

    def mouse_button(button, state, x, y):
        ''' state 0 is down; state 1 is up '''
        if app.level.gameover:
            if button == 0:
                return
            return
        if button == 4: #scroll down
            app.level.player.angle -= SPEED*state
            return
        if button == 3: #scroll up
            app.level.player.angle += SPEED*state
            return
        return

    def keyboard_down(key, x, y):
        ''' Keyboard repeat is enabled by default '''
        ''' x and y represent the mouse position  '''
        if key == b'\x1b': # ESC key
            glutLeaveMainLoop()
            return
        if key == b' ': # SPACE key
            app.level = Level(Player(RADIUS, SIZE),[Hexagon(WIDTH),Hexagon(WIDTH*1.5)])
            return
        #check if non-special character
        key = key.decode()
        return

    def keyboard_up(key, x, y):
        return

    def mouse_move(x, y):
        return
    
    app = App(TITLE)
    app.create_window(WIDTH,HEIGHT)
    glutDisplayFunc( draw )              
    glutIdleFunc( draw )             
    glutMouseFunc( mouse_button )
    glutKeyboardFunc( keyboard_down )    
    glutKeyboardUpFunc( keyboard_up )    
    glutPassiveMotionFunc( mouse_move )
    
    app.level_setup = (Player(RADIUS, SIZE),[Hexagon(WIDTH),Hexagon(WIDTH*1.5)])
    app.level = Level(*app.level_setup)
    
    glClearColor(1, 1, 1, 0);
    glutMainLoop()
    return

if __name__ == "__main__":
    main()
