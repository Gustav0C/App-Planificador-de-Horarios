import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
#IMPORTANTO EL CUSTOM TKINTER PARA LA INTERFAZ DE USUARIO
import customtkinter as ctk

#ASIGNANDO VALORES GLOBALES AL CTK
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

days = 5
periods = 8
recess_break_aft = 3 # recess after 3rd Period
section = None
butt_grid = []

period_names =['7:45-8:30', '8:30-9:15', '9:15-10:00', '10:00-10:45', '10:45-11:30','11:30-12:15','12:15-1:00','1:00-1:45']
day_names = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']

def update_p(d, p, tree, parent):
    # print(section, d, p, str(sub.get()))
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Seleccione un tema a la vez!")
            parent.destroy()
            return
        row = tree.item(tree.selection()[0])['values']
        if row[0] == 'NULL' and row[1] == 'NULL':
            conn.execute(f"DELETE FROM SCHEDULE WHERE ID='{section+str((d*periods)+p)}'")
            conn.commit()
            update_table()
            parent.destroy()
            return

        conn.commit()
        print(row)
        conn.execute(f"REPLACE INTO SCHEDULE (ID, DAYID, PERIODID, SUBCODE, SECTION, FINI)\
            VALUES ('{section+str((d*periods)+p)}', {d}, {p}, '{row[1]}', '{section}', '{row[0]}')")
        conn.commit()
        update_table()

    except IndexError:
        messagebox.showerror("Bad Select", "Por favor seleccione un tema de la lista!")
        parent.destroy()
        return

    parent.destroy()

def process_button(d, p):
    print(d, p)
    add_p = tk.Tk()
    # add_p.geometry('200x500')

    # get subject code list from the database
    cursor = conn.execute("SELECT SUBCODE FROM SUBJECTS")
    subcode_li = [row[0] for row in cursor]
    subcode_li.insert(0, 'NULL')

    # Label10
    tk.Label(
        add_p,
        text='Selecciona el Curso',
        font=('Arial', 12, 'bold')
    ).pack()

    tk.Label(
        add_p,
        text=f'Día: {day_names[d]}',
        font=('Arial', 12)
    ).pack()

    tk.Label(
        add_p,
        text=f'Periodo: {p+1}',
        font=('Arial', 12)
    ).pack()

    tree = ttk.Treeview(add_p)
    tree['columns'] = ('one', 'two')
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("one", width=70, stretch=tk.NO)
    tree.column("two", width=80, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('one', text="Profesor")
    tree.heading('two', text="Curso ID")
    
    cursor = conn.execute("SELECT FACULTY.INI, FACULTY.SUBCODE1, FACULTY.SUBCODE2, SUBJECTS.SUBCODE\
    FROM FACULTY, SUBJECTS\
    WHERE FACULTY.SUBCODE1=SUBJECTS.SUBCODE OR FACULTY.SUBCODE2=SUBJECTS.SUBCODE")
    for row in cursor:
        print(row)
        tree.insert(
            "",
            0,
            values=(row[0],row[-1])
        )
    tree.insert("", 0, value=('NULL', 'NULL'))
    tree.pack(pady=10, padx=30)

    tk.Button(
        add_p,
        text="OK",
        padx=15,
        command=lambda x=d, y=p, z=tree, d=add_p: update_p(x, y, z, d)
    ).pack(pady=20)

    add_p.mainloop()

def select_sec():
    global section
    section = str(combo1.get())
    print(section)
    update_table()

def update_table():
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute(f"SELECT SUBCODE, FINI FROM SCHEDULE\
                WHERE DAYID={i} AND PERIODID={j} AND SECTION='{section}'")
            cursor = list(cursor)
            print(cursor)
            if len(cursor) != 0:
                butt_grid[i][j]['text'] = str(cursor[0][0]) + '\n' + str(cursor[0][1])
                butt_grid[i][j].update()
                butt_grid[i][j]['bg']='Green'
                print(i, j, cursor[0][0])
            else:
                butt_grid[i][j]['text'] = "Sin Curso"
                butt_grid[i][j].update()
            
#CONECTANDO A LA BASE DE DATOS
conn = sqlite3.connect(r'files/timetable.db')

# creating Tabe in the database
conn.execute('CREATE TABLE IF NOT EXISTS SCHEDULE\
(ID CHAR(10) NOT NULL PRIMARY KEY,\
DAYID INT NOT NULL,\
PERIODID INT NOT NULL,\
SUBCODE CHAR(10) NOT NULL,\
SECTION CHAR(5) NOT NULL,\
FINI CHAR(10) NOT NULL)')
# DAYID AND PERIODID ARE ZERO INDEXED

#VENTANA PRINCIPAL
tt = tk.Tk()
tt.geometry('1200x600')
tt.title('Horario General')
tt.iconbitmap("files/images/favicon.ico")
tt.config(bg='SkyBlue2')

title_lab = tk.Label(
    tt,
    text='H O R A R I O',
    font=('Arial', 20, 'bold'),
    pady=5,
    bg='SkyBlue2'
)
title_lab.pack(pady=(20,10))

table = tk.Frame(tt, bg='Skyblue2')
table.pack()

first_half = tk.Frame(table, bg='Skyblue2')
first_half.pack(side='left')

recess_frame = tk.Frame(table, bg='Skyblue2')
recess_frame.pack(side='left')

second_half = tk.Frame(table, bg='Skyblue2')
second_half.pack(side='left')

for i in range(days):
    b = ctk.CTkLabel(
        first_half,
        text=day_names[i],
        font=('Arial', 16, 'bold'),
        width=12,
        height=2,
        bg_color="SkyBlue2",
        wraplength=400,
    )
    b.grid(row=i+1, column=0,padx=(0,10))

for i in range(periods):
    if i < recess_break_aft:
        b = tk.Label(first_half)
        b.grid(row=0, column=i+1)
    else:
        b = tk.Label(second_half)
        b.grid(row=0, column=i)

    b.config(
        text=period_names[i],
        font=('Arial', 14, 'bold'),
        width=10,
        height=2,
        bg="SkyBlue2"
    )
    b.grid(pady=(0,10))

for i in range(days):
    b = []
    for j in range(periods):
        if j < recess_break_aft:
            bb = tk.Button(first_half)
            bb.grid(row=i+1, column=j+1)
        else:
            bb = tk.Button(second_half)
            bb.grid(row=i+1, column=j)

        bb.config(
            text='Hello World!',
            font=('Arial', 10),
            width=13,
            height=3,
            bd=5,
            relief='raised',
            wraplength=80,
            justify='center',
            command=lambda x=i, y=j: process_button(x, y)
        )
        b.append(bb)

    butt_grid.append(b)
    # print(b)
    b = []
sec_select_f = tk.Frame(tt, pady=15,bg="SkyBlue2")
sec_select_f.pack()

tk.Label(
    sec_select_f,
    text='Seleccionar Sección:  ',
    font=('Arial', 12, 'bold'),
    bg="SkyBlue2"
).pack(side=tk.LEFT)

cursor = conn.execute("SELECT DISTINCT SECTION FROM STUDENT")
sec_li = [row[0] for row in cursor]
# sec_li.insert(0, 'NULL')
print(sec_li)
combo1 = ttk.Combobox(
    sec_select_f,
    values=sec_li,
)
combo1.pack(side=tk.LEFT)
combo1.current(0)

b = tk.Button(
    sec_select_f,
    text="OK",
    font=('Arial', 12, 'bold'),
    padx=10,
    command=select_sec
)
b.pack(side=tk.LEFT, padx=10)
b.invoke()

print(butt_grid[0][1], butt_grid[1][1])
update_table()

tt.mainloop()