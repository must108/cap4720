#version 330 core

uniform float distance;
uniform float angle;

void main() {
    vec2 position = vec2(0);
    if (gl_VertexID > 0) {
        float angleR = radians(-angle);
        position = distance * vec2(cos(angleR), sin(angleR));
    }
    gl_Position = vec4(position, 0.0, 1.0);
}

