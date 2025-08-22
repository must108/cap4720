# render a trapezoid with opengl

import pygame
import moderngl
import math
import numpy as np

WIDTH = 600
HEIGHT = 600

with open("vert.glsl") as vert_file:
    vertex_shader_code = vert_file.read()
with open("frag.glsl") as frag_file:
    fragment_shader_code = frag_file.read()

pygame.init()
clock = pygame.time.Clock()
running = True

pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)

pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption(title="Trapezoid Practice")
gl = moderngl.get_context()

num_sides = 6
radius = 0.5
center = (0, 0)
position_data = []
for i in range(num_sides):
    angle1 = 2 * math.pi * i / num_sides
    angle2 = 2 * math.pi * (i + 1) / num_sides
    x1, y1 = math.cos(angle1) * radius, math.sin(angle1) * radius
    x2, y2 = math.cos(angle2) * radius, math.sin(angle2) * radius
    position_data += [center[0], center[1], x1, y1, x2, y2]

triangle_vertex_positions = np.array(position_data).astype("f4")
triangle_positions_buffer = gl.buffer(triangle_vertex_positions.tobytes())

program = gl.program(
    vertex_shader=vertex_shader_code,
    fragment_shader=fragment_shader_code,
)

renderable = gl.vertex_array(
    program,
    [ (triangle_positions_buffer, "2f", "position") ]
)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
            running = False

    gl.clear(1.0, 1.0, 1.0) # background color

    renderable.render()

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
