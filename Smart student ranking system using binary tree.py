class Node:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
        self.left = None
        self.right = None

# Insert based on marks
def insert(root, name, marks):
    if root is None:
        return Node(name, marks)
    if marks < root.marks:
        root.left = insert(root.left, name, marks)
    else:
        root.right = insert(root.right, name, marks)
    return root

# Reverse inorder → gives highest first
def rank_students(root, ranks):
    if root:
        rank_students(root.right, ranks)
        ranks.append((root.name, root.marks))
        rank_students(root.left, ranks)

# MAIN SYSTEM
root = None
n = int(input("Enter number of students: "))

for _ in range(n):
    name = input("Name: ")
    marks = int(input("Total Marks: "))
    root = insert(root, name, marks)

result = []
rank_students(root, result)

print("\n--- SMART STUDENT RANK LIST ---")
rank = 1
for name, marks in result:
    print(f"Rank {rank}: {name} - {marks}")
    rank += 1
