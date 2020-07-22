import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from Analysis import Analysis
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from PIL import Image, ImageTk


class AppGUI:
    def startGraph(self):
        plt.style.use('dark_background')
        for widgets in self.display_frame.winfo_children():
            widgets.destroy()
        years = ["2016", "2017", "2018"]
        total = []
        for year in years:
            total_per_year = self.A.maxperyear(year)
            total.append(total_per_year)
        f = Figure(figsize=(3, 4), dpi=100)
        a = f.add_subplot(111)
        a.set_xlabel("Years")
        a.set_ylabel("Max")
        a.set_title("Max per Year")
        a.plot(years, total)
        canvas = FigureCanvasTkAgg(f, self.display_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side='right', fill='both', expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self.display_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
        self.message.set("Successfully graph data")

    def startSort(self):
        for widgets in self.display_frame.winfo_children():
            widgets.destroy()
        self.A.setYear(self.year_click.get())
        self.data = self.A.read()
        self.sortedData = self.A.sort(self.data)
        self.drawTable(self.sortedData)
        self.message.set("Successfully sort data")

    def startRead(self):
        for widgets in self.display_frame.winfo_children():
            widgets.destroy()
        self.data = self.A.read()
        self.drawTable(self.data)
        self.message.set("Successfully read data")

    def findMax(self):
        for widgets in self.display_frame.winfo_children():
            widgets.destroy()
        self.A.setYear(self.year_click.get())
        self.data = self.A.read()
        self.sortedData = self.A.sort(self.data)
        self.A.mapPrep(self.sortedData)

        self.image = Image.open('Map.gif')
        self.img_copy = self.image.copy
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = tk.Label(self.display_frame, image = self.background_image)
        self.background.pack(fill='both',expand = True)
        self.background.bind('<Configure>', self._resize_image)

        self.message.set("Successfully map data")

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height
        self.image = self.image.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image = self.background_image)


    # Drawing table
    def drawTable(self, df):
        self.cols = list(df.columns)
        self.table = ttk.Treeview(self.display_frame, style='style.Treeview')

        self.table['columns'] = self.cols
        self.table['show'] = 'headings'
        for i in self.cols:
            self.table.column(i, anchor='n', width=25)
            self.table.heading(i, text=i, anchor='n')

        for index, row in df.iterrows():
            self.table.insert('', index, text=index, values=list(row))

        self.table.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.tablescroll = ttk.Scrollbar(self.display_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=self.tablescroll.set)
        self.tablescroll.pack(side='left', fill='y')

    def changeType(self, event):
        self.A.setType(self.type_click.get())

    def changeYear(self, event):
        self.A.setYear(self.year_click.get())

    def __init__(self, master):

        self.A = Analysis()
        master.title("Calgary Traffic and Incident")
        master.geometry("1124x768")

        # Theme set-up
        ttk.Style().configure('display.TFrame', background="#addbcb")

        # Treeview Style
        treestyle = ttk.Style()
        treestyle.configure("style.Treeview", highlightthickness=0, bd=0, background='#d8ede6')
        treestyle.configure("style.Treeview.Heading", font=('Arial', 12, 'bold'), foreground='#216e54')

        # Frame for button
        self.button_frame = ttk.Frame(master)
        self.button_frame.place(relwidth=0.25, relheight=1, anchor='nw')

        # Type of analysis button
        self.type_click = tk.StringVar()
        self.type_drop = ttk.Combobox(self.button_frame, state="readonly", width=20, textvariable=self.type_click)
        self.type_drop['values'] = ('Volume Analysis',
                                    'Incident Analysis')
        self.type_drop.current(0)
        self.type_drop.place(relwidth=0.8, relx=0.05, rely=0.1)
        self.type_drop.bind('<<ComboboxSelected>>', self.changeType)

        # Year button
        self.year_click = tk.StringVar()
        self.year_drop = ttk.Combobox(self.button_frame, state="readonly", width=20, textvariable=self.year_click)
        self.year_drop['values'] = ('2016',
                                    '2017',
                                    '2018')
        self.year_drop.current(0)
        self.year_drop.place(relwidth=0.8, relx=0.05, rely=0.2)
        self.year_drop.bind('<<ComboboxSelected>>', self.changeYear)

        # Read button
        self.read_button = ttk.Button(self.button_frame, cursor="hand1", text="Read",
                                      command=self.startRead)
        self.read_button.place(relwidth=0.8, relx=0.05, rely=0.3)

        # Sort button
        self.sort_button = ttk.Button(self.button_frame, cursor="hand1", text="Sort",
                                      command=self.startSort)
        self.sort_button.place(relwidth=0.8, relx=0.05, rely=0.4)

        # Analysis button
        self.analysis_button = ttk.Button(self.button_frame, cursor="hand1", text="Analysis",
                                          command=self.startGraph)
        self.analysis_button.place(relwidth=0.8, relx=0.05, rely=0.5)

        # Map button
        self.map_button = ttk.Button(self.button_frame, cursor="hand1", text="Map"
                                     ,command = self.findMax)
        self.map_button.place(relwidth=0.8, relx=0.05, rely=0.6)

        # Status label
        self.status_label = ttk.Label(self.button_frame, text="Status:")
        self.status_label.place(relx=0.05, rely=0.68)

        # Message label
        self.message = tk.StringVar()
        self.message.set("Loading...")
        self.message_label = ttk.Label(self.button_frame, textvariable=self.message, background="yellow")
        self.message_label.place(relx=0.05, rely=0.73)

        # display frame
        self.display_frame = ttk.Frame(master, style='display.TFrame')
        self.display_frame.place(relx=0.25, relwidth=0.75, relheight=1, anchor='nw')


root = ThemedTk(theme='arc')
AppGUI(root)
root.mainloop()
