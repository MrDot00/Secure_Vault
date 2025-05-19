import base64
import json
import tkinter
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
import sys
import subprocess
try:
    from cryptography.fernet import Fernet
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
from cryptography.fernet import Fernet

name=''
pas=''
mail=''
Key=''
switch=0
n = ''

def switch_frames():
    page.pack_forget()
    pagee.pack()
    profile()

def save_files():
    files = filedialog.askopenfilenames()
    if len(files)!=0:
        Encrypt(files)
    with open (name+'.txt','w') as f:
        for file in files:
            f.write(file+'\n')
    show_files()


def load_file_names():
    global name
    try:
        with open(name+'.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def show_files():
    global name
    files=load_file_names()

    text_box.delete(0, tkinter.END)
    if len(files) ==0:
        text_box.insert(tkinter.END, "Nothing to see here")
    else:
        for file in files:
            text_box.insert(tkinter.END,file+'\n')


def delete_selected():
    files=load_file_names()
    selected_indices = text_box.curselection()
    if selected_indices:
        # Remove items from both the list and the Listbox
        for index in reversed(selected_indices):
            text_box.delete(index)
            Decrypt(files[index])
            del files[index]
        with open(name + '.txt', 'w') as f:
            for file in files:
                f.write(file + '\n')
        show_files()


def save():
    global name,pas,mail,Key
    name=UserN_e.get()
    pas=pass_e.get()
    mail=mail_e.get()
    if name=='' or pas=='' or mail=='':
        messagebox.showerror(title='Error',message='Insufficient Data')
        return
    key=Fernet.generate_key()
    Key=key
    e_key=base64.b64encode(key).decode('utf-8')
    e_mail=base64.b64encode(mail.encode('utf-8'))
    e_mail= e_mail.decode()
    e_pas=Fernet(key).encrypt(pas.encode('utf-8'))
    e_pas=e_pas.decode()
    user_data = [{"u": name, "p": e_pas, "m": e_mail, 'y': e_key}]

    try:
        with open("inFo.txt", 'r') as file:
            try:
                existing_data = json.load(file)
                for x in existing_data:
                    if x["u"] == name:
                        messagebox.showerror(title='Error',message='This Username has been used')
                        return 

            except json.decoder.JSONDecodeError:
                existing_data = []

    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list
        existing_data = []

    # Append the new data (not as a list)
    existing_data.append(user_data[0])

    # Write the updated data back to the file
    with open("inFo.txt", 'w') as file:
        json.dump(existing_data, file)
    messagebox.showinfo(title='Success',message='You have successfully Created an Id..!!')
    switch_frames()
    


def loginC():
    global name,pas,switch, Key,Mail
    name=UserN_e.get()
    pas=pass_e.get()

    try:
        with open("inFo.txt", 'r') as file:
            try:
                usr_data = json.load(file)
            except json.decoder.JSONDecodeError:
                messagebox.showerror(title='Error',message='Try Register First..!')
                return
    except FileNotFoundError:
        messagebox.showerror(title='Error', message='Try Register First..!')
        return

    signal=0
    for n in usr_data:
        if n['u'] == name:
            paswd=n['p']
            key=n['y']

            signal=0
            break
        else:
            signal=1    
    if signal==1:
        messagebox.showinfo(title='Incorrect',message='Your User name is Incorrect..!!')
        return
    key=base64.b64decode(key.encode('utf-8'))
    Key=key
    paswd=Fernet(key).decrypt(paswd.encode('utf-8'))
    if paswd.decode() == pas:
        messagebox.showinfo(title='Success',message='Logged in Successfully..!!')
        switch_frames()

    else:
        messagebox.showinfo(title='Incorrect',message='Your Password is Incorrect..!!')


def user_data():
    try:
        with open("inFo.txt", 'r') as file:
            try:
                usr_data = json.load(file)
                return usr_data
            except json.decoder.JSONDecodeError:
                messagebox.showerror(title='Error',message='Try Register First..!')
                return
    except FileNotFoundError:
        messagebox.showerror(title='Error', message='Try Register First..!')
        return



def f_pass():
    result = simpledialog.askstring("Input", "Enter Your E Mail here")
    result=base64.b64encode(result.encode()).decode()

    usr_data=user_data()

    signal=0
    for n in usr_data:
        if n['m'] == result:
            usr_name=n['u']
            usr_pas=n['p']
            key=n['y']
            key = base64.b64decode(key.encode('utf-8'))
            usr_pas = Fernet(key).decrypt(usr_pas.encode('utf-8')).decode()
            messagebox.showinfo(title=usr_name, message='Your Pass Is ==>  ' + usr_pas)
            signal=0
            break
        else:
            signal=1
    if signal==1:
        messagebox.showinfo(title='Incorrect',message='Your Email is Incorrect..!!')
        return


def switchUP():
    level.title("Registration")
    login_l.config(text='Registration')
    login_b.config(text='Register',command=save)

    mail_l.grid(row=3,column=0,pady=20,padx=5)
    mail_e.grid(row=3,column=1)

    switch_l.config(text='Have an account?')
    switch_b.config(text='Switch to Log In',command=switchIN)

def switchIN():
    level.title('Login')
    login_l.config(text='Log In')
    login_b.config(text='Log in',command=loginC)
    mail_l.grid_forget()
    mail_e.grid_forget()
    switch_l.config(text='Don\'t have ave an account?')
    switch_b.config(text='Switch to Registration',command=switchUP)

def name_b():
    name_z=tkinter.Toplevel(pagee)
    name_z.title(name)
    name_z.geometry('300x200')

    l=tkinter.Label(name_z,text='Customize your Account')
    l.grid(row=1,column=1,pady=10)
    change_name_b=tkinter.Button(name_z,text='Change Name',command=chage_u)
    change_name_b.grid(row=2,column=1)
    change_pass_b=tkinter.Button(name_z,text='Change Password',command=chage_p)
    change_pass_b.grid(row=3,column=1)
    change_mail_b=tkinter.Button(name_z,text='Change Email',command=change_m)
    change_mail_b.grid(row=4,column=1)

def load_data():
    with open('inFo.txt','r') as f:
        return json.load(f)
def chage_u():
     data=load_data()

     for x in data:
         if x['u']==name:
             x['u']=simpledialog.askstring("Name", "New name")
             with open('inFo.txt','w') as f:
                 json.dump(data,f)
         messagebox.showinfo(title='Success', message='Name changed successfully')
         return

def chage_p():

    data=load_data()

    for x in data:
        if x['u']==name:
             usr_pass=simpledialog.askstring("Password", "New password")
             usr_pass=Fernet(Key).encrypt(usr_pass.encode()).decode()
             x['p']=usr_pass
             with open('inFo.txt','w') as f:
                 json.dump(data,f)
             messagebox.showinfo(title='Success',message='Password changed successfully')
             return

def change_m():
    data = load_data()

    for x in data:
        if x['u'] == name:
            usr_m = simpledialog.askstring("Email", "New mail")
            usr_m = base64.b64encode(usr_m.encode()).decode()
            x['m'] = usr_m
            with open('inFo.txt', 'w') as f:
                json.dump(data, f)
            messagebox.showinfo(title='Success', message='Email changed successfully')
            return


def profile():
    level.title('Profile')
    level.configure(bg='#6C6C6F')
    level.geometry('700x600')
    head_l = tkinter.Label(pagee, text='Profile', font=('Arial', 30),bg='#6C6C6F',fg='#07E9FC')
    head_l.grid(row=0, column=2, padx=40)

    head_b = tkinter.Button(pagee, text=name,command=name_b,bg='#6C6C6F',fg='#AFFEF2')
    head_b.grid(row=0, column=3, padx=40)

    files_l = tkinter.Label(pagee, text='Secured Files',bg='#6C6C6F',fg='#07B5FC')
    files_l.grid(row=1, column=1, pady=20)

    global text_box
    text_box = tkinter.Listbox(pagee, height=20, width=50, selectmode=tkinter.MULTIPLE,bg='#DBDBE4')
    text_box.grid(row=1, column=2, padx=20)
    show_files()

    add_files_b = tkinter.Button(pagee, text='Add Files?', command=save_files,bg='#6C6C6F',fg='#AFFEF2')
    add_files_b.grid(row=2, column=2)

    delete_button = tkinter.Button(pagee, text="Delete Selected", command=delete_selected,bg='#7B7BB6',fg='#AFFEF2')
    delete_button.grid(row=1, column=3,padx=20,pady=20)






def Encrypt(files):

    if len(files) == 0:
        return
    for file in files:
        with open(file, "rb") as CON:
            context = CON.read()
        context = Fernet(Key).encrypt(context)
        with open(file, "wb") as f:
            f.write(context)
def Decrypt(file):
    with open(file,"rb") as CON:
        context = CON.read()
    context = Fernet(Key).decrypt(context)
    with open(file, "wb") as f:
        f.write(context)


level=tkinter.Tk()
level.geometry("700x500")
level.configure(bg='#595E64')
level.title("Login")

page=tkinter.Frame(level,bg='#595E64')
page.pack()

login_l=tkinter.Label(page,text='Log In',bg='#595E64', fg= '#8BBEFB', font=('Ariral',30))
login_l.grid(row=0, column=0, columnspan=2,pady=20)

UserN_l=tkinter.Label(page,text='User Name :',bg='#595E64', fg= '#FEAD66',font=('Arial',15))
UserN_l.grid(row=1,column=0,pady=20,padx=5)
UserN_e=tkinter.Entry(page)
UserN_e.grid(row=1,column=1)

pass_l=tkinter.Label(page,text='Password : ',bg='#595E64', fg= '#FEAD66',font=('Arial',15))
pass_l.grid(row=2,column=0,pady=20,padx=5)
pass_e=tkinter.Entry(page,show='#')
pass_e.grid(row=2, column=1)


login_b=tkinter.Button(page,text='Login',fg='#9BF3FA',command=loginC,bg='#595E64',activeforeground='#2249F7',font=('Arial',15))
login_b.grid(row=4,column=0,columnspan=2)

mail_l=tkinter.Label(page,text='Mail Address :',bg='#595E64', fg= '#FEAD66',font=('Arial',15))

mail_e=tkinter.Entry(page)



switch_l=tkinter.Label(page,text='Dont ave an accunt?',bg='#595E64', fg= '#9EC9FC',font=('Arial',10))
switch_l.grid(row=6,column=0)

switch_b=tkinter.Button(page,text='Switch to Sing Up',fg='#9EC9FC',command=switchUP,bg='#595E64',activeforeground='#595E64',font=('Arial',10))
switch_b.grid(row=6,column=1,pady=10)

forget_b=tkinter.Button(page,text='Forget Password?',bg='#595E64',fg='#FFFFFF',font=('Arial',10),command=f_pass)
forget_b.grid(row=7,column=0,padx=10,columnspan=2)

pagee = tkinter.Frame(level,bg='#6C6C6F')
pagee.pack()


print(name)

level.mainloop()
