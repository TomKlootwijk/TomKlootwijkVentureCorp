#version 330 core

out vec4 FragColor;
uniform vec2 uResolution;
uniform float uTime;

const float PI = 3.14159265358979323846;

float sdCircle(vec2 p, float r) { return length(p) - r; }
float sdSegment(vec2 p, vec2 a, vec2 b, float r) {
    vec2 pa = p - a, ba = b - a;
    float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0);
    return length(pa - ba * h) - r;
}
float opUnion(float a, float b) { return min(a, b); }

vec2 logPolar(vec2 p) {
    float r = max(length(p), 1e-5); // explicit core chart; log does not remove the singularity
    return vec2(log(r), atan(p.y, p.x));
}

float hash12(vec2 p) {
    vec3 p3 = fract(vec3(p.xyx) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.x + p3.y) * p3.z);
}

float glyphR(vec2 p) {
    float stem = sdSegment(p, vec2(-0.30, -0.82), vec2(-0.30, 0.82), 0.055);
    float upper = abs(sdCircle(p - vec2(0.02, 0.37), 0.43)) - 0.055;
    upper = max(upper, -p.y + 0.02); // retain upper loop only
    float leg = sdSegment(p, vec2(-0.05, 0.02), vec2(0.62, -0.82), 0.055);
    return opUnion(opUnion(stem, upper), leg);
}

void main() {
    vec2 p = (2.0 * gl_FragCoord.xy - uResolution.xy) / min(uResolution.x, uResolution.y);
    vec2 lp = logPolar(p);

    float d = glyphR(p);
    float coverage = smoothstep(0.02, -0.02, d);

    // Log-polar sector mask: a one-bit admission flag, not the complete state.
    float active = step(-2.8, lp.x) * step(lp.x, 0.35);
    float angularBands = step(0.5, 0.5 + 0.5 * sin(24.0 * lp.y + 2.0 * uTime));
    active *= mix(1.0, angularBands, 0.08);

    // Static 1-bit jitter for preview. In a real engine this is an optional projection adapter.
    float bit = step(hash12(gl_FragCoord.xy), coverage * active);
    FragColor = vec4(vec3(bit), 1.0);
}
