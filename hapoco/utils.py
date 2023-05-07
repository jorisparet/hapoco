def clamp(value, min_value, max_value):
    value = max(value, min_value)
    value = min(value, max_value)
    return value

def lerp(a, b, t):
    return (1 - t) * a + t * b

def inv_lerp(a, b, v):
    return (v - a) / (b - a)