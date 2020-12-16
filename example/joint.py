'''
origin code:
'''

import pygame
from pygame.locals import *
import math

import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480

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

# r = math.sqrt(0.2 * dynamic_body.inertia / dynamic_body.mass)
# '''模擬摩擦力'''
# world.CreateFrictionJoint(
#     bodyA=ground,
#     bodyB=dynamic_body,
#     localAnchorA=(0, 0),
#     localAnchorB=(0, 0),
#     collideConnected=True,
#     maxForce=dynamic_body.mass * gravity,
#     maxTorque=dynamic_body.mass * r * gravity
# )

sensor_left = world.CreateDynamicBody(position = (19.8, 3))
ball = sensor_left.CreateCircleFixture(radius = 0.2)

sensor_right = world.CreateDynamicBody(position = (22.2, 3))
ball = sensor_right.CreateCircleFixture(radius = 0.2)

world.CreateDistanceJoint(bodyA=sensor_left,bodyB=dynamic_body,collideConnected=True)
world.CreateDistanceJoint(bodyA=sensor_right,bodyB=dynamic_body,collideConnected=True)

def cross_point(dot1, vec1, dot2, vec2 ):
    '''
    define line A and line B, write a function which can return the point two lines cross.
    dot_1 = (x1, y1)
    dot_2 = (x2, y2)
    vec_1 = (vx1, vy1)
    vec_2 = (vx2, vy2)
    line1 = [(x1, y1), (x1 + vx1, y1 + vy1)], line2 = [(x2, y2), (x2 + vx2, y2 + vy2)]
    '''
    x1 = dot1[0]
    y1 = dot1[1]
    x2 = dot2[0]
    y2 = dot2[1]
    vx1 = vec1[0]
    vy1 = vec1[1]
    vx2 = vec2[0]
    vy2 = vec2[1]
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
def cross_point_dot(dot1, vec1, dot2, dot3 ):
    '''
    this function is same as above. But in this case, one of lines has starting point and ending point.
    If the point two line cross out of the line, function should return None.
    '''
    x2 = dot2[0]
    y2 = dot2[1]
    x3 = dot3[0]
    y3 = dot3[1]
    p = cross_point(dot1, vec1, dot2, (x3-x2, y3-y2))
    if p:
        if x2 <= p[0] <= x3 or x3 <= p[0] <= x2:
            if y2 <= p[1] <= y3 or y3 <= p[1] <= y2:
                return p
            else:
                return None
    else:
        return None

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
def front_sensor_detect(walls):
    distance = []
    results = []
    vector = None
    if sensor_left.position[0] == sensor_right.position[0]:
        vector = (1, 0)
    elif sensor_left.position[1] == sensor_right.position[1]:
        vector = (0, 1)
    else:
        vector = (sensor_left.position[1]-sensor_right.position[1], sensor_right.position[0] - sensor_left.position[0])

    for wall in walls:
        distance.append(cross_point_dot(dynamic_body.position,
                        vector,
                        wall[0], wall[1])
                        )
    for i in distance:
        if i:
            if i[0] - dynamic_body.position[0] > 0 and vector[0] >0:
                results.append(math.sqrt((i[0] - dynamic_body.position[0]) ** 2 + (i[1] - dynamic_body.position[1]) ** 2) - 1.5)
                pygame.draw.line(screen, (255,255,0), (dynamic_body.position[0] *PPM,SCREEN_HEIGHT-dynamic_body.position[1]*PPM),
                                     (i[0]*PPM, SCREEN_HEIGHT-i[1]*PPM), 5)
            elif i[0] - dynamic_body.position[0] < 0 and vector[0] < 0:
                results.append(math.sqrt((i[0] - dynamic_body.position[0]) ** 2 + (i[1] - dynamic_body.position[1]) ** 2) - 1.5)
                pygame.draw.line(screen, (255,255,0), (dynamic_body.position[0] *PPM,SCREEN_HEIGHT-dynamic_body.position[1]*PPM),
                                     (i[0]*PPM, SCREEN_HEIGHT-i[1]*PPM), 5)
            else:
                pass
        else:
            pass

    try:
        if len(results) ==1:
            result = results[0]
        else:
            result = min(results)
        return round(result, 3)
    except TypeError:
        return None
    except ValueError:
        return None

def right_sensor_detect(walls):
    distance = []
    results = []
    for wall in walls:
        distance.append(cross_point_dot(sensor_right.position,
                        sensor_left.position-sensor_right.position,
                        wall[0], wall[1])
                        )
    for i in distance:
        if i:
            if sensor_left.position[0] > sensor_right.position[0] >= i[0]:
                results.append(math.sqrt((i[0]-sensor_right.position[0])**2 + (i[1]-sensor_right.position[1])**2))
                pygame.draw.line(screen, (255,0,255), (sensor_right.position[0] *PPM,SCREEN_HEIGHT-sensor_right.position[1]*PPM),
                                 (i[0]*PPM, SCREEN_HEIGHT-i[1]*PPM), 5)
            elif i[0] >= sensor_right.position[0] >sensor_left.position[0]:
                results.append(math.sqrt((i[0]-sensor_right.position[0])**2 + (i[1]-sensor_right.position[1])**2))
                pygame.draw.line(screen, (255, 0, 255),
                                 (sensor_right.position[0] * PPM, SCREEN_HEIGHT - sensor_right.position[1] * PPM),
                                 (i[0] * PPM,SCREEN_HEIGHT- i[1] * PPM), 5)

            else:
                pass

    try:
        if len(results) == 1:
            result = results[0]
        else:
            result = min(results)
        return result
    except TypeError:
        return None
    except ValueError:
        return None

def left_sensor_detect(walls):
    distance = []
    results = []
    for wall in walls:
        distance.append(cross_point_dot(sensor_left.position,
                        sensor_right.position - sensor_left.position,
                        wall[0], wall[1])
                        )
    for i in distance:
        if i:
            if sensor_right.position[0] > sensor_left.position[0] >= i[0]:
                results.append(math.sqrt((i[0]-sensor_left.position[0])**2 + (i[1]-sensor_left.position[1])**2))
                pygame.draw.line(screen, (0, 255, 255),
                                 (sensor_left.position[0] * PPM, SCREEN_HEIGHT - sensor_left.position[1] * PPM),
                                 (i[0] * PPM, SCREEN_HEIGHT- i[1] * PPM), 5)
            elif i[0] >= sensor_left.position[0] >sensor_right.position[0]:
                results.append(math.sqrt((i[0]-sensor_left.position[0])**2 + (i[1]-sensor_left.position[1])**2))
                pygame.draw.line(screen, (0, 255, 255),
                                 (sensor_left.position[0] * PPM, SCREEN_HEIGHT - sensor_left.position[1] * PPM),
                                 (i[0] * PPM, SCREEN_HEIGHT - i[1] * PPM), 5)
            else:
                pass
    try:

        if len(results) == 1:
            result = results[0]
        else:
            result = min(results)
        return result
    except TypeError:
        return None
    except ValueError:
        return None

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
    # 改變物體的中心點
    dynamic_body.localCenter = (1,0)

    screen.fill((0, 0, 0, 0))
    # print(front_sensor_detect(wall_info))
    # print(left_sensor_detect(wall_info))
    # print(right_sensor_detect(wall_info))

    # detact distance by using b2Distance
    # Check the event queue
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # The user closed the window or pressed escape
            running = False
        if (event.type == KEYDOWN and event.key == K_UP):
            f = dynamic_body.GetWorldVector(localVector=(0.0, 100.0))
            p = dynamic_body.GetWorldPoint(localPoint=(1.0, 0.0))
            dynamic_body.ApplyForce(f, p, True)

        if (event.type == KEYDOWN and event.key == K_DOWN):
            f = dynamic_body.GetWorldVector(localVector=(0.0, -100.0))
            p = dynamic_body.GetWorldPoint(localPoint=(1.0, 0.0))
            dynamic_body.ApplyForce(f, p, True)
            pass

        # if (event.type == KEYDOWN and event.key == K_LEFT):
        #     dynamic_body.ApplyTorque(100.0, True)
        #     pass
        #
        # if (event.type == KEYDOWN and event.key == K_RIGHT):
        #     dynamic_body.ApplyTorque(-100.0, True)
        #     pass

        if (event.type == KEYDOWN and event.key == K_s):
            f = dynamic_body.GetWorldVector(localVector=(0.0, -100.0))
            p = dynamic_body.GetWorldPoint(localPoint=(-1.0, 0.0))
            dynamic_body.ApplyForce(f, p, True)

        if (event.type == KEYDOWN and event.key == K_w):
            f = dynamic_body.GetWorldVector(localVector=(0.0, 100.0))
            p = dynamic_body.GetWorldPoint(localPoint=(-1.0, 0.0))
            dynamic_body.ApplyForce(f, p, True)
            pass


    # screen.fill((0, 0, 0, 0))
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