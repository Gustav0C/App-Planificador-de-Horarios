import tkinter as tk
from tkinter import messagebox
import os, sys
sys.path.insert(0, 'windows/')
from windows import timetable_stud
from windows import timetable_fac
import sqlite3

#IMPORTANTO EL CUSTOM TKINTER
import customtkinter as ctk
#ASIGNANDO VALORES GLOBALES AL CTK
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

#ACCEDEMOS A LA BASE DE DATOS Y VERIFICAMOS EL USUARIO
def challenge():
    conn = sqlite3.connect(r'files/timetable.db')
    user = str(combo1.get())
    if user == "Estudiante":
        cursor = conn.execute(f"SELECT PASSW, SECTION, NAME, ROLL FROM STUDENT WHERE SID='{id_entry.get()}'")
        cursor = list(cursor)
        if len(cursor) == 0:
            messagebox.showwarning('Bad id', '¡Nombre de Usuario Incorrecto!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Bad pass', '¡Contraseña Incorrecta!')
        else:
            nw = tk.Tk()
            nw.geometry('1200x600')
            nw.title('Horario')
            nw.iconbitmap("files/images/favicon.ico")
            nw.config(bg="SkyBlue2")
            tk.Label(
                nw,
                text=f'{cursor[0][2]}\tSection: {cursor[0][1]}\tRoll No.: {cursor[0][3]}',
                font=('Arial', 12, 'italic'),
                bg="SkyBlue2"
            ).pack(pady=(10, 0))
            m.destroy()
            timetable_stud.student_tt_frame(nw, cursor[0][1])
            nw.mainloop()

    elif user == "Profesor":
        cursor = conn.execute(f"SELECT PASSW, INI, NAME, EMAIL FROM FACULTY WHERE FID='{id_entry.get()}'")
        cursor = list(cursor)
        if len(cursor) == 0:
            messagebox.showwarning('Bad id', '¡NOMBRE DE USUARIO INCORRECTO!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Bad pass', '¡CONTRASEÑA INCORRECTA!')
        else:
            nw = tk.Tk()
            tk.Label(
                nw,
                text=f'{cursor[0][2]} ({cursor[0][1]})\tEmail: {cursor[0][3]}',
                font=('Arial', 12, 'italic'),
            ).pack()
            m.destroy()
            timetable_fac.fac_tt_frame(nw, cursor[0][1])
            nw.mainloop()

    elif user == "Admin":
        if id_entry.get() == 'admin' and passw_entry.get() == 'admin':
            m.destroy()
            os.system('python windows\\admin_screen.py')
            # sys.exit()
        else:
            messagebox.showerror('Bad Input', '¡Nombre de usuario INCORRECTA/CONTRASEÑA!')

#CREANDO LA VENTANA PRINCIPAL
m = ctk.CTk()
m.geometry('400x430')
m.maxsize(width=400, height=430)
m.title('App v1.5')
m.iconbitmap("files/images/favicon.ico")
m.config(bg="SkyBlue2")

#TITULO DE LA VENTANA
ctk.CTkLabel(
    m,
    text='Planificador de Horarios',
    font=('Arial', 20, 'bold'),
    fg_color="SkyBlue2"
).pack(pady=20)

#FRASE DE BIENVENIDA
ctk.CTkLabel(
    m,
    text='Bienvenido!\nInicia Sesion para continuar',
    font=('Arial', 20, 'italic'),
    bg_color="SkyBlue2"
).pack(pady=10)

# LABEL DE NOMBRE DE USUARIO
ctk.CTkLabel(
    m,
    text='Nombre de Usuario',
    font=('Arial', 15),
    bg_color="SkyBlue2"
).pack()

#ENTRADA DE NOMBRE DE USUARIO
id_entry = ctk.CTkEntry(
    m,
    corner_radius=10,
    bg_color="SkyBlue2"
)
id_entry.pack()

# LABEL DE CONTRASEÑA
ctk.CTkLabel(
    m,
    text='Contraseña:',
    font=('Arial', 15),
    bg_color="SkyBlue2"
).pack()

# FUNCION PARA MOSTRAR/OCULTAR LA CONTRASEÑA
def show_passw():
    if passw_entry.cget("show") == "●":
        passw_entry.configure(show="")
        B1_show.configure(text='●')
    else:
        passw_entry.configure(show="●")
        B1_show.configure(text='○')

# 7
pass_entry_f = tk.Frame(bg='SkyBlue2')
pass_entry_f.pack()

# ENTRADA DE LA CONTRASEÑA
passw_entry = ctk.CTkEntry(
    pass_entry_f,
    show="●",
    corner_radius=10,
    bg_color='SkyBlue2'
)
passw_entry.pack(side=tk.LEFT,padx=(39, 10))

# BOTON PARA MOSTRAR/OCULTAR LA CONTRASEÑA
B1_show = ctk.CTkButton(
    pass_entry_f,
    text='○',
    font=('Arial', 12, 'bold'),
    width=25,
    height=25,
    corner_radius=10,
    command=show_passw
)
B1_show.pack(side=tk.LEFT,)

# COMBOBOX DE TIPO DE USUARIO ADMIN/PROFESOR/ESTUDIANTE
combo1 = ctk.CTkComboBox(
    m,
    values=['Estudiante', 'Profesor', 'Admin'],
    bg_color="SkyBlue2"
)
combo1.pack(pady=15)

#BOTON PARA INICIAR SESION
ctk.CTkButton(
    m,
    text='Iniciar Sesion',
    font=('Arial', 12, 'bold'),
    command=challenge,
    bg_color="SkyBlue2"
).pack(pady=10)

m.mainloop()