COLOR_CODES = {
    WHITE = 'ÿc0',
    RED = 'ÿc1',
    LIGHTGREEN = 'ÿc2',
    BLUE = 'ÿc3',
    GOLD = 'ÿc4',
    GRAY = 'ÿc5',
    BLACK = 'ÿc6',
    LIGHTGOLD = 'ÿc7',
    ORANGE = 'ÿc8',
    YELLOW = 'ÿc9',
    PURPLE = 'ÿc;'
}

RegisterInstruction("Color", function(text, color)
    return COLOR_CODES[color:upper()] .. text
end)
