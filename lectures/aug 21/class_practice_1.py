import pygame
import moderngl
import numpy as np

# load glsl files
with open("vert.glsl") as vert_file:
    vertex_shader_code = vert_file.read()
with open("frag.glsl") as frag_file:
    fragment_shader_code = frag_file.read()

# start running clock
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
running = True

width = 600
height = 600

# for mac, using different version bc of this
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)

# display must have opengl context
pygame.display.set_mode((width, height), flags=pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption(title="Class Practice 1")
gl = moderngl.get_context() # get context that was just created

# print the current gl version
print(gl.info["GL_VERSION"])


position_data = [
    0.0, 0.8,
    -0.8, -0.8,
    0.8, -0.8
]

triangle_vertex_positions = np.array(position_data, dtype="float32")
# ^get geometry data in position_data and make into np array

# create a buffer with the triangle positions, with gl.buffer()
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

    gl.clear(0.5, 0.5, 0.0)

    renderable.render()

    pygame.display.flip()
    clock.tick(10)

pygame.quit()