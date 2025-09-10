#version 330 core

layout (location = 0) in vec2 position;
uniform float scale;
uniform float distance;
uniform float angle;

void main() {
    float angleR = radians(-angle);
    vec2 d_vector = distance * vec2(cos(angleR), sin(angleR));
    vec2 P = position * scale + d_vector;
    gl_Position = vec4(P, 0.0, 1.0);
}

