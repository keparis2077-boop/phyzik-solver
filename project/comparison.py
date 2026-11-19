"""
comparison.py — система сравнения решений
Позволяет пользователю ввести своё решение и сравнить с правильным
"""

def compare_solutions(user_steps, correct_steps, tolerance=0.05):
    """
    Сравнивает решение пользователя с правильным.
    
    Args:
        user_steps: список шагов пользователя
        correct_steps: список правильных шагов
        tolerance: допустимая погрешность для чисел (5%)
    
    Returns:
        dict с результатами сравнения
    """
    result = {
        'is_correct': False,
        'score': 0,
        'total': len(correct_steps),
        'differences': [],
        'suggestions': []
    }
    
    if not correct_steps:
        result['score'] = 0
        result['is_correct'] = False
        return result
    
    # Считаем количество совпавших шагов
    matched = 0
    for i, correct_step in enumerate(correct_steps):
        if i < len(user_steps):
            user_step = user_steps[i]
            if _steps_match(user_step, correct_step, tolerance):
                matched += 1
            else:
                result['differences'].append({
                    'step': i + 1,
                    'user': user_step,
                    'correct': correct_step
                })
        else:
            result['differences'].append({
                'step': i + 1,
                'user': '(не указано)',
                'correct': correct_step
            })
    
    # Если пользователь добавил лишние шаги, это не всегда плохо
    if len(user_steps) > len(correct_steps):
        result['suggestions'].append('Вы добавили дополнительные шаги — это хорошо, но можно короче!')
    
    # Вычисляем оценку
    result['score'] = round((matched / len(correct_steps)) * 100, 1)
    result['is_correct'] = result['score'] >= 90
    
    # Добавляем рекомендации
    if result['score'] < 50:
        result['suggestions'].append('Попробуйте ещё раз — обратите внимание на формулы!')
    elif result['score'] < 90:
        result['suggestions'].append('Хорошо, но есть небольшие ошибки. Проверьте вычисления.')
    else:
        result['suggestions'].append('Отличное решение! 🎉')
    
    return result


def _steps_match(user_step, correct_step, tolerance):
    """Проверяет, совпадают ли два шага с учётом допустимой погрешности."""
    user_step = user_step.strip().lower()
    correct_step = correct_step.strip().lower()
    
    # Точное совпадение
    if user_step == correct_step:
        return True
    
    # Извлекаем числа из обоих шагов
    user_nums = _extract_numbers(user_step)
    correct_nums = _extract_numbers(correct_step)
    
    # Если в обоих шагах есть числа — сравниваем их
    if user_nums and correct_nums:
        if len(user_nums) == len(correct_nums):
            return all(
                _numbers_close(u, c, tolerance)
                for u, c in zip(user_nums, correct_nums)
            )
    
    # Проверяем, содержит ли один шаг другой
    if correct_step in user_step or user_step in correct_step:
        return True
    
    return False


def _extract_numbers(text):
    """Извлекает все числа из строки."""
    import re
    return [float(x) for x in re.findall(r'[-+]?\d*\.?\d+', text)]


def _numbers_close(a, b, tolerance):
    """Проверяет, близки ли два числа с учётом погрешности."""
    if b == 0:
        return abs(a) < tolerance
    return abs(a - b) / abs(b) <= tolerance
