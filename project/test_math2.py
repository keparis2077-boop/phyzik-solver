import sys
sys.stdout = open('test_output.txt', 'w')
from math_tasks import MATH_TASKS
print(f"Total tasks: {len(MATH_TASKS)}")
for k, v in MATH_TASKS.items():
    print(f"  {k}: {v['category']}")
