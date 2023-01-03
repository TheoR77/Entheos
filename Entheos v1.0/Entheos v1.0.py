import datetime
from datetime import timedelta
import random
import statistics
from tkinter import messagebox
from tkinter import filedialog

import numpy as np
import pandas as pd
from pathlib import Path
import json
from colorama import *
from tkinter import ttk
from tkinter import *
import ctypes
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




with open('jentheos_v1.json', 'r') as f:
    past_data = json.load(f)


# get the data from the "jentheos_v1.json" file
date_list = []
for i in range(0, len(past_data.get('Date'))):
    date_list.append(past_data.get('Date')[i])

slqu_list = []
for i in range(0, len(past_data.get('Sleep Quality'))):
    slqu_list.append(past_data.get('Sleep Quality')[i])

gemo_list = []
for i in range(0, len(past_data.get('General Mood'))):
    gemo_list.append(past_data.get('General Mood')[i])

supr_list  = []
for i in range(0, len(past_data.get('Productivity'))):
    supr_list.append(past_data.get('Productivity')[i])

phac_list = []
for i in range(0, len(past_data.get('Physical Activity'))):
    phac_list.append(past_data.get('Physical Activity')[i])

last_value_list = [date_list, slqu_list, gemo_list, supr_list, phac_list]

f_time = str(datetime.datetime.now())[:16]
print('Data e horário desse registro: ', f_time)




# TKINTER AREA
window = Tk()
window.title("Entheos")

window.geometry('800x450')
ctypes.windll.shcore.SetProcessDpiAwareness(True)
window.resizable(width=False, height=False)


progression = 0
aval = "Sleep Quality"
display_string = "Today's register, "+str(datetime.datetime.now())[:16]+":\n"

def popup():
    messagebox.showinfo("", "The Excel file was created")

def dump_data():
    dict = {'Date': date_list, 'Sleep Quality': slqu_list, 'General Mood': gemo_list,
            'Productivity': supr_list,
            'Physical Activity': phac_list}
    filename = Path.cwd() / "jentheos_v1.json"
    data = dict  # data to be dumped
    with open(filename, 'w') as f:
        json.dump(data, f)

def clean_func():
    mainentry.delete(0, last="end")  # clean the entry space

def add():
    global progression
    global add_button
    if (mainentry.get().isnumeric() == True) and (float(mainentry.get()) <= 0):
        pass
    else:
        global progression
        if progression == (4 or 5) and ((mainentry.get() != 'y') and (mainentry.get() != 'n')):
            print("You must digit 'y' or 'n'!")
            pass
        else:
            if (mainentry.get().isnumeric() == False) and (progression <= 3):
                print("You must insert a number between 0 and 20!")

                pass
            else:
                if progression == 0:
                    aval = "Sleep Quality"
                if progression == 1:
                    aval = "General Mood"
                if progression == 2:
                    aval = "Productivity"
                if progression == 3:
                    aval = "Physical Activity"
                global display_string
                display_string = display_string + "✦ " + aval + ": " + str(mainentry.get() + "; \n")
                label_text2.config(text=display_string)
                label_text2.pack(fill=X)
                if progression == 0:
                    slqu_list.append(str(mainentry.get()))
                if progression == 1:
                    gemo_list.append(str(mainentry.get()))
                if progression == 2:
                    supr_list.append(str(mainentry.get()))
                if progression == 3:
                    phac_list.append(str(mainentry.get()))
                progression = progression + 1
                if progression == 0:  # Appends the entry string to lists
                    aval = "Sleep Quality"
                if progression == 1:
                    aval = "General Mood"
                if progression == 2:
                    aval = "Productivity"
                if progression == 3:
                    aval = "Physical Activity"
                if progression == 4:
                    #date_list.append(str(datetime.datetime.now())[:16])
                    dump_data()
                    add_button['state'] = 'disabled'
                    addnewdata_button['state'] = 'normal'

                label_text1.config(text="Evaluate " + aval + " ")
                if progression == 4:
                    label_text1.config(text="Daily register completed;")
                    label_text1.pack()
                clean_func()
                label_text1.pack()

def refresh_gd(): #  get the means and put in a label
    dict = {'Sleep Quality': slqu_list, 'General Mood': gemo_list,
     'Productivity': supr_list,
     'Physical Activity': phac_list}
    ffdb = pd.DataFrame(data=dict)
    ffslqu_list = []
    for i in range(0, len(ffdb.get('Sleep Quality'))):
        ffslqu_list.append(ffdb.get('Sleep Quality').astype('float')[i])
    ffgemo_list = []
    for i in range(0, len(ffdb.get('General Mood'))):
        ffgemo_list.append(ffdb.get('General Mood').astype('float')[i])
    ffsupr_list = []
    for i in range(0, len(ffdb.get('Productivity'))):
        ffsupr_list.append(ffdb.get('Productivity').astype('float')[i])
    ffphac_list = []
    for i in range(0, len(ffdb.get('Physical Activity'))):
        ffphac_list.append(ffdb.get('Physical Activity').astype('float')[i])

    def stringfy(i):
        k = statistics.mean(i)
        l = round(k, 2)
        m = str(l)
        return m

    week_mean = []
    for i in range(1,7):
        week_mean.append(ffslqu_list[-i])
    pretext = '😴 Sleep Quality:  All period mean: ' + stringfy(ffslqu_list) + "   |   Last week mean: " + stringfy(week_mean)
    a = pretext
    label_mean1['text'] = a

    week_mean = []
    for i in range(1,7):
        week_mean.append(ffphac_list[-i])
    pretext = '🏀 Physical Activity:  All period mean: ' + stringfy(ffphac_list) + "   |   Last week mean: " + stringfy(week_mean)
    a = pretext
    label_mean2['text'] = a

    week_mean = []
    for i in range(1,7):
        week_mean.append(ffsupr_list[-i])
    pretext = '🖋 Productivity:  All period mean: ' + stringfy(ffsupr_list) + "   |   Last week mean: " + stringfy(week_mean)
    a = pretext
    label_mean3['text'] = a

    week_mean = []
    for i in range(1,7):
        week_mean.append(ffgemo_list[-i])
    pretext = '🍀 General Mood:  All period mean: ' + stringfy(ffgemo_list) + "   |  Last week mean: " + stringfy(week_mean)
    a = pretext
    label_mean4['text'] = a


load = 0

def float_dataset():  #  getting all the values of the DataFrame to float

    global load, fdb, shortdatetime_list, fshortdatetime_list, count_list, fslqu_list, slqu_list, fphac_list, fsupr_list, fgemo_list, figure1
    dict = {'Date': date_list, 'Sleep Quality': slqu_list, 'General Mood': gemo_list,
            'Productivity': supr_list,
            'Physical Activity': phac_list}
    #print("Float Dataset Lenghts: ")
    #print(len(dict["Date"]))
    #print(len(dict["Sleep Quality"]))
    #print(len(dict["General Mood"]))
    #print(len(dict["Productivity"]))
    #print(len(dict["Physical Activity"]))

    db = pd.DataFrame(data=dict)

    count_list = []
    for i in range(0, 30):
        got_time = datetime.datetime.now()
        delta = datetime.timedelta(days=-i)
        got_time2 = got_time + delta
        got_time3 = str(got_time2)[8:10]
        count_list.append(got_time3)
    count_list = list(reversed(count_list))
    meta_list = []

    global bol
    bol = True
    for i in range(1, 30):
        beta = int(count_list[i])
        if bol == False:
            meta_list.append("'")
            bol = True
        else:
            meta_list.append(str(count_list[i]))
            bol = False
    count_list = meta_list

    shortdatetime_list = []  # Here you get the last 14 days in base with today and associate the last 14 inputs with it
    for i in range(1, 30):
        got_time = datetime.datetime.now()
        delta = datetime.timedelta(days=-i)
        got_time2 = got_time + delta
        got_time3 = str(got_time2)[8:10]
        shortdatetime_list.append(got_time3)
    shortdatetime_list = list(reversed(shortdatetime_list))

    fshortdatetime_list = []  # Here you get the last 14 days in base with today and associate the last 14 inputs with it
    for i in range(1, 30):
        got_time = datetime.datetime.now()
        delta = datetime.timedelta(days=-i)
        got_time2 = got_time + delta
        got_time3 = str(got_time2)[8:10]
        got_time4 = float(got_time3)
        fshortdatetime_list.append(got_time4)
    fshortdatetime_list = list(reversed(fshortdatetime_list))

    # ///
    fslqu_list = []
    for i in range(1, len(db.get('Sleep Quality'))):  # gets the databases values and convert to float
        fslqu_list.append(db.get('Sleep Quality').astype('float')[i])

    meta_list = []
    for i in range(1, 30):
        meta_list.append(fslqu_list[-i])  # gets the last 30 values from the list
    fslqu_list = meta_list
    fslqu_list = list(reversed(fslqu_list))
    # ///

    # ///
    fgemo_list = []
    for i in range(1, len(db.get('General Mood'))):  # gets the databases values and convert to float
        fgemo_list.append(db.get('General Mood').astype('float')[i])

    meta_list = []
    for i in range(1, 30):
        meta_list.append(fgemo_list[-i])  # gets the last 30 values from the list
    fgemo_list = meta_list
    fgemo_list = list(reversed(fgemo_list))
    # ///

    # ///
    fsupr_list = []
    for i in range(1, len(db.get('Productivity'))):  # gets the databases values and convert to float
        fsupr_list.append(db.get('Productivity').astype('float')[i])
    #fslqu_list = list(reversed(fslqu_list))

    meta_list = []
    for i in range(1, 30):
        meta_list.append(fsupr_list[-i])  # gets the last 30 values from the list
    fsupr_list = meta_list
    fsupr_list = list(reversed(fsupr_list))
    # ///

    # ///
    fphac_list = []
    for i in range(1, len(db.get('Physical Activity'))):  # gets the databases values and convert to float
        fphac_list.append(db.get('Physical Activity').astype('float')[i])
    #fslqu_list = list(reversed(fslqu_list))

    meta_list = []
    for i in range(1, 30):
        meta_list.append(fphac_list[-i])  # gets the last 30 values from the list
    fphac_list = meta_list
    fphac_list = list(reversed(fphac_list))

    fdict = {'Sleep Quality': fslqu_list, 'General Mood': fgemo_list,
            'Productivity': fsupr_list,
            'Physical Activity': fphac_list}
    fdb = pd.DataFrame(data=fdict)





def show_data():
    global load, shortdatetime_list, count_list, fslqu_list, fphac_list, fsupr_list, fgemo_list, figure1
    label_text2.destroy()
    add_button.destroy()
    clean_button.destroy()
    mainentry.destroy()
    addnewdata_button.destroy()
    label_textdel.destroy()

    excel_export_button.config(state='normal')
    csv_export_button.config(state='normal')
    graph_button1.config(state='normal')
    graph_button2.config(state='normal')
    graph_button3.config(state='normal')
    graph_button4.config(state='normal')


    #label_text1.config(text="Daily register completed;\n" + display_string)
    #label_text1.pack(fill=Y, side=BOTTOM)

    if load == 0:  # creates a list with float values one single time
        refresh_gd()
        date_list.append(str(datetime.datetime.now())[:16])
        dump_data()


        with open('jentheos_v1.json', 'r') as f:
            dict = json.load(f)

        db = pd.DataFrame(data=dict)

        label_textdel.destroy()
        label_textdel2.destroy()
        label_text_title_genov.destroy()
        label_fill.destroy()

        shortdatetime_list = []
        for i in range(1, 30):
            got_time = datetime.datetime.now()
            delta = datetime.timedelta(days=-i)
            got_time2 = got_time + delta
            got_time3 = str(got_time2)[8:10]
            d = timedelta(days=-i)
            b = []
            b.append(got_time3)
            shortdatetime_list.append(got_time3)
        shortdatetime_list = list(reversed(shortdatetime_list))


        count_list = []
        for i in range(1, 30):
            count_list.append(i)

        fslqu_list = []
        for i in range(1, 30):
           g = db.iloc[(len(slqu_list)-i), 1]
           r = float(g)
           fslqu_list.append(r)
        fslqu_list = list(reversed(fslqu_list))

        fgemo_list = []
        for i in range(1, 30):
           g = db.iloc[(len(gemo_list)-i), 2]
           r = float(g)
           fgemo_list.append(r)
        fgemo_list = list(reversed(fgemo_list))

        fsupr_list = []
        for i in range(1, 30):
           g = db.iloc[(len(supr_list)-i), 3]
           r = float(g)
           fsupr_list.append(r)
        fsupr_list = list(reversed(fsupr_list))

        fphac_list = []
        for i in range(1, 30):
           g = db.iloc[(len(phac_list)-i), 4]
           r = float(g)
           fphac_list.append(r)
        fphac_list = list(reversed(fphac_list))
    load = 1

    print("Graph page... ",ftd_graph,"\nLenghs:", len(fslqu_list),len(count_list),'\n Yaxis: ', fslqu_list,'\n Countlist: ', count_list)

    figure1 = plt.Figure(figsize=(9, 5), dpi=90, facecolor="white")
    ax1 = figure1.add_subplot(111) # #e6e6e6
    canvas_graph = FigureCanvasTkAgg(figure1, tab_3)
    ax1.plot(shortdatetime_list, fslqu_list, color='#5D18D9', label='Sleep Quality')  # purple
    ax1.plot(shortdatetime_list, fphac_list, color='#FA9F10', label='Physical Activity')  # orange
    ax1.plot(shortdatetime_list, fgemo_list, color='#1C77FF', label='General Mood')  # blue
    ax1.plot(shortdatetime_list, fsupr_list, color='#F02E05', label='Productivity')  # red

    ax1.legend(loc='lower left', ncol=2,frameon=True)
    canvas_graph.get_tk_widget().pack(side=BOTTOM)  #https://matplotlib.org/stable/tutorials/intermediate/artists.html


ftd_graph = 1

def auto():
    for i in range (0, 4):
        ny = random.randint(6,19)
        ny = str(ny)
        mainentry.insert(0, ny)
        add()

def excel_export():
    json_file = pd.read_json('jentheos_v1.json')
    file = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel file (.xlsx)",".xlsx")])
    json_file.to_excel(file)

def csv_export():
    json_file = pd.read_json('jentheos_v1.json')
    file = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("Comma-separated values (csv)",".csv")])
    json_file.to_csv(file)


def add_numbervalue():
    if mainentry.get().isnumeric() == False:  # y or n
        if progression == 4 or progression == 5:
            if (mainentry.get() == 'y') or (mainentry.get() =='n'):
                add()
            else:
                print("You MuST digit 'y' or 'n'!")
        else:
            print("You must put a value between 0 and 20")
            pass
    else:  # numeric: number between 0 and 20
        if float(mainentry.get()) <= 0:
            print("The value must be bigger than 0")
        else:
            if float(mainentry.get()) >= 21:
                print("The value must be less than 20")
                pass
            else:
                add()

style = ttk.Style()
style.configure("BW.TLabel", foreground="black", background="white")


s = ttk.Style()
s.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [25, 8],
                                        "font" : ('Ubuntu Medium', '12')},}})
s.theme_use("MyStyle")



tabControl = ttk.Notebook(window)
tab_1 = ttk.Frame(tabControl)
tab_2 = ttk.Frame(tabControl)
tab_3 = ttk.Frame(tabControl)
tab_4 = ttk.Frame(tabControl)

tabControl.add(tab_1, text='Data Input')
tabControl.add(tab_2, text='Specific Graphs')
tabControl.add(tab_3, text='Overview')
tabControl.add(tab_4, text='Means')
tabControl.pack(side='top', fill='x')





label_text1 = Label(tab_1, pady=1,text="Evaluate the Sleep Quality Value:",background="#dadada",fg="black", height=3,font=("Ubuntu", "14"))
label_text1.pack()

mainentry = Entry(tab_1, width=25, background="black", fg="white", font=("Ubuntu Light", "14"))
mainentry.bind("<Enter>", add())
mainentry.pack(side=RIGHT and TOP)



addnewdata_button = Button(tab_1, state='disabled', width=60, border=40, background="#dadada",fg="black", font=("Ubuntu Light", "12"), borderwidth=3, text="Add new data", command=show_data)
addnewdata_button.pack(fill=X)
add_button = Button(tab_1, width=60,  border=40, background="#dadada",fg="black", font=("Ubuntu Light", "12"), borderwidth=3, text="Add value", command=add_numbervalue)
add_button.pack(fill=X)
clean_button = Button(tab_1, width=60, background="#dadada",fg="black", font=("Ubuntu Light", "12"), borderwidth=3, padx=25, text="Delete", command=clean_func)
clean_button.pack(fill=X)

def slqu_graph():
    float_dataset()
    fig = plt.figure(figsize=(10, 5))

    coef = np.polyfit(fshortdatetime_list, fslqu_list, deg=1)
    linearregline = np.poly1d(coef)
    global xaxis
    xaxis = []
    for i in range(1, 30):
        xaxis.append(i)

    plt.plot(shortdatetime_list, fslqu_list, linewidth = 2, color='black')
    plt.plot(xaxis, fslqu_list, 'none', xaxis, linearregline(xaxis), '--k')
    plt.plot(shortdatetime_list, fslqu_list, '.', markersize=12, color='black')
    plt.ticklabel_format()
    plt.plot(shortdatetime_list, fphac_list, alpha=0.3, color='#FA9F10')
    plt.plot(shortdatetime_list, fgemo_list, alpha=0.3, color='#1C77FF')
    plt.plot(shortdatetime_list, fsupr_list, alpha=0.3, color='#F02E05')
    plt.title('Sleep Quality Graph', color='black', fontsize=18)
    plt.xlabel('Last 30 days', color='black', fontsize=14)
    plt.show()

def gemo_graph():
    float_dataset()
    fig = plt.figure(figsize=(10, 5))

    coef = np.polyfit(fshortdatetime_list, fgemo_list, deg=1)
    linearregline = np.poly1d(coef)
    global xaxis
    xaxis = []
    for i in range(1, 30):
        xaxis.append(i)

    plt.plot(shortdatetime_list, fgemo_list, linewidth = 2, color='black')
    plt.plot(xaxis, fgemo_list, 'none', xaxis, linearregline(xaxis), '--k')
    plt.plot(shortdatetime_list, fgemo_list, '.', markersize=12, color='black')
    plt.ticklabel_format()
    plt.plot(shortdatetime_list, fphac_list, alpha=0.3, color='#FA9F10')
    plt.plot(shortdatetime_list, fslqu_list, alpha=0.3, color='#5D18D9')
    plt.plot(shortdatetime_list, fsupr_list, alpha=0.3, color='#F02E05')
    plt.title('General Mood Graph', color='black', fontsize=18)
    plt.xlabel('Last 30 days', color='black', fontsize=12)
    plt.show()

def phac_graph():
    float_dataset()
    fig = plt.figure(figsize=(10, 5))

    coef = np.polyfit(fshortdatetime_list, fphac_list, deg=1)
    linearregline = np.poly1d(coef)
    global xaxis
    xaxis = []
    for i in range(1, 30):
        xaxis.append(i)

    plt.plot(shortdatetime_list, fphac_list, linewidth = 2, color='black')
    plt.plot(xaxis, fphac_list, 'none', xaxis, linearregline(xaxis), '--k')
    plt.plot(shortdatetime_list, fphac_list, '.', markersize=12, color='black')
    plt.ticklabel_format()
    plt.plot(shortdatetime_list, fgemo_list, alpha=0.3, color='#1C77FF')
    plt.plot(shortdatetime_list, fslqu_list, alpha=0.3, color='#5D18D9')
    plt.plot(shortdatetime_list, fsupr_list, alpha=0.3, color='#F02E05')
    plt.title('Physical Activity', color='black', fontsize=18)
    plt.xlabel('Last 30 days', color='black', fontsize=12)
    plt.show()

def supr_graph():
    float_dataset()
    fig = plt.figure(figsize=(10, 5))

    coef = np.polyfit(fshortdatetime_list, fsupr_list, deg=1)
    linearregline = np.poly1d(coef)
    global xaxis
    xaxis = []
    for i in range(1, 30):
        xaxis.append(i)

    plt.plot(shortdatetime_list, fsupr_list, linewidth = 2, color='black')
    plt.plot(xaxis, fsupr_list, 'none', xaxis, linearregline(xaxis), '--k')
    plt.plot(shortdatetime_list, fsupr_list, '.', markersize=12, color='black')
    plt.ticklabel_format()
    plt.plot(shortdatetime_list, fgemo_list, alpha=0.3, color='#1C77FF')
    plt.plot(shortdatetime_list, fslqu_list, alpha=0.3, color='#5D18D9')
    plt.plot(shortdatetime_list, fphac_list, alpha=0.3, color='#FA9F10')
    plt.title('Productivity', color='black', fontsize=18)
    plt.xlabel('Last 30 days', color='black', fontsize=12)
    plt.show()

label_text_title_genov = Label(tab_3, height=3, pady=2,padx=3, background="white",text=">>>    General Overview    <<<", fg="black", font=("Ubuntu Medium", "18"), justify=LEFT)
label_text_title_genov.pack(fill=X, anchor='s')
label_textdel = Label(tab_3, height=1, pady=1,padx=3, background="white",text="Input your data first",fg="black", font=("Ubuntu Light", "14"), justify=LEFT)
label_textdel.pack(fill=X, anchor='s')
label_fill = Label(tab_3, background="white")
label_fill.pack(fill='both', side=BOTTOM, expand=True)



label_titletab2 = Label(tab_2, height=3, pady=2, padx=3, text=">>>    Specific Graphs    <<<", background="#dadada",fg="black", font=("Ubuntu", "18", "bold"), justify=LEFT)
label_titletab2.pack()

graph_button1 = Button(tab_2, width=60, state='disabled', text="Sleep Quality Graph", border=40, background="#dadada",fg="black", font=("Ubuntu", "12"), borderwidth=3, command=slqu_graph)
graph_button1.pack()
graph_button2 = Button(tab_2, width=60, state='disabled', border=40, background="#dadada",fg="black", font=("Ubuntu", "12"), borderwidth=3, text="General Mood Graph", command=gemo_graph)
graph_button2.pack()

graph_button3 = Button(tab_2, width=60,  state='disabled', border=40, background="#dadada",fg="black", font=("Ubuntu", "12"), borderwidth=3, text="Productivity Graph", command=supr_graph)
graph_button3.pack()
graph_button4 = Button(tab_2, width=60,  state='disabled', border=40, background="#dadada",fg="black", font=("Ubuntu", "12"), borderwidth=3, text="Physical Activity Graph", command=phac_graph)
graph_button4.pack()

label_espace3 = Label(tab_2, border=40, background="#dadada",fg="black", font=("Ubuntu", "14"), borderwidth=3).pack()

excel_export_button = Button(tab_2,  state='disabled', width=50, text='Save dataframe as .xlsx file', border=40, background="#dadada",fg="black", font=("Ubuntu", "12"), borderwidth=3, command=excel_export)
excel_export_button.pack()
csv_export_button = Button(tab_2,  state='disabled', width=50, text='Save dataframe as .csv file', border=40, background="#dadada",fg="black", font=("Ubuntu", "12"), borderwidth=3, command=csv_export)
csv_export_button.pack()

label_text2 = Label(tab_1, height=250, pady=2,padx=3,text=display_string, background="#dadada",fg="black", font=("Ubuntu Light", "14"), justify=LEFT)
label_text2.pack(fill=Y, side=BOTTOM)

label_overview = Label(tab_4, height=3, pady=1, text=">>>    Means    <<<",background="#dadada",fg="black", font=("Ubuntu Medium", "18"))
label_overview.pack(anchor='s')
label_textdel2 = Label(tab_4, height=1, pady=1,padx=3, background="#dadada",text="Input your data first",fg="black", font=("Ubuntu Light", "14"), justify=LEFT)
label_textdel2.pack(fill=X, anchor='s')

label_mean1 = Label(tab_4, pady=1, text="",background="#dadada",fg="black", font=("Ubuntu Light", "16"))
label_mean1.pack()
label_mean2 = Label(tab_4, pady=1, text="",background="#dadada",fg="black", font=("Ubuntu Light", "16"))
label_mean2.pack()
label_mean3 = Label(tab_4, pady=1, text="",background="#dadada",fg="black", font=("Ubuntu Light", "16"))
label_mean3.pack()
label_mean4 = Label(tab_4, pady=1, text="",background="#dadada",fg="black", font=("Ubuntu Light", "16"))
label_mean4.pack()



window.configure(bg='white')
window.mainloop()




dict = {'Date': date_list, 'Sleep Quality': slqu_list, 'General Mood': gemo_list, 'Productivity': supr_list,
        'Physical Activity': phac_list}
db = pd.DataFrame(data=dict)


filename = Path.cwd() / "jentheos_v1.json"
data = dict

with open(filename, 'w') as f:
    json.dump(data, f)

print(Fore.CYAN + 'Finished')

