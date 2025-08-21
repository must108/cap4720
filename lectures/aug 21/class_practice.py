import pygame
import moderngl
import numpy as np

pygame.init()

width = 600
height = 600

pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.set_mode((width, height), flags= pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption(title = "Class Practice 1")
gl = moderngl.get_context()

print(gl.info['GL_VERSION'])

position_data = [
    0.0, 0.8,
    -0.8, -0.8,
    0.8, -0.8
]
triangle_vertex_positions = np.array(position_data).astype("float32")