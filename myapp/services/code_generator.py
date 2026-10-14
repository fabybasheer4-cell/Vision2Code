def generate_html(layout):
    """
    Generate HTML/CSS code from layout analysis
    """
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated UI</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        {styles}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
</body>
</html>"""

    content = []
    styles = []

    for row in layout.get('grid_rows', []):
        row_html = '<div class="row">\n'

        for comp in row['components']:
            comp_html, comp_style = generate_component_html(comp)
            row_html += f'        {comp_html}\n'
            styles.append(comp_style)

        row_html += '    </div>'
        content.append(row_html)

        # Add row style
        styles.append(f"""
.row {{
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 20px;
    gap: 20px;
}}""")

    return html_template.format(
        styles='\n'.join(set(styles)),
        content='\n'.join(content)
    )


def generate_flutter(layout):
    """
    Generate Flutter/Dart code from layout analysis
    """
    flutter_template = """import 'package:flutter/material.dart';

class GeneratedScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Generated UI'),
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            {content}
          ],
        ),
      ),
    );
  }
}"""

    content = []

    for row in layout.get('grid_rows', []):
        if len(row['components']) > 1:
            # Row with multiple components
            row_widget = """
            Row(
              children: [
                {row_content}
              ],
            ),"""

            row_content = []
            for comp in row['components']:
                row_content.append(generate_flutter_component(comp))

            content.append(row_widget.format(
                row_content=',\n                '.join(row_content)
            ))
        else:
            # Single component
            content.append(generate_flutter_component(row['components'][0]))

    return flutter_template.format(content='\n'.join(content))


def generate_component_html(component):
    """Generate HTML for individual component"""
    comp_type = component['type']
    comp_id = f"comp_{id(component)}"

    if comp_type == 'button':
        html = f'<button class="{comp_type}">{component["content"]}</button>'
    elif comp_type == 'text_field':
        html = f'<input type="text" class="{comp_type}" placeholder="{component["content"]}">'
    elif comp_type == 'heading':
        html = f'<h2 class="{comp_type}">{component["content"]}</h2>'
    elif comp_type == 'paragraph':
        html = f'<p class="{comp_type}">{component["content"]}</p>'
    elif comp_type == 'image':
        html = f'<img src="https://via.placeholder.com/{int(component["size"]["width"])}x{int(component["size"]["height"])}" class="{comp_type}">'
    elif comp_type == 'card':
        html = f'<div class="{comp_type}"><div class="card-content">{component["content"]}</div></div>'
    else:
        html = f'<div class="{comp_type}">{component["content"]}</div>'

    style = f"""
.{comp_type} {{
    width: {component['size']['width']}px;
    min-height: {component['size']['height']}px;
    padding: 8px 12px;
    border-radius: 4px;
}}"""

    return html, style


def generate_flutter_component(component):
    """Generate Flutter widget for individual component"""
    comp_type = component['type']

    if comp_type == 'button':
        return f"""
                ElevatedButton(
                  onPressed: () {{}},
                  child: Text('{component["content"]}'),
                )"""
    elif comp_type == 'text_field':
        return f"""
                TextField(
                  decoration: InputDecoration(
                    hintText: '{component["content"]}',
                    border: OutlineInputBorder(),
                  ),
                )"""
    elif comp_type == 'heading':
        return f"""
                Text(
                  '{component["content"]}',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                )"""
    elif comp_type == 'paragraph':
        return f"""
                Text(
                  '{component["content"]}',
                  style: TextStyle(fontSize: 16),
                )"""
    elif comp_type == 'image':
        return f"""
                Container(
                  width: {component['size']['width']},
                  height: {component['size']['height']},
                  color: Colors.grey[300],
                  child: Center(
                    child: Icon(Icons.image, size: 40),
                  ),
                )"""
    else:
        return f"""
                Container(
                  width: {component['size']['width']},
                  height: {component['size']['height']},
                  color: Colors.grey[100],
                  child: Center(
                    child: Text('{component["content"]}'),
                  ),
                )"""