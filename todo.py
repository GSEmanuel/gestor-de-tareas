from tkinter import *
from tkinter import ttk

import sqlite3

root = Tk()
root.title("gestor de tareas")
root.geometry("500x500")

conn = sqlite3.connect('to_do.db')
c = conn.cursor()

def render_todo():
	rows = c.execute('SELECT * FROM todo').fetchall()

	for i in rows:
		completed = i[3]
		description = i[2]

def addTodo():
	todo = e.get()
	c.execute("""
			INSERT INTO todo(description, completed) VALUES(?,?)
	""",(todo, False))
	conn.commit()
	e.delete(0, END)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(row= 0, column=0, sticky= 'nsew')

l = ttk.Label(mainframe ,text= 'Tarea')
l.grid(row=0, column=0)

e = ttk.Entry(mainframe, width=60)
e.grid(row=0, column=1)

btn = ttk.Button(mainframe, text= 'Agregar', command= addTodo)
btn.grid(row=0, column=2)

frame = ttk.LabelFrame(mainframe, text= 'Mis tareas')
frame.grid(row=1, column=0 , columnspan=3, sticky= 'nswe', padx=5, pady=5)

e.focus()
root.bind('<Return>', lambda x: addTodo())
render_todo()

root.mainloop()
