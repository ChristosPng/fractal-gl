#version 400 core

uniform dvec2 center;
uniform double complex_width;
uniform vec2 resolution;
uniform int max_iterations;

// 0 = Mandelbrot, 1 = Julia Set, 2 = Burning Ship, 3 = Multibrot (z^3)
uniform int u_mode;
uniform dvec2 u_julia_c;

//palette uniforms sent from python
uniform vec3 u_a;
uniform vec3 u_b;
uniform vec3 u_c;
uniform vec3 u_d;

out vec4 out_color;

//cosine palette gen (a is offset, b is ampl, c is freq, d is phase)
vec3 palette(float t, vec3 a, vec3 b, vec3 c, vec3 d) {
    return a + b * cos(6.28318530718 * (c * t + d));  //color = a + b * cos (2pi * (c *t) + d)
}

void main(){
    
    double p_x = double(gl_FragCoord.x) / double(resolution.x);
    double p_y = double(gl_FragCoord.y) / double(resolution.y);

    double aspect_ratio = resolution.x / resolution.y;
    double complex_height = complex_width / aspect_ratio;

    double coord_real = center.x + (p_x - 0.5) * complex_width;
    double coord_imag = center.y + (p_y - 0.5) * complex_height;

    double z_real, z_imag, c_real, c_imag;

    if (u_mode == 1) {
        // Julia Set: z starts at pixel coordinate, c is constant
        z_real = coord_real;
        z_imag = coord_imag;
        c_real = u_julia_c.x;
        c_imag = u_julia_c.y;
    } else {
        // Mandelbrot / Burning Ship / Multibrot: z starts at 0, c is pixel coordinate
        z_real = 0.0;
        z_imag = 0.0;
        c_real = coord_real;
        c_imag = coord_imag;
    }

    int iterations = 0;

    for (int i = 0; i < max_iterations; i++){
        double z_real_sq = z_real * z_real;
        double z_imag_sq = z_imag * z_imag;

        if (z_real_sq + z_imag_sq > 4.0) {
            break;
        }

        double next_z_real, next_z_imag;

        if (u_mode == 2) {
            // Burning Ship: |Re(z)| + i|Im(z)|
            double abs_r = abs(z_real);
            double abs_i = abs(z_imag);
            next_z_real = abs_r * abs_r - abs_i * abs_i + c_real;
            next_z_imag = 2.0 * abs_r * abs_i + c_imag;
        } 
        else if (u_mode == 3) {
            // Multibrot z^3 + c
            next_z_real = z_real * (z_real_sq - 3.0 * z_imag_sq) + c_real;
            next_z_imag = z_imag * (3.0 * z_real_sq - z_imag_sq) + c_imag;
        } 
        else {
            // Standard z^2 + c (Mandelbrot or Julia)
            next_z_real = z_real_sq - z_imag_sq + c_real;
            next_z_imag = 2.0 * z_real * z_imag + c_imag;
        }

        z_real = next_z_real;
        z_imag = next_z_imag;

        iterations++;
    }

    if (iterations == max_iterations) {
        out_color = vec4(0.0, 0.0, 0.0, 1.0); //still in set paint it black
    } else {
        float log_zn = log(float(z_real * z_real + z_imag * z_imag)) / 2.0;
        float nu = log(log_zn / 0.69314718056) / 0.69314718056; // 0.693147... = ln(2))
        float iter_smooth = float(iterations) + 1.0 - nu;

        float t = iter_smooth * 0.015;
        vec3 rgb = palette(t, u_a, u_b, u_c, u_d);

        out_color = vec4(rgb, 1.0);
    }
}