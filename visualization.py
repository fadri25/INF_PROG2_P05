import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from difflib import get_close_matches
import calculations

class Visualization:
    def __init__(self, df1_sorted, df2, start_saturday, start_sunday, end_saturday, end_sunday):
        self.root = tk.Tk()
        self.df1 = df1_sorted
        self.df2 = df2
        self.start_saturday = start_saturday
        self.start_sunday = start_sunday
        self.end_saturday = end_saturday
        self.end_sunday = end_sunday
        self.create_widgets()
        self.root.title = "Mean Delays"
        self.root.geometry("600x600")
        self.close_button = ttk.Button(self.root, text='Close', command=self.close_window)
        self.close_button.pack()
        self.root.mainloop() 
        
    def create_widgets(self):
        frame1 = tk.Frame(self.root)
        frame1.pack(side="left", fill="both", expand=True)
        self.treeview = tk.ttk.Treeview(frame1)
        self.treeview.pack(side='left', fill='both', expand=True)
        self.scrollbar = ttk.Scrollbar(frame1, orient='vertical', command=self.treeview.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.combine_dataframes()
             
    def combine_dataframes(self):
        combined_df = self.df1.merge(self.df2[['stop', 'delay']], on='stop', how='left')
        combined_df.columns = ['stop', f'delay {self.start_saturday}-{self.start_sunday}', f'delay {self.end_saturday}-{self.end_sunday}']

        self.treeview['columns'] = combined_df.columns.tolist()
        for col in combined_df.columns:
            if combined_df[col].any():
                self.treeview.heading(col, text=col)
                self.treeview.column(col, width=10)  # adjustment

        for _, row in combined_df.iterrows():
            self.treeview.insert('', 'end', values=row.tolist())

    def close_window(self):
        self.root.destroy()   
    
class App:
    def __init__(self, start_saturday, start_sunday, end_saturday, end_sunday, dataframe, data_delay1, top_stops1, df1_sorted, df2):
        self.root = tk.Tk()
        self.start_saturday = start_saturday
        self.start_sunday = start_sunday
        self.end_saturday = end_saturday
        self.end_sunday = end_sunday
        self.dataframe = dataframe
        self.data_delay1 = data_delay1
        self.top_stops1 = top_stops1
        self.df1_sorted = df1_sorted
        self.df2 = df2
        self.root.title("VBZ Delays")
        width=504
        height=195
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)
        background_image = ImageTk.PhotoImage(Image.open("bushaltestelle.jpg"))
        icon_path = "bus.png"
        self.root.iconbitmap(icon_path)
        
        l_background=tk.Label(self.root, image=background_image)
        l_background.place(x=0, y=0, relwidth=1, relheight=1)
        l_background.image = background_image

        b_delay=tk.Button(self.root)
        b_delay["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        b_delay["font"] = ft
        b_delay["fg"] = "#000000"
        b_delay["justify"] = "center"
        b_delay["text"] = "Delays"
        b_delay.place(x=140,y=150,width=103,height=30)
        b_delay["command"] = self.b_delay_command

        b_bar=tk.Button(self.root)
        b_bar["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        b_bar["font"] = ft
        b_bar["fg"] = "#000000"
        b_bar["justify"] = "center"
        b_bar["text"] = "Barplot"
        b_bar.place(x=260,y=150,width=104,height=30)
        b_bar["command"] = self.b_bar_command

        b_close=tk.Button(self.root)
        b_close["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        b_close["font"] = ft
        b_close["fg"] = "#000000"
        b_close["justify"] = "center"
        b_close["text"] = "Close"
        b_close.place(x=380,y=150,width=103,height=30)
        b_close["command"] = self.b_close_command
        
        b_dataframe=tk.Button(self.root)
        b_dataframe["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        b_dataframe["font"] = ft
        b_dataframe["fg"] = "#000000"
        b_dataframe["justify"] = "center"
        b_dataframe["text"] = "Data"
        b_dataframe.place(x=20,y=150,width=104,height=30)
        b_dataframe["command"] = self.b_dataframe_command
        
        l_delay=tk.Label(self.root)
        ft = tkFont.Font(family='Times',size=23)
        l_delay["font"] = ft
        l_delay["fg"] = "#333333"
        l_delay["justify"] = "center"
        l_delay["text"] = "VBZ Delays"
        l_delay.place(x=100,y=20,width=321,height=30)
        self.root.mainloop()

    def b_delay_command(self):
        stops = calculations.Stops(self.dataframe).unique_stops()
        line_diagram = Weeklymeandelay(stops, self.data_delay1)
        line_diagram.search('stop')

    def b_bar_command(self):
        title1 =f'Top 10 Delays of Stations({self.start_sunday}-{self.start_saturday})'
        visualizer = Barvisualizer(self.top_stops1, title1)
        visualizer.plot_bar()

    def b_close_command(self):
        self.root.destroy()

    def b_dataframe_command(self):
        Visualization(self.df1_sorted, self.df2, self.start_saturday, self.start_sunday, self.end_saturday, self.end_sunday)

class Barvisualizer:
    def __init__(self, top_stops, title):
        self.df = top_stops
        self.title = title
    
    def plot_bar(self):
        x_values = self.df['stop']
        y_values = self.df['delay']
        plt.bar(x_values, y_values)
        for i,v in enumerate(y_values):
            plt.text(i,v, str(v), ha='center', va='bottom')
        plt.xlabel('Stations in Zurich')
        plt.ylabel('Delay in seconds')
        plt.title(self.title)
        plt.xticks(rotation=45, ha='right') # Rotation um 45 der X-Achsenbeschriftung um lesen zu können
        plt.tight_layout() 
        plt.gca().xaxis.set_tick_params(pad=0) # schriftzug nach links
        plt.show()

class Weeklymeandelay:
    def __init__(self, dataframe, df1):
        self.dataframe = dataframe
        self.df = df1
        self.search_results = []
        self.window = Tk()
        self.window.title("")
        self.label = Label(self.window, text="Station:")
        self.label.pack()
        self.entry = Entry(self.window)
        self.entry.pack()
        self.search_button = Button(self.window, text="Search", command=self.perform_search)
        self.search_button.pack()
        self.close_button = Button(self.window, text="Close", command=self.close_window)
        self.close_button.pack()

    def perform_search(self):
        search_term = self.entry.get()

        matches = get_close_matches(search_term, self.dataframe['stop'])
        if matches:
            match = matches[0]
            calc = calculations.Stop_calculation(self.df, match)
            barplot = calc.find_columns_with_same_value()
            x_values = barplot['betriebsdatum']
            y_values = barplot['delay'].round(1)
            plt.bar(x_values, y_values)
            for i,v in enumerate(y_values):
                plt.text(i,v, str(v), ha='center', va='bottom')
            plt.xlabel('Date')
            plt.ylabel('Mean delay in seconds')
            plt.title(f'Mean delays for {match}')
            plt.xticks(rotation=45, ha='right') # Rotation um 45 der X-Achsenbeschriftung um lesen zu können
            plt.tight_layout() # Anpassen um überlappungen vorzubeugen
            plt.gca().xaxis.set_tick_params(pad=0) # Schrift ein wenig weiter nach links um es besser lesen zu können aber hä
            plt.show()

        else:
            messagebox.showinfo("search result", "No station found.")

    def close_window(self):
        self.window.destroy()

    def search(self, column):
        self.window.mainloop()

if __name__ == '__main__':
    pass

