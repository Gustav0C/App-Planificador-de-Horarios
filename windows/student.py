import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
#IMPORTANTO EL CUSTOM TKINTER PARA LA INTERFAZ DE USUARIO
import customtkinter as ctk
#ASIGNANDO VALORES GLOBALES AL CTK
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

fid = passw = conf_passw = name = roll = section = None

'''
    LIST OF FUNCTIONS USED FOR VARIOUS FUNCTIONS THROUGH TKinter INTERFACE
        * create_treeview()
        * update_treeview()
        * parse_data()
        * update data()
        * remove_data()
        * show_passw()
'''

# create treeview (call this function once)
def create_treeview():
    tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 5)))
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("#1", width=70, stretch=tk.NO)
    tree.column("#2", width=200, stretch=tk.NO)
    tree.column("#3", width=80, stretch=tk.NO)
    tree.column("#4", width=80, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('#1', text="sid")
    tree.heading('#2', text="Name")
    tree.heading('#3', text="Roll")
    tree.heading('#4', text="Section")
    tree['height'] = 12

# update treeview (call this function after each update)
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT SID, NAME, ROLL, SECTION FROM STUDENT")
    for row in cursor:
        tree.insert(
            "",
            0,
            values=(row[0], row[1], row[2], row[3])
        )
    tree.place(x=530, y=100)

# Parse and store data into database and treeview upon clcicking of the add button
def parse_data():
    fid = str(fid_entry.get())
    passw = str(passw_entry.get())
    conf_passw = str(conf_passw_entry.get())
    name = str(name_entry.get()).upper()
    roll = str(roll_entry.get())
    section = str(sec_entry.get()).upper()

    if fid == "" or passw == "" or \
        conf_passw == "" or name == "" or \
        roll == "" or section == "":
        messagebox.showwarning("Bad Input", "Algunos campos están vacíos. Por favor, rellénelos.!")
        return

    if passw != conf_passw:
        messagebox.showerror("Passwords mismatch", "La contraseña y la confirmación de contraseña no coinciden. Inténtalo de nuevo.!")
        passw_entry.delete(0, tk.END)
        conf_passw_entry.delete(0, tk.END)
        return

    conn.execute(f"REPLACE INTO STUDENT (SID, PASSW, NAME, ROLL, SECTION)\
        VALUES ('{fid}','{passw}','{name}', '{roll}', '{section}')")
    conn.commit()
    update_treeview()
    
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    sec_entry.delete(0, tk.END)
    

# update a row in the database
def update_data():
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    sec_entry.delete(0, tk.END)
    try:
        # print(tree.selection())
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Seleccione un estudiante a la vez para actualizar!")
            return

        q_fid = tree.item(tree.selection()[0])['values'][0]
        cursor = conn.execute(f"SELECT * FROM STUDENT WHERE SID = '{q_fid}'")

        cursor = list(cursor)
        fid_entry.insert(0, cursor[0][0])
        passw_entry.insert(0, cursor[0][1])
        conf_passw_entry.insert(0, cursor[0][1])
        name_entry.insert(0, cursor[0][2])
        roll_entry.insert(0, cursor[0][3])
        sec_entry.insert(0, cursor[0][4])
        
        conn.execute(f"DELETE FROM STUDENT WHERE SID = '{cursor[0][0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Por favor seleccione un estudiante de la lista primero!")
        return


# remove selected data from databse and treeview
def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Por favor seleccione un estudiante de la lista primero!")
        return
    for i in tree.selection():
        # print(tree.item(i)['values'][0])
        conn.execute(f"DELETE FROM STUDENT WHERE SID = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()


# toggles between show/hide password
def show_passw():
    if passw_entry.cget("show") == "●":
        passw_entry.configure(show="")
        B1_show.configure(text="●")
    else:
        passw_entry.configure(show="●")
        B1_show.configure(text="○")

# main
if __name__ == "__main__":  

    '''
        DATABASE CONNECTIONS AND SETUP
    '''

    # connecting database
    conn = sqlite3.connect(r'files/timetable.db')

    # creating Tabe in the database
    conn.execute('CREATE TABLE IF NOT EXISTS STUDENT\
    (SID CHAR(10) NOT NULL PRIMARY KEY,\
    PASSW CHAR(50) NOT NULL,\
    NAME CHAR(50) NOT NULL,\
    ROLL INTEGER NOT NULL,\
    SECTION CHAR(5) NOT NULL)')


    '''
        TKinter WINDOW SETUP WITH WIDGETS
            * Label(1-11)
            * Entry(6)
            * ComboBox(1-2)
            * Treeview(1)
            * Button(1-3)
    '''

    # TKinter Window
    subtk = tk.Tk()
    subtk.geometry('1000x470')
    subtk.title('Añadir/Actualizar Estudiantes')
    subtk.config(bg='SkyBlue2')

    # Label1
    tk.Label(
        subtk,
        text='Lista de Estudiantes',
        font=('Arial', 20, 'bold'),
        bg='SkyBlue2'
    ).place(x=620, y=50)

    # Label2
    tk.Label(
        subtk,
        text='Añadir/Actualizar Estudiantes',
        font=('Arial', 20, 'bold'),
        bg='SkyBlue2'
    ).place(x=110, y=50)

    # Label3
    tk.Label(
        subtk,
        text='En este apartado podras añadir o actualizar un estudiante',
        font=('Arial', 10, 'italic'),
        bg='SkyBlue2'
    ).place(x=110, y=85)

    # Label4
    tk.Label(
        subtk,
        text='ID Estudiante:',
        font=('Arial', 12),
        bg='SkyBlue2'
    ).place(x=100, y=130)

    # Entry1
    fid_entry = ctk.CTkEntry(
        subtk,
        font=('Arial', 12),
        width=60
    )
    fid_entry.place(x=260, y=130)

    # Label5
    tk.Label(
        subtk,
        text='Contraseña:',
        font=('Arial', 12),
        bg='SkyBlue2'
    ).place(x=100, y=170)

    # Entry2
    passw_entry = ctk.CTkEntry(
        subtk,
        font=('Arial', 12),
        width=160,
        show="●"
    )
    passw_entry.place(x=260, y=170)

    B1_show = ctk.CTkButton(
        subtk,
        text="○",
        font=('Arial', 9, 'bold'),
        command=show_passw,
        width=25,  # Ancho del botón
        height=25,  # Alto del botón
        corner_radius=10
    )
    B1_show.place(x=430, y=170)

    # Label6
    tk.Label(
        subtk,
        text='Confirmar Contraseña:',
        font=('Arial', 12),
        bg='SkyBlue2'
    ).place(x=100, y=210)

    # Entry3
    conf_passw_entry = ctk.CTkEntry(
        subtk,
        font=('Arial', 12),
        width=160,
        show="●"
    )
    conf_passw_entry.place(x=260, y=210)

    # Label7
    tk.Label(
        subtk,
        text='Nombre:',
        font=('Arial', 12),
        bg='SkyBlue2'
    ).place(x=100, y=250)

    # Entry4
    name_entry = ctk.CTkEntry(
        subtk,
        font=('Arail', 12),
        width=200,
    )
    name_entry.place(x=260, y=250)

    # Label8
    tk.Label(
        subtk,
        text='Roll no.:',
        font=('Arial', 12),
        bg='SkyBlue2'
    ).place(x=100, y=290)

    # Entry5
    roll_entry = ctk.CTkEntry(
        subtk,
        font=('Arial', 12),
        width=40,
    )
    roll_entry.place(x=260, y=290)

    # Label9
    tk.Label(
        subtk,
        text='Seccion:',
        font=('Arial', 12),
        bg='SkyBlue2'
    ).place(x=100, y=330)

    # Entry6
    sec_entry = ctk.CTkEntry(
        subtk,
        font=('Arial', 12),
        width=40,
    )
    sec_entry.place(x=260, y=330)

    # Button1
    B1 = ctk.CTkButton(
        subtk,
        text='Añadir Estudiante',
        font=('Arial', 12),
        command=parse_data,
        text_color='black'
    )
    B1.place(x=150,y=400)

    # Button2
    B2 = ctk.CTkButton(
        subtk,
        text='Actualizar Estudiante',
        font=('Arial', 12),
        command=update_data,
        text_color='black'
    )
    B2.place(x=410,y=400)

    # Treeview1
    tree = ttk.Treeview(subtk)
    create_treeview()
    update_treeview()

    # Button3
    B3 = ctk.CTkButton(
        subtk,
        text='Delete Student(s)',
        font=('Arial', 12),
        command=remove_data,
        text_color='black'
    )
    B3.place(x=650,y=400)

    # looping Tkiniter window
    subtk.mainloop()
    conn.close() # close database after all operations
