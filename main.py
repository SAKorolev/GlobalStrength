


def add_material():
    en_material_name = tk.Entry(frame_material)
    en_material_name.insert(0, 'material ' + str(frame_material.grid_size()[1]))
    en_material_name.grid(row=frame_material.grid_size()[1], column=0)

# ['Name', 'Material', 'E, MPa', 'Sig, MPa', 'Tau, MPa', 'Thickness, mm']

def del_material():
    children = frame_material.winfo_children()
    widget = frame_material.focus_get()
    if widget in children:
        i = widget.grid_info()['row']
        for widget1 in children:
            if int(widget1.grid_info()['row']) == i:
                widget1.destroy()




if __name__ == '__main__':

    import tkinter as tk
    import tkinter.ttk as ttk



    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.title('GlobalStrength')

    frame_main = tk.Frame()
    frame_main.rowconfigure(0, weight=1)
    frame_main.columnconfigure(0, weight=1)
    frame_main.grid(row=0, column=0, sticky='wesn')
    # main sheets
    sheet = ttk.Notebook(frame_main)
    sheet_material = ttk.Frame(sheet)
    sheet.add(sheet_material,text='Materials')
    sheet_laminate = ttk.Frame(sheet)
    sheet.add(sheet_laminate,text='Laminates')
    sheet_elements = ttk.Frame(sheet)
    sheet.add(sheet_elements,text='Global strength')
    sheet.grid(row=0, column=0, sticky='snwe')
    # sheet materials
    frame_material_button = tk.Frame(sheet_material)
    frame_material_button.pack(side="top", fill='both')
    canvas_material = tk.Canvas(sheet_material, borderwidth=0)
    frame_material = tk.Frame(canvas_material)
    scroll_material_vertical = tk.Scrollbar(sheet_material, orient="vertical", command=canvas_material.yview)
    canvas_material.configure(yscrollcommand=scroll_material_vertical.set)
    scroll_material_vertical.pack(side="right", fill="y")
    canvas_material.pack(side="top", fill="both", expand=True)
    canvas_material.create_window((1, 1), window=frame_material, anchor="nw")
    frame_material.bind("<Configure>", lambda event: canvas_material.configure(scrollregion=canvas_material.bbox("all")))
        # buttons on materials sheet
    button_config = {'relief': 'solid', 'bd': 0, 'bg': '#DBDBDB', 'width': 3, 'pady': 4}
    tk.Button(frame_material_button, text='Add', **button_config, command=add_material).grid(row=0, column=0,
                                                                                                  padx=5, pady=5)
    tk.Button(frame_material_button, text='Del', **button_config, command=del_material).grid(row=0, column=1,
                                                                                                  padx=5, pady=5)
    title_material = ['Name', 'Material', 'E, MPa', 'Sig, MPa', 'Tau, MPa', 'Thickness, mm']
    for title in title_material:
        tk.Label(frame_material, text=title).grid(row=0, column=title_material.index(title))


    root.mainloop()