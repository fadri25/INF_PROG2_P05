import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from difflib import get_close_matches
import calculations

"""Visualization of the delay comparison"""
class Visualization:
    def __init__(self, df1_sorted, df2, start_saturday, start_sunday, end_saturday, end_sunday):
        self.df1 = df1_sorted
        self.df2 = df2[['stop', 'halt_diva_von', 'delay']]
        self.start_saturday = start_saturday
        self.start_sunday = start_sunday
        self.end_saturday = end_saturday
        self.end_sunday = end_sunday
        self.combined_df = self.df1.merge(self.df2[['stop', 'halt_diva_von', 'delay']], on='stop', how='left')[['stop', 'halt_diva_von', 'delay_x', 'delay_y']]
        self.combined_df.columns = ['Stop', 'Stop ID', f'Delay ({self.start_saturday}-{self.start_sunday})', f'Delay ({self.end_saturday}-{self.end_sunday})']
        self.root = tk.Tk()
        self.root.title("Dataset insights")
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL) # Creates scrollbar to scroll through all delays
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview = ttk.Treeview(self.frame, yscrollcommand=scrollbar.set, show="headings") # Only show headings in the Frame without the index
        self.treeview.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.treeview.yview)
        self.populate_treeview()
        self.root.geometry("750x600")
        self.close_button = ttk.Button(self.root, text='Close', command=self.close_window)
        self.close_button.pack()
        icon_path = "bus.ico"
        self.root.iconbitmap(icon_path)
        self.root.mainloop() 
        
    """Insert the Dataframe in the tk.Frame"""
    def populate_treeview(self):
        columns = self.combined_df.columns.tolist()
        self.treeview["columns"] = columns
        self.treeview.heading("#0", text="", anchor=tk.W)
        for col in columns:
            self.treeview.heading(col, text=col, anchor=tk.W)
            self.treeview.column(col, anchor=tk.W)

        for index, row in self.combined_df.iterrows():
            self.treeview.insert("", tk.END, text=index, values=row.tolist())
        self.treeview.column("#2", width=40)

    def close_window(self):
        self.root.destroy()   

"""Visualization of Main menu"""
class App:
    def __init__(self, start_saturday, start_sunday, end_saturday, end_sunday, dataframe, data_delay1, top_stops1, df1_sorted, df2):
        self.root = tk.Tk()
        self.root.title("Main menu")
        self.start_saturday = start_saturday
        self.start_sunday = start_sunday
        self.end_saturday = end_saturday
        self.end_sunday = end_sunday
        self.dataframe = dataframe
        self.data_delay1 = data_delay1
        self.top_stops1 = top_stops1
        self.df1_sorted = df1_sorted
        self.df2 = df2
        self.root.title = ("VBZ Delays")
        width=504
        height=195
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)
        background_image = ImageTk.PhotoImage(Image.open("bushaltestelle.jpg"))
        icon_path = "bus.ico"
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
        b_dataframe["text"] = "Compare Delays"
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
        Weeklymeandelay(stops, self.data_delay1)

    def b_bar_command(self):
        title1 =f'Top 10 Delays of Stations({self.start_sunday}-{self.start_saturday})'
        visualizer = Barvisualizer(self.top_stops1, title1)
        visualizer.plot_bar()

    def b_close_command(self):
        self.root.destroy()

    def b_dataframe_command(self):
        Visualization(self.df1_sorted, self.df2, self.start_saturday, self.start_sunday, self.end_saturday, self.end_sunday)

"""Creates the Barplot of the top 10 delays for the week"""
class Barvisualizer:
    def __init__(self, top_stops, title):
        self.df = top_stops
        self.title = title
    
    def plot_bar(self):
        x_values = self.df['stop']
        y_values = self.df['delay']
        max_value = max(y_values)
        plt.bar(x_values, y_values)
        for i,v in enumerate(y_values):
            plt.text(i,v, str(v), ha='center', va='bottom')
        plt.xlabel('Stations in Zurich')
        plt.ylabel('Delay in seconds')
        plt.title(self.title)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout() 
        plt.gca().xaxis.set_tick_params(pad=0)
        plt.ylim(top=max_value * 1.1)
        plt.show()

"""Autocomplete entrybox for the mean delay of a specific station"""
class Autocompleteentry(tk.Entry):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)

    def autocomplete(self, delta=0):
        if delta:
            self.delete(self.position, tk.END)
        else:
            self.position = len(self.get())
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):
                _hits.append(element)
        if _hits != self._hits:
            self._hit_index = 0
            self._hits =_hits
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        if self._hits:
            self.delete(0,tk.END)
            self.insert(0,self._hits[self._hit_index])
            self.select_range(self.position,tk.END)

    def handle_keyrelease(self, event):
        if event.keysym == "BackSpace":
            self.delete(self.index(tk.INSERT), tk.END)
            self.position = self.index(tk.END)
        if event.keysym == "Left":
            if self.position < self.index(tk.END):
                self.delete(self.position, tk.END)
            else:
                self.position = self.position-1
                self.delete(self.position, tk.END)
        if event.keysym == "Right":
            self.position = self.index(tk.END)
        if event.keysym == "Down":
            self.autocomplete(1)
        if event.keysym == "Up":
            self.autocomplete(-1)
        if len(event.keysym) == 1:
            self.autocomplete()

"""Visualization for the station search and mean delay plot of the station"""
class Weeklymeandelay:
    def __init__(self, dataframe, df1):
        self.dataframe = dataframe
        self.df = df1
        self.window = tk.Tk()
        self.label = tk.Label(self.window, text="Station:")
        self.label.pack()
        self.entry = Autocompleteentry(self.window)
        self.entry.set_completion_list(self.dataframe['stop'])
        self.entry.pack()
        self.entry.focus_set()
        self.window.bind('<Control-Q>', lambda event=None: self.window.destroy())
        self.window.bind('<Control-q>', lambda event=None: self.window.destroy())        
        self.search_button = tk.Button(self.window, text="Search", command=self.perform_search)
        self.search_button.pack()
        self.close_button = tk.Button(self.window, text="Close", command=self.close_window)
        self.close_button.pack()
        icon_path = "bus.ico"
        self.window.iconbitmap(icon_path)
        self.window.mainloop()
        
    """Search the selected station and plot the barplot"""
    def perform_search(self):
        search_term = self.entry.get()

        matches = get_close_matches(search_term, self.dataframe['stop'])
        if matches:
            match = matches[0]
            calc = calculations.Stopcalculation(self.df, match)
            barplot = calc.find_columns_with_same_value()
            x_values = barplot['betriebsdatum']
            y_values = barplot['delay'].round(1)
            plt.bar(x_values, y_values)
            for i, v in enumerate(y_values):
                plt.text(i, v, str(v), ha='center', va='bottom')
            plt.xlabel('Date')
            plt.ylabel('Mean delay in seconds')
            plt.title(f'Mean delays for {match}')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.gca().xaxis.set_tick_params(width=0.5)
            plt.gca().yaxis.set_tick_params(width=0.5)
            plt.show()
        else:
            messagebox.showinfo("Search Result", "No matching station found.")

    def close_window(self):
        self.window.destroy()

if __name__ == '__main__':
    pass

