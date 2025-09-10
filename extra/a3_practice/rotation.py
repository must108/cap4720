import pygame
import moderngl
import numpy

with open("vert.glsl") as vert_file:
    vertex_shader_code = vert_file.read()

with open("frag.glsl") as frag_file:
    fragment_shader_code = frag_file.read()

with open("vert_line.glsl") as vert_line_file:
    vertex_shader_code_line = vert_line_file.read()

WIDTH = 600
HEIGHT = 600
pygame.init()
clock = pygame.time.Clock()
running = True

pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)



pygame.display.set_mode((HEIGHT, WIDTH), flags=pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption(title="Practice Rotation")
gl = moderngl.get_context()

position_data = [
    0.0, 0.8,
    0.8, 0.0,
    -0.8, 0.0,

    0.0, -0.8,
    0.8, 0.0,
    -0.8, 0.0
]

triangle_vertex_positions = numpy.array(position_data).astype("float32")
triangle_position_buffer = gl.buffer(triangle_vertex_positions)

program = gl.program(
    vertex_shader = vertex_shader_code,
    fragment_shader= fragment_shader_code
)

program_line = gl.program(
    vertex_shader= vertex_shader_code_line,
    fragment_shader= fragment_shader_code
)

renderable = gl.vertex_array(program, [( triangle_position_buffer, "2f", "position", )])
line_renderable = gl.vertex_array(program_line, [])

angle = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
            running = False
        
    gl.clear(0.5, 0.5, 0.5)

    program['scale'] = 0.1
    program['distance'] = 0
    program['inColor'] = [1, 1, 0]
    program['angle'] = 0

    renderable.render(moderngl.TRIANGLES, vertices=6)

    program['distance'] = 0.8
    program['angle'] = angle
    renderable.render(moderngl.TRIANGLES, vertices=6)

    program_line['distance'] = 0.8
    program_line['angle'] = angle
    line_renderable.render(moderngl.LINES, vertices=2)

    pygame.display.flip()
    clock.tick(60)
    angle = angle + 0.1
    if angle > 360:
        angle = 0

pygame.quit()
