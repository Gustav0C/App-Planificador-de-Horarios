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

def select_sec():
    global section
    section = str(combo1.get())
    print(section)
    update_table(section)

def update_table(sec):
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute(f"SELECT SUBCODE, FINI FROM SCHEDULE\
                WHERE DAYID={i} AND PERIODID={j} AND SECTION='{sec}'")
            cursor = list(cursor)
            print(cursor)
            
            butt_grid[i][j]['bg'] = 'white'
            if len(cursor) != 0:
                subcode = cursor[0][0]
                cur1 = conn.execute(F"SELECT SUBTYPE FROM SUBJECTS WHERE SUBCODE='{subcode}'")
                cur1 = list(cur1)
                subtype = cur1[0][0]
                butt_grid[i][j]['fg'] = 'white'
                if subtype == 'T':
                    butt_grid[i][j]['bg'] = 'green'
                elif subtype == 'P':
                    butt_grid[i][j]['bg'] = 'blue'

                butt_grid[i][j]['text'] = str(cursor[0][0]) + '\n' + str(cursor[0][1])
                butt_grid[i][j].update()
                print(i, j, cursor[0][0])
            else:
                butt_grid[i][j]['fg'] = 'black'
                butt_grid[i][j]['text'] = "Sin Curso"
                butt_grid[i][j].update()

def process_button(d, p, sec):
    details = tk.Tk()
    cursor = conn.execute(f"SELECT SUBCODE, FINI FROM SCHEDULE\
                WHERE ID='{section+str((d*periods)+p)}'")
    cursor = list(cursor)
    if len(cursor) != 0:
        subcode = str(cursor[0][0]) 
        fini =  str(cursor[0][1])

        cur1 = conn.execute(f"SELECT SUBNAME, SUBTYPE FROM SUBJECTS\
            WHERE SUBCODE='{subcode}'")
        cur1 = list(cur1)
        subname = str(cur1[0][0])
        subtype = str(cur1[0][1])

        cur2 = conn.execute(f"SELECT NAME, EMAIL FROM FACULTY\
            WHERE INI='{fini}'")
        cur2 = list(cur2)
        fname = str(cur2[0][0])
        femail = str(cur2[0][1]) 

        if subtype == 'T':
            subtype = 'Theory'
        elif subtype == 'P':
            subtype = 'Practical'

    else:
        subcode = fini = subname = subtype = fname = femail = 'None'

    print(subcode, fini, subname, subtype, fname, femail)
    tk.Label(details, text='Detalles del Curso', font=('Arial', 15, 'bold')).pack(pady=15)
    tk.Label(details, text='Día: '+day_names[d], font=('Arial'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Periodo: '+str(p+1), font=('Arial'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='ID: '+subcode, font=('Arial'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Nombre: '+subname, font=('Arial'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Tipo: '+subtype, font=('Arial'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Iniciales: '+fini, font=('Arial'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Nombre del Profesor: '+fname, font=('Arial'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Correo del Profesor: '+femail, font=('Arial'), anchor="w").pack(expand=1, fill=tk.X, padx=20)

    tk.Button(
        details,
        text="OK",
        font=('Arial'),
        width=10,
        command=details.destroy
    ).pack(pady=10)

    details.mainloop()

def student_tt_frame(tt, sec):
    title_lab = tk.Label(
        tt,
        text='H O R A R I O',
        font=('Arial', 20, 'bold'),
        pady=5,
        bg="SkyBlue2"
    )
    title_lab.pack()

    legend_f = tk.Frame(tt,bg="SkyBlue2")
    legend_f.pack(pady=15)
    tk.Label(
        legend_f,
        text='Leyenda: ',
        font=('Arial', 10, 'italic'),
        bg="SkyBlue2"
    ).pack(side=tk.LEFT)

    tk.Label(
        legend_f,
        text='Clases Teoricas',
        bg='green',
        fg='white',
        relief='raised',
        font=('Arial', 10, 'italic'),
        height=2
    ).pack(side=tk.LEFT, padx=10)

    tk.Label(
        legend_f,
        text='Clases Practicas',
        bg='blue',
        fg='white',
        relief='raised',
        font=('Arial', 10, 'italic'),
        height=2
    ).pack(side=tk.LEFT, padx=10)
    
    global butt_grid
    global section
    section = sec

    table = tk.Frame(tt, bg="SkyBlue2")
    table.pack()

    first_half = tk.Frame(table, bg="SkyBlue2")
    first_half.pack(side='left')

    recess_frame = tk.Frame(table,bg="SkyBlue2")
    recess_frame.pack(side='left')

    second_half = tk.Frame(table,bg="SkyBlue2")
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

        b.configure(
            text=period_names[i],
            font=('Arial', 14, 'bold'),
            width=10,
            height=2,
            bg="SkyBlue2"
        )

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
                text='None',
                font=('Arial', 10),
                width=13,
                height=3,
                bd=5,
                relief='raised',
                wraplength=80,
                justify='center',
                command=lambda x=i, y=j, z=sec: process_button(x, y, z)
            )
            b.append(bb)
        butt_grid.append(b)
        # print(b)
        b = []

    print(butt_grid[0][1], butt_grid[1][1])
    update_table(sec)

conn = sqlite3.connect(r'files/timetable.db')
if __name__ == "__main__":
    
    # connecting database
    tt = tk.Tk()
    tt.title('Horario para Estudiantes')
    tt.geometry('1200x600')
    tt.iconbitmap("files/images/favicon.ico")
    tt.config(bg="SkyBlue2")
    student_tt_frame(tt, section)

    sec_select_f = tk.Frame(tt, pady=15,bg="SkyBlue2")
    sec_select_f.pack()

    tk.Label(
        sec_select_f,
        text='Selecciona la Sección:  ',
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


    tt.mainloop()