import numpy as np
from collections import defaultdict


def analyze_layout(components):
    """
    Analyze detected components to understand layout structure
    """
    if not components:
        return {}

    # Sort components by y-coordinate (top to bottom)
    components.sort(key=lambda x: x['position']['y'])

    layout = {
        'structure': 'flex_column',  # default
        'components': [],
        'grid_rows': [],
        'grid_columns': []
    }

    # Group components by rows
    rows = defaultdict(list)
    y_positions = [c['position']['y'] for c in components]

    # Simple row detection (components with similar y positions)
    threshold = 20  # pixels
    current_row = 0

    for i, comp in enumerate(components):
        if i == 0:
            rows[current_row].append(comp)
        else:
            prev_y = components[i - 1]['position']['y']
            if abs(comp['position']['y'] - prev_y) < threshold:
                rows[current_row].append(comp)
            else:
                current_row += 1
                rows[current_row].append(comp)

    # Analyze each row
    for row_idx, row_comps in rows.items():
        # Sort row components by x position (left to right)
        row_comps.sort(key=lambda x: x['position']['x'])

        row_data = {
            'row_index': row_idx,
            'components': [],
            'alignment': 'row',
            'justify_content': 'flex-start'
        }

        for comp in row_comps:
            comp_info = {
                'type': comp['type'],
                'size': {
                    'width': comp['position']['width'],
                    'height': comp['position']['height']
                },
                'position': comp['position'],
                'content': generate_placeholder_content(comp['type'])
            }
            row_data['components'].append(comp_info)

        layout['grid_rows'].append(row_data)

    # Detect layout structure
    if len(rows) == 1 and len(rows[0]) > 1:
        layout['structure'] = 'flex_row'
    elif len(rows) > 1 and all(len(row) == 1 for row in rows.values()):
        layout['structure'] = 'flex_column'
    elif len(rows) > 1 and any(len(row) > 1 for row in rows.values()):
        layout['structure'] = 'grid'

    return layout


def generate_placeholder_content(component_type):
    """Generate placeholder content based on component type"""
    placeholders = {
        'button': 'Button',
        'text_field': 'Input field',
        'heading': 'Sample Heading',
        'paragraph': 'Lorem ipsum dolor sit amet...',
        'image': 'image_placeholder.jpg',
        'navbar': 'Home About Contact',
        'card': 'Card content here'
    }
    return placeholders.get(component_type, 'Content')