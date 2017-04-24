from __future__ import print_function
from __future__ import division
import visual as v
import random as rand
from math import pi
from math import sqrt
import time
from subprocess import Popen

class Main(object):
    def __init__(self):

        self.zombiePopulationTracker = []
        self.fishPopulationTracker = []

        self.counter = 0
        self.startTime = time.time()
        self.vmax = .15

        self.fishList = []
        self.zombieList = []
        self.cureList = []

        self.selfCount = 0

        self.fishMultiply = False
        self.fishMultiplyDelay = 0
        self.fishMultiplyDelayMax = 0

        self.spawnCures = True
        self.spawnCureDelayMax = 75
        self.spawnCureDelay = 0
        self.cureMax = 18   

        self.FPS = 30
        self.createDisplay()
        self.startSimulation()
        self.loop()

    def startSimulation(self):
        ''' Spawns all of the things needed for the simulation'''
        for i in range(12):
            self.createFish()
        for i in range(3):
            self.createFish(type="zombie")

    def createDisplay(self):
        ''' Creates the main display screen for the game '''
        self.mainScene = v.display(title='Fish Zombies: Simulation', x=0, y=0, width=1280, height=800, center=(0,0,0), background=(0,0,0))
        self.mainScene.select() #Makes this the main display
        #self.mainScene.lights = [] #no distant lighting
        #self.fullLight = v.distant_light(direction=(0.22, 0.44, 0.88), color=v.color.white)
        #self.fullLight.visible = False
        self.mainScene.userspin = False
        self.mainScene.userzoon = False
        self.mainScene.autoscale = False
        self.mainScene.range = (12,6,1)
        self.mainScene.show_rendertime = True

    def createCure(self):
        ''' Creates the blobs that will cure the zombie-fish '''
        #ball = v.sphere(pos=(rand.random()*24 - 12,rand.random()*12-6,0), radius=0.1, color=v.color.blue)
        ball = v.extrusion(radius = .1, pos=(rand.random()*24 - 12, rand.random()*12-6), color = v.color.blue, shape = v.shapes.circle(pos=(0,0), radius=.1))
        self.cureList.append(ball)

    def createFish(self, type="regular"):
        ball = v.sphere(pos=(rand.random()*24 - 12, rand.random()*12-6,0), radius=0.15, vel = [rand.random()*.15-.075,   rand.random()*.15-.075,0]) #goes from -12 to 12
        if type == "regular":
            #Here, we will create regular fish!
            ball.color = v.color.white
            self.fishList.append(ball)
        elif type == "zombie":
            #Here, we will create zombie fish!
            ball.color = v.color.green
            self.zombieList.append(ball)

    def loop(self):
        ''' We use this funciton as the time stream for our simulation '''
        while True:
            self.counter += 1
            if self.counter % 15 == 0:
                self.zombiePopulationTracker.append(len(self.zombieList))
                self.fishPopulationTracker.append(len(self.fishList))

            for i in range(len(self.fishList)):
                if rand.random() < .001:
                    self.createFish()

            if self.counter >= 5000:
                p = Popen('''C:\Users\Gabe\Desktop\main.bat''')
                file = open('data.txt', 'w')
                file.write(str(self.zombiePopulationTracker) + "\n" + str(self.fishPopulationTracker))
                file.close()
                stdout, stderr = p.communicate()
                break

            print("Progress: " + str(100* (self.counter / 5000) ) + "%", end="\r")

            v.rate(self.FPS)

            self.selfCount += 1
            if self.selfCount > 2:
                self.checkCollisions()

            for i in self.fishList:
                i.pos.x += i.vel[0]
                i.pos.y += i.vel[1]

                i.vel[0] += rand.random()*.02 - .01
                i.vel[1] += rand.random()*.02 - .01

                if i.vel[0] > self.vmax:
                    i.vel[0] = self.vmax
                if i.vel[1] > self.vmax:
                    i.vel[1] = self.vmax
                if i.vel[0] < -1*self.vmax:
                    i.vel[0] = -1*self.vmax
                if i.vel[1] < -1*self.vmax:
                    i.vel[1] = -1*self.vmax

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

            for i in self.zombieList:
                i.pos.x += i.vel[0]
                i.pos.y += i.vel[1]

                i.vel[0] += rand.random()*.02 - .01
                i.vel[1] += rand.random()*.02 - .01

                if i.vel[0] > self.vmax:
                    i.vel[0] = self.vmax
                if i.vel[1] > self.vmax:
                    i.vel[1] = self.vmax
                if i.vel[0] < -1*self.vmax:
                    i.vel[0] = -1*self.vmax
                if i.vel[1] < -1*self.vmax:
                    i.vel[1] = -1*self.vmax

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

            self.spawnCureDelay += 1
            spawnCureProbability = rand.random() * (self.spawnCureDelay/self.spawnCureDelayMax)
            if spawnCureProbability > .5 and len(self.cureList) < self.cureMax:
                self.createCure()
                self.spawnCureDelay = 0

    def checkCollisions(self):
        for zombieIndex in range(len(self.zombieList)-1, -1, -1):
            zombie = self.zombieList[zombieIndex]
            for fishIndex in range(len(self.fishList)-1, -1, -1):
                fish = self.fishList[fishIndex]
                if self.isColliding(zombie, fish) == True:
                    zombie.vel[0] *= -1
                    zombie.vel[1] *= -1
                    fish.vel[0] *= -1
                    fish.vel[1] *= -1
                    fish.color = v.color.green
                    self.zombieList.append(fish)
                    self.fishList.pop(fishIndex)
            for cureIndex in range(len(self.cureList)-1, -1, -1):
                cure = self.cureList[cureIndex]
                if self.isColliding(zombie, cure, 1) == True:
                    zombie.color = v.color.white
                    cure.visible = False
                    self.cureList.pop(cureIndex)
                    del cure
                    self.fishList.append(zombie)
                    self.zombieList.pop(zombieIndex)
                    break

    def isColliding(self, o1, o2, type=0):
        ''' Checks for collision between two spherical objects in the XY plane'''
        if type == 0:
            distX = o1.pos.x - o2.pos.x
            distY = o1.pos.y - o2.pos.y
        else:
            distX = o1.pos.x - o2.pos[0][0]
            distY = o1.pos.y - o2.pos[0][1]
        dist = sqrt(distX**2 + distY**2)

        if dist <= (o1.radius + o2.radius):
            return True
        return False

if __name__ == "__main__":
    main = Main()
