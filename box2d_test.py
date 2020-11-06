'''
origin code:
'''
import pygame
from pygame.locals import *

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
world = world(gravity=(0, 0), doSleep=True,CollideConnected = False)

# And a static body to hold the ground shape
# body = world.CreateDynamicBody(position=(22.5, 0.5))
# box = body.CreatePolygonFixture(box=(22.5, 0.5), density=999999, friction=10)

# body = world.CreateDynamicBody(position=(0.5, 12.5))
# box = body.CreatePolygonFixture(box=(0.5, 11.5), density=999999, friction=10)

# body = world.CreateDynamicBody(position=(23, 23.5))
# box = body.CreatePolygonFixture(box=(22, 0.5), density=999999, friction=10)

# body = world.CreateDynamicBody(position=(44.5, 12))
# box = body.CreatePolygonFixture(box=(0.5, 11), density=999999, friction=10)

'''
Creat a static body
'''
bodyDef = b2BodyDef() # Box2D.b2BodyDef
bodyDef.position = (22.5,12)
body = world.CreateBody(bodyDef)
groundBody = b2PolygonShape(box = (1,7))
groundBoxFixture = b2FixtureDef(shape=groundBody)
body.CreateFixture(groundBoxFixture)
# above is equal in this：
ground_body = world.CreateStaticBody(
    position=(0, 0),
    shapes=polygonShape(box=(50, 1))
)

# Create a couple dynamic bodies
# body1 = world.CreateDynamicBody(position=(10,20),linearVelocity=(0,0))
# circle = body1.CreateCircleFixture(radius=0.5, density=9999999, friction=0.3)

# body2 = world.CreateDynamicBody(position=(20,25),linearVelocity=(0,5))
# circle2 = body2.CreateCircleFixture(radius=0.5, density=1, friction=0.3)

# joint = world.CreateJoint(bodyA = body1,bodyB = body2, collideConnected = True, type = b2RevoluteJoint)

# body = world.CreateDynamicBody(position=(30, 20), angle=10,linearVelocity = (0,-10))
# box = body.CreatePolygonFixture(vertices=[(3,5), (1,1), (0,1),(5,3)], density=1, friction=0.3, restitution = 0.9)

body = world.CreateDynamicBody(position=(12.5, 12), angle=0,linearVelocity = (0,0))
box = body.CreatePolygonFixture(box=(3,0.5), density=1, friction=0.1, restitution = 0.5)

# body = world.CreateDynamicBody(position=(30, 20), angle=0,linearVelocity = (0,0))
# box = body.CreatePolygonFixture(box=(3,3), density=100, friction=0.1, restitution = 0.5)

# body = world.CreateDynamicBody(position=(12.5, 15), angle=1,linearVelocity = (0,0))
# box = body.CreatePolygonFixture(box=(3,0.5), density=1, friction=0.1)

# body_test = world.CreateDynamicBody(position=(12.5, 18), angle=1.5,linearVelocity = (0,0))
# box = body_test.CreatePolygonFixture(box=(3,0.5), density=1, friction=0.1)

# body = world.CreateKinematicBody(position =(12.5, 18))
# box = body.CreatePolygonFixture(box = (3,1),density = 1, friction = 0.1)

dynamic_body = world.CreateDynamicBody(position =(12.5, 18))
box = dynamic_body.CreatePolygonFixture(box = (3,1),density = 1, friction = 0.1, restitution = 0.5)
colors = {
    kinematicBody :(255,255,255,255),
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

# --- main game loop ---

running = True
while running:
    # Check the event queue
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # The user closed the window or pressed escape
            running = False
        if (event.type == KEYDOWN and event.key == K_UP):
            dynamic_body.linearVelocity[1] += 1
        if (event.type == KEYDOWN and event.key == K_DOWN):
            dynamic_body.linearVelocity[1] -= 1
        if (event.type == KEYDOWN and event.key == K_LEFT):
            dynamic_body.linearVelocity[0] -= 1
        if (event.type == KEYDOWN and event.key == K_RIGHT):
            dynamic_body.linearVelocity[0] += 1

            # body.ApplyForce(force=(10,0), point=(1,0), wake=True)
            # print(dynamic_body)

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