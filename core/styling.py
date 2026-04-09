"""
Terminal styling module providing ANSI escape sequences for colors and text formatting.
Equipped with Standard 8/16-color, 256-color (8-bit), and TrueColor (24-bit) support.
"""

# --- Fundamental Constants ---
RESET = "\033[0m"

# --- Text Formatting Styles ---
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
RAPID_BLINK = "\033[6m"
REVERSE = "\033[7m"
HIDDEN = "\033[8m"
STRIKE = "\033[9m"
OVERLINE = "\033[53m"  # Supported by some modern terminals

# --- Standard Foreground Colors (3/4-bit) ---
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# --- Standard Background Colors (3/4-bit) ---
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"


# --- Dynamic Color Generators ---

def fore256(n: int) -> str:
    """Returns the ANSI escape sequence for a 256-color foreground."""
    return f"\033[38;5;{max(0, min(255, n))}m"


def back256(n: int) -> str:
    """Returns the ANSI escape sequence for a 256-color background."""
    return f"\033[48;5;{max(0, min(255, n))}m"


def rgb(r: int, g: int, b: int) -> str:
    """Returns the ANSI escape sequence for a TrueColor (24-bit) foreground."""
    return f"\033[38;2;{max(0, min(255, r))};{max(0, min(255, g))};{max(0, min(255, b))}m"


def back_rgb(r: int, g: int, b: int) -> str:
    """Returns the ANSI escape sequence for a TrueColor (24-bit) background."""
    return f"\033[48;2;{max(0, min(255, r))};{max(0, min(255, g))};{max(0, min(255, b))}m"


# --- Namespaces for organization ---

class Fore:
    """Namespace for Foreground Colors"""
    BLACK, RED, GREEN, YELLOW = BLACK, RED, GREEN, YELLOW
    BLUE, MAGENTA, CYAN, WHITE = BLUE, MAGENTA, CYAN, WHITE
    BRIGHT_BLACK, BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW = BRIGHT_BLACK, BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW
    BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN, BRIGHT_WHITE = BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN, BRIGHT_WHITE
    
    @staticmethod
    def c256(n: int) -> str: return fore256(n)
    
    @staticmethod
    def rgb(r: int, g: int, b: int) -> str: return rgb(r, g, b)


class Back:
    """Namespace for Background Colors"""
    BLACK, RED, GREEN, YELLOW = BG_BLACK, BG_RED, BG_GREEN, BG_YELLOW
    BLUE, MAGENTA, CYAN, WHITE = BG_BLUE, BG_MAGENTA, BG_CYAN, BG_WHITE
    BRIGHT_BLACK, BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW = BG_BRIGHT_BLACK, BG_BRIGHT_RED, BG_BRIGHT_GREEN, BG_BRIGHT_YELLOW
    BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN, BRIGHT_WHITE = BG_BRIGHT_BLUE, BG_BRIGHT_MAGENTA, BG_BRIGHT_CYAN, BG_BRIGHT_WHITE
    
    @staticmethod
    def c256(n: int) -> str: return back256(n)
    
    @staticmethod
    def rgb(r: int, g: int, b: int) -> str: return back_rgb(r, g, b)


class Style:
    """Namespace for Text Styles"""
    RESET, BOLD, DIM, ITALIC = RESET, BOLD, DIM, ITALIC
    UNDERLINE, BLINK, RAPID_BLINK = UNDERLINE, BLINK, RAPID_BLINK
    REVERSE, HIDDEN, STRIKE, OVERLINE = REVERSE, HIDDEN, STRIKE, OVERLINE


class Palette:
    """Extended Palette using 256-color codes for high compatibility."""
    ORANGE = fore256(208)
    PINK = fore256(201)
    PURPLE = fore256(165)
    TEAL = fore256(37)
    LIME = fore256(118)
    TURQUOISE = fore256(45)
    GOLD = fore256(220)
    SILVER = fore256(250)
    SKY_BLUE = fore256(33)
    CRIMSON = fore256(160)
    DEEP_PURPLE = fore256(129)
    MINT = fore256(121)
    DARK_GREY = fore256(238)
    LIGHT_GREY = fore256(250)
    NAVY = fore256(18)
    BROWN = fore256(94)
    LEMON = fore256(227)
    ROSE = fore256(211)


# --- Utility Functions ---

def apply_style(text: str, *styles: str) -> str:
    """Apply any number of styles to text and append a reset."""
    return f"{''.join(styles)}{text}{RESET}"


# --- Status Shortcuts ---
SUCCESS = f"{BOLD}{GREEN}"
WARNING = f"{BOLD}{YELLOW}"
ERROR = f"{BOLD}{RED}"
INFO = f"{BOLD}{CYAN}"
DEBUG = f"{DIM}{MAGENTA}"

# Legacy support
_ANSII_ESCAPE_SEQUENCE = {
    'cyan': CYAN,
    'red': RED,
    'reset': RESET
}

if __name__ == "__main__":
    print(apply_style("Social Automation Agent - Extended Styling", BOLD, Palette.GOLD))
    print(f"{INFO}INFO{RESET} | {SUCCESS}SUCCESS{RESET} | {WARNING}WARNING{RESET} | {ERROR}ERROR{RESET} | {DEBUG}DEBUG{RESET}")
    print(apply_style("Custom 256 Color (Orange)", Palette.ORANGE))
    print(apply_style("TrueColor RGB Sample", rgb(255, 100, 50)))