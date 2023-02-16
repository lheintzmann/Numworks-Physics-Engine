import kandinsky as k
from turtle import *
from time import *
from ion import *
import math

WIDTH = 320
HEIGHT = 220

GRAVITY = 9.81
WATER_VISCOSITY = 0.5
particles = []

class WaterObject:
    def __init__(self, x, y, mass, color):
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.velocity = [0, 0]
        self.radius = int(mass/2)
        self.density = mass / (math.pi * self.radius ** 2)
        self.pressure = 0
    
    def move(self, dt, particles):
      self.velocity[1] -= GRAVITY*dt
      total_force = [0, 0]
      for particle in particles:
        if particle != self:
            distance = math.sqrt((self.x - particle.x)**2 + (self.y - particle.y)**2)
            if distance < self.radius + particle.radius:
                overlap = (self.radius + particle.radius - distance) / 2
                angle = math.atan2(self.y - particle.y, self.x - particle.x)
                force = 0.5 * WATER_VISCOSITY * self.density * particle.density * overlap * dt
                total_force[0] += force * math.cos(angle)
                total_force[1] += force * math.sin(angle)
                repulsion_force = 0.5 * (overlap**2) / dt
                total_force[0] += repulsion_force * math.cos(angle + math.pi)
                total_force[1] += repulsion_force * math.sin(angle + math.pi)
      self.velocity[0] += total_force[0]
      self.velocity[1] += total_force[1]
      self.x -= self.velocity[0]*dt
      self.y -= self.velocity[1]*dt
      if self.y > HEIGHT - self.radius:
          self.y = HEIGHT - self.radius
          self.velocity[1] = -self.velocity[1] * 0.5
      if self.x < self.radius:
          self.x = self.radius
          self.velocity[0] = -self.velocity[0] * 0.5
      if self.x > WIDTH - self.radius:
          self.x = WIDTH - self.radius
          self.velocity[0] = -self.velocity[0] * 0.5
      for particle in particles:
        if particle != self:
            distance = math.sqrt((self.x - particle.x)**2 + (self.y - particle.y)**2)
            if distance < self.radius + particle.radius:
                overlap = (self.radius + particle.radius - distance) / 2
                angle = math.atan2(self.y - particle.y, self.x - particle.x)
                self.x += overlap * math.cos(angle)
                self.y += overlap * math.sin(angle)

    def draw(self):
        k.fill_circle(int(self.x), int(self.y), self.radius, self.color)

for i in range(6):
    particles.append(WaterObject(i*32 + 32, 20, 32, (80, 148, 224)))

def add():
    if keydown(KEY_OK):
        particles.append(WaterObject(120, 12, 32, (64, 164, 223)))

def display():
    k.draw_string('Particles:' + str(len(particles)),0,0)

while True:
    reset()
    display()
    for particle in particles:
        particle.move(0.1, particles)
        particle.draw()
    add()
    sleep(0.01)
