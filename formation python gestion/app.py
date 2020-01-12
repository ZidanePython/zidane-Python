# TTK utiliser pour cree des nouvelle fentre dans la meme fenetre
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar,DateEntry
from tkinter.scrolledtext import *
from tkinter import messagebox
from PIL import Image, ImageTk

#db [  CONNECTION TO DATABASE WITH SQL3
import sqlite3
import csv

conn = sqlite3.connect("datas.db")
c = conn.cursor()

#create table manually
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS userdatas(id INTEGER PRIMARY KEY ,fname TEXT, lname TEXT,"
              "email TEXT,age TEXT,  date_of_birth TEXT,"
              " address TEXT, phonenumber REAL, formation TEXT)")

def add_data(fname,lname,email,age,date_of_birth,address,phonenumber, formation):
    c.execute("INSERT INTO userdatas VALUES (NULL,?,?,?,?,?,?,?,?)",(fname,lname,email,age,date_of_birth,address,phonenumber,formation))#protect from sql injections")
    conn.commit()

def view_all_users():
    tree.delete(*tree.get_children())
    c.execute('SELECT * FROM userdatas')
    data = c.fetchall()
    #adding data to the tree view
    global i
    i=1
    for row in data:
        tree.insert("",i, values=row)
        i+=1





def get_single_user(first_name):
    c.execute('SELECT * FROM userdatas WHERE fname=?',(first_name,))
    data = c.fetchall()
    return data


#OTHER FUNCIONS

def clear_text():
    entry_fname.delete(0,END)
    entry_lname.delete(0,END)
    entry_adress.delete(0,END)
    entry_age.delete(0,END)
    entry_email.delete(0,END)
    entry_phone.delete(0,END)
    formation_var.set("PYTHON")


def add_detail():
    firstname=str(entry_fname.get())
    lastname = str(entry_lname.get())
    email = str(entry_email.get())
    age = str(entry_age.get())
    date_of_birth=str(cal.get())
    phone_number = str(entry_phone.get())
    address = str(entry_adress.get())
    formation = str(formation_var.get())
    print(formation)
    add_data(firstname,lastname,email,age,date_of_birth,address,phone_number, formation)
    list = ["firstname:"+entry_fname.get(),"lastname :"+entry_lname.get(),entry_email.get(), entry_age.get(), cal.get(),entry_phone.get(),entry_adress.get(),formation_var.get()]
    for row in list:
        elemnt_list.insert(END, row)
    messagebox.showinfo(title="Registrio Gui", message="Submitted to Database")


def clear_display_result():
    elemnt_list.delete(0,END)


def search_user_by_name():
    firstname= str(entry_search.get())
    result = get_single_user(firstname)
    tab2_display.insert(END,result)


def clear_view_display():
    tab2_display.delete('1.0',END)


def clear_entered_search():
    entry_search.delete('0',END)


def clear_tree_view():
    tree.delete('1.0',END)


def export_as_csv():
    filename=str(entry_filename.get())#getting the file
    myfilename = filename+'.csv'#creating the file
    with open(myfilename, 'w') as f :#
        writer = csv.writer(f)
        c.execute("SELECT * FROM userdata")
        data = c.fetchall()
        writer.writerow(['id','fname','lname','email','age','date_of_birth','address','phonenumber','formation'])#the column names
        writer.writerows(data)#the row inserting the datas
        messagebox.showinfo(title="Registerio Gui", message="Exported as {}".format(myfilename))


def get_current_selection(event):
    global id
    global r

    item = tree.item(tree.selection())
    id = item['values'][0]

    r = tree.selection()[0]
    print(id)

    #qund je click je vais afficher les element dans les entrer
    entry_fname_1.insert(0,item['values'][1])
    entry_lname_1.insert(0,item['values'][2])
    entry_email_1.insert(0,item['values'][3])
    entry_age_1.insert(0,item['values'][4])
    cal_1.delete(0, END)
    cal_1.insert(0,item['values'][5])
    entry_phone_1.insert(0,item['values'][6])
    entry_adress_1.insert(0,item['values'][7])
    formation_var_1.set(item['values'][8])


def remouve_item():
    global id
    global tree
    ids =id
    tree.detach(r)

    c.execute("delete from userdatas where id = ?",(ids,))
    conn.commit()
    tree.delete(*tree.get_children())
    view_all_users()


def export_as_xls():
        pass



def update():
    entry_fname_1.get(),
    entry_lname_1.get(),
    entry_email_1.get(),
    entry_age_1.get(),
    cal_1.get(),
    entry_phone_1.get(),
    entry_adress_1.get(),
    formation_var_1.get(),

    global id
    print(id)
    c.execute("update userdatas set fname= ?,lname=? ,"
              "email= ?,age= ?,date_of_birth= ?,address=? "
                  ",phonenumber= ?,formation=? where id = ?",( entry_fname_1.get(),entry_lname_1.get(),entry_email_1.get(),entry_age_1.get(),cal_1.get(),
                                                                entry_phone_1.get(),entry_adress_1.get(), formation_var_1.get(),id))
    conn.commit()
    tree.delete(*tree.get_children())
    view_all_users()

#structur and layout
window = Tk()

window.title("Enregistrement Stagaire")
window.geometry("1020x510")

style = ttk.Style(window)
style.configure("lefttab.TNotebook",tabposition="wn")

#tab layout
tab_control = ttk.Notebook(window,style='lefttab.TNotebook')
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)
tab5 = ttk.Frame(tab_control)

#add tabs tp NoteBook
tab_control.add(tab1,text=f'{"Home":^24s}')
tab_control.add(tab2,text=f'{"View":^26s}')
tab_control.add(tab3,text=f'{"Search" :^25s}')
tab_control.add(tab4,text=f'{"Export":^26}')
tab_control.add(tab5,text=f'{"About":^25s}')
tab_control.pack(expand=1,fill="both")

create_table()



label1  =Label(tab1,text="Registartion Gui",padx=5,pady=5)
label1.grid(row=0,column=0)

label2  =Label(tab2,text="Registartion Gui",padx=5,pady=5)
label2.grid(row=0,column=0)

label3  =Label(tab3,text="Registartion Gui",padx=5,pady=5)
label3.grid(row=0,column=0)

label4  =Label(tab4,text="Registartion Gui",padx=5,pady=5)
label4.grid(row=0,column=0)

label5  =Label(tab5,text="Registartion Gui",padx=5,pady=5)
label5.grid(row=0,column=0)

# MAIN HOME

fname_raw_entry = StringVar()
l1 = Label(tab1,text="First Name",padx=5,pady=5)
l1.grid(row =1,column=0)
entry_fname=Entry(tab1,width=50,textvariable=fname_raw_entry)
entry_fname.grid(row=1,column=1)

lname_raw_entry = StringVar()
l2 = Label(tab1,text="Last Name",padx=5,pady=5)
l2.grid(row =2,column=0)
entry_lname=Entry(tab1,width=50,textvariable=lname_raw_entry)
entry_lname.grid(row=2,column=1)

email_raw_entry = StringVar()
l3 = Label(tab1,text="Email",padx=5,pady=5)
l3.grid(row =3,column=0)
entry_email=Entry(tab1,width=50,textvariable=email_raw_entry)
entry_email.grid(row=3,column=1)

raw_entry = IntVar()#  recuperer les donner dans une varibale (les donner saisie)
l4 = Label(tab1,text="Age",padx=5,pady=5)
l4.grid(row =4,column=0)
entry_age=Entry(tab1,width=50,textvariable=raw_entry)
entry_age.grid(row=4,column=1)

l5 =Label(tab1,text="Date of Birth",padx=5,pady=5)
l5.grid(row=5, column=0)

dob_raw_entery=StringVar()
cal = DateEntry(tab1,width=30, textvariable=dob_raw_entery, background='darkblue'
                ,foreground='white',borderwidth=2,year=2010)
cal.grid(row=5,column=1,padx=5,pady=5)

adress_raw_entry = StringVar()
l6 = Label(tab1,text="Adress",padx=5,pady=5)
l6.grid(row =6,column=0)
entry_adress=Entry(tab1,width=50,textvariable=adress_raw_entry)
entry_adress.grid(row=6,column=1)

phone_raw_entry = StringVar()
l7 = Label(tab1,text="Phone Number",padx=5,pady=5)
l7.grid(row =7,column=0)
entry_phone=Entry(tab1,width=50,textvariable=phone_raw_entry)
entry_phone.grid(row=7,column=1)

l7 = Label(tab1,text="Formation ",padx=5,pady=5)
l7.grid(row =8,column=0)
formation_var = StringVar()
formation_var.set("Python")
formation = OptionMenu(tab1, formation_var,"Python", "Java", "C++")
formation.grid(row=8, column=1)


#buttons


button1 = Button(tab1, text="Add", width=12,bg="#03A9F4", fg="#fff", command=add_detail)
button1.grid(row=10,column=0,padx=5, pady=5)

button2 = Button(tab1, text="Clear", width=12,bg="#03A9F4", fg="#fff", command=clear_text)
button2.grid(row=10,column=1,padx=5, pady=5)



#List BoX
elemnt_list = Listbox(tab1, height=8, width=87, border=0)
elemnt_list.grid(row=11, column=0, padx=20, columnspan=2)
#scrool bar
scrool = Scrollbar(tab1, width=19)
scrool.grid(row=11, column=3, ipady=10)
#mettre le scroolbar pour la list box
elemnt_list.configure(yscrollcommand=scrool)
scrool.configure(command=elemnt_list.yview())

button3 = Button(tab1, text="Clear Result", width=12,bg="#03A9F4", fg="#fff", command=clear_display_result)
button3.grid(row=12,column=1,padx=10, pady=10)
fname_raw_entry = StringVar()
l1 = Label(tab1,text="First Name",padx=5,pady=5)
l1.grid(row =1,column=0)
entry_fname=Entry(tab1,width=50,textvariable=fname_raw_entry)
entry_fname.grid(row=1,column=1)

lname_raw_entry = StringVar()
l2 = Label(tab1,text="Last Name",padx=5,pady=5)
l2.grid(row =2,column=0)
entry_lname=Entry(tab1,width=50,textvariable=lname_raw_entry)
entry_lname.grid(row=2,column=1)

email_raw_entry = StringVar()
l3 = Label(tab1,text="Email",padx=5,pady=5)
l3.grid(row =3,column=0)
entry_email=Entry(tab1,width=50,textvariable=email_raw_entry)
entry_email.grid(row=3,column=1)

raw_entry = IntVar()#  recuperer les donner dans une varibale (les donner saisie)
l4 = Label(tab1,text="Age",padx=5,pady=5)
l4.grid(row =4,column=0)
entry_age=Entry(tab1,width=50,textvariable=raw_entry)
entry_age.grid(row=4,column=1)

l5 =Label(tab1,text="Date of Birth",padx=5,pady=5)
l5.grid(row=5, column=0)

dob_raw_entery=StringVar()
cal = DateEntry(tab1,width=30, textvariable=dob_raw_entery, background='darkblue'
                ,foreground='white',borderwidth=2,year=2010)
cal.grid(row=5,column=1,padx=5,pady=5)

adress_raw_entry = StringVar()
l6 = Label(tab1,text="Adress",padx=5,pady=5)
l6.grid(row =6,column=0)
entry_adress=Entry(tab1,width=50,textvariable=adress_raw_entry)
entry_adress.grid(row=6,column=1)

phone_raw_entry = StringVar()
l7 = Label(tab1,text="Phone Number",padx=5,pady=5)
l7.grid(row =7,column=0)
entry_phone=Entry(tab1,width=50,textvariable=phone_raw_entry)
entry_phone.grid(row=7,column=1)

l7 = Label(tab1,text="Formation ",padx=5,pady=5)
l7.grid(row =8,column=0)
formation_var = StringVar()
formation_var.set("Python")
formation = OptionMenu(tab1, formation_var,"Python", "Java", "C++")
formation.grid(row=8, column=1)


#buttons
button1 = Button(tab1, text="Add", width=12,bg="#03A9F4", fg="#fff", command=add_detail)
button1.grid(row=10,column=0,padx=5, pady=5)

button2 = Button(tab1, text="Clear", width=12,bg="#03A9F4", fg="#fff", command=clear_text)
button2.grid(row=10,column=1,padx=5, pady=5)



#List BoX
elemnt_list = Listbox(tab1, height=8, width=87, border=0)
elemnt_list.grid(row=11, column=0, padx=20, columnspan=2)
#scrool bar
scrool = Scrollbar(tab1, width=19)
scrool.grid(row=11, column=3, ipady=10)
#mettre le scroolbar pour la list box
elemnt_list.configure(yscrollcommand=scrool)
scrool.configure(command=elemnt_list.yview())

button3 = Button(tab1, text="Clear Result", width=12,bg="#03A9F4", fg="#fff", command=clear_display_result)
button3.grid(row=12,column=1,padx=10, pady=10)


#VIEW

def si(event):
    global item
    item = tree.item(tree.selection())
    print(item)
    print(tree.selection()[0])
    s= tree.selection()[0]
    print(s[3])

def ss():
    tree.detach(tree.selection()[1])







#############################   view ##################
fname_raw_entry_1 = StringVar()
l1_1 = Label(tab2,text="First Name",padx=5,pady=5)
l1_1.grid(row =1,column=0)
entry_fname_1=Entry(tab2,width=50,textvariable=fname_raw_entry_1)
entry_fname_1.grid(row=1,column=1)

lname_raw_entry_1 = StringVar()
l2_1 = Label(tab2,text="Last Name",padx=5,pady=5)
l2_1.grid(row =2,column=0)
entry_lname_1=Entry(tab2,width=50,textvariable=lname_raw_entry_1)
entry_lname_1.grid(row=2,column=1)

email_raw_entry_1 = StringVar()
l3_1 = Label(tab2,text="Email",padx=5,pady=5)
l3_1.grid(row =3,column=0)
entry_email_1=Entry(tab2,width=50,textvariable=email_raw_entry_1)
entry_email_1.grid(row=3,column=1)

raw_entry_1 = IntVar()#  recuperer les donner dans une varibale (les donner saisie)
l4_1 = Label(tab2,text="Age",padx=5,pady=5)
l4_1.grid(row =4,column=0)
entry_age_1=Entry(tab2,width=50,textvariable=raw_entry_1)
entry_age_1.grid(row=4,column=1)

l5_1 =Label(tab2,text="Date of Birth",padx=5,pady=5)
l5_1.grid(row=5, column=0)

dob_raw_entery_1=StringVar()
cal_1 = DateEntry(tab2,width=30, textvariable=dob_raw_entery_1, background='darkblue'
                ,foreground='white',borderwidth=2,year=2010)
cal_1.grid(row=5,column=1,padx=5,pady=5)

adress_raw_entry_1 = StringVar()
l6_1 = Label(tab2,text="Adress",padx=5,pady=5)
l6_1.grid(row =6,column=0)
entry_adress_1=Entry(tab2,width=50,textvariable=adress_raw_entry_1)
entry_adress_1.grid(row=6,column=1)

phone_raw_entry_1 = StringVar()
l7_1 = Label(tab2,text="Phone Number",padx=5,pady=5)
l7_1.grid(row =7,column=0)
entry_phone_1=Entry(tab2,width=50,textvariable=phone_raw_entry_1)
entry_phone_1.grid(row=7,column=1)

l7_1 = Label(tab2,text="Formation ",padx=5,pady=5)
l7_1.grid(row=8, column=0)
formation_var_1 = StringVar()
formation_var_1.set("Python")
formation_1 = OptionMenu(tab2, formation_var_1,"Python", "Java", "C++")
formation_1.grid(row=8, column=1)

button_view2 = Button(tab2, text="View ALL", width=12, bg="#03A9F4", fg="#fff", command=view_all_users)
button_view2.grid(row=9, column=0, padx=10, pady=10)
tree = ttk.Treeview(tab2, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8", "column9"), show="headings")
tree.heading("#1", text="ID")
tree.column("#1", minwidth=0, width=100)
tree.heading("#2", text="First Name")
tree.column("#2", minwidth=0, width=100)
tree.heading("#3", text="Last Name")
tree.column("#3", minwidth=0, width=100)
tree.heading("#4", text="Email")
tree.column("#4", minwidth=0, width=100)
tree.heading("#5", text="Age")
tree.column("#5", minwidth=0, width=100)
tree.heading("#6", text="Date of Birth")
tree.column("#6", minwidth=0, width=100)
tree.heading("#7", text="Adresse")
tree.column("#7", minwidth=0, width=100)
tree.heading("#8", text="Phone Number")
tree.column("#8", minwidth=0, width=100)
tree.column("#9", minwidth=0, width=100)
tree.heading("#9", text="Formation")

tree.grid(row=10, column=0, columnspan=3, padx=5, pady=5)
tree.bind("<ButtonRelease-1>", get_current_selection)

img1 = ImageTk.PhotoImage(Image.open("D:/buttons_with_TKinter_and_Python/tuto_tkinter_new/icones/iconfinder_trash-delete-remove_2931168.png"))
button1 = Button(tab2, text="Remouve", width=20, bg="#03A9F4", fg="#fff", image=img1, border=0, command=remouve_item)
button1.grid(row=9, column=1, padx=5, pady=5)

button1 = Button(tab2, text="Update", width=12,bg="#03A9F4", fg="#fff", command=update)
button1.grid(row=9, column=2, padx=5, pady=5)


#SEARCH
label_search = Label(tab3, text="Search Name", padx=5, pady=5)
label_search.grid(row=1, column=0)


search_raw_entery = StringVar()
entry_search = Entry(tab3, textvariable=search_raw_entery, width=30)
entry_search.grid(row=1, column=1)

button_view3 = Button(tab3, text="Clear Search ", width=12, bg="#03A9F4", fg="#fff", command=clear_entered_search)
button_view3.grid(row=2, column=1, padx=10, pady=10)

button_view4 = Button(tab3, text="Clear Result", width=12, bg="#03A9F4", fg="#fff", command=clear_display_result)
button_view4.grid(row=2, column=2, padx=10, pady=10)

button_view5 = Button(tab3, text="Search", width=12, bg="#03A9F4", fg="#fff", command=search_user_by_name)
button_view5.grid(row=1, column=2, padx=10, pady=10)

tab2_display = ScrolledText(tab3, height=5)
#tab2_display = Listbox(tab2, height=5, width=60)
tab2_display.grid(row=10, column=0, pady=20, columnspan=3)

#EXPORT
#export to database
label1_export = Label(tab4, text="File Name", padx=5, pady=5)
label1_export.grid(row=2, column=0)

filname_raw_entry = StringVar()

entry_filename=Entry(tab4, width=50, textvariable=filname_raw_entry)
entry_filename.grid(row=2, column=1)

button_export1 = Button(tab4, text="To CSV", width=12, bg="#03A9F4", fg="#fff", command=export_as_csv)
button_export1.grid(row=3, column=1, padx=10, pady=10)




# ABOUT
about_label = Label(tab5, text="Registrio Guit V.0.0.1 \n Zidane saves \n zidane.aghouiles74@gmail.com", padx=5, pady=5)
about_label.grid(row=1, column=0)



"""
tree = ttk.Treeview(tab5,selectmode="extended",columns=("A","B"))
tree.heading("#0", text="C/C++ compiler")
tree.column("#0",minwidth=0,width=100)

tree.heading("A", text="A")
tree.column("A",minwidth=0,width=200)

tree.heading("B", text="B")
tree.column("B",minwidth=0,width=100)
tree.grid(row=6, column=0,pady=5,padx=5)

"""




window.mainloop()
