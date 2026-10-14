class FractalCamera:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.aspect_ratio = screen_width / screen_height

        #starting center of view in complex plane 
        self.center_x = -0.5  #middle of -2.0, 1.0
        self.center_y = 0.0   #middle of -1.0, 1.0

        #Mandelbrot spans betw -2.0 and 1.0 so 3.0 is enough
        self.complex_width = 3.0

    def pixel_to_complex(self, mouse_x, mouse_y):
        """Converts a screen pixel coord into a complex plane coord"""
        gl_mouse_y = self.screen_height - mouse_y

        percent_x = mouse_x / self.screen_width
        percent_y = gl_mouse_y / self.screen_height

        complex_height = self.complex_width / self.aspect_ratio

        real = self.center_x + (percent_x - 0.5) * self.complex_width
        imaginary = self.center_y + (percent_y - 0.5) * complex_height

        return real, imaginary

    def zoom(self, mouse_x, mouse_y, zoom_factor):
        """zooms in cursor stays still"""

        target_real, target_imag = self.pixel_to_complex(mouse_x, mouse_y)

        self.complex_width *= zoom_factor

        #recalc point for smoothness

        new_target_real, new_target_imag = self.pixel_to_complex(mouse_x, mouse_y)

        self.center_x += (target_real - new_target_real)
        self.center_y += (target_imag - new_target_imag)

    def pan(self, dx, dy):
        complex_height = self.complex_width / self.aspect_ratio

        self.center_x -= (dx / self.screen_width) * self.complex_width

        self.center_y += (dy / self.screen_height) * complex_height