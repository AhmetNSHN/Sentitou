def centeralize_screen(screen_width, screen_height, window_width, window_height): # always centralizing window according to screen size
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    return f"{window_width}x{window_height}+{x}+{y}"

def safe_div(x, y):
    if y == 0:
        return 0
    return x / y