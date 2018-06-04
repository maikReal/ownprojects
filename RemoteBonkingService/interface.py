from tkinter import *
from dbo import *
from PIL import Image, ImageTk


def yur_is_clicked(event):
    print('qew')
    person['text'] = 'yur.xlsx'
    user['text'] = 'Юр. лицо'

    entry_service.delete(0, END)
    entry_support.delete(0, END)
    entry_price.delete(0, END)
    entry_security.delete(0, END)


def fiz_is_clicked(event):
    print('qwasd')
    person['text'] = 'fiz.xlsx'
    user['text'] = 'Физ. лицо'

    entry_service.delete(0, END)
    entry_support.delete(0, END)
    entry_price.delete(0, END)
    entry_security.delete(0, END)


def output(event):
    client = person['text']
    services = entry_service.get().split()
    security = entry_security.get().lower()
    price = int(entry_price.get())
    support = entry_support.get().lower()

    data = pd.read_excel(client)
    res = choose_bank(data, services, security, price, support)

    result['text'] = res



file = 'no'

root = Tk()
root.geometry('800x600')
root.resizable(width=False, height=False)
# Заголовок
title = Label(root, text="Брокер ДБО")

title["font"] = "Montserrat 26 bold"
title.pack(fill=X)

post_title = Label(root, text='Система подбора банка, нужного Вам')
post_title["fg"] = "#73B3FF"
post_title["font"] = 'Montserrat 17 bold'
post_title.pack(fill=X)

img = Image.open('img/line.png')
render = ImageTk.PhotoImage(img)
empty_filed = Label(root, image=render, width=200, height=20)
empty_filed.pack()

# Block 1
question = Label(root, text='Пожалуйста, определите себя в одну из категорий')
question["font"] = "Montserrat 20"
question.pack(fill=X)

button1 = Button(root, text='Физическое лицо', width=16, bg='white', fg='black', font='Montserrat 16')
button1.place(x=100, y=140)

user = Label(root, font='Montserrat 16')
user.place(x=355, y=140)

button2 = Button(root, text='Юридическое лицо', width=16, bg='white', fg='black', font='Montserrat 16')
button2.place(x=510, y=140)

person = Label(root, font='Montserrat 16')
button1.bind('<Button-1>', fiz_is_clicked)
button2.bind('<Button-1>', yur_is_clicked)

# Block 2
service_label = Label(root, text="Выберите услуги: ", font='Montserrat 20')
entry_service = Entry(root, font='Montserrat 16')
service_label.place(x=135, y=200)
entry_service.place(x=470, y=200)

security_label = Label(root, font='Montserrat 20')
security_label['text'] = 'Важен ли вам' + '\n' + 'уровень безопасности?'
entry_security = Entry(root, font='Montserrat 16')
security_label.place(x=105, y=240)
entry_security.place(x=470, y=265)

price_label = Label(root, font='Montserrat 20')
price_label['text'] = 'Сколько вы могли бы' + '\n' + 'потратить на обслуживание?'
entry_price = Entry(root, font='Montserrat 16')
price_label.place(x=80, y=300)
entry_price.place(x=470, y=325)

support_label = Label(root, text="Нужно ли вам круглосуточное обслуживание? ", font='Montserrat 20')
support_label['text'] = 'Нужно ли вам' + '\n' + 'круглосуточное обслуживание?'
entry_support = Entry(root, font='Montserrat 16')
support_label.place(x=70, y=360)
entry_support.place(x=470, y=385)

# Block 3
show_result_button = Button(root, text="Показать результат", width=18, height=2,
                            bg="blue", fg="white", font="Montserrat 16")
show_result_button.place(x=100, y=480)

result = Label(root, font="Montserrat 16")
result.place(x=440, y=495)

show_result_button.bind('<Button-1>', output)

root.mainloop()
