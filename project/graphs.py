"""
Модуль для генерации SVG-графиков функций.
Поддерживаемые типы: linear, quadratic, trigonometric, custom.
"""


def generate_graph(graph_type, data):
    """
    Генерация SVG-графика.

    Args:
        graph_type: тип графика ('linear', 'quadratic', 'trigonometric', 'custom')
        data: словарь с данными:
            - 'points': список кортежей (x, y) для custom
            - 'a', 'b', 'c': коэффициенты для quadratic (y = ax² + bx + c)
            - 'amplitude', 'frequency': для trigonometric
            - 'x_range': кортеж (x_min, x_max)
            - 'y_range': кортеж (y_min, y_max)

    Returns:
        SVG-строка с графиком
    """
    width = 600
    height = 400
    padding = 50

    if graph_type == 'linear':
        return _generate_linear(data, width, height, padding)
    elif graph_type == 'quadratic':
        return _generate_quadratic(data, width, height, padding)
    elif graph_type == 'trigonometric':
        return _generate_trigonometric(data, width, height, padding)
    elif graph_type == 'custom':
        return _generate_custom(data, width, height, padding)
    else:
        return _error_svg("Unknown graph type")


def _generate_linear(data, width, height, padding):
    """Генерация линейного графика y = ax + b."""
    a = data.get('a', 1)
    b = data.get('b', 0)
    x_min = data.get('x_range', (-10, 10))[0]
    x_max = data.get('x_range', (-10, 10))[1]

    y_min_val = data.get('y_range', (-10, 10))[0]
    y_max_val = data.get('y_range', (-10, 10))[1]

    svg = _create_svg_template(width, height, padding)
    svg += _draw_axes(width, height, padding, x_min_val=x_min, x_max_val=x_max,
                      y_min_val=y_min_val, y_max_val=y_max_val)

    # Рисуем линию y = ax + b
    points = []
    steps = 200
    for i in range(steps + 1):
        x = x_min + (x_max - x_min) * i / steps
        y = a * x + b
        svg_y = height - padding - (y - y_min_val) / (y_max_val - y_min_val) * (height - 2 * padding)
        svg_x = padding + (x - x_min) / (x_max - x_min) * (width - 2 * padding)
        svg_y = max(padding, min(height - padding, svg_y))
        points.append(f"{svg_x:.1f},{svg_y:.1f}")

    if len(points) >= 2:
        svg += f'  <polyline points="{" ".join(points)}" fill="none" stroke="#667eea" stroke-width="2"/>\n'

    return svg


def _generate_quadratic(data, width, height, padding):
    """Генерация квадратичного графика y = ax² + bx + c."""
    a = data.get('a', 1)
    b = data.get('b', 0)
    c = data.get('c', 0)
    x_min = data.get('x_range', (-10, 10))[0]
    x_max = data.get('x_range', (-10, 10))[1]

    y_min_val = data.get('y_range', (-10, 10))[0]
    y_max_val = data.get('y_range', (-10, 10))[1]

    svg = _create_svg_template(width, height, padding)
    svg += _draw_axes(width, height, padding, x_min_val=x_min, x_max_val=x_max,
                      y_min_val=y_min_val, y_max_val=y_max_val)

    # Рисуем параболу
    points = []
    steps = 200
    for i in range(steps + 1):
        x = x_min + (x_max - x_min) * i / steps
        y = a * x * x + b * x + c
        svg_y = height - padding - (y - y_min_val) / (y_max_val - y_min_val) * (height - 2 * padding)
        svg_x = padding + (x - x_min) / (x_max - x_min) * (width - 2 * padding)
        svg_y = max(padding, min(height - padding, svg_y))
        points.append(f"{svg_x:.1f},{svg_y:.1f}")

    if len(points) >= 2:
        svg += f'  <polyline points="{" ".join(points)}" fill="none" stroke="#f093fb" stroke-width="2"/>\n'

    return svg


def _generate_trigonometric(data, width, height, padding):
    """Генерация тригонометрического графика y = A * sin(B * x)."""
    amplitude = data.get('amplitude', 1)
    frequency = data.get('frequency', 1)
    x_min = data.get('x_range', (-6.28, 6.28))[0]
    x_max = data.get('x_range', (-6.28, 6.28))[1]

    y_min_val = data.get('y_range', (-2, 2))[0]
    y_max_val = data.get('y_range', (-2, 2))[1]

    svg = _create_svg_template(width, height, padding)
    svg += _draw_axes(width, height, padding, x_min_val=x_min, x_max_val=x_max,
                      y_min_val=y_min_val, y_max_val=y_max_val)

    # Рисуем синусоиду
    points = []
    steps = 300
    import math
    for i in range(steps + 1):
        x = x_min + (x_max - x_min) * i / steps
        y = amplitude * math.sin(frequency * x)
        svg_y = height - padding - (y - y_min_val) / (y_max_val - y_min_val) * (height - 2 * padding)
        svg_x = padding + (x - x_min) / (x_max - x_min) * (width - 2 * padding)
        svg_y = max(padding, min(height - padding, svg_y))
        points.append(f"{svg_x:.1f},{svg_y:.1f}")

    if len(points) >= 2:
        svg += f'  <polyline points="{" ".join(points)}" fill="none" stroke="#43e97b" stroke-width="2"/>\n'

    return svg


def _generate_custom(data, width, height, padding):
    """Генерация произвольного графика по точкам."""
    points_data = data.get('points', [])
    x_min = data.get('x_range', (0, 10))[0]
    x_max = data.get('x_range', (0, 10))[1]
    y_min_val = data.get('y_range', (0, 10))[0]
    y_max_val = data.get('y_range', (0, 10))[1]

    svg = _create_svg_template(width, height, padding)
    svg += _draw_axes(width, height, padding, x_min_val=x_min, x_max_val=x_max,
                      y_min_val=y_min_val, y_max_val=y_max_val)

    if not points_data:
        return svg + '  <text x="300" y="200" text-anchor="middle" fill="#999">Нет данных</text>\n'

    svg_points = []
    for x, y in points_data:
        svg_x = padding + (x - x_min) / (x_max - x_min) * (width - 2 * padding)
        svg_y = height - padding - (y - y_min_val) / (y_max_val - y_min_val) * (height - 2 * padding)
        svg_x = max(padding, min(width - padding, svg_x))
        svg_y = max(padding, min(height - padding, svg_y))
        svg_points.append(f"{svg_x:.1f},{svg_y:.1f}")

    if len(svg_points) >= 2:
        svg += f'  <polyline points="{" ".join(svg_points)}" fill="none" stroke="#fa709a" stroke-width="2"/>\n'

    # Точки
    for x, y in points_data:
        svg_x = padding + (x - x_min) / (x_max - x_min) * (width - 2 * padding)
        svg_y = height - padding - (y - y_min_val) / (y_max_val - y_min_val) * (height - 2 * padding)
        svg_x = max(padding, min(width - padding, svg_x))
        svg_y = max(padding, min(height - padding, svg_y))
        svg += f'  <circle cx="{svg_x:.1f}" cy="{svg_y:.1f}" r="3" fill="#fa709a"/>\n'

    return svg


def _create_svg_template(width, height, padding):
    """Создаёт базовый SVG-шаблон."""
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="{width}" height="{height}" fill="#f8f9fa"/>
  <g transform="translate(0, {height - 2 * padding})">
'''
    return svg


def _draw_axes(width, height, padding, x_min_val, x_max_val, y_min_val, y_max_val):
    """Рисует оси координат и подписи."""
    svg = ''

    # Ось X
    svg += f'    <line x1="{padding}" y1="{height - padding}" x2="{width - padding}" y2="{height - padding}" stroke="#333" stroke-width="1"/>\n'
    # Ось Y
    svg += f'    <line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height - padding}" stroke="#333" stroke-width="1"/>\n'

    # Подписи оси X
    x_steps = 5
    for i in range(x_steps + 1):
        x_val = x_min_val + (x_max_val - x_min_val) * i / x_steps
        svg_x = padding + i / x_steps * (width - 2 * padding)
        svg += f'    <text x="{svg_x}" y="{height - padding + 15}" text-anchor="middle" font-size="10" fill="#666">{x_val:.1f}</text>\n'

    # Подписи оси Y
    for i in range(x_steps + 1):
        y_val = y_min_val + (y_max_val - y_min_val) * i / x_steps
        svg_y = height - padding - i / x_steps * (height - 2 * padding)
        svg += f'    <text x="{padding - 5}" y="{svg_y + 3}" text-anchor="end" font-size="10" fill="#666">{y_val:.1f}</text>\n'

    return svg


def _error_svg(message):
    """Возвращает SVG с сообщением об ошибке."""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
  <rect width="600" height="400" fill="#f8f9fa"/>
  <text x="300" y="200" text-anchor="middle" fill="#e74c3c" font-size="14">{message}</text>
</svg>
'''
