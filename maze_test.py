import pygame
import Box2D
from math import pi, sin, cos, sqrt
from Box2D import b2
from pygame import *

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 480

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Simple pygame example')
clock = pygame.time.Clock()

# --- pybox2d world setup ---
# Create the world
gravity = 0.5
world = b2.world(gravity=(0, 0), doSleep=True)
ground = world.CreateBody(position=(0, 20))

# --- setup mazz ---

def createMaze():
    wall = world.CreateKinematicBody(position = (12, 0.5), linearVelocity = (0, 0))
    box = wall.CreatePolygonFixture(box = (12, 0.5))

    wall = world.CreateKinematicBody(position = (12, 23.5), linearVelocity = (0, 0))
    box = wall.CreatePolygonFixture(box = (12, 0.5))

    wall = world.CreateKinematicBody(position = (0.5, 12), linearVelocity = (0, 0))
    box = wall.CreatePolygonFixture(box = (0.5, 11))

    wall = world.CreateKinematicBody(position = (23.5, 12), linearVelocity = (0, 0))
    box = wall.CreatePolygonFixture(box = (0.5, 11))

    wall = world.CreateKinematicBody(position = (17.5, 9.25), linearVelocity = (0, 0))
    box = wall.CreatePolygonFixture(box = (0.5, 8.25))

    wall = world.CreateKinematicBody(position = (6.5, 9), linearVelocity = (0, 0))
    box = wall.CreatePolygonFixture(box = (0.5, 3))

    wall = world.CreateKinematicBody(position = (12, 15.25), linearVelocity = (0, 0))
    box = wall.CreatePolygonFixture(box = (0.5, 2.75))

    wall = world.CreateKinematicBody(position = (12, 3.75), linearVelocity = (0, 0))
    box = wall.CreatePolygonFixture(box = (0.5, 3))

    wall = world.CreateKinematicBody(position = (6.5, 17.5), linearVelocity = (0, 0))
    box = wall.CreatePolygonFixture(box = (5.5, 0.5))

    wall = world.CreateKinematicBody(position = (3.75, 6.5), linearVelocity = (0, 0))
    box = wall.CreatePolygonFixture(box = (2.75, 0.5))

# --- setup car ---
dynamic_body = world.CreateDynamicBody(position=(21, 4))
box1 = dynamic_body.CreatePolygonFixture(box=(1, 1.5), density=2, friction=0.1, restitution=0)

r = sqrt(0.2 * dynamic_body.inertia / dynamic_body.mass)


'''模擬摩擦力'''
world.CreateFrictionJoint(
    bodyA=ground,
    bodyB=dynamic_body,
    localAnchorA=(0, 0),
    localAnchorB=(0, 0),
    collideConnected=True,
    maxForce=dynamic_body.mass * gravity,
    maxTorque=dynamic_body.mass * r * gravity
)

sensor_left = world.CreateDynamicBody(position = (19.8, 4))
ball = sensor_left.CreateCircleFixture(radius = 0.2)

sensor_right = world.CreateDynamicBody(position = (22.2, 4))
ball = sensor_right.CreateCircleFixture(radius = 0.2)

world.CreateDistanceJoint(bodyA=sensor_left,bodyB=dynamic_body,collideConnected=True)
world.CreateDistanceJoint(bodyA=sensor_right,bodyB=dynamic_body,collideConnected=True)


# --- pygame draw function setup ---
colors = {
    b2.dynamicBody:(127, 127,127), # grey
    b2.staticBody: (255, 255, 255), # white
    b2.kinematicBody:(100,127,180)
}
def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, colors[body.type], vertices)
b2.polygonShape.draw = my_draw_polygon

def my_draw_circle(circle, body, fixture):
    position = body.transform * circle.pos * PPM
    position = (position[0], SCREEN_HEIGHT - position[1])
    pygame.draw.circle(screen, colors[body.type], [int(
        x) for x in position], int(circle.radius * PPM))
    # Note: Python 3.x will enforce that pygame get the integers it requests,
    #       and it will not convert from float.
b2.circleShape.draw = my_draw_circle

createMaze()
# --- main game loop ---
running = True
while running:
    # Check the event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # The user closed the window or pressed escape
            running = False

        if (event.type == KEYDOWN and event.key == K_UP):
            f = dynamic_body.GetWorldVector(localVector=(0.0, 200.0))
            p = dynamic_body.GetWorldPoint(localPoint=(0.0, 2.0))
            dynamic_body.ApplyForce(f, p, True)

        if (event.type == KEYDOWN and event.key == K_DOWN):
            f = dynamic_body.GetWorldVector(localVector=(0.0, -200.0))
            p = dynamic_body.GetWorldPoint(localPoint=(0.0, 2.0))
            dynamic_body.ApplyForce(f, p, True)

        if (event.type == KEYDOWN and event.key == K_LEFT):
            dynamic_body.ApplyTorque(100.0, True)

        if (event.type == KEYDOWN and event.key == K_RIGHT):
            dynamic_body.ApplyTorque(-100.0, True)

    screen.fill((0, 0, 0, 0))
    # Draw the world
    for ground_body in world.bodies:
        for fixture in ground_body.fixtures:
            fixture.shape.draw(ground_body, fixture)

    # Make Box2D simulate the physics of our world for one step.
    world.Step(TIME_STEP, 10, 10)

    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')