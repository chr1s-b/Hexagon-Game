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

def ntext(text, x, y, font, color=(0, 0, 0)):
    @use_color(*color)
    def wrapper():
        glWindowPos2i(x, y)
        
        lines = 0
        for c in text:
            if c == '\n':
                glWindowPos2i(x, y-(lines*18))
            else:
                glutBitmapCharacter(font, ord(c))
    return wrapper()

def text(text,x,y,font,color=(0,0,0)):
    @use_color(*color)
    def wrapper():
        glPushMatrix()
        glTranslate(x,y,0)
        for c in text:
            glutStrokeCharacter(font,ord(c))
        glPopMatrix()
        return
    return wrapper()
    

def main():
    p = Player(RADIUS, SIZE)
    hexagons = [Hexagon(WIDTH),Hexagon(WIDTH*1.5)]
    def draw():
        # clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glOrtho(0,WIDTH,HEIGHT,0,-1,1)
        # draw some stuff
        glTranslate(WIDTH/2, HEIGHT/2, 0) # center things
        glPushMatrix()
        #slowly rotate to make it more difficult
        glRotate(myapp.frame*ROTATION_SPEED,0,0,1)
            
        if not myapp.gameover:
            for h in hexagons:
                #check for collision
                if h.radius - p.radius < p.size + h.thickness/2:
                    #check angle
                    if floor((p.angle +120)%360/60) != h.slot:
                        #collision
                        myapp.gameover = True
                        break
                elif h.radius > p.radius: break
            for h in hexagons:
                h.radius -= SHRINK_SPEED * (1+myapp.score/20.)
                if h.radius < h.thickness:
                    hexagons.remove(h)
                    hexagons.append(Hexagon(WIDTH))
                    myapp.score += 1
            myapp.frame+=1
        
        #render
        p.display()
        for h in hexagons:
            h.display()
        glPopMatrix()

        glRotate(180,1,0,0)
        scale = 0.4
        glLineWidth(4)
        glPushMatrix()
        glTranslate(-WIDTH/2,HEIGHT/2 - scale*120 , 0)
        glScale(scale, scale, scale)
        text("Score: {}".format(myapp.score), 0, 0, GLUT_STROKE_ROMAN)
        glPopMatrix()
        #check again here for gameover because it must be top layer
        if myapp.gameover:
            glPushMatrix()
            scale = 0.5
            glTranslate(-200, -scale*120/2,0)
            glScale(scale, scale, 0)
            text("Game over!", 0, 0, GLUT_STROKE_ROMAN)
            glPopMatrix()
        glutSwapBuffers()
        return

    def mouse_button(button, state, x, y):
        ''' state 0 is down; state 1 is up '''
        if button == 4: #scroll down
            p.angle -= SPEED*state
        if button == 3: #scroll up
            p.angle += SPEED*state
        return

    def keyboard_down(key, x, y):
        ''' Keyboard repeat is enabled by default '''
        ''' x and y represent the mouse position  '''
        if key == b'\x1b': # ESC key
            glutLeaveMainLoop()

        #check if non-special character
        key = key.decode()
        return

    def keyboard_up(key, x, y):
        return

    def mouse_move(x, y):
        return
    myapp = App(TITLE)
    myapp.create_window(WIDTH,HEIGHT)
    myapp.score = 0
    myapp.gameover = False
    glutDisplayFunc( draw )              
    glutIdleFunc( draw )             
    glutMouseFunc( mouse_button )
    glutKeyboardFunc( keyboard_down )    
    glutKeyboardUpFunc( keyboard_up )    
    glutPassiveMotionFunc( mouse_move )         
    
    glClearColor(1, 1, 1, 0);
    glutMainLoop()
    print(" Clean exit ")
    return

if __name__ == "__main__":
    main()
