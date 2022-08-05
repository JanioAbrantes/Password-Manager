from tkinter import *
from tkinter import messagebox
from random import choice
from string import ascii_letters, punctuation, digits
import pyperclip  # Biblioteca legal pra copiar o texto que tu gerar
import json

FONTE_LABEL = ('Verdana', 12, 'bold')
FONTE_TXT = ('Verdana', 10, 'normal')
TIPOS = [ascii_letters, punctuation, digits]
BASE_MAIL = ''


# ------------------------------- DATA SEARCH  ---------------------------------- #
def search():
    site_name = website_text.get()
    try:
        with open('my_secrets.json', mode='r') as data_file:
            dados = json.load(data_file)
            messagebox.showinfo(title=site_name, message=f'User: {dados[site_name]["user"]}\n'
                                                         f'Pass: {dados[site_name]["segredo"]}')
    except KeyError or FileNotFoundError:
        messagebox.showinfo(title='Nops', message=f'{site_name} não encontrado')


# ------------------------------- DATA RESET ------------------------------------ #
def reset():
    website_text.delete(0, END)
    email_text.delete(0, END)
    pass_text.delete(0, END)

    email_text.insert(0, BASE_MAIL)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    random_pass = []
    for _ in range(15):
        caracter = choice(TIPOS)
        random_pass.append(choice(caracter))

    pass_text.delete(0, END)
    pass_text.insert(0, ''.join(random_pass))


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    site_name = website_text.get()
    user_name = email_text.get()
    pass_name = pass_text.get()
    new_data = {
        site_name: {
            'user': user_name,
            'segredo': pass_name,
        }
    }
    pyperclip.copy(pass_name)

    if site_name.strip() == '' or user_name.strip() == '' or pass_name.strip() == '':
        messagebox.showinfo(title='Nops', message='Por favor, preencha os 3 campos')
        return

    is_ok = messagebox.askokcancel(title=site_name, message=f'User: {user_name}\n'
                                                            f'pass: {pass_name}\n'
                                                            f'Press OK to save')
    if is_ok:
        try:
            with open('my_secrets.json', mode='r') as data_file:
                # Lendo o arquivo antigo com mode=r
                data = json.load(data_file)
                # Agora dando update no antigo com o novo
                data.update(new_data)

            with open('my_secrets.json', mode='w') as data_file:
                # Agora escrever, com o modo w
                json.dump(data, data_file, indent=4)  # O indent é pra ficar mais bonitinho

        except FileNotFoundError:
            with open('my_secrets.json', mode='w') as data_file:
                # Caso o arquivo não exista, basta criar
                json.dump(new_data, data_file, indent=4)


# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title('Salvador de ******')
root.config(padx=50, pady=50, bg='#69DADB')
root.minsize(width=400, height=300)

# Setting the image
canvas = Canvas(height=200, width=200, bg='#69DADB', highlightthickness=0)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Setting the Labels
website_label = Label(text='Website:', font=FONTE_LABEL, bg='#69DADB', highlightthickness=0)
email_label = Label(text='Email/Username:', font=FONTE_LABEL, bg='#69DADB', highlightthickness=0)
password_label = Label(text='Password:', font=FONTE_LABEL, bg='#69DADB', highlightthickness=0)

website_label.grid(row=1, column=0)
email_label.grid(row=2, column=0)
password_label.grid(row=3, column=0)

# Setting the Buttons
search_button = Button(text='Search', font=FONTE_TXT, command=search)
reset_button = Button(text='Reset', font=FONTE_TXT, command=reset)
generate_button = Button(text='Generate Password', font=FONTE_TXT, command=generate_password)
add_button = Button(text='Add', font=FONTE_TXT, command=save_password)

search_button.grid(row=1, column=2)
reset_button.grid(row=2, column=2)
generate_button.grid(row=3, column=2)
add_button.grid(row=4, column=1)

search_button.config(width=16)
reset_button.config(width=16)
add_button.config(width=16)

# Setting the Text Areas
website_text = Entry(width=42, font=FONTE_TXT)
email_text = Entry(width=42, font=FONTE_TXT)
pass_text = Entry(width=42, font=FONTE_TXT)

website_text.grid(row=1, column=1, pady=10)
email_text.grid(row=2, column=1)
pass_text.grid(row=3, column=1, pady=10, padx=5)
website_text.focus()
email_text.insert(0, BASE_MAIL)

root.mainloop()
