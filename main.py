#################################################################################
#   Autoren: Sarah, Kristina, Fadri
#   Erstellungsdatum: 27.04.2023
#   Beschreibung: INF_PROG2_P05
#   Version: 3.0 (GVC)
#   Letze Änderung: 03.06.2023
#################################################################################

import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import calculations
import visualization
import timetransformations
import datapreparation

"""Checks if there is data for the inserted dates"""
def search_button_click():
    start_date = e_start.get()
    end_date = e_end.get()
    start_date_obj = timetransformations.Timespan(start_date)
    end_date_obj = timetransformations.Timespan(end_date)
    start_time = start_date_obj.calculate_time()
    end_time = end_date_obj.calculate_time()
    if start_time is not None and end_time is not None:
        start_sunday, start_saturday = start_time
        end_sunday, end_saturday = end_time
        messagebox.showinfo("Success", "Search successful! This Window will close. Please wait until the next window opens.")
        root.destroy()
        return start_sunday, start_saturday, end_sunday, end_saturday
    else:
        return None # Error handling in function on_search_button_click
    
"""Gets data, calculates and returns the new DataFrame. It also opens the Main menu"""
def on_search_button_click():
    result = search_button_click()
    start_saturday = None
    start_sunday = None
    end_saturday = None
    end_sunday = None
    if result is not None:
        start_sunday, start_saturday, end_sunday, end_saturday = result
        urls = [
        f'https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Fahrzeiten_SOLL_IST_{start_sunday}_{start_saturday}.csv',
        f'https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Fahrzeiten_SOLL_IST_{end_sunday}_{end_saturday}.csv',
        'https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Haltestelle.csv']
        
        downloader = datapreparation.Downloader(urls[0])
        file_path1 = downloader.download()

        downloader = datapreparation.Downloader(urls[1])
        file_path2 = downloader.download()

        downloader = datapreparation.Downloader(urls[2])
        downloader.download()

        data_path1 = datapreparation.Data(file_path1)
        dataframe1 = data_path1.data()
        calculator = calculations.Calculator(dataframe1)
        top_stops1, data_delay1, df1_sorted = calculator.calculate_df1()
        
        data_path2 = datapreparation.Data(file_path2)
        dataframe2 = data_path2.data()
        calculator = calculations.Calculator(dataframe2)
        df2= calculator.calculate_df2()
        visualization.App(start_saturday, start_sunday, end_saturday, end_sunday, dataframe1, data_delay1, top_stops1, df1_sorted, df2)
    else: # Error if no dataset is found from the dates inserted
        messagebox.showerror("Error", "No weekly dataset found for at least one week of the dates provided. Please enter other dates!")

def close():
    root.destroy()
    
"""Visualization of first window"""
root = tk.Tk()
root.title("Date selection")
icon_path = "bus.ico"
root.iconbitmap(icon_path)
WIDTH=350
HEIGHT=190
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (WIDTH, HEIGHT, (screenwidth - WIDTH) / 2, (screenheight - HEIGHT) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)

l_title=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
l_title["font"] = ft
l_title["fg"] = "#333333"
l_title["justify"] = "center"
l_title["text"] = "Dataset Search"
l_title.place(x=100,y=10,width=122,height=30)

l_start_date=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
l_start_date["font"] = ft
l_start_date["fg"] = "#333333"
l_start_date["justify"] = "center"
l_start_date["text"] = "Date for weekly Dataset (format: dd.mm.yyyy):"
l_start_date.place(x=10,y=30,width=300,height=34)

e_start=tk.Entry(root)
e_start["borderwidth"] = "1px"
ft = tkFont.Font(family='Times',size=10)
e_start["font"] = ft
e_start["fg"] = "#333333"
e_start["justify"] = "center"
e_start.place(x=80,y=60,width=164,height=30)

l_end_date=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
l_end_date["font"] = ft
l_end_date["fg"] = "#333333"
l_end_date["justify"] = "center"
l_end_date["text"] = "Date for weekly Dataset to compare (format: dd.mm.yyyy):"
l_end_date.place(x=10,y=90,width=350,height=32)

e_end=tk.Entry(root)
e_end["borderwidth"] = "1px"
ft = tkFont.Font(family='Times',size=10)
e_end["font"] = ft
e_end["fg"] = "#333333"
e_end["justify"] = "center"
e_end.place(x=80,y=120,width=167,height=30)

b_search=tk.Button(root)
b_search["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times',size=10)
b_search["font"] = ft
b_search["fg"] = "#000000"
b_search["justify"] = "center"
b_search["text"] = "Search"
b_search.place(x=40,y=160,width=70,height=25)
b_search["command"] = on_search_button_click

b_close=tk.Button(root)
b_close["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times',size=10)
b_close["font"] = ft
b_close["fg"] = "#000000"
b_close["justify"] = "center"
b_close["text"] = "Close"
b_close.place(x=210,y=160,width=70,height=25)
b_close["command"] = close

root.mainloop()
