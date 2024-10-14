#!/usr/bin/env python3

"""For game styles"""

# text styles
font_style = {
    'default': ('Helvetica', 12),
    'default_bold': ('Helvetica', 12, 'bold'),
}

# Button styles
button_style = {
    'bg': 'coral',
    'fg': 'white',
    'font': font_style.get('default_bold'),
    'padx': 12,
    'pady': 10,
    'width': 25,
}

canvas_colors = {
    'default': {
        'alive': 'teal',
        'just_died': 'orange',
        'dead': 'white',
        'cell_border': 'gray',
        'slider_trough': 'teal',
    }
}
