import sys
import os
import pandas as pd
from tkinter.messagebox import showerror, showinfo
import tkinter as tk
from tkinter import ttk
import random

name_atribute = ['ФИО', 'Паспортные данные', 'Откуда', 'Куда', 'Дата отъезда', 'Дата приезда', 'Рейс', 'Выбор вагона и места', 'Стоимость (руб)', 'Карта оплаты']
dict_include_column = dict()
include_quasi = [0]*10
name_input_file = ""
name_output_file = ""
dataset = pd.DataFrame({'A': [1]})
depersonalization_dataset = pd.DataFrame({'A': [1]})

def search_wrong()->bool:
    if name_input_file == "" or name_output_file == "":
        showerror(title="ошибка", message="некорректное имя файла ввода или вывода")
        return False
    k = 0
    for line in name_check_button:
        include_quasi[k] = dict_include_column[line].get()
        k += 1
    if sum(include_quasi)== 0:
        showerror(title="ошибка", message="нет данных о квази идентификаторов")
        return False
    return True
    
def open_file()->None:
    global dataset
    if not os.path.isfile(name_input_file + ".xlsx"):
        showerror(title="ошибка", message="файл не найден")
        return
    if dataset.shape == (1, 1):
        dataset = pd.read_excel(name_input_file + ".xlsx", sheet_name='Sheet1')
        
def dict_generation_checkbutton(array_name)->dict:
    this_dict = dict()
    for line in array_name:
        this_dict[line] = tk.IntVar()
    return this_dict

def autor()->None:
    showinfo(title="я", message="самый лучший человек на свете")
    
def safe()->None:
    global name_input_file, name_output_file
    name_input_file = file_name.get()
    name_output_file = save_file_name.get()
    good_parameters = search_wrong()
    if not good_parameters:
        return
    showinfo(title="Успешный успех", message = "данные обновлены")
    
def no_good_k_anonimity_top()->None:
    good_parameters = search_wrong()
    if not good_parameters:
        return
    global dataset, name_atribute
    open_file()
    dataset_key = list()
    for i in range(len(include_quasi)):
        if include_quasi[i]: dataset_key.append(name_atribute[i])
    dataset.sort_values(dataset_key)
    groups_dataset = dataset.groupby(dataset_key)
    k_anonimity = set()
    for group in groups_dataset:
        k_anonimity.add(len(group[1]))
        if len(group[1]) == 1: print(group[0])
    k_anonimity = list(k_anonimity)
    k_anonimity.sort()
    k_anonimity_good = 0
    if len(dataset) <= 51000: k_anonimity_good = 10
    elif len(dataset) <= 105000: k_anonimity_good = 7
    elif len(dataset) <= 26000: k_anonimity_good = 5
    else: k = 1 
    showinfo(title="k-anonimity", message=f"k-anonimity = {k_anonimity[0]}, необходимое k-anonimity = {k_anonimity_good}")
    for i in range(5):
        if len(k_anonimity) == i:
            break
        bad_k_anonimity[i]["text"] = f"{str(i + 1)}.{str(k_anonimity[i])} ({str(k_anonimity[i] / len(dataset))})" 
    showinfo(title="Успешный успех", message = "k anonymity рассчитано, обновлен топ")
    
def delete_atribute(atribute):
    global depersonalization_dataset
    if atribute == 'Паспортные данные':
        depersonalization_dataset.drop(atribute, axis=1)

def masketization(atribute):
    global depersonalization_dataset
    num = len(depersonalization_dataset.loc[0, atribute])
    if atribute == "Паспортные данные":
        for i in range(len(depersonalization_dataset)):
            depersonalization_dataset.loc[i, atribute] = 'X' * 4 + ' ' + 'X' * (num - 4 - 1)
    if atribute == "Карта оплаты":
         for i in range(len(depersonalization_dataset)):
             line = depersonalization_dataset.loc[i, atribute]
             depersonalization_dataset.loc[i, atribute] = 'X' * 4 + ' ' + 'X' * (num - 4 - 1)

def micro_agregation(atribute):
    if atribute == "Стоимость (руб)":
        num_place = dict()
        sum_price_place = dict()
        names_trains = set()
        index_element = dict()
        for i in range(len(depersonalization_dataset)):
            name_train = dataset.loc[i, 'Рейс']
            if not name_train in names_trains:
                names_trains.add(name_train)
                num_place[name_train] = 0
                sum_price_place[name_train] = 0
                index_element[name_train] = []
            num_place[name_train] += 1
            sum_price_place[name_train] += int(dataset.loc[i, atribute])
            index_element[name_train].append(i)
        for name_train, index_name_train in index_element.items():
            for k in index_name_train:
                price = round(sum_price_place[name_train] / num_place[name_train])
                depersonalization_dataset.loc[k, atribute] = str(price)
             

def outrage(atribute):
    global depersonalization_dataset
    if atribute == 'Дата отъезда' or atribute == 'Дата приезда':
        for i in range(len(depersonalization_dataset)):
            line = depersonalization_dataset.loc[i, atribute]
            months = line[line.find("-") + 1:line.rfind("-")]
            print(months)
            if int(months) <= 3: months = "Зима"
            elif int(months) <= 6: months = "Весна"
            elif int(months) <= 9: months = "Лето"
            elif int(months) <= 12: months = "Осень"
            line = line[:line.find("-")]
            depersonalization_dataset.loc[i, atribute] = line + "," + months    
        

def local_generalization(atribute):
    global depersonalization_dataset
    if atribute == 'ФИО':
        for i in range(len(depersonalization_dataset)):
            line = depersonalization_dataset.loc[i, atribute]
            if line[0] == " ":
                while line[0] == " ":
                    line = line[1:]
                    
            line = line[:line.find(" ")]
            if line[-1] == "а":
                depersonalization_dataset.loc[i, atribute] = "женский"
            else:
                depersonalization_dataset.loc[i, atribute] = "мужской"
        depersonalization_dataset.rename(columns={atribute:"Пол"}, inplace=True)
    elif atribute == 'Куда' or atribute == 'Откуда':
        file = open("C:/home screen/programming/python/study on python\study/dataset/data/" +"city_with_region.txt", "r", encoding="utf-8")
        city_region = dict()
        for line in file:
            city = line[:line.find(",")]
            region = line[line.find(",") + 1:-1]
            city_region[city] = region
        file.close()
        for i in range(len(depersonalization_dataset)):
            line = depersonalization_dataset.loc[i, atribute]
            depersonalization_dataset.loc[i, atribute] = city_region[line]
    elif atribute == 'Рейс':
        for i in range(len(depersonalization_dataset)):
            line = depersonalization_dataset.loc[i, atribute]
            num_train = int(line[:-1])
            if num_train <= 298: type_train = "Скорый"
            elif num_train <= 598: type_train = "Пассажирский"
            elif num_train <= 750: type_train = "скоростной"
            else: type_train = "Сверхскоростной"
            depersonalization_dataset.loc[i, atribute] = type_train
        depersonalization_dataset.rename(columns={atribute:"Тип поезда"}, inplace=True)
    elif atribute == 'Выбор вагона и места':
        max_num_vagon = dict()
        names_trains = set()
        index_element = dict()
        for i in range(len(dataset)):
            name_train = dataset.loc[i, "Рейс"]
            line = dataset.loc[i, atribute]
            num_vagon = int(line[:line.find("-")])
            if not name_train in names_trains:
                names_trains.add(name_train)
                index_element[name_train] = []
                max_num_vagon[name_train] = num_vagon
            if num_vagon > max_num_vagon[name_train]:
                max_num_vagon[name_train] = num_vagon
            index_element[name_train].append(i)
        for name_train, array_index in index_element.items():
            low = round(max_num_vagon[name_train] / 3)
            normally = low * 2
            high = max_num_vagon[name_train]
            for k in array_index:
                line = depersonalization_dataset.loc[k, atribute]
                num_vagon = int(line[:line.find("-")])
                if num_vagon <= low:
                    depersonalization_dataset.loc[k, atribute] = "Начало"
                elif num_vagon <= normally:
                    depersonalization_dataset.loc[k, atribute] = "Середина"
                else:
                    depersonalization_dataset.loc[k, atribute] = "Хвост"
        depersonalization_dataset.rename(columns={atribute:"Местоположение вагона"}, inplace=True)
            
def random_dataset(dataset):
    for i in range(len(dataset)):
        k1 = random.randint(0, len(dataset) - 1)
        k2 = random.randint(0, len(dataset) - 1)
        dataset.iloc[k1], dataset.iloc[k2] = dataset.iloc[k2].copy(), dataset.iloc[k1].copy()
            
def depersonalization():
    good_parameters = search_wrong()
    if not good_parameters:
        return
    open_file()
    global dataset, depersonalization_dataset, name_atribute
    depersonalization_dataset = dataset.copy()
    index = 0
    for line in name_atribute:
        if not include_quasi[index]: continue
        index += 1
        if line in ['ФИО', 'Откуда', 'Куда', 'Выбор вагона и места', 'Рейс']:
            local_generalization(line)
        elif line in ['Паспортные данные', 'Карта оплаты']:
            masketization(line)
        elif line in ['Дата отъезда', 'Дата приезда']:
            outrage(line)
        elif line in ["Стоимость (руб)"]:
            micro_agregation(line)
    dataset, depersonalization_dataset = depersonalization_dataset, dataset
    name_atribute = dataset.columns
    no_good_k_anonimity_top()
    random_dataset(dataset)
    dataset_key = list()
    for i in range(len(include_quasi)):
        if include_quasi[i]: dataset_key.append(name_atribute[i])
    dataset.sort_values(dataset_key)
    groups_dataset = dataset.groupby(dataset_key)
    write_name_groups = ttk.Frame(root, style="Style.TFrame")
    write_name_groups.grid(row=2, column=0, columnspan=2)
    for group in groups_dataset:
        name_group = ttk.Label(write_name_groups, style="TLabel", text=group[0])
        name_group.grid()

def safe_new_dataset():
    good_parameters = search_wrong()
    if not good_parameters:
        return
    dataset.to_excel(name_output_file + ".xlsx", index=False)
    showinfo(title="успешный успех", message=f"датасет сохранен в файл {name_output_file}.xlsx")  

if __name__ == "__main__":
    root = tk.Tk()
    root.title("обезличивание датасета")
    root.geometry('620x400')
    root['background'] = "gray"
    root. resizable(True, True)
    imgicon = tk.PhotoImage(file=os.path.join('C:\home screen\programming\python\study on python\study\dataset\data\icon.ico'))
    root.tk.call('wm', 'iconphoto', root._w, imgicon) 
    
    style_frame = ttk.Style()
    style_frame.configure("CustomFrame.TFrame", background = "white")
    style_way_frame = ttk.Style()
    style_frame.configure("Style.TFrame", background = "gray")
    style_check_button = ttk.Style()
    style_check_button.configure("TCheckbutton", font=("Arial", 12), background="white", foreground = "gray")
    style_button = ttk.Style()
    style_button.configure("TButton", font=("Arial", 12))
    style_label = ttk.Style()
    style_label.configure("TLabel", font=("Arial", 14), padding = 10, foreground="white", background="gray")
    style_label_top = ttk.Style()
    style_label_top.configure("Top.TLabel", font=("Arial", 16), padding = 10, foreground="gray", background="white", width = 23)
    
    main_menu = tk.Menu()
    main_menu.add_cascade(label="сохранить", command=safe)
    main_menu.add_cascade(label="рассчитать k-anonymity", command=no_good_k_anonimity_top)
    main_menu.add_cascade(label="обезличить", command=depersonalization)
    main_menu.add_cascade(label="сохранить датасет", command=safe_new_dataset)
    main_menu.add_cascade(label="выход", command=sys.exit)
    
    quasi_defectors = ttk.Frame(root, style="CustomFrame.TFrame")
    quasi_defectors.grid(row=0, column=0)
    name_check_button = ['ФИО', 'Паспортные данные', 'Откуда', 'Куда', 'Дата отъезда', 'Дата приезда', 'Рейс', 'Выбор вагона и места', 'Стоимость (руб)', 'Карта оплаты']
    dict_include_column = dict_generation_checkbutton(name_check_button)
    Check_button = dict()
    quasi_label = ttk.Label(quasi_defectors, style="TLabel", text="Выберите квази идентификаторы")
    quasi_label.grid()
    for line in name_check_button:
        Check_button[line] = ttk.Checkbutton(quasi_defectors, text=line, style="TCheckbutton", variable=dict_include_column[line])
        Check_button[line].grid(sticky="w")
        
    way_file = ttk.Frame(root, style="Style.TFrame")
    way_file.grid(row=1, column=0)
    name_file_label = ttk.Label(way_file, style="TLabel", text="имя файла ввода")
    name_file_label.grid()
    file_name = ttk.Entry(way_file , style="TEntry", justify="center", width=28, font=("Arial", 14))
    file_name.grid()
    
    top_bad_k_anonimity = ttk.Frame(root, style="Style.TFrame")
    top_bad_k_anonimity.grid(column=1, row=0)
    top_bad_label = ttk.Label(top_bad_k_anonimity, style="TLabel", text="Топ плохиx k anonymity")
    top_bad_label.grid()
    bad_k_anonimity = list()
    for i in range(5):
        bad_k_anonimity.append(ttk.Label(top_bad_k_anonimity, style="Top.TLabel", text=str(i + 1) + "." + "нет"))
        bad_k_anonimity[i].grid()
    
    way_safe_file = ttk.Frame(root, style="Style.TFrame")
    way_safe_file.grid(row=1, column=1)
    name_safe_file_label = ttk.Label(way_safe_file, style="TLabel", text="имя файла вывода")
    name_safe_file_label.grid()
    save_file_name = ttk.Entry(way_safe_file , style="TEntry", justify="center", width=27, font=("Arial", 14))
    save_file_name.grid()
    
    root.config(menu=main_menu)
    root.mainloop()
