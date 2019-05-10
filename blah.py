import tkinter as tk
import random

numbers = [1,2,3,4,5]
answers = [2,4,6,8,10]

root = tk.Tk()
tk.Label(root, text = "Hello").pack()
chosen = random.choice(numbers)
tk.Label(root, text = chosen).pack()
index = numbers.index(chosen)
boolean_check = False
for x in range(3):
    if x == 2 and boolean_check == False:
        tk.Button(root, text = answers[index]).pack()
        boolean_check = True
        break
    if boolean_check == False:
        number_boolean = random.randint(0,1)
        if number_boolean == 1:
            tk.Button(root, text = answers[index]).pack()
            boolean_check = True
        else:
            tk.Button(root, text = random.randint(0, (answers[index] - 1))).pack()
    else:
        tk.Button(root, text = random.randint(0, (answers[index] - 1))).pack()



