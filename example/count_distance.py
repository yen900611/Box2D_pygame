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

def cross_point(x1, y1, vx1, vy1, x2, y2, vx2, vy2, ):
    '''
    define line A and line B, write a function which can return the point two lines cross.
    dot_1 = (x1, y1)
    dot_2 = (x2, y2)
    vec_1 = (vx1, vy1)
    vec_2 = (vx2, vy2)
    line1 = [(x1, y1), (x1 + vx1, y1 + vy1)], line2 = [(x2, y2), (x2 + vx2, y2 + vy2)]
    '''
    if vx1 == 0:  # 如果斜率為0
        k1 = None
        b1 = 0
    else:
        k1 = vy1 * 1.0 / vx1
        b1 = (y1 + vy1) * 1.0 - (x1 + vx1) * k1 * 1.0
    if vx2 == 0:
        k2 = None
        b2 = 0
    else:
        k2 = vy2 * 1.0 / vx2
        b2 = (y2 + vy2) * 1.0 - (x2 + vx2) * k2 * 1.0

    if k1 == k2:
        return None
    elif k1 == None:  # 如果Line1斜率不存在，則取Line1上的點帶入Line2的公式
        x = x1 + vx1
        k1 = k2
        b1 = b2
    elif k2 == None:
        x = x2 + vx2
    else:
        x = (b2 - b1) * 1.0 / (k1 - k2)
    y = k1 * x * 1.0 + b1 * 1.0
    return (x, y)
def cross_point_dot(x1, y1, vx1, vy1, x2, y2, x3, y3, ):
    '''
    this function is same as above. But in this case, one of lines has starting point and ending point.
    If the point two line cross out of the line, function should return None.
    '''
    p = cross_point(x1, y1, vx1, vy1, x2, y2, x3 - x2, y3-y2)
    if p:
        if x2 <= p[0] <= x3 or x3 <= p[0] <= x2:
            if y2 <= p[1] <= y3 or y3 <= p[1] <= y2:
                return p
            else:
                return None
    else:
        return None

def create_wall():
    wall_bottom = world.CreateKinematicBody(position=(12, 0.5), linearVelocity=(0, 0))
    box = wall_bottom.CreatePolygonFixture(box=(12, 0.5))

    wall_top = world.CreateKinematicBody(position=(12, 23.5), linearVelocity=(0, 0))
    box = wall_top.CreatePolygonFixture(box=(12, 0.5))

    wall_left = world.CreateKinematicBody(position=(0.5, 12), linearVelocity=(0, 0))
    box = wall_left.CreatePolygonFixture(box=(0.5, 11))

    wall_right = world.CreateKinematicBody(position=(23.5, 12), linearVelocity=(0, 0))
    box = wall_right.CreatePolygonFixture(box=(0.5, 11))

create_wall()

wall_info = [
    [(1,1),(23,1)], [(1,1), (1,23)], [(23,1), (23,23)], [(1,23),(23,23)]
]

colors = {
    kinematicBody: (255, 255, 255, 255),
    staticBody: (255, 255, 255, 255),
    dynamicBody: (127, 127, 127, 255),
}

def right_sensor_detect(walls):
    distance = []
    result = None
    for wall in walls:
        distance.append(cross_point_dot(sensor_right.position[0], sensor_right.position[1],
                        sensor_left.position[0]-sensor_right.position[0], sensor_left.position[1]-sensor_right.position[1],
                        wall[0][0], wall[0][1], wall[1][0],wall[1][1])
                        )
    for i in distance:
        if i:
            if sensor_left.position[0] > sensor_right.position[0] >= i[0]:
                result = math.sqrt((i[0]-sensor_right.position[0])**2 + (i[1]-sensor_right.position[1])**2)
            elif i[0] >= sensor_right.position[0] >sensor_left.position[0]:
                result = math.sqrt((i[0]-sensor_right.position[0])**2 + (i[1]-sensor_right.position[1])**2)
            else:
                pass

    try:
        return round(result, 3)
    except TypeError:
        return result

def left_sensor_detect(walls):
    distance = []
    result = None
    for wall in walls:
        distance.append(cross_point_dot(sensor_left.position[0], sensor_left.position[1],
                        sensor_right.position[0]-sensor_left.position[0], sensor_right.position[1]-sensor_left.position[1],
                        wall[0][0], wall[0][1], wall[1][0],wall[1][1])
                        )
    for i in distance:
        if i:
            if sensor_right.position[0] > sensor_left.position[0] >= i[0]:
                result = math.sqrt((i[0]-sensor_left.position[0])**2 + (i[1]-sensor_left.position[1])**2)
            elif i[0] >= sensor_left.position[0] >sensor_right.position[0]:
                result = math.sqrt((i[0]-sensor_left.position[0])**2 + (i[1]-sensor_left.position[1])**2)
            else:
                pass
    try:
        return round(result, 3)
    except TypeError:
        return result


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
    screen.fill((0, 0, 0, 0))
    print("left sensor:" + str(left_sensor_detect(wall_info)))
    print("right sensor:" + str(right_sensor_detect(wall_info)))

    # detact distance by using b2Distance
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


    # screen.fill((0, 0, 0, 0))
    # Draw the world
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)


    # Make Box2D simulate the physics of our world for one step.
    world.Step(TIME_STEP, 10, 10)

    # screen.blit(car,((dynamic_body.position[0]-2)*20, (24-dynamic_body.position[1]-2)*20))


    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')