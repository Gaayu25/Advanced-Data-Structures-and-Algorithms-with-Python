back_stack = []
forward_stack = []
current_page = "Home"

def visit(page):
    global current_page
    back_stack.append(current_page)
    current_page = page
    forward_stack.clear()
    print(f"Visited: {current_page}")

def go_back():
    global current_page
    if not back_stack:
        print("No pages in Back!")
        return
    forward_stack.append(current_page)
    current_page = back_stack.pop()
    print(f"Back to: {current_page}")

def go_forward():
    global current_page
    if not forward_stack:
        print("No pages in Forward!")
        return
    back_stack.append(current_page)
    current_page = forward_stack.pop()
    print(f"Forward to: {current_page}")

def status():
    print("\nCurrent Page:", current_page)
    print("Back Stack:", back_stack)
    print("Forward Stack:", forward_stack, "\n")

# Demo operations
visit("google.com")
visit("youtube.com")
visit("gmail.com")
go_back()
go_back()
go_forward()
status()
