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

# inputs in this window
subcode = subname = subtype = None

'''
    LIST OF FUNCTIONS USED FOR VARIOUS FUNCTIONS THROUGH TKinter INTERFACE
        * create_treeview()
        * update_treeview()
        * parse_data()
        * update_data()
        * remove_data()
'''

# create treeview (call this function once)
def create_treeview():
    tree['columns'] = ('one', 'two', 'three','four')
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("one", width=70, stretch=tk.NO)
    tree.column("two", width=300, stretch=tk.NO)
    tree.column("three", width=60, stretch=tk.NO)
    tree.column("four", width=70, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('one', text="Code")
    tree.heading('two', text="Name")
    tree.heading('three', text="Type")
    tree.heading('four',text="Section")


# update treeview (call this function after each update)
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT * FROM SUBJECTS")
    for row in cursor:
        # print(row[0], row[1], row[2])
        if row[2] == 'T':
            t = 'Theory'
        elif row[2] == 'P':
            t = 'Practical'
        tree.insert(
            "",
            0,
            values=(row[0],row[1],t)
        )
    tree.place(x=500, y=100)


# Parse and store data into database and treeview upon clcicking of the add button
def parse_data():
    subcode = str(subcode_entry.get())
    subname = str(subname_entry.get("1.0", tk.END)).upper().rstrip()
    subtype = str(radio_var.get()).upper()

    if subcode=="":
        subcode = None
    if subname=="":
        subname = None

    if subcode is None or subname is None:
        messagebox.showerror("Bad Input", "Por favor, rellene el código de area y/o el nombre de la area!")
        subcode_entry.delete(0, tk.END)
        subname_entry.delete("1.0", tk.END)
        return

    conn.execute(f"REPLACE INTO SUBJECTS (SUBCODE, SUBNAME, SUBTYPE)\
        VALUES ('{subcode}','{subname}','{subtype}')")
    conn.commit()
    update_treeview()
    
    subcode_entry.delete(0, tk.END)
    subname_entry.delete("1.0", tk.END)


# update a row in the database
def update_data():
    subcode_entry.delete(0, tk.END)
    subname_entry.delete("1.0", tk.END)
    try:
        # print(tree.selection())
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Seleccione un area a la vez para actualizar!")
            return

        row = tree.item(tree.selection()[0])['values']
        subcode_entry.insert(0, row[0])
        subname_entry.insert("1.0", row[1])
        if row[2][0] == "T":
            R1.select()
        elif row[2][0] == "P":
            R2.select()

        conn.execute(f"DELETE FROM SUBJECTS WHERE SUBCODE = '{row[0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Por favor seleccione un area de la lista primero!")
        return

# remove selected data from databse and treeview
def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Por favor seleccione un area de la lista primero!")
        return
    for i in tree.selection():
        # print(tree.item(i)['values'][0])
        conn.execute(f"DELETE FROM SUBJECTS WHERE SUBCODE = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()



# main
if __name__ == "__main__":  

    '''
        DATABASE CONNECTIONS AND SETUP
    '''

    # connecting database
    conn = sqlite3.connect(r'files/timetable.db')

    # creating Tabe in the database
    conn.execute('CREATE TABLE IF NOT EXISTS SUBJECTS\
    (SUBCODE CHAR(10) NOT NULL PRIMARY KEY,\
    SUBNAME CHAR(50) NOT NULL,\
    SUBTYPE CHAR(1) NOT NULL)')


    '''
        TKinter WINDOW SETUP WITH WIDGETS
            * Label(1-6)
            * Entry(1)
            * Text(1)
            * Radiobutton(1-2)
            * Treeview(1)
            * Button(1-2)
    '''

    # TKinter Window
    subtk = tk.Tk()
    subtk.geometry('1100x550')
    subtk.title('Add/Update Subjects')
    subtk.config(bg='SkyBlue2')

    # Label1
    tk.Label(
        subtk,
        text='Lista de Cursos',
        font=('Arial', 20, 'bold'),
        bg='SkyBlue2'
    ).place(x=600, y=50)

    # Label2
    tk.Label(
        subtk,
        text='Añadir/Actualizar Cursos',
        font=('Arial', 20, 'bold'),
        bg='SkyBlue2'
    ).place(x=100, y=50)

    # Label3
    tk.Label(
        subtk,
        text='En este apartado puedes añadir o actualizar los cursos',
        font=('Arial', 10, 'italic'),
        bg='SkyBlue2'
    ).place(x=100, y=85)

    # Label4
    tk.Label(
        subtk,
        text='Curso ID:',
        font=('Arial', 15),
        bg='SkyBlue2'
    ).place(x=100, y=150)

    # Entry1
    subcode_entry = ctk.CTkEntry(
        subtk,
        font=('Arial', 15),
        width=120
    )
    subcode_entry.place(x=270, y=150)
    
    # Label5
    tk.Label(
        subtk,
        text='Nombre de Curso:',
        bg='SkyBlue2',
        font=('Arial', 15)
    ).place(x=100, y=200)

    # ENTRY 2
    subname_entry = ctk.CTkTextbox(
        master=subtk,
        font=('Arial', 14),
        border_color='grey',
        border_width=2,
        width=200,  # Ancho en píxeles
        height=60,  # Alto en píxeles
        wrap="word"  # Equivalente a tk.WORD
    )
    subname_entry.place(x=270, y=200)

    # Label6
    tk.Label(
        subtk,
        text='Tipo de Curso:',
        font=('Arial', 15),
        bg='SkyBlue2'
    ).place(x=100, y=270)

    # RadioButton variable to store RadioButton Status
    radio_var = tk.StringVar()

    # RadioButton1
    R1 = ctk.CTkRadioButton(
        subtk,
        text='Teoria',
        font=('Arial', 14),
        variable=radio_var,
        value="T"
    )
    R1.place(x=270, y=270)
    R1.select()

    # RadioButton2
    R2 = ctk.CTkRadioButton(
        subtk,
        text='Practica',
        font=('Arial', 14),
        variable=radio_var,
        value="P"
    )
    R2.place(x=270, y=300)
    R2.select()
    # Label6
    tk.Label(
        subtk,
        text='Sección:',
        font=('Arial', 15),
        bg='SkyBlue2'
    ).place(x=100, y=340)

    # Entry1
    section_entry = ctk.CTkEntry(
        subtk,
        font=('Arial', 15),
        width=120
    )
    section_entry.place(x=270, y=340)
    # Recopilando datos de la hora de inicio del curso
    tk.Label(
        subtk,
        text='Horario:',
        font=('Arial', 15),
        bg='SkyBlue2'
    ).place(x=100, y=380)

    # horas entry
    i_horas_entry = ctk.CTkEntry(
        subtk,
        font=('Arial', 15),
        width=40,
        placeholder_text="HH"
    )
    i_horas_entry.place(x=270, y=380)
    # minutos entry
    i_minutos_entry = ctk.CTkEntry(
        subtk,
        font=('Arial', 15),
        width=40,
        placeholder_text="MM"
    )
    i_minutos_entry.place(x=320, y=380)

    # Recopilando datos del fin de hora del curso
    tk.Label(
        subtk,
        text='Fin de Hora:',
        font=('Arial', 15),
        bg='SkyBlue2'
    ).place(x=100, y=420)

    # horas entry
    f_horas_entry = ctk.CTkEntry(
        subtk,
        font=('Arial', 15),
        width=40,
        placeholder_text="HH"
    )
    f_horas_entry.place(x=270, y=420)
    # minutos entry
    f_minutos_entry = ctk.CTkEntry(
        subtk,
        font=('Arial', 15),
        width=40,
        placeholder_text="MM"
    )
    f_minutos_entry.place(x=320, y=420)

    # Button1
    B1 = ctk.CTkButton(
        subtk,
        text='Añadir Curso',
        font=('Arial', 12),
        text_color='black',
        command=parse_data
    )
    B1.place(x=150,y=470)

    # Button2
    B2 = ctk.CTkButton(
        subtk,
        text='Actualizar Curso',
        font=('Arial', 12),
        text_color='black',
        command=update_data
    )
    B2.place(x=410,y=470)

    # Treeview1
    tree = ttk.Treeview(subtk)
    create_treeview()
    update_treeview()

    # Button3
    B3 = ctk.CTkButton(
        subtk,
        text='Eliminar Curso(s)',
        font=('Arial', 12),
        text_color='black',
        command=remove_data
    )
    B3.place(x=650,y=470)

    # looping Tkiniter window
    subtk.mainloop()
    conn.close() # close database ad=fter all operations