# Gabriel Bessler
# April 23, 2017
# Zombie-Fish VPython Simulation

from __future__ import print_function
from __future__ import division
from subprocess import Popen
from math import pi, sqrt
import random as rand
import visual as v


class Main(object):

    def __init__(self):
        '''Sets all initial variables of simulation and then handles function
        calls'''

        # Initial options:
        self.carryingCapacity = True
        self.initialZombiePop = 3
        self.fishMultiply = True
        self.initialFishPop = 10
        self.cureSpheres = False
        self.showTrails = True
        self.spawnCures = True
        self.showTTip = True
        self.timeOut = 400
        self.smarterFish = False

        # Data gathering for graph
        self.zombiePopulationTracker = []
        self.fishPopulationTracker = []
        self.timeOutCounter = 0

        # Simulation parameters
        self.spawnFoodDelayMax = 13
        self.spawnCureDelayMax = 60
        self.spawnCureDelay = 0
        self.spawnFoodDelay = 0
        self.viewDistance = 3
        self.cureMax = 22
        self.xmax = 11.5
        self.vmax = .15
        self.ymax = 6

        # Display parameters
        self.zombieColor = v.color.green
        self.fishColor = v.color.white

        # Stores current objects
        self.zombieShapeTest = []
        self.zombieHitList = []
        self.fishHitList = []
        self.zombieList = []
        self.shapeTest = []
        self.fishList = []
        self.cureList = []
        self.foodList = []

        # Used for only doing collision detection every 2 frames
        self.selfCountMax = 2
        self.selfCount = 0

        # Begins the simulation
        self.FPS = 30
        self.createDisplay()
        self.startSimulation()
        self.fishLabelText = v.label(pos=(-15, 0, 0), text='')
        self.ttFish = None
        self.fishLabelTimer = 0
        self.loop()

    def createFood(self):
        ''' Creates the food that regular fish will eat '''
        if self.cureSpheres:
            ball = v.sphere(pos=(rand.random()*24 - 12, rand.random()*12-6, 0),
                            radius=0.1, color=v.color.blue)
        else:
            ball = v.extrusion(radius=.1, pos=(rand.random()*23 - 11.5,
                                               rand.random()*12-6),
                               color=v.color.yellow,
                               shape=v.shapes.circle(pos=(0, 0), radius=.1))
        self.foodList.append(ball)

    def startSimulation(self):
        ''' Spawns fish and generates display for simulation'''
        self.labelText = v.label(pos=(-9.8, 5.3, 0),
                                 text='Number of Zombies: ' +
                                 str(len(self.zombieList)) +
                                 '\nNumber of Fish: ' +
                                 str(len(self.fishList)))
        for i in range(self.initialFishPop):
            self.createFish(type="regular")
        for i in range(self.initialZombiePop):
            self.createFish(type="zombie")

        # Create boundary displays
        bigSquare = v.shapes.rectangle(pos=(0, 0), height=14, width=24)
        littleSquare = v.shapes.rectangle(pos=(0, 0), height=12.2, width=23.1)
        v.extrusion(shape=bigSquare - littleSquare, color=v.color.black)

    def createDisplay(self):
        ''' Creates the main display screen for the game '''
        self.mainScene = v.display(title='Fish Zombies: Simulation', x=0, y=0,
                                   width=1280, height=800,
                                   center=(0, 0, 0),
                                   background=(0, .5, 1))
        self.mainScene.select()  # Makes this the main display
        self.mainScene.userspin = False
        self.mainScene.userzoon = False
        self.mainScene.autoscale = False
        self.mainScene.range = (12, 6, 1)
        self.mainScene.bind('mousemove', self.mouseMove)

    def createCure(self):
        ''' Creates the blobs that will cure the zombie-fish '''
        if self.cureSpheres:
            ball = v.sphere(pos=(rand.random()*24 - 12, rand.random()*12-6, 0),
                            radius=0.1, color=v.color.blue)
        else:
            ball = v.extrusion(radius=.1, pos=(rand.random()*23 - 11.5,
                                               rand.random()*12-6),
                               color=v.color.blue,
                               shape=v.shapes.circle(pos=(0, 0), radius=.1))
        self.cureList.append(ball)

    def createFish(self, type="regular"):
        ''' Creates a fish (either regular or zombie) w/ necessary initial
        variables and adds to display'''

        ball = v.sphere(make_trail=self.showTrails, retain=10,
                        pos=(rand.random()*23 - 11.5, rand.random()*12-6, 0),
                        radius=0.15, vel=[rand.random()*.15-.075,
                                          rand.random()*.15-.075, 0],
                        fitness=1.0, trail_type="points",
                        material=v.materials.rough)
        if self.smarterFish:
            f = v.frame()
            cr = v.shapes.circle(radius=1, np=64, angle1=.5, angle2=-.5)
            cr2 = v.extrusion(radius=1, frame=f, shape=cr, color=v.color.red,
                              pos=ball.pos)
        if type == "regular":
            # Here, we will create regular fish!
            ball.color = self.fishColor
            ball.trail_object.color = self.fishColor
            self.fishList.append(ball)
            if self.smarterFish:
                self.fishHitList.append(cr2)
                self.shapeTest.append(f)
        elif type == "zombie":
            # Here, we will create zombie fish!
            ball.color = self.zombieColor
            ball.trail_object.color = self.zombieColor
            self.zombieList.append(ball)
            if self.smarterFish:
                self.zombieHitList.append(cr2)
                self.zombieShapeTest.append(f)

    def mouseMove(self, e):
        ''' This function runs every time the mouse moves in the frame '''
        # If the mouse is over an object, display tooltip
        if self.mainScene.mouse.pick is not None:
            self.ttFish = self.mainScene.mouse.pick
            self.fishLabelTimer = 100

    def updateTTip(self):
        ''' Runs every frame to update tooltips showing fish metadata '''
        if self.fishLabelTimer > 0 and self.showTTip:
            self.fishLabelTimer -= 5
            # BUG: items with nparray time position return error when
            # attempting to set fishLabel pos
            try:
                self.fishLabelText.pos = self.ttFish.pos
            except:
                pass
            self.fishLabelText.text = 'Vel: ' + \
                ("%.2f" % (100. * sqrt(self.ttFish.vel[0]**2 +
                                       self.ttFish.vel[0]**2))) + \
                "\nFitness: " + str(self.ttFish.fitness)
            if self.fishLabelTimer == 0:
                self.fishLabelText.pos = (-100, 0, 0)

    def loop(self):
        ''' We use this funciton as the time stream for our simulation '''
        while True:
            # Necessary for vpython to run
            v.rate(self.FPS)

            self.updateTTip()

            # Updates the text display
            self.labelText.text = 'Number of Zombies: ' + \
                str(len(self.zombieList)) + '\nNumber of Fish: ' + \
                str(len(self.fishList)) + '\n' + \
                ("Progress: %.2f" %
                 (100 * (self.timeOutCounter / self.timeOut))) + "%"

            # Handles the spawning of the food
            if self.carryingCapacity:
                self.spawnFoodDelay += 1
                if self.spawnFoodDelay > self.spawnFoodDelayMax and \
                        len(self.foodList) < 40:
                    self.spawnFoodDelay = 0
                    self.createFood()
                    self.createFood()

            # Handles data gathering for simulation graph
            self.timeOutCounter += 1
            if self.timeOutCounter % 15 == 0:
                self.zombiePopulationTracker.append(len(self.zombieList))
                self.fishPopulationTracker.append(len(self.fishList))

            # After a set amount of time, close the simulation, store data,
            # and run python3 script for graph
            if self.timeOutCounter >= self.timeOut:
                p = Popen('''C:\Users\Gabe\Desktop\main.bat''')
                file = open('data.txt', 'w')
                print('true')
                file.write(str(self.zombiePopulationTracker) + "\n" +
                           str(self.fishPopulationTracker))
                file.close()
                stdout, stderr = p.communicate()
                break

            # Only check for collisions every other frame
            self.selfCount += 1
            if self.selfCount > self.selfCountMax:
                self.checkCollisions()

            # Handles the spawning of cures
            if self.spawnCures:
                self.spawnCureDelay += 1
                # The probability of spawning a cure increases linearly with
                # time until a vcre spawns
                spawnCureProbability = rand.random() * \
                    (self.spawnCureDelay / self.spawnCureDelayMax)
                if spawnCureProbability > .5 and \
                   len(self.cureList) < self.cureMax:
                    self.createCure()
                    self.spawnCureDelay = 0

            # Handles all updating of fish
            for fishIndex in range(len(self.fishList)-1, -1, -1):

                i = self.fishList[fishIndex]
                if self.smarterFish:
                    k = self.fishHitList[fishIndex]

                # Here, we check collisions between fish and other food
                for foodIndex in range(len(self.foodList)-1, -1, -1):
                    food = self.foodList[foodIndex]
                    if self.isColliding(i, food, 1):
                        i.fitness = 1
                        food.visible = False
                        self.foodList.pop(foodIndex)
                        del food

                # Fish slowly starve to death
                i.fitness -= .001
                if i.fitness <= 0:
                    i.fitness = 0
                if rand.random() < .01 * (1 - i.fitness):
                    if self.smarterFish:
                        j = self.shapeTest[fishIndex]
                    i.trail_object.visible = False
                    i.retain = 0
                    i.visible = False
                    if self.smarterFish:
                        k.visible = False
                        j.visible = False
                    if self.smarterFish:
                        self.shapeTest.pop(fishIndex)
                    self.fishList.pop(fishIndex)
                    if self.smarterFish:
                        self.fishHitList.pop(fishIndex)
                    if self.smarterFish:
                        del k
                    del i
                    if self.smarterFish:
                        del j
                    break

                # Spawns new fish
                if self.fishMultiply:
                    if rand.random() < .002:
                        self.createFish()

                # Update fish position according to velocity
                i.pos.x += i.vel[0]
                i.pos.y += i.vel[1]
                if self.smarterFish:
                    k.pos[0][0] = i.pos.x
                    k.pos[0][1] = i.pos.y

                # Give fish random acceleration to simulate random walk
                i.vel[0] += rand.random()*.02 - .01
                i.vel[1] += rand.random()*.02 - .01

                # If AI enabled, we move each fish's AI hitbox
                if self.smarterFish:
                    self.shapeTest[fishIndex].pos = k.pos[0]
                    k.pos[0][0] = 0
                    k.pos[0][1] = 0
                    self.shapeTest[fishIndex].rotate(angle=.02, axis=(0, 0, 1))

                # Make sure velocity is below maximum velocity
                if i.vel[0] > self.vmax:
                    i.vel[0] = self.vmax
                if i.vel[1] > self.vmax:
                    i.vel[1] = self.vmax
                if i.vel[0] < -self.vmax:
                    i.vel[0] = -self.vmax
                if i.vel[1] < -self.vmax:
                    i.vel[1] = -self.vmax

                # Make fish bounce off sides of simulation
                if i.pos.x > 11.5:
                    i.vel[0] *= -1
                    i.pos.x = 11.5
                if i.pos.x < -11.5:
                    i.vel[0] *= -1
                    i.pos.x = -11.5
                if i.pos.y > 6:
                    i.vel[1] *= -1
                    i.pos.y = 6
                if i.pos.y < -6:
                    i.vel[1] *= -1
                    i.pos.y = -6

            # Handles all updating of zombies
            for i_index in range(len(self.zombieList)):

                i = self.zombieList[i_index]
                if self.smarterFish:
                    k = self.zombieHitList[i_index]

                # Updates position based on velocity
                i.pos.x += i.vel[0]
                i.pos.y += i.vel[1]
                if self.smarterFish:
                    k.pos[0][0] = i.pos.x
                    k.pos[0][1] = i.pos.y

                # Give zombies random acceleration to simulate random walk
                i.vel[0] += rand.random()*.02 - .01
                i.vel[1] += rand.random()*.02 - .01

                # Test rotating FOV hitbox
                if self.smarterFish:
                    self.zombieShapeTest[i_index].pos = k.pos[0]
                    k.pos[0][0] = 0
                    k.pos[0][1] = 0
                    self.zombieShapeTest[i_index].rotate(angle=.02,
                                                         axis=(0, 0, 1))

                # Prevent zombies from moving too fast
                if i.vel[0] > self.vmax:
                    i.vel[0] = self.vmax
                if i.vel[1] > self.vmax:
                    i.vel[1] = self.vmax
                if i.vel[0] < -1*self.vmax:
                    i.vel[0] = -1*self.vmax
                if i.vel[1] < -1*self.vmax:
                    i.vel[1] = -1*self.vmax

                # Add collisions to boundaries of simulation
                if i.pos.x > self.xmax:
                    i.vel[0] *= -1
                    i.pos.x = self.xmax
                    if self.smarterFish:
                        k.pos[0][0] = self.xmax
                if i.pos.x < -self.xmax:
                    i.vel[0] *= -1
                    i.pos.x = -self.xmax
                    if self.smarterFish:
                        k.pos[0][0] = -self.xmax
                if i.pos.y > self.ymax:
                    i.vel[1] *= -1
                    i.pos.y = self.ymax
                    if self.smarterFish:
                        k.pos[0][1] = self.ymax
                if i.pos.y < -self.ymax:
                    i.vel[1] *= -1
                    i.pos.y = -self.ymax
                    if self.smarterFish:
                        k.pos[0][1] = -self.ymax

    def checkCollisions(self):
        ''' Runs all of the collision detection for the simulation '''
        # First, we iterate through each zombie
        for zombieIndex in range(len(self.zombieList)-1, -1, -1):
            zombie = self.zombieList[zombieIndex]

            # Check collisions between zombies and regular fish
            for fishIndex in range(len(self.fishList)-1, -1, -1):
                fish = self.fishList[fishIndex]

                if self.isColliding(zombie, fish):
                    # Make fish bounce off
                    zombie.vel[0] *= -1
                    zombie.vel[1] *= -1
                    fish.vel[0] *= -1
                    fish.vel[1] *= -1

                    # Turn fish into zombies
                    fish.color = self.zombieColor
                    fish.trail_object.color = self.zombieColor
                    self.zombieList.append(fish)
                    if self.smarterFish:
                        self.zombieHitList.append(self.fishHitList[fishIndex])
                    if self.smarterFish:
                        self.zombieShapeTest.append(self.shapeTest[fishIndex])
                    self.fishList.pop(fishIndex)
                    if self.smarterFish:
                        self.fishHitList.pop(fishIndex)
                        self.shapeTest.pop(fishIndex)

            # Check collisions between zombies and cures
            for cureIndex in range(len(self.cureList)-1, -1, -1):
                cure = self.cureList[cureIndex]

                # If a collision occurs, turn zombies into regular fish
                if not self.cureSpheres:

                    if self.isColliding(zombie, cure, 1):
                        zombie.color = self.fishColor
                        zombie.trail_object.color = self.fishColor
                        cure.visible = False
                        self.cureList.pop(cureIndex)
                        del cure
                        self.fishList.append(zombie)
                        if self.smarterFish:
                            L1 = self.zombieHitList[zombieIndex]
                            L2 = self.zombieShapeTest[zombieIndex]
                            self.fishHitList.append(L1)
                            self.shapeTest.append(L2)
                        self.zombieList.pop(zombieIndex)
                        if self.smarterFish:
                            self.zombieHitList.pop(zombieIndex)
                            self.zombieShapeTest.pop(zombieIndex)
                        break
                else:
                    if self.isColliding(zombie, cure):

                        zombie.color = self.fishColor
                        zombie.trail_object.color = self.fishColor
                        cure.visible = False
                        self.cureList.pop(cureIndex)
                        del cure
                        self.fishList.append(zombie)
                        if self.smarterFish:
                            L1 = self.zombieHitList[zombieIndex]
                            L2 = self.zombieShapeTest[zombieIndex]
                            self.fishHitList.append(L1)
                            self.shapeTest.append(L2)
                        self.zombieList.pop(zombieIndex)
                        if self.smarterFish:
                            self.zombieHitList.pop(zombieIndex)
                            self.zombieShapeTest.pop(zombieIndex)
                        break

    def isColliding(self, o1, o2, type=0):
        ''' Checks for collision between two spherical
        objects in the XY plane'''

        # Collisions between spherical vpython objects
        if type == 0:
            distX = o1.pos[0] - o2.pos[0]
            distY = o1.pos[1] - o2.pos[1]
        # Collisions between a spherical object and a circle (extrusion)
        else:
            distX = o1.pos[0] - o2.pos[0][0]
            distY = o1.pos[1] - o2.pos[0][1]

        dist = sqrt(distX**2 + distY**2)
        if dist <= (o1.radius + o2.radius):
            return True
        return False

# This automatically runs our code when we run the file with python
if __name__ == "__main__":
    main = Main()
