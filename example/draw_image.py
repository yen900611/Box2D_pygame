import pygame
from pygame.locals import *
import math

import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D import *
from Box2D.b2 import *

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 480

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Simple pygame example')
clock = pygame.time.Clock()

# --- pybox2d world setup ---
# Create the world

world = world(gravity=(0, 0), doSleep=True, CollideConnected=False)

body1 = world.CreateDynamicBody(position=(14, 18), angle=0, linearVelocity=(0, 0))
# circle = body1.CreateCircleFixture(radius=1, density=1, friction=0.1, restitution = 0.3)
box = body1.CreatePolygonFixture(box=(1, 3), density=1, friction=0.3, restitution=0.3)

body2 = world.CreateDynamicBody(position=(20, 18), angle=0, linearVelocity=(0, 0))
# circle = body2.CreateCircleFixture(radius=1, density=1, friction=0.1, restitution = 0.3)
box = body2.CreatePolygonFixture(box=(1, 3), density=1, friction=0.1, restitution=0.3)

right_wheel_velocity = 0
left_wheel_velocity = 0

dynamic_body = world.CreateDynamicBody(position=(17, 18))
box = dynamic_body.CreatePolygonFixture(box=(2, 2), density=1, friction=0.1, restitution=0.3)

joint = world.CreateJoint(bodyA=dynamic_body, bodyB=body1, collideConnected=True, type=b2WheelJoint)
joint = world.CreateJoint(bodyA=dynamic_body, bodyB=body2, collideConnected=True, type=b2WheelJoint)

colors = {
    kinematicBody: (255, 255, 255, 255),
    staticBody: (255, 255, 255, 255),
    dynamicBody: (127, 127, 127, 255),
}


# Let's play with extending the shape classes to draw for us.


def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, colors[body.type], vertices)


polygonShape.draw = my_draw_polygon


def my_draw_circle(circle, body, fixture):
    position = body.transform * circle.pos * PPM
    position = (position[0], SCREEN_HEIGHT - position[1])
    pygame.draw.circle(screen, colors[body.type], [int(
        x) for x in position], int(circle.radius * PPM))
    # Note: Python 3.x will enforce that pygame get the integers it requests,
    #       and it will not convert from float.


circleShape.draw = my_draw_circle

# load image
car_origin = pygame.transform.scale(pygame.image.load("car2.png"),(80,80))
car_rect = car_origin.get_rect()

angle = dynamic_body.angle*180/math.pi

# --- main game loop ---

running = True
while running:

    # Check the event queue
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # The user closed the window or pressed escape
            running = False
        if (event.type == KEYDOWN and event.key == K_UP):
            right_wheel_velocity = 10
            left_wheel_velocity = 10

        if (event.type == KEYDOWN and event.key == K_DOWN):
            right_wheel_velocity = -10
            left_wheel_velocity = -10

        if (event.type == KEYDOWN and event.key == K_LEFT):
            dynamic_body.ApplyTorque(1000.0, True)
            pass

        if (event.type == KEYDOWN and event.key == K_RIGHT):
            dynamic_body.ApplyTorque(-1000.0, True)
            pass


    screen.fill((0, 0, 0, 0))
    # Draw the world
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)


    # Make Box2D simulate the physics of our world for one step.
    world.Step(TIME_STEP, 10, 10)
    world.ClearForces()

    car = pygame.transform.rotate(car_origin,angle%360)
    car_rect.center = dynamic_body.position[0]* PPM, SCREEN_HEIGHT - dynamic_body.position[1]* PPM
    angle = dynamic_body.angle*180/math.pi
    screen.blit(car,car_rect)


    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')