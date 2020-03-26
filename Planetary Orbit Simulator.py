'''
IMPORTANT:
    
Before running this program, change the working directory to the file containing
this Python file and these images: Background.png, Background2.png, Button.gif

In some cases, the following error message might show up:
'TclError: image "pyimage(somenumber)" doesn't exist'
Restart Python kernel to fix this error.

'''

import math
import turtle
import Tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from matplotlib import pyplot as plt
import webbrowser

G = 6.67408e-11
AU = (149.6e6 * 1000) # scale: 100 pixels = 1 AU.
scale = 250 / AU

root = tk.Tk() # creates a Tkinter window
root.title('Planetary Orbit Simulator') # sets title for window
root.geometry("700x600") # sets dimensions for window

im = Image.open('Background.png') # imports the image
tkimage = ImageTk.PhotoImage(im)
im1 = tk.Label(root, image=tkimage)
im1.place(x=0, y=0, relwidth=1, relheight=1) # sets the image as a background


def get_new_win(): # function for getting a new window
     
    NewWin = tk.Toplevel(root) # creates new window
    NewWin.title('Planetary Orbit Simulator')
    NewWin.geometry('500x650')
    im2 = Image.open('Background2.png')
    tkimage1 = ImageTk.PhotoImage(im2)
    im3 = tk.Label(NewWin, image=tkimage1)
    im3.place(x=0, y=0, relwidth=1, relheight=1)

    def quit_win(): # function for quitting the program
        
        NewWin.destroy()
        turtle.bye()
        
    QuitButton = tk.Button(NewWin, text='Quit', command=quit_win, height=2,
    width=10, bg='gray7', fg='white') # creates a quit button
    QuitButton.place(relx=.5, rely=.85, anchor="c") # places button on window
    NewWin.protocol("WM_DELETE_WINDOW", quit_win)
    
    
    def plot_mercury(): # function for plotting velocity graph for Mercury
        
        x = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        y = np.array([35701, 45890, 56785, 39190, 36630, 50913, 52074, 36976,
        38609, 55892])
        plt.plot(x, y, color='k')
        plt.title('Velocity of Mercury', fontsize=16)
        plt.xlabel('Steps (weeks)', fontsize=12)
        plt.ylabel('Velocity $(m/s)$', fontsize=12)
        plt.show()
        
    plot1 = tk.Button(NewWin, text='Mercury', command=plot_mercury, height=1,
    width=11, bg='black', fg='white') # creates button which plots graph
    plot1.place(relx=.2, rely=.7, anchor="c") # places the button on window
    
    def plot_venus():
        
        x = np.array([10, 20, 30, 40, 50, 60,70, 80, 90, 100])
        y = np.array([38006, 32402, 32866, 38234, 33731, 31858, 37352, 35415,
        31466, 35769]) # data found from animation
        plt.plot(x, y, color='y')
        plt.title('Velocity of Venus', fontsize=16)
        plt.xlabel('Steps (weeks)', fontsize=12)
        plt.ylabel('Velocity $(m/s)$', fontsize=12)
        plt.show()
        
    plot2 = tk.Button(NewWin, text='Venus', command=plot_venus, height=1,
    width=11, bg='black', fg='white')
    plot2.place(relx=.4, rely=.7, anchor="c")
    
    def plot_earth():
        
        x = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        y = np.array([31374, 30861, 28837, 27948, 29058, 31059, 31244, 29321,
        27984, 28615])
        plt.plot(x, y, color='b')
        plt.title('Velocity of Earth', fontsize=16)
        plt.xlabel('Steps (weeks)', fontsize=12)
        plt.ylabel('Velocity $(m/s)$', fontsize=12)
        plt.show()
        
    plot3 = tk.Button(NewWin, text='Earth', command=plot_earth, height=1,
    width=11, bg='black', fg='white')
    plot3.place(relx=.6, rely=.7, anchor="c")
    
    def plot_mars():
        
        x = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        y = np.array([24516, 24868, 24918, 24612, 24172, 23712, 23431, 23422,
        23686, 24139])
        plt.plot(x, y, color='r')
        plt.title('Velocity of Mars', fontsize=16)
        plt.xlabel('Steps (weeks)', fontsize=12)
        plt.ylabel('Velocity $(m/s)$', fontsize=12)
        plt.show()
        
    plot4 = tk.Button(NewWin, text='Mars', command=plot_mars, height=1,
    width=11, bg='black', fg='white')
    plot4.place(relx=.8, rely=.7, anchor="c")
    
    
    class Simulator(turtle.Turtle): # class for creating turtle animation
        
        name = 'Simulator'
        mass = None
        vx = vy = 0.000 # intial value
        px = py = 0.000
        
        def gravity(self, other): # function for calculation of force
            
            sx, sy = self.px, self.py
            ox, oy = other.px, other.py
            dx = (ox - sx)
            dy = (oy - sy)
            d = math.sqrt(dx**2 + dy**2) # infinitesimally small distance 
            f = G * self.mass * other.mass / (d**2) # from Newton's Gravity Law
            theta = math.atan2(dy, dx)
            fx = math.cos(theta) * f # x-component of force
            fy = math.sin(theta) * f # y-component of force
            return fx, fy
    
    
    def data(step, planets): # function for printing data
    
        print('Step #{}'.format(step))
        for planet in planets:
            
            s = '{:<8}  Pos.={:>6.2f} {:>6.2f} Vel.={:>10.3f} {:>10.3f}'.format(
                planet.name, planet.px/AU, planet.py/AU, planet.vx, planet.vy)
            print(s)   
        print()
    
  
    def loop(planets): # function for drawing orbits
    
        timestep = 24*3600*7 # 7 days
        
        for planet in planets:
            
            planet.penup()
            planet.hideturtle()
            
        step = 1
        
        while True:
            
            data(step, planets)
            step += 1 # adds 1 after each step
            force = {} # creates array for force
            
            for planet in planets:
                
                total_fx = total_fy = 0.0
                for other in planets:
                    
                    if planet is other:
                        
                        continue
                    fx, fy = planet.gravity(other) 
                    total_fx += fx
                    total_fy += fy
                force[planet] = (total_fx, total_fy) # total force on planet
                
            for planet in planets:
                
                fx, fy = force[planet]
                planet.vx += fx / planet.mass * timestep
                # calculates vx after timestep
                planet.vy += fy / planet.mass * timestep
                planet.px += planet.vx * timestep # calculates vx after timestep
                planet.py += planet.vy * timestep
                planet.goto(planet.px*scale, planet.py*scale)
                # calculates position according to scale
                planet.dot(6) # prints dot at positon

          
    def main(): # function for adding objects to turtle animation
        
        '''Data taken from NASA website:
        http://nssdc.gsfc.nasa.gov/planetary/factsheet/'''
        
        sun = Simulator()
        sun.name = 'Sun'
        sun.mass = 1.98855 * 10**30
        sun.pencolor('yellow')
        
        mercury = Simulator()
        mercury.name = 'Mercury'
        mercury.mass = 0.33011 * 10**24
        mercury.px = 0.3870 * AU
        mercury.vy = 47.362 * 1000
        mercury.pencolor('brown')
        
        venus = Simulator()
        venus.name = 'Venus'
        venus.mass = 4.8675 * 10**24
        venus.px = 0.7230 * AU
        venus.vy = -35.020 * 1000
        venus.pencolor('orange')
        
        earth = Simulator()
        earth.name = 'Earth'
        earth.mass = 5.9724 * 10**24
        earth.px = 1.000 * AU
        earth.vy = 29.783 * 1000
        earth.pencolor('blue')
        
        mars = Simulator()
        mars.name = 'Mars'
        mars.mass = 0.64171 * 10**24
        mars.px = 1.524 * AU
        mars.vy = 24.077 * 1000
        mars.pencolor('red')
        
        loop([sun, mercury, venus, earth, mars]) # creates a loop for objects

    turtle.bgcolor("black") # sets background for turtle window
    turtle.setup(800, 800) # sets screen size for turtle window
    app = main()
    app.mainloop() # starts animation
    
im2 = tk.PhotoImage(file="Button.gif")
NewWinButton = tk.Button(root, command=get_new_win, bg='black')
NewWinButton.config(image=im2)
NewWinButton.place(relx=.5, rely=.625, anchor="c")

def latex():
    
    webbrowser.open_new('Planetary Orbit Simulator Report.pdf')

ReportButton = tk.Button(root, text='LaTeX Report', command=latex, height=2,
width=15, bg='black', fg='white')
ReportButton.place(relx=.4, rely=.85, anchor="c")

def quit_win2():
    
    root.destroy()

QuitButton2 = tk.Button(root, text='Quit', command=quit_win2, height=2,
width=15, bg='black', fg='white')
QuitButton2.place(relx=.6, rely=.85, anchor="c")

root.mainloop()