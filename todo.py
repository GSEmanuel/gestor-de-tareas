from tkinter import *
from tkinter import ttk

import sqlite3

root = Tk()
root.title("gestor de tareas")
#root.geometry("500x500")

conn = sqlite3.connect('to_do.db')
c = conn.cursor()

def remove(id):
	def _remove():
		c.execute("DELETE FROM todo WHERE id = ?",(id,))
		conn.commit()
		render_todo()

	return _remove

#curring
def complete(id):
	def _complete():


		todo = c.execute("SELECT * FROM todo WHERE id = ?", (id)).fetchone()
		if todo[3] == 1:
			val = False
		else:
			val = True
		c.execute("UPDATE  todo SET completed = ? WHERE id =?",(val, id))
		conn.commit()
		render_todo()

	return _complete

def render_todo():
	rows = c.execute('SELECT * FROM todo').fetchall()

	for widget in frame.winfo_children():
		widget.destroy()

	for i in rows:
		id = i[0]
		completed = i[3]
		description = i[2]
		color = '#555555' if completed else '#ffffff'
		ch = Checkbutton(frame, text=description, command= lambda: complete(id))
		ch.grid(row=rows.index(i), column=0, sticky='w')
		but = ttk.Button(frame, text='eliminar', command=remove(id))
		but.grid(row=rows.index(i), column=(1))
		ch.select() if completed ==1 else ch.deselect()


def addTodo():
	todo = e.get()
	if todo:
		c.execute("""
		INSERT INTO todo(description, completed) VALUES(?,?)
		""",(todo, False))
		conn.commit()
		e.delete(0, END)
		render_todo()
	else:
		pass

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(row= 0, column=0, sticky= 'nsew')

l = ttk.Label(mainframe ,text= 'Tarea')
l.grid(row=0, column=0)

e = ttk.Entry(mainframe, width=45)
e.grid(row=0, column=1)

btn = ttk.Button(mainframe, text= 'Agregar', command= addTodo)
btn.grid(row=0, column=2)

frame = ttk.LabelFrame(mainframe, text= 'Mis tareas')
frame.grid(row=1, column=0 , columnspan=3, sticky= 'nswe', padx=5, pady=5)

e.focus()
root.bind('<Return>', lambda x: addTodo())
render_todo()

root.mainloop()
