import tkinter as tk
import sys
import os
import threading
import customtkinter as ctk
def run_sub(): os.system('pythonw windows\\subjects.py')
def run_fac(): os.system('pythonw windows\\faculty.py')
def run_stud(): os.system('pythonw windows\\student.py')
def run_sch(): os.system('pythonw windows\\scheduler.py')
def run_tt_s(): os.system('pythonw windows\\timetable_stud.py')
def run_tt_f(): os.system('pythonw windows\\timetable_fac.py')

ad = tk.Tk()
ad.geometry('500x430')
ad.title('Administrador')
ad.config(bg="SkyBlue2")
tk.Label(
    ad,
    text='A D M I N I S T R A D O R',
    font=('Arial', 20, 'bold'),
    pady=10,
    bg="SkyBlue2"
).pack()

tk.Label(
    ad,
    text='Tú eres el administrador',
    font=('Arial', 12, 'italic'),
    bg="SkyBlue2"
).pack(pady=9)

modify_frame = tk.LabelFrame(text='Modificar', font=('Arial'), padx=20,bg="SkyBlue2", fg="blue")
modify_frame.place(x=50, y=100)

ctk.CTkButton(
    modify_frame,
    text='Cursos',
    font=('Arial', 14),
    command=run_sub,
    text_color="black",
    width=120
).pack(pady=20)

ctk.CTkButton(
    modify_frame,
    text='Profesor',
    font=('Arial', 14),
    text_color="black",
    command=run_fac,
    width=120
).pack(pady=20)

ctk.CTkButton(
    modify_frame,
    text='Estudiantes',
    font=('Arial', 14),
    text_color="black",
    command=run_stud,
    width=120
).pack(pady=20)

tt_frame = tk.LabelFrame(text='Horario', font=('Arial'), padx=20, bg="SkyBlue2",fg="blue")
tt_frame.place(x=250, y=100)

ctk.CTkButton(
    tt_frame,
    text='Horario General',
    font=('Arial', 14),
    text_color="black",
    command=run_sch,
    width=120
).pack(pady=20)

ctk.CTkButton(
    tt_frame,
    text='Ver por Secciones',
    font=('Arial', 14),
    text_color="black",
    command=run_tt_s,
    width=120
).pack(pady=20)

ctk.CTkButton(
    tt_frame,
    text='Ver por Profesores',
    font=('Arial', 14),
    text_color="black",
    command=run_tt_f,
    width=120
).pack(pady=20)


ctk.CTkButton(
    ad,
    text='Salir',
    font=('Arial', 14),
    text_color="black",
    command=ad.destroy,
).place(x=180, y=360)

ad.mainloop()