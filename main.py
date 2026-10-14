import pygame 
import sys
import moderngl
import numpy as np
import random
from camera import FractalCamera
import os

def resource_path(relative_path):
    """Gets absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
#config
INITIAL_WIDTH = 800
INITIAL_HEIGHT = 600
FPS = 60

PALETTES = [
    [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.8, 0.8, 0.5], [0.00, 0.20, 0.50]],
    [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.00, 0.10, 0.20]],
    [[0.3, 0.3, 0.4], [0.5, 0.4, 0.5], [0.4, 0.4, 0.4], [0.00, 0.15, 0.30]],
    [[0.4, 0.3, 0.2], [0.5, 0.4, 0.3], [0.5, 0.5, 0.4], [0.10, 0.20, 0.30]],
    [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.3, 0.3, 0.3], [0.00, 0.33, 0.67]],
]

def get_random_julia_c():
    """Generates a random complex constant c that produces an new Julia set"""
    return (random.uniform(-0.8, 0.4), random.uniform(-0.8, 0.8))

def get_random_palette():
    """randomized cosine palette each run"""
    a = [0.5, 0.5, 0.5]
    b = [0.5, 0.5, 0.5]
    c = [round(random.uniform(0.5, 2.0), 2) for _ in range(3)]
    d = [round(random.uniform(0.0, 1.0), 2) for _ in range(3)]
    return [a, b, c, d]

def main():
    pygame.init()

    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

    screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
    pygame.display.set_caption("Dynamic Fractal")

    ctx = moderngl.create_context()

    with open(resource_path("shader.glsl"), "r") as f:
        fragment_shader_code = f.read()

    vertex_shader_code = """
    #version 400 core
    in vec2 in_vert;
    void main() {
        gl_Position = vec4(in_vert, 0.0, 1.0);
    }
    """

    prog = ctx.program(vertex_shader=vertex_shader_code, fragment_shader=fragment_shader_code)
    
    vertices = np.array([-1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0], dtype='f4')
    vbo = ctx.buffer(vertices)
    vao = ctx.vertex_array(prog, [(vbo, '2f', 'in_vert')])

    camera = FractalCamera(INITIAL_WIDTH, INITIAL_HEIGHT)
    max_iterations = 100

    fractal_mode = 0 # 0: Mandelbrot, 1: Julia, 2: Burning Ship, 3: Multibrot
    julia_c = (-0.7, 0.27015) # Julia constant

    current_palette_idx = 0
    palette = PALETTES[current_palette_idx]

    clock = pygame.time.Clock()
    running = True
    is_fullscreen = False

    dragging = False
    last_mouse_pos = (0,0)

    needs_redraw = True

    while running:
        for event in pygame.event.get():          
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # SPACE to cycle
                elif event.key == pygame.K_SPACE:
                    current_palette_idx = (current_palette_idx + 1) % len(PALETTES)
                    palette = PALETTES[current_palette_idx]
                    needs_redraw = True

                elif event.key == pygame.K_1:
                    fractal_mode = 0 
                    camera.center_x, camera.center_y, camera.complex_width = -0.5, 0.0, 3.0
                    needs_redraw = True

                elif event.key == pygame.K_2:
                    fractal_mode = 1 
                    camera.center_x, camera.center_y, camera.complex_width = 0.0, 0.0, 3.0
                    needs_redraw = True

                elif event.key == pygame.K_3:
                    fractal_mode = 2 
                    camera.center_x, camera.center_y, camera.complex_width = -0.45, -0.5, 3.0
                    needs_redraw = True

                elif event.key == pygame.K_4:
                    fractal_mode = 3 
                    camera.center_x, camera.center_y, camera.complex_width = 0.0, 0.0, 3.0
                    needs_redraw = True

                # 'R' for random Julia const
                elif event.key == pygame.K_r:
                    julia_c = get_random_julia_c()
                    fractal_mode = 1 
                    camera.center_x, camera.center_y, camera.complex_width = 0.0, 0.0, 3.0
                    needs_redraw = True

                # 'C' for random palette
                elif event.key == pygame.K_c:
                    palette = get_random_palette()
                    needs_redraw = True

                elif event.key in (pygame.K_F11, pygame.K_f):
                    pygame.display.toggle_fullscreen()
                    is_fullscreen = not is_fullscreen

                    w, h = screen.get_size()
                    camera.screen_width = w
                    camera.screen_height = h
                    camera.aspect_ratio = w / h
                    ctx.viewport = (0, 0, w, h)
                    needs_redraw = True

            elif event.type == pygame.VIDEORESIZE:
                camera.screen_width = event.w
                camera.screen_height = event.h
                camera.aspect_ratio = event.w / event.h
                ctx.viewport = (0, 0, event.w, event.h)
                needs_redraw = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    dragging = True
                    last_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dx = event.pos[0] - last_mouse_pos[0]
                    dy = event.pos[1] - last_mouse_pos[1]
                    camera.pan(dx, dy)
                    last_mouse_pos = event.pos
                    needs_redraw = True

            elif event.type == pygame.MOUSEWHEEL:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.y > 0: 
                    camera.zoom(mouse_x, mouse_y, 0.9)
                    max_iterations = min(400, int(max_iterations * 1.1)) 
                elif event.y < 0: 
                    camera.zoom(mouse_x, mouse_y, 1.1)
                    max_iterations = max(400, int(max_iterations * 0.9))
                needs_redraw = True

        if needs_redraw:
            prog['center'].value = (camera.center_x, camera.center_y)
            prog['complex_width'].value = camera.complex_width
            prog['resolution'].value = (camera.screen_width, camera.screen_height)
            prog['max_iterations'].value = max_iterations

            prog['u_mode'].value = fractal_mode
            prog['u_julia_c'].value = julia_c

            prog['u_a'].value = tuple(palette[0])
            prog['u_b'].value = tuple(palette[1])
            prog['u_c'].value = tuple(palette[2])
            prog['u_d'].value = tuple(palette[3])

        
            ctx.clear(0.0, 0.0, 0.0)
            vao.render(moderngl.TRIANGLE_STRIP)

            pygame.display.flip() 

            needs_redraw = False

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()