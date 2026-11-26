import sys
import os

# Добавляем путь к venv site-packages
venv_site_packages = os.path.join(
    os.path.dirname(__file__),
    '.venv', 'lib',
    f'python{sys.version_info.major}.{sys.version_info.minor}', 'site-packages'
)
if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)

# Добавляем директорию проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'project'))

from app import app
app.run(host='0.0.0.0', port=5000, debug=True)
