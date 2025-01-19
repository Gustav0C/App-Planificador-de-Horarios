import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

fid = passw = conf_passw = name = ini = email = subcode1 = subcode2 = None


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
    tree.heading('#1', text="ID")
    tree.heading('#2', text="Nombre")
    tree.heading('#3', text="Curso 1")
    tree.heading('#4', text="Curso 2")
    tree['height'] = 15


# update treeview (call this function after each update)
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT FID, NAME, SUBCODE1, SUBCODE2 FROM FACULTY")
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
    ini = str(ini_entry.get()).upper()
    email = str(email_entry.get())
    subcode1 = str(combo1.get())
    subcode2 = str(combo2.get())

    if fid == "" or passw == "" or \
        conf_passw == "" or name == "":
        messagebox.showwarning("Bad Input", "Algunos campos están vacíos! Por favor llenelas!")
        return

    if passw != conf_passw:
        messagebox.showerror("Las contraseñas no coinciden", "La contraseña y la confirmación de contraseña no coinciden. Intentar otra vez!")
        passw_entry.delete(0, tk.END)
        conf_passw_entry.delete(0, tk.END)
        return

    if subcode1 == "NULL":
        messagebox.showwarning("Bad Input", "El curso 1 no puede ser nulo")
        return
    
    conn.execute(f"REPLACE INTO FACULTY (FID, PASSW, NAME, INI, EMAIL, SUBCODE1, SUBCODE2)\
        VALUES ('{fid}','{passw}','{name}', '{ini}', '{email}', '{subcode1}', '{subcode2}')")
    conn.commit()
    update_treeview()
    
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    ini_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    combo1.current(0)
    combo2.current(0)
    

# update a row in the database
def update_data():
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    ini_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    combo1.current(0)
    combo2.current(0)
    try:
        # print(tree.selection())
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Seleccione una aula a la vez para actualizar!")
            return

        q_fid = tree.item(tree.selection()[0])['values'][0]
        cursor = conn.execute(f"SELECT * FROM FACULTY WHERE FID = '{q_fid}'")

        cursor = list(cursor)
        fid_entry.insert(0, cursor[0][0])
        passw_entry.insert(0, cursor[0][1])
        conf_passw_entry.insert(0, cursor[0][1])
        name_entry.insert(0, cursor[0][2])
        ini_entry.insert(0, cursor[0][3])
        email_entry.insert(0, cursor[0][4])
        combo1.current(subcode_li.index(cursor[0][5]))
        combo2.current(subcode_li.index(cursor[0][6]))

        conn.execute(f"DELETE FROM FACULTY WHERE FID = '{cursor[0][0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "¡Primero seleccione una aula de la lista!")
        return


# remove selected data from databse and treeview
def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "¡Primero seleccione una aula de la lista!")
        return
    for i in tree.selection():
        # print(tree.item(i)['values'][0])
        conn.execute(f"DELETE FROM FACULTY WHERE FID = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()


# toggles between show/hide password
def show_passw():
    if passw_entry['show'] == "●":
        passw_entry['show'] = ""
        B1_show['text'] = '●'
        B1_show.update()
    elif passw_entry['show'] == "":
        passw_entry['show'] = "●"
        B1_show['text'] = '○'
        B1_show.update()
    passw_entry.update()




# main
if __name__ == "__main__":  

    '''
        DATABASE CONNECTIONS AND SETUP
    '''

    # connecting database
    conn = sqlite3.connect(r'files/timetable.db')

    # creating Tabe in the database
    conn.execute('CREATE TABLE IF NOT EXISTS FACULTY\
    (FID CHAR(10) NOT NULL PRIMARY KEY,\
    PASSW CHAR(50) NOT NULL,\
    NAME CHAR(50) NOT NULL,\
    INI CHAR(5) NOT NULL,\
    EMAIL CHAR(50) NOT NULL,\
    SUBCODE1 CHAR(10) NOT NULL,\
    SUBCODE2 CHAR(10)    )')


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
    subtk.geometry('1000x550')
    subtk.title('Add/Update Faculties')

    # Label1
    tk.Label(
        subtk,
        text='Lista de Profesores',
        font=('Arial', 20, 'bold')
    ).place(x=600, y=50)

    # Label2
    tk.Label(
        subtk,
        text='Agregar/Actualizar Profesor',
        font=('Arial', 20, 'bold')
    ).place(x=90, y=50)

    # Label3
    tk.Label(
        subtk,
        text='¡Agregue información en el siguiente mensaje!',
        font=('Arial', 10, 'italic')
    ).place(x=100, y=85)

    # Label4
    tk.Label(
        subtk,
        text='Id:',
        font=('Arial', 12)
    ).place(x=100, y=130)

    # Entry1
    fid_entry = tk.Entry(
        subtk,
        font=('Arial', 12),
        width=20
    )
    fid_entry.place(x=260, y=130)

    # Label5
    tk.Label(
        subtk,
        text='Contraseña:',
        font=('Arial', 12)
    ).place(x=100, y=170)

    # Entry2
    passw_entry = tk.Entry(
        subtk,
        font=('Arial', 12),
        width=20,
        show="●"
    )
    passw_entry.place(x=260, y=170)

    B1_show = tk.Button(
        subtk,
        text='○',
        font=('Arial', 9, 'bold'),
        command=show_passw
    )
    B1_show.place(x=460,y=170)

    # Label6
    tk.Label(
        subtk,
        text='Confirmar contraseña:',
        font=('Arial', 12)
    ).place(x=100, y=210)

    # Entry3
    conf_passw_entry = tk.Entry(
        subtk,
        font=('Arial', 12),
        width=20,
        show="●"
    )
    conf_passw_entry.place(x=260, y=210)

    # Label7
    tk.Label(
        subtk,
        text='Nombre del Profesor:',
        font=('Arial', 12)
    ).place(x=100, y=250)

    # Entry4
    name_entry = tk.Entry(
        subtk,
        font=('Arial', 12),
        width=25,
    )
    name_entry.place(x=260, y=250)

    # Label8
    tk.Label(
        subtk,
        text='Inicial:',
        font=('Arial', 12)
    ).place(x=100, y=290)

    # Entry5
    ini_entry = tk.Entry(
        subtk,
        font=('Arial', 12),
        width=5,
    )
    ini_entry.place(x=260, y=290)

    # Label9
    tk.Label(
        subtk,
        text='Correo:',
        font=('Arial', 12)
    ).place(x=100, y=330)   

    # Entry6
    email_entry = tk.Entry(
        subtk,
        font=('Arial', 12),
        width=25,
    )
    email_entry.place(x=260, y=330)

    # get subject code list from the database
    cursor = conn.execute("SELECT SUBCODE FROM SUBJECTS")
    subcode_li = [row[0] for row in cursor]
    subcode_li.insert(0, 'NULL')

    # Label10
    tk.Label(
        subtk,
        text='Curso 1:',
        font=('Arial', 12)
    ).place(x=100, y=370)

    # ComboBox1
    combo1 = ttk.Combobox(
        subtk,
        values=subcode_li,
    )
    combo1.place(x=260, y=370)
    combo1.current(0)

    # Label11
    tk.Label(
        subtk,
        text='Curso 2:',
        font=('Arial', 12)
    ).place(x=100, y=410)

    # ComboBox2
    combo2 = ttk.Combobox(
        subtk,
        values=subcode_li,
    )
    combo2.place(x=260, y=410)
    combo2.current(0)

    # Button1
    B1 = tk.Button(
        subtk,
        text='Agregar Profesor',
        font=('Arial', 12),
        command=parse_data
    )
    B1.place(x=150,y=465)

    # Button2
    B2 = tk.Button(
        subtk,
        text='Actualizar Profesor',
        font=('Arial', 12),
        command=update_data
    )
    B2.place(x=410,y=465)

    # Treeview1
    tree = ttk.Treeview(subtk)
    create_treeview()
    update_treeview()

    # Button3
    B3 = tk.Button(
        subtk,
        text='Eliminar facultades',
        font=('Arial', 12),
        command=remove_data
    )
    B3.place(x=650,y=465)

    # looping Tkiniter window
    subtk.mainloop()
    conn.close() # close database after all operations
