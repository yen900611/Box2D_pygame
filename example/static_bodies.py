import pygame
import Box2D
from Box2D import b2
import math

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
world = b2.world(gravity=(0, -10), doSleep=True)

# --- pybox2d static body setup ---
bodyDef = Box2D.b2BodyDef()
bodyDef.position = (22.5,12) # the center of object
body = world.CreateBody(bodyDef) # The default bodies are static. # The default density is zero.
groundBody = Box2D.b2PolygonShape(box = (1,7))
groundBoxFixture = Box2D.b2FixtureDef(shape=groundBody)
body.CreateFixture(groundBoxFixture)
# above is equal in this：
ground_body = world.CreateStaticBody(
    position=(3, 1),
    shapes=b2.polygonShape(box=(10, 1)),

)
# circle shape
body1 = world.CreateStaticBody(position=(30,12))
circle = body1.CreateCircleFixture(radius=0.1, density=1, friction=0.3)

# other shape:create by offering vertices
body = world.CreateStaticBody(position = (30, 12), angle = math.pi * 90 /180)
box = body.CreatePolygonFixture(vertices = [(1,1), (2,3), (1,0),(0,2)], density = 1, friction = 0.3, restitution = 0.9)


# --- pygame draw function setup ---
colors = {
    b2.staticBody: (255, 255, 255), # white
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

# --- main game loop ---
running = True
while running:
    # Check the event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # The user closed the window or pressed escape
            running = False

    screen.fill((0, 0, 0, 0))

    # Make Box2D simulate the physics of our world for one step.
    world.Step(TIME_STEP, 10, 10)

    # Draw the world
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)

    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')