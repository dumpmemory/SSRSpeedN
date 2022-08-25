# Tested on Windows 10 (python3.9), Ubuntu 16.4.1 (python3.5)

import os
import sys
import typing
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    NOTSET,
    WARNING,
    LogRecord,
    StreamHandler,
    addLevelName,
)
from sys import stdout
from typing import Optional, TextIO, Union

# this is the magic for ASCII escape sequences of text
# attribute control to work on Windows platform
if sys.platform.lower() == "win32":
    os.system("color")

# Group of Different functions for different styles
# For a list of ASCII sequences that change display graphics, see http://ascii-table.com/ansi-escape-sequences.php
# Text attributes
RESET = "0"
BOLD = "1"
UNDERSCORE = "4"  # on monochrome display adapter only
BLINK = "5"
REVERSE = "7"
CONCEALED = "8"

# Foreground colors
FG_COLOR_START = 30
FG_BLACK = 30
FG_RED = 31
FG_GREEN = 32
FG_YELLOW = 33
FG_BLUE = 34
FG_MAGENTA = 35
FG_CYAN = 36
FG_WHITE = 37

# Background colors
BG_COLOR_START = 40
BG_BLACK = 40
BG_RED = 41
BG_GREEN = 42
BG_YELLOW = 43
BG_BLUE = 44
BG_MAGENTA = 45
BG_CYAN = 46
BG_WHITE = 47

ALL_COLORS = [
    FG_BLACK,
    FG_RED,
    FG_GREEN,
    FG_YELLOW,
    FG_BLUE,
    FG_MAGENTA,
    FG_CYAN,
    FG_WHITE,
    BG_BLACK,
    BG_RED,
    BG_GREEN,
    BG_YELLOW,
    BG_BLUE,
    BG_MAGENTA,
    BG_CYAN,
    BG_WHITE,
]


# reset text attribute.
def reset() -> str:
    return "\033[{0}m".format(RESET)


# major function
def deco(
    s: str,
    fg_color: int = 0x111,
    bg_color: Optional[int] = None,
    const_deco: Union[int, str] = "",
    **kwargs
) -> str:
    """
    Params:
    fg_color, bg_color: int or 3-tuple
        if given as a three digit hex integer, each digit
          represents red, green or blue respectively, either 0 or 1.
          for example:
            0x100 red, 0x010 green, 0x001 blue
            0x110 yellow, 0x101 magenta.
        if given a value in the list `ALL_COLORS`, it is used
          directly.
    kwargs: all kwargs are of boolean type.
        reset:  same as reset() if True, else no effect.
        bold:   set bold.
        underscore: set underscore. on monochrome display adapter only.
        blink:  set blink.
        reverse: reverse background and foreground color.
        concealed: Concealed on.
    """
    if not isinstance(s, str):
        s = str(s)
    if not isinstance(const_deco, str):
        const_deco = str(const_deco)

    if const_deco:
        return const_deco + s

    fg = _parse_color_param(fg_color, FG_COLOR_START)
    bg = _parse_color_param(bg_color, BG_COLOR_START) if bg_color is not None else ""

    text_attr_map = {
        "reset": RESET,
        "bold": BOLD,
        "underscore": UNDERSCORE,
        "blink": BLINK,
        "reverse": REVERSE,
        "concealed": CONCEALED,
    }

    attr = []
    for a in kwargs:
        if kwargs.get(a, False):
            attr.append(text_attr_map[a])
    c = ";".join(attr)
    return "\033[" + ";".join([x for x in (fg, bg, c) if x]) + "m" + s


def _parse_color_param(color_param: int, color_start: int) -> str:
    assert isinstance(color_param, int)

    if color_param in ALL_COLORS:
        c = color_param

    else:
        color_list = [
            int(color_param / 0x100),
            int(color_param % 0x100 / 0x10),
            int(color_param % 0x10),
        ]

        if any([x > 1 for x in color_list]):
            raise ColorError(
                "Invalid color! Each integer of the available three-hex colors must be 0 or 1, e.g. 0x100 (red)."
            )
        c = color_start
        c += 1 * color_list[0]
        c += 2 * color_list[1]
        c += 4 * color_list[2]

    return str(c)


# new log level
NOTIFY = INFO + 1

level_to_decos = {
    CRITICAL: deco("", FG_RED, bold=True),
    ERROR: deco("", FG_RED),
    WARNING: deco("", FG_YELLOW, bold=True),
    INFO: deco("", FG_WHITE),
    DEBUG: deco("", FG_GREEN),
    NOTSET: deco("", FG_WHITE),  # same as INFO
}


class ColorError(Exception):
    pass


class ConsoleHandler(StreamHandler):
    def __init__(self, stream: TextIO = stdout):
        super().__init__(stream)
        self.addLogLevel(NOTIFY, "NOTIFY", deco("", FG_YELLOW))

    @staticmethod
    def addLogLevel(level: int, levelName: str, deco_str: str = deco("", FG_WHITE)):
        try:
            level_to_decos[level] = deco_str
        finally:
            pass
        addLevelName(level, levelName)

    def emit(self, record: LogRecord):
        const_deco = level_to_decos.get(record.levelno, level_to_decos[NOTSET])
        # record.message is dynamically generated by record.getMessage().
        record.msg = deco(record.msg, const_deco=const_deco) + reset()
        # all properties of `record` that are of string type can be decorated.
        record.levelname = deco(record.levelname, bold=True) + reset()
        record.filename = deco(record.filename, FG_MAGENTA) + reset()
        return super().emit(record)

    # def format(self, record: LogRecord) -> str:
    #     """NOT COMPATIBLE with `emit()`, do not use them together."""
    #     msg = super().format(record)
    #     const_deco = level_to_decos.get(record.levelno, NOTSET)
    #     return deco(msg, const_deco=const_deco) + reset()


# convenience functions


@typing.no_type_check
def warning(wrnmsg: str):
    wrnmsg = "Warning: " + wrnmsg
    print(deco(wrnmsg, FG_YELLOW, bold=True), reset())


@typing.no_type_check
def error(errmsg: str):
    wrnmsg = "Error: " + errmsg
    print(deco(wrnmsg, FG_RED, bold=True), reset())
    sys.exit()


# demo usage
if __name__ == "__main__":
    print(deco("Hello, ", 0x011, bold=True) + reset() + "world!")
    print(deco("Hello, ", reverse=True) + reset() + "world!")
    print(deco("Hello, ", FG_BLUE, bold=True) + reset() + "world!")
    print(deco("Hello, ", FG_YELLOW, BG_GREEN, bold=True) + reset() + "world!")
    print(deco("Hello, ", FG_MAGENTA, bold=True) + reset() + "w...")
    warning("emmm, seems there is a small problem...")
    error("Unknown error!")
