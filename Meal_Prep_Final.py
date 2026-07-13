from collections import defaultdict, deque


menu = {
    "Starter": [],
    "Main Course": [],
    "Dessert": []
}

resources = {
    "stove": 3,
    "oven": 2,
    "airfryer": 2,
    "chef": 5
}

tasks = {}              
graph = defaultdict(list)
indegree = {}



class Task:
    def __init__(self, name, course, duration, resource):
        self.name = name
        self.course = course
        self.duration = duration
        self.resource = resource



def assign_resources_and_create_task(dish_name, course_type):
    
    if course_type == "Starter":
        needed_resource = "airfryer"
        duration = 5
    elif course_type == "Main Course":
        needed_resource = "stove"
        duration = 10
    elif course_type == "Dessert":
        needed_resource = "oven"
        duration = 15
    else:
        return False

    
    if resources[needed_resource] <= 0 or resources["chef"] <= 0:
        print(f"❌ Not enough resources for {dish_name}")
        return False

    resources[needed_resource] -= 1
    resources["chef"] -= 1

    task = Task(dish_name, course_type, duration, needed_resource)
    tasks[dish_name] = task
    indegree[dish_name] = 0

    print(f"✅ {dish_name} added with resource {needed_resource}")
    return True


def add_dependency(task1, task2):
    if task1 not in tasks or task2 not in tasks:
        print("❌ One of the tasks does not exist")
        return
    graph[task1].append(task2)
    indegree[task2] += 1
    print(f"Dependency added: {task1} → {task2}")


def show_menu():
    print("\n🍽️ Menu:")
    for category in menu:
        print(f"\n{category}:")
        for dish in menu[category]:
            print(f" - {dish}")


def show_resources():
    print("\n📊 Resources:")
    for r in resources:
        print(f"{r} : {resources[r]}")

#topological sort
def schedule_tasks():
    queue = deque()
    time = 0

    for task in tasks:
        if indegree[task] == 0:
            queue.append(task)

    print("\n⏳ Scheduling Tasks...\n")

    while queue:
        current = queue.popleft()
        task = tasks[current]

        print(f"Time {time}: Start {task.name} ({task.resource})")

        time += task.duration

        print(f"Time {time}: Finished {task.name}\n")

        resources[task.resource] += 1
        resources["chef"] += 1

        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    print("🎉 All dishes prepared successfully!")

#Menu
while True:
    print("\n===== Advanced Meal Preparation System =====")
    print("1. Add Starter")
    print("2. Add Main Course")
    print("3. Add Dessert")
    print("4. Add Dependency")
    print("5. Show Menu")
    print("6. Show Resources")
    print("7. Schedule Tasks")
    print("8. Exit")

    choice = input("Enter choice: ")
    if choice == "1":
        dish = input("Enter Starter: ")
        if assign_resources_and_create_task(dish, "Starter"):
            menu["Starter"].append(dish)

    elif choice == "2":
        dish = input("Enter Main Course: ")
        if assign_resources_and_create_task(dish, "Main Course"):
            menu["Main Course"].append(dish)

    elif choice == "3":
        dish = input("Enter Dessert: ")
        if assign_resources_and_create_task(dish, "Dessert"):
            menu["Dessert"].append(dish)

    elif choice == "4":
        t1 = input("Enter prerequisite dish: ")
        t2 = input("Enter dependent dish: ")
        add_dependency(t1, t2)

    elif choice == "5":
        show_menu()

    elif choice == "6":
        show_resources()

    elif choice == "7":
        schedule_tasks()

    elif choice == "8":
        print("Exiting system 👋")
        break

    else:
        print("Invalid choice!")
