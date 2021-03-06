'''
try different type of joint # it has not started yet.
'''
import pygame
import math
from example.setting import *

import Box2D  # The main library

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Simple pygame example')
clock = pygame.time.Clock()


# --- pybox2d world setup ---
# Create the world
gravity = 0.5

world = Box2D.b2.world(gravity=(0, 0), doSleep=True, CollideConnected=False)

ground = world.CreateBody(position=(0, 20))

dynamic_body = world.CreateDynamicBody(position=(21, 3))
box1 = dynamic_body.CreatePolygonFixture(box=(1, 1.5), density=2, friction=0.1, restitution=0.3)

sensor_left = world.CreateDynamicBody(position = (19.8, 3))
ball = sensor_left.CreateCircleFixture(radius = 0.2)

sensor_right = world.CreateDynamicBody(position = (22.2, 3))
ball = sensor_right.CreateCircleFixture(radius = 0.2)

world.CreateDistanceJoint(bodyA=sensor_left,bodyB=dynamic_body,collideConnected=True)
world.CreateDistanceJoint(bodyA=sensor_right,bodyB=dynamic_body,collideConnected=True)

def create_wall():
    wall_bottom = world.CreateKinematicBody(position=(9, 0.5), linearVelocity=(0, 0))
    box = wall_bottom.CreatePolygonFixture(box=(9, 0.5))

    wall_top = world.CreateKinematicBody(position=(15, 23.5), linearVelocity=(0, 0))
    box = wall_top.CreatePolygonFixture(box=(9, 0.5))

    wall_left = world.CreateKinematicBody(position=(0.5, 12), linearVelocity=(0, 0))
    box = wall_left.CreatePolygonFixture(box=(0.5, 12))

    wall_right = world.CreateKinematicBody(position=(23.5, 12), linearVelocity=(0, 0))
    box = wall_right.CreatePolygonFixture(box=(0.5, 12))

    # wall = world.CreateKinematicBody(position=(18, 9.5), linearVelocity=(0, 0))
    # box = wall.CreatePolygonFixture(box=(0.5, 10))

create_wall()

wall_info = [
    [(1,1),(17.5,1)], [(1,1), (1,24)], [(23,0), (23,23)], [(1,24),(23,23)], [(18.5,0), (18.5, 19.5)]
]

colors = {
    Box2D.b2.kinematicBody: (255, 255, 255, 255),
    Box2D.b2.staticBody: (255, 255, 255, 255),
    Box2D.b2.dynamicBody: (127, 127, 127, 255),
}

# Let's play with extending the shape classes to draw for us.

def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, colors[body.type], vertices)

Box2D.b2.polygonShape.draw = my_draw_polygon

def my_draw_circle(circle, body, fixture):
    position = body.transform * circle.pos * PPM
    position = (position[0], SCREEN_HEIGHT - position[1])
    pygame.draw.circle(screen, colors[body.type], [int(
        x) for x in position], int(circle.radius * PPM))
    # Note: Python 3.x will enforce that pygame get the integers it requests,
    #       and it will not convert from float.

Box2D.b2.circleShape.draw = my_draw_circle


# --- main game loop ---

running = True
while running:

    screen.fill((0, 0, 0, 0))
    # Check the event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # The user closed the window or pressed escape
            running = False
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
            f = dynamic_body.GetWorldVector(localVector=(0.0, 100.0))
            p = dynamic_body.GetWorldPoint(localPoint=(1.0, 0.0))
            dynamic_body.ApplyForce(f, p, False)

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
            f = dynamic_body.GetWorldVector(localVector=(0.0, -100.0))
            p = dynamic_body.GetWorldPoint(localPoint=(1.0, 0.0))
            dynamic_body.ApplyForce(f, p, False)
            pass

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_s):
            f = dynamic_body.GetWorldVector(localVector=(0.0, -100.0))
            p = dynamic_body.GetWorldPoint(localPoint=(-1.0, 0.0))
            dynamic_body.ApplyForce(f, p, False)

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_w):
            f = dynamic_body.GetWorldVector(localVector=(0.0, 100.0))
            p = dynamic_body.GetWorldPoint(localPoint=(-1.0, 0.0))
            dynamic_body.ApplyForce(f, p, False)
            pass

    screen.fill((0, 0, 0, 0))
    # Draw the world
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)


    # Make Box2D simulate the physics of our world for one step.
    world.Step(TIME_STEP, 10, 10)


    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')