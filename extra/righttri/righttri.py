# render a right triangle with opengl

import pygame
import moderngl
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
pygame.display.set_caption(title="Right Triangle Practice")
gl = moderngl.get_context()

position_data = [
    -0.5, 0.5,
    -0.5, -0.5,
    0.5, 0.5,
]

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
