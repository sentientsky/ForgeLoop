from __future__ import annotations


ORANGE = "\033[38;5;208m"
RESET = "\033[0m"

ASCII_BANNER = r"""
########  #######  ########   ######   ######## ##        #######   #######  ########
##       ##     ## ##     ## ##    ##  ##       ##       ##     ## ##     ## ##     ##
##       ##     ## ##     ## ##        ##       ##       ##     ## ##     ## ##     ##
######   ##     ## ########  ##   #### ######   ##       ##     ## ##     ## ########
##       ##     ## ##   ##   ##    ##  ##       ##       ##     ## ##     ## ##
##       ##     ## ##    ##  ##    ##  ##       ##       ##     ## ##     ## ##
##        #######  ##     ##  ######   ######## ########  #######   #######  ##
""".strip("\n")

TAGLINE = "Discover. Frame. Build. Check. Capture."


def render_intro(colour: bool = True, tagline: bool = True) -> str:
    body = ASCII_BANNER
    if tagline:
        body = f"{body}\n\n{TAGLINE}"
    if not colour:
        return body
    return f"{ORANGE}{body}{RESET}"


def is_ascii(text: str) -> bool:
    return all(ord(character) < 128 for character in text)

