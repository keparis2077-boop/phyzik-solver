"""
Конфигурация pytest для проекта.
"""

import sys
from pathlib import Path

# Добавляем корень проекта в путь для импорта модулей
sys.path.insert(0, str(Path(__file__).parent.parent))
