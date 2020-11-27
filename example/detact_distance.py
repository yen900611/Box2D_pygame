'''
origin code:
'''
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
gravity = 0.5

world = world(gravity=(0, 0), doSleep=True, CollideConnected=False)

ground = world.CreateBody(position=(0, 20))

dynamic_body = world.CreateDynamicBody(position=(17, 18))
box1 = dynamic_body.CreatePolygonFixture(box=(1, 1.5), density=2, friction=0.1, restitution=0.3)

r = math.sqrt(0.2 * dynamic_body.inertia / dynamic_body.mass)


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

sensor_left = world.CreateDynamicBody(position = (15.8, 18))
ball = sensor_left.CreateCircleFixture(radius = 0.2)

sensor_right = world.CreateDynamicBody(position = (18.2, 18))
ball = sensor_right.CreateCircleFixture(radius = 0.2)

world.CreateDistanceJoint(bodyA=sensor_left,bodyB=dynamic_body,collideConnected=True)
world.CreateDistanceJoint(bodyA=sensor_right,bodyB=dynamic_body,collideConnected=True)


wall_bottom = world.CreateKinematicBody(position=(12, 0.5), linearVelocity=(0, 0))
box = wall_bottom.CreatePolygonFixture(box=(12, 0.5))

wall_top = world.CreateKinematicBody(position=(12, 23.5), linearVelocity=(0, 0))
box = wall_top.CreatePolygonFixture(box=(12, 0.5))

wall_left = world.CreateKinematicBody(position=(0.5, 12), linearVelocity=(0, 0))
box = wall_left.CreatePolygonFixture(box=(0.5, 11))

wall_right = world.CreateKinematicBody(position=(23.5, 12), linearVelocity=(0, 0))
box = wall_right.CreatePolygonFixture(box=(0.5, 11))

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


# transform1 = b2Transform()

circleShape.draw = my_draw_circle

# load image
car_origin = pygame.transform.scale(pygame.image.load("car2.png"),(80,80))

angle = dynamic_body.angle*180/math.pi

# --- main game loop ---

running = True
while running:
    # print("worldVector " + str(dynamic_body.GetWorldVector(localVector = (0, 10))))
    # print("WorldPoint " + str(dynamic_body.GetWorldPoint(localPoint=(0.0, 0.0))))
    # print("position " + str(dynamic_body.position))
    # TODO Distance
    right_distance = b2Distance(shapeA=ball.shape, shapeB=box.shape, transformA=sensor_right.transform, transformB=wall_right.transform)
    # print("origin data " + str(right_distance.distance))
    # print("count data " + str(right_distance.distance * math.cos(dynamic_body.angle)))
    # print(dynamic_body.angle)
    # Check the event queue
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # The user closed the window or pressed escape
            running = False
        if (event.type == KEYDOWN and event.key == K_UP):
            f = dynamic_body.GetWorldVector(localVector=(0.0, 200.0))
            # p = dynamic_body.GetWorldPoint(localPoint=(0.0, 2.0))
            p = dynamic_body.position
            dynamic_body.ApplyForce(f, p, True)

        if (event.type == KEYDOWN and event.key == K_DOWN):
            f = dynamic_body.GetWorldVector(localVector=(0.0, -200.0))
            p = dynamic_body.GetWorldPoint(localPoint=(0.0, 2.0))
            dynamic_body.ApplyForce(f, p, True)
            pass

        if (event.type == KEYDOWN and event.key == K_LEFT):
            dynamic_body.ApplyTorque(100.0, True)
            pass

        if (event.type == KEYDOWN and event.key == K_RIGHT):
            dynamic_body.ApplyTorque(-100.0, True)
            pass

        if (event.type == KEYDOWN and event.key == K_s):
            PPM += 1

        if (event.type == KEYDOWN and event.key == K_w):
            PPM -= 1


    screen.fill((0, 0, 0, 0))
    # Draw the world
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)


    # Make Box2D simulate the physics of our world for one step.
    world.Step(TIME_STEP, 10, 10)
    world.ClearForces()

    car = pygame.transform.rotate(car_origin,angle%360 + 90)
    angle = dynamic_body.angle*180/math.pi
    # screen.blit(car,((dynamic_body.position[0]-2)*20, (24-dynamic_body.position[1]-2)*20))


    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')