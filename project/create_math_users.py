"""
Создаёт демо-пользователей с историей решений по математике.
Запуск: python create_math_users.py
"""
from models import init_db, register_user, save_solution, add_xp, add_coins

def create_math_users():
    """Создаёт демо-пользователей с историей по математике."""
    init_db()
    
    # Демо-пользователи
    users = [
        {'username': 'math_alex', 'email': 'alex@math.com', 'password': '123'},
        {'username': 'math_maria', 'email': 'maria@math.com', 'password': '123'},
        {'username': 'math_ivan', 'email': 'ivan@math.com', 'password': '123'},
    ]
    
    # Создаём пользователей
    user_ids = {}
    for user_data in users:
        success, error = register_user(
            user_data['username'],
            user_data['email'],
            user_data['password']
        )
        if success:
            print(f"✅ Создан пользователь: {user_data['username']}")
        else:
            print(f"⚠️  {user_data['username']} уже существует")
    
    # Получаем user_id
    from models import login_user
    for user_data in users:
        user = login_user(user_data['username'], user_data['password'])
        if user:
            user_ids[user_data['username']] = user['id']
    
    # Задачи по математике для каждого пользователя
    math_tasks = {
        'math_alex': [
            {'task_id': 'quadratic_equation', 'task_name': 'Квадратное уравнение', 'inputs': 'a=1, b=-5, c=6', 'results': 'x₁=3.00, x₂=2.00'},
            {'task_id': 'linear_equation', 'task_name': 'Линейное уравнение', 'inputs': 'a=2, b=-10', 'results': 'x=5.00'},
            {'task_id': 'circle_area', 'task_name': 'Площадь круга', 'inputs': 'r=5', 'results': 'S=78.54'},
            {'task_id': 'sin_cos_tan', 'task_name': 'Тригонометрические функции', 'inputs': 'angle=30', 'results': 'sin=0.5000, cos=0.8660, tan=0.5774'},
        ],
        'math_maria': [
            {'task_id': 'system_equations', 'task_name': 'Система уравнений', 'inputs': 'a1=2, b1=3, c1=8, a2=1, b2=-1, c2=1', 'results': 'x=2.00, y=0.00'},
            {'task_id': 'pythagorean_theorem', 'task_name': 'Теорема Пифагора', 'inputs': 'a=3, b=4', 'results': 'c=5.00'},
            {'task_id': 'triangle_area', 'task_name': 'Площадь треугольника', 'inputs': 'a=10, h=5', 'results': 'S=25.00'},
        ],
        'math_ivan': [
            {'task_id': 'law_of_cosines', 'task_name': 'Теорема косинусов', 'inputs': 'a=5, b=7, gamma=60', 'results': 'c=6.24'},
            {'task_id': 'quadratic_equation', 'task_name': 'Квадратное уравнение', 'inputs': 'a=1, b=0, c=-4', 'results': 'x₁=2.00, x₂=-2.00'},
        ],
    }
    
    # Добавляем историю
    for username, user_tasks in math_tasks.items():
        user_id = user_ids.get(username)
        if not user_id:
            continue
        
        for task_data in user_tasks:
            save_solution(
                user_id,
                task_data['task_id'],
                task_data['task_name'],
                task_data['inputs'],
                task_data['results']
            )
        
        # Добавляем XP и монеты
        add_xp(user_id, len(user_tasks) * 15)
        add_coins(user_id, len(user_tasks) * 10)
        
        print(f"📊 {username}: {len(user_tasks)} задач по математике, XP={len(user_tasks)*15}, coins={len(user_tasks)*10}")
    
    print("\n✅ Демо-пользователи по математике созданы!")
    print("\n🔑 Данные для входа:")
    for user_data in users:
        print(f"  Логин: {user_data['username']}, Пароль: 123")


if __name__ == "__main__":
    create_math_users()
