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

ground_body = world.CreateStaticBody(position = (SCREEN_WIDTH / 2, 1))
box = ground_body.CreatePolygonFixture(box = (SCREEN_WIDTH / 2, 0.5), density = 1, friction = 0.3, restitution = 0.3)

# --- pybox2d dynamic body setup ---

# circle shape
ball = world.CreateDynamicBody(position=(30, 12),linearVelocity = (2,-1))
circle = ball.CreateCircleFixture(radius=0.1, density=1, friction=0.3)

# box shape
board = world.CreateDynamicBody(position = (10,15), angle = math.pi * 60/180,linearVelocity = (2,0))
box = board.CreatePolygonFixture(box = (3,2))

# --- pygame draw function setup ---
colors = {
    b2.dynamicBody:(127, 127,127), # grey
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
    for ground_body in world.bodies:
        for fixture in ground_body.fixtures:
            fixture.shape.draw(ground_body, fixture)

    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')