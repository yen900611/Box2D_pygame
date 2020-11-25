import pygame
import Box2D
from math import pi, sin, cos
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
world = b2.world(gravity=(0, 0), doSleep=True)

# --- setup mazz ---

well = world.CreateKinematicBody(position = (12,0.5),linearVelocity = (0,0))
box = well.CreatePolygonFixture(box = (12,0.5))

well = world.CreateKinematicBody(position = (12,23.5),linearVelocity = (0,0))
box = well.CreatePolygonFixture(box = (12,0.5))

well = world.CreateKinematicBody(position = (0.5,12),linearVelocity = (0,0))
box = well.CreatePolygonFixture(box = (0.5,11))

well = world.CreateKinematicBody(position = (23.5,12),linearVelocity = (0,0))
box = well.CreatePolygonFixture(box = (0.5,11))

well = world.CreateKinematicBody(position = (17.5,9.25),linearVelocity = (0,0))
box = well.CreatePolygonFixture(box = (0.5,8.25))

well = world.CreateKinematicBody(position = (6.5,9),linearVelocity = (0,0))
box = well.CreatePolygonFixture(box = (0.5,3))

well = world.CreateKinematicBody(position = (12,15.25),linearVelocity = (0,0))
box = well.CreatePolygonFixture(box = (0.5,2.75))

well = world.CreateKinematicBody(position = (12,3.75),linearVelocity = (0,0))
box = well.CreatePolygonFixture(box = (0.5,3))

well = world.CreateKinematicBody(position = (6.5,17.5),linearVelocity = (0,0))
box = well.CreatePolygonFixture(box = (5.5,0.5))

well = world.CreateKinematicBody(position = (3.75,6.5),linearVelocity = (0,0))
box = well.CreatePolygonFixture(box = (2.75,0.5))

var_well = world.CreateKinematicBody(position = (42,16),linearVelocity = (-2,0))
var_well.CreatePolygonFixture(box = (2,0.5))

# --- setup car ---
car_image = pygame.transform.scale(pygame.image.load("car2.png"),(96,60))
car_ori_image = pygame.transform.rotate(car_image,90)
left_wheel = car = world.CreateDynamicBody(position = (19.25, 3))
left_wheel.CreateCircleFixture(radius=0.3, density=1, friction=0.1,)

right_wheel = car = world.CreateDynamicBody(position = (21.75, 3))
right_wheel.CreateCircleFixture(radius=0.3, density=1, friction=0.1,)

car = world.CreateDynamicBody(position = (20.5,3))
car.CreatePolygonFixture(box = (1,1.4),density = 1, friction = 0.1,)

joint = world.CreateJoint(bodyA = left_wheel,bodyB = car, collideConnected = True, type = Box2D.b2WheelJoint)
joint = world.CreateJoint(bodyA = right_wheel,bodyB = car, collideConnected = True, type = Box2D.b2WheelJoint)


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
right_force = 0
left_force = 0
# --- main game loop ---
running = True
while running:
    # Check the event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # The user closed the window or pressed escape
            running = False

        if (event.type == KEYDOWN and event.key == K_UP):
            right_force = 10
            # right_wheel.linearVelocity = (0,5)
            # right_wheel.ApplyForce(force=(0,10), point=(right_wheel.position[0],right_wheel.position[1]), wake=True)
        if (event.type == KEYDOWN and event.key == K_DOWN):
            # right_wheel.ApplyForce(force=(0,-10), point=(right_wheel.position[0],right_wheel.position[1]), wake=True)
            right_force = -10

        if (event.type == KEYDOWN and event.key == K_w):
            left_force = 10
            # left_wheel.linearVelocity = (0,5)
            # left_wheel.ApplyForce(force=(0,10), point=(left_wheel.position[0],left_wheel.position[1]), wake=True)
        if (event.type == KEYDOWN and event.key == K_s):
            left_force = -10
            # left_wheel.ApplyForce(force=(0,-10), point=(left_wheel.position[0],left_wheel.position[1]), wake=True)
    right_force_y = right_force * cos(car.angle)
    right_force_x = right_force * sin(car.angle)
    # print(right_force_x,right_force_y,car.angle)
    print("angle",car.angle*180/pi)
    right_wheel.ApplyForce(force=(right_force_x, right_force_y), point=(car.position[0]+0.3, car.position[1]-0.1), wake=True)
    left_wheel.ApplyForce(force=(left_force * sin(car.angle), left_force * cos(car.angle)), point=(car.position[0]-0.3, car.position[1]-0.1), wake=True)
    if right_force>0:
        right_force-=0.1
    if left_force>0:
        left_force-=0.1
    if right_force<=0:
        right_wheel.linearVelocity = (0,0)
    if left_force<=0:
        left_wheel.linearVelocity = (0,0)

    # if var_well.position[0] >= 42:
    #     var_well.linearVelocity[0] = -2
    # elif var_well.position[0] <= 38:
    #     var_well.linearVelocity[0] = 2
    # else:
    #     pass

    screen.fill((0, 0, 0, 0))
    # Draw the world
    for ground_body in world.bodies:
        for fixture in ground_body.fixtures:
            fixture.shape.draw(ground_body, fixture)

    car_ = pygame.transform.rotate(car_ori_image,(car.angle*180/pi)%360)
    screen.blit(car_, ((car.position[0] - 1)*PPM, (24-car.position[1] - 1)*PPM))
    # Make Box2D simulate the physics of our world for one step.
    world.Step(TIME_STEP, 10, 10)

    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')