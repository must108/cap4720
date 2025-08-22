# render a cube with opengl

import pygame
import moderngl
import numpy as np
import pyrr

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
pygame.display.set_caption(title="Cube Practice")
gl = moderngl.get_context()

num_sides = 6
radius = 0.5
center = (0, 0)
position_data = [
    # Front face (z = 1.1)
    -1.1, -1.1,  1.1,
     1.1, -1.1,  1.1,
     1.1,  1.1,  1.1,
    -1.1, -1.1,  1.1,
     1.1,  1.1,  1.1,
    -1.1,  1.1,  1.1,

    # Back face (z = -1.1)
    -1.1, -1.1, -1.1,
     1.1,  1.1, -1.1,
     1.1, -1.1, -1.1,
    -1.1, -1.1, -1.1,
    -1.1,  1.1, -1.1,
     1.1,  1.1, -1.1,

    # Left face
    -1.1, -1.1, -1.1,
    -1.1, -1.1,  1.1,
    -1.1,  1.1,  1.1,
    -1.1, -1.1, -1.1,
    -1.1,  1.1,  1.1,
    -1.1,  1.1, -1.1,

    # Right face
     1.1, -1.1, -1.1,
     1.1,  1.1,  1.1,
     1.1, -1.1,  1.1,
     1.1, -1.1, -1.1,
     1.1,  1.1, -1.1,
     1.1,  1.1,  1.1,

    # Top face
    -1.1,  1.1, -1.1,
    -1.1,  1.1,  1.1,
     1.1,  1.1,  1.1,
    -1.1,  1.1, -1.1,
     1.1,  1.1,  1.1,
     1.1,  1.1, -1.1,

    # Bottom face
    -1.1, -1.1, -1.1,
     1.1, -1.1,  1.1,
    -1.1, -1.1,  1.1,
    -1.1, -1.1, -1.1,
     1.1, -1.1, -1.1,
     1.1, -1.1,  1.1,
]

triangle_vertex_positions = np.array(position_data).astype("f4")
triangle_positions_buffer = gl.buffer(triangle_vertex_positions.tobytes())

program = gl.program(
    vertex_shader=vertex_shader_code,
    fragment_shader=fragment_shader_code,
)

# make it 3d
projection = pyrr.matrix44.create_perspective_projection(45.0, WIDTH/HEIGHT, 0.1, 10.0)
view = pyrr.matrix44.create_look_at([5, 5, 5], [0, 0, 0], [0, 1, 0])
model = pyrr.matrix44.create_identity()
mvp = pyrr.matrix44.multiply(model, pyrr.matrix44.multiply(view, projection))

program['mvp'].write(mvp.astype('f4').tobytes())

renderable = gl.vertex_array(
    program,
    [ (triangle_positions_buffer, "3f", "position") ]
)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
            running = False

    gl.clear(1.0, 1.0, 1.0) # background color

    angle = pygame.time.get_ticks()
    model = pyrr.matrix44.create_from_y_rotation(angle)
    mvp = pyrr.matrix44.multiply(model, pyrr.matrix44.multiply(view, projection))
    program['mvp'].write(mvp.astype('f4').tobytes())

    renderable.render()
    renderable.render(mode=moderngl.LINES)
    # can also do moderngl.POINTS to add points

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
