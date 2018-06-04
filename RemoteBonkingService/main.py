from tkinter import *
from dbo import *


def yur_is_clicked(event):
    print("yur is clicked")


def fiz_is_clicked(event):
    print("fiz is clicked")


def show_is_clicked(event):
    print("show is clicked")

root = Tk()

# Заголовок
title = Label(root)
title["text"] = "Брокер ДБО"
title["font"] = "roboto 24 bold"

post_title = Label(root, text="Система подбора банка, нужного Вам")
post_title["fg"] = "#73B3FF"
post_title["font"] = "roboto 15"

title.grid(row=0, padx=80, sticky=W)
post_title.grid(row=1, padx=80, sticky=W)

# Блок 1
question = Label(root)
question["text"] = "Пожалуйста, определите себя в одну из категорий"
question["font"] = "roboto 20"
question.grid(row=2, column=0, padx=80, pady=40)

button1 = Button(root, text='Физическое лицо', width=16, height=5, bg='white', fg='black', font='roboto 14')
button1.grid(row=4, pady=10)

button2 = Button(root, text='Юридическое лицо', width=16, height=5, bg='white', fg='black', font='roboto 14')
button2.grid(row=4, column=1, pady=10)

# Блок 2
#question2 = Label(root)
#question2["text"] = "Выберите защиту"
#question2["font"] = "roboto 20"
#question2.grid(row=5, pady=40)

#button_standart = Button(root, text='Стандартная защищенность', width=22, height=5, bg='white', fg='black', font='roboto 14')
#button_standart.grid(column=0, row=9, padx=20, pady=10)

#button_high = Button(root, text='Высокая защищенность', width=20, height=5, bg='white', fg='black', font='roboto 14')
#button_high.grid(column=1, row=9, padx=20, pady=10)


service_label = Label(root, text="Выберите сервис: ")
entry_service = Entry(root)

security_label = Label(root, text="Важен ли вам уровень безопасности? ")
entry_security = Entry(root)

price_label = Label(root, text="Сколько вы могли бы потратить на обслуживание? ")
entry_price = Entry(root)

support_label = Label(root, text="Нужно ли вам круглосуточное обслуживание? ")
entry_support = Entry(root)

service_label.grid(row=5, column=0, sticky=W)
security_label.grid(row=6, column=0, sticky=W)
price_label.grid(row=7, column=0, sticky=W)
support_label.grid(row=8, column=0, sticky=W)

entry_service.grid(row=5, column=1, sticky=W)
entry_security.grid(row=6, column=1, sticky=W)
entry_price.grid(row=7, column=1, sticky=W)
entry_support.grid(row=8, column=1, sticky=W)


show_result_button = Button(root, text="Показать результат", width=18, height=2, bg="blue", fg="white", font="roboto 12")
show_result_button.grid(column=0, row=11)

button1.bind("<Button-1>", fiz_is_clicked)
button2.bind("<Button-1>", yur_is_clicked)
show_result_button.bind("<Button-1>", show_is_clicked)

data_fiz = pd.read_excel('fiz.xlsx')
data_yur = pd.read_excel('yur.xlsx')

service = entry_service.get()
security = entry_security.get()
price = entry_price.get()
support = entry_support.get()

if show_is_clicked and fiz_is_clicked:
    bank = str (choose_bank(data_fiz, service, security, price, support))
    result = Label(root, text=bank)

elif show_is_clicked and yur_is_clicked:
    bank = str(choose_bank(data_yur, service, security, price, support))
    result = Label(root, text=bank)

else:
    print("error")


root.mainloop()
