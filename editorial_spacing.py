from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import re
import requests
from bs4 import BeautifulSoup

BLACKLIST = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head',
    'input',
    'script',
    'style'
]
WORDS = re.compile(r'\W+')


file_name = []
url_path = [];

file_name.append('')
url_path.append('')


def get_filename():
    global file_name
    file_name[0] = filedialog.askopenfilename(filetypes=(("HTML files", "*.html"),))
    url_path[0] = ''

def get_url():
    global file_name 
    global url_path
    file_name[0] = ''
    url_path[0] = url_input.get()

def get_text_by_url():
    addr = str(url_path[0])
    res = requests.get(addr)
    return get_text(res.content)

def get_text_by_file():
    file = open(file_name[0], 'r')
    return get_text(file)

def try_get_text():
    if file_name[0] != '':
         return get_text_by_file()
    elif url_path[0]!= '':
        return get_text_by_url()

def get_text(url):
    html_page = url
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    output = ''
    for t in text:
        if t.parent.name not in BLACKLIST:
            output += '{} '.format(t)

    output = ' '.join(output.split())
    return WORDS.split(output)


def distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

def run():
    if file_name[0] != '' or url_path[0] != '':
        incorrect_word = user_input_text.get()#(1.0, END)
        incorrect_word = incorrect_word.replace('\n', '')
        count_errors = user_input_error.get()#(1.0, END)
        count_errors = count_errors.replace('\n', '')
        if count_errors != '' and incorrect_word != '':
            list_box.delete(0, END)
            all_words = try_get_text()
            list_word = all_words
            dict_words_and_errors = {}
            for word in list_word:
                errors = distance(incorrect_word.lower(), word.lower())
                dict_words_and_errors.update({word: errors})
            list_with_tuple = list(dict_words_and_errors.items())
            list_with_tuple.sort(key=lambda i: i[1])
            for word in list_with_tuple[::-1]:
                if int(word[1]) < int(count_errors) + 1:
                    list_box.insert(0, str(word[0]) + ' ' + str(word[1]))


def info():
    messagebox.askquestion("Help", "1. Открыть html файл с правильными словами или ввести url адрес сайта и нажать на кноку `Загрузить по url`.\n"
                                   "2. Написать в первой строке неправильное слово.\n"
                                   "3. Написать во второй строке количество допустимых ошибок.\n"
                                   "4. Снизу увидите упорядоченный список с вариантами.", type='ok')


# user interface
#
#
#

root = Tk()
root.title("Lab 2")
root.resizable(width=True, height=True)
root.geometry("580x250+300+300")

label_url = Label(root, text ='Введите url')
label_url.grid(row=1, column=0)
url_input = Entry(root,width=40)
url_input.grid(row=1, column=1, sticky='nsew', columnspan=3)

url_btn = Button(text="Загрузить по url", command=get_url)
url_btn.grid(row=1, column=4)

label = Label(root, text='Введите слово:')
label.grid(row=2, column=0)
user_input_text =  Entry(root,width=20)
user_input_text.grid(row=2, column=1, sticky='nsew', columnspan=3)

label2 = Label(root, text='Введите кол-во ошибок:')
label2.grid(row=3, column=0)
user_input_error =  Entry(root,width=5)
user_input_error.grid(row=3, column=1, sticky='nsew', columnspan=3)

run_btn = Button(text="Запуск", command=run)
run_btn.grid(row=4, column=1)

open_file_btn = Button(text="Открыть файл", command=get_filename)
open_file_btn.grid(row=4, column=2)

help_btn = Button(text="Помощь?", command=info)
help_btn.grid(row=2, column=4)

list_box = Listbox(root, height=10, width=65)
scrollbar = Scrollbar(root, command=list_box.yview)
scrollbar.grid(row=5, column=4, sticky='nsew')
list_box.grid(row=5, column=0, sticky='nsew', columnspan=3)
list_box.configure(yscrollcommand=scrollbar.set)


root.mainloop()
