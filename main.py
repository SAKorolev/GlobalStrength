

def add_material():
    row_number = frame_material.grid_size()[1]
    add_material_widgets(row_number)
    add_material_dict(row_number)
    print(mat)


def add_material_widgets(row_number):
    wd_material[row_number] = {}
    for title in title_material:
        match title:
            case 'Material':
                tuple_material = ('Metal', 'FRP')
                wd_material[row_number][title] = ttk.Combobox(frame_material, values=tuple_material)
                wd_material[row_number][title].current(1)
                wd_material[row_number][title].grid(row=row_number, column=0)
                wd_material[row_number][title].bind('<<ComboboxSelected>>',
                                                    lambda e, i=row_number, t=title: change_material_dict(e, i, t))
            case 'Name':
                wd_material[row_number][title] = tk.Entry(frame_material)
                wd_material[row_number][title].insert(0, 'material ' + str(row_number))
                wd_material[row_number][title].grid(row=row_number, column=title_material.index(title))
            case _:
                wd_material[row_number][title] = tk.Entry(frame_material)
                wd_material[row_number][title].insert(0, '0.00')
                wd_material[row_number][title].grid(row=row_number, column=title_material.index(title))
                wd_material[row_number][title].bind('<FocusOut>', lambda e, i=row_number, t=title: change_material_dict(e, i, t))
                wd_material[row_number][title].bind('<Return>', lambda e, i=row_number, t=title: change_material_dict(e, i, t))


def add_material_dict(row_number):
    mat[wd_material[row_number][name].get()] = {}
    for title in title_material:
        mat[wd_material[row_number][name].get()][title] = wd_material[row_number][title].get()


def del_material():
    children = frame_material.winfo_children()
    widget = frame_material.focus_get()
    if widget in children:
        i = widget.grid_info()['row']
        del mat[wd_material[i][name].get()]
        del wd_material[i]
        for widget1 in children:
            if int(widget1.grid_info()['row']) == i:
                widget1.destroy()
    print(mat)


def change_material_dict(e, i, t):
    mat[wd_material[i][name].get()][t] = wd_material[i][t].get()
    print(mat)


def update_listbox_materials(e):
    lb_lam2.delete(0, tk.END)
    for key in mat:
        lb_lam2.insert(tk.END, key)


def add_laminate():
    pass


def del_laminate():
    pass


def add_layer_in_laminate():
    pass


def select_laminate():
    pass


def current_name_laminate():
    pass


def change_laminate_name():
    pass


def del_layer_in_laminate():
    pass


def up_layer_in_laminate():
    pass


def down_layer_in_laminate():
    pass


def add_elements():
    row_number = frame_elements.grid_size()[1]
    en_elements[row_number] = {}
    for title in title_elements:
        match title:
            case 'Material':
                cb_elements = ttk.Combobox(frame_elements)#, values=tuple_material)
                # cb_elements.current(1)
                cb_elements.grid(row=row_number, column=0)
            case 'Name':
                en_elements[row_number][title] = tk.Entry(frame_elements)
                en_elements[row_number][title].insert(0, 'element ' + str(row_number))
                en_elements[row_number][title].grid(row=row_number, column=title_elements.index(title))
            case _:
                en_elements[row_number][title] = tk.Entry(frame_elements, width=10)
                en_elements[row_number][title].insert(0, '0.00')
                en_elements[row_number][title].grid(row=row_number, column=title_elements.index(title))


def del_elements():
    pass


if __name__ == '__main__':

    import tkinter as tk
    import tkinter.ttk as ttk

    name = 'Name'
    material = 'Material'
    title_material = ['Material', 'Name', 'E, MPa', 'Sig, MPa', 'Tau, MPa', 'Thickness, mm']
    wd_material = {}
    mat = {}

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
    sheet_general = ttk.Frame(sheet)
    sheet.add(sheet_general, text='General')
    sheet_material = ttk.Frame(sheet)
    sheet.add(sheet_material,text='Materials')
    sheet_laminate = ttk.Frame(sheet)
    sheet.add(sheet_laminate,text='Laminates')
    sheet_elements = ttk.Frame(sheet)
    sheet.add(sheet_elements,text='Global strength')
    sheet.grid(row=0, column=0, sticky='snwe')
    sheet.bind('<<NotebookTabChanged>>', update_listbox_materials)
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
        # buttons and title on materials sheet
    button_config = {'relief': 'solid', 'bd': 0, 'bg': '#DBDBDB', 'width': 3, 'pady': 4}
    tk.Button(frame_material_button, text='Add', **button_config, command=add_material).grid(row=0, column=0,
                                                                                                  padx=5, pady=5)
    tk.Button(frame_material_button, text='Del', **button_config, command=del_material).grid(row=0, column=1,
                                                                                                  padx=5, pady=5)
    for title in title_material:
        tk.Label(frame_material, text=title).grid(row=0, column=title_material.index(title))

    # sheet laminate
    sheet_laminate.rowconfigure(1, weight=1)
    sheet_laminate.columnconfigure(0, minsize=200)
    sheet_laminate.columnconfigure(1, minsize=250)
    sheet_laminate.columnconfigure(2, weight=1)

        # laminate names
    frame_laminate_name = tk.LabelFrame(sheet_laminate, text='Laminates')
    frame_laminate_name.grid(row=0, column=0, sticky='nsew')
    frame_laminate_name.rowconfigure(1, weight=1)
    frame_laminate_name.columnconfigure(0, weight=1)
    frame_laminate_name_button = tk.Frame(frame_laminate_name)
    frame_laminate_name_button.grid(row=0, column=0, sticky='ew')
    tk.Button(frame_laminate_name_button, text='Add', **button_config, command=add_laminate).grid(row=0, column=0,
                                                                                               padx=5, pady=5)
    tk.Button(frame_laminate_name_button, text='Del', **button_config, command=del_laminate).grid(row=0,
                                                                                               column=1, padx=5, pady=5)
    frame_laminate_name_lb1 = tk.Frame(frame_laminate_name)
    frame_laminate_name_lb1.grid(row=1, column=0, sticky='ewns')
    frame_laminate_name_lb1.rowconfigure(0, weight=1)
    frame_laminate_name_lb1.columnconfigure(0, weight=1)
    sb3 = ttk.Scrollbar(frame_laminate_name_lb1)
    sb3.grid(row=0, column=1, sticky='ns')
    lb_lam1 = tk.Listbox(frame_laminate_name_lb1, yscrollcommand=sb3.set, selectmode='single')
    sb3.config(command=lb_lam1.yview)
    lb_lam1.grid(row=0, column=0, padx=2, pady=5, sticky='ewns')
    lb_lam1.bind('<<ListboxSelect>>', select_laminate)

        # layers
    frame_laminate_layer = tk.LabelFrame(sheet_laminate, text='Layers')
    frame_laminate_layer.grid(row=0, column=1, sticky='nsew')
    frame_laminate_layer.rowconfigure(0, weight=1)
    frame_laminate_layer.columnconfigure(0, weight=1)
    sb4 = ttk.Scrollbar(frame_laminate_layer)
    sb4.grid(row=0, column=1, sticky='sn')
    lb_lam2 = tk.Listbox(frame_laminate_layer, yscrollcommand=sb4.set, selectmode='single')
    sb4.config(command=lb_lam2.yview)
    lb_lam2.bind('<Double-Button-1>', add_layer_in_laminate)

    lb_lam2.grid(row=0, column=0, padx=2, pady=5, sticky='snwe')
    tk.Button(frame_laminate_layer, text='Add', **button_config, command=add_layer_in_laminate).grid(row=0,
                                                                                                  column=2, padx=10)
        # structure of the laminate
    frame_laminate_structure = tk.LabelFrame(sheet_laminate, text='Laminate')
    frame_laminate_structure.grid(row=0, column=2, sticky='nsew')

    tk.Label(frame_laminate_structure, text='Label: ').grid(row=0, column=0, sticky='w')
    en_laminate_name = tk.Entry(frame_laminate_structure)
    en_laminate_name.grid(row=0, column=1, sticky='w')
    en_laminate_name.bind('<Return>', change_laminate_name)
    en_laminate_name.bind('<FocusOut>', change_laminate_name)
    en_laminate_name.bind('<FocusIn>', current_name_laminate)

    frame_laminate_structure_button = tk.Frame(frame_laminate_structure)
    frame_laminate_structure_button.grid(row=2, column=0, columnspan=3, sticky='w')
    tk.Button(frame_laminate_structure_button, text='Del', **button_config, command=del_layer_in_laminate) \
        .grid(row=2, column=0, padx=5, pady=5)
    tk.Button(frame_laminate_structure_button, text='Up', **button_config, command=up_layer_in_laminate) \
        .grid(row=2, column=1, padx=5, pady=5)
    tk.Button(frame_laminate_structure_button, text='Dn', **button_config, command=down_layer_in_laminate) \
        .grid(row=2, column=2, padx=5, pady=5)

    frame_laminate_structure_tree = tk.Frame(frame_laminate_structure)
    frame_laminate_structure_tree.grid(row=3, column=0, rowspan=2, columnspan=10, sticky='nsew')
    sb = ttk.Scrollbar(frame_laminate_structure_tree, orient='vertical')
    sb.pack(side='right', fill='y')
    tree_laminate = ttk.Treeview(frame_laminate_structure_tree, show="headings", columns=("#1", "#2", "#3"))
    tree_laminate.column(0, width=250)
    tree_laminate.column(1)
    tree_laminate.heading("#1", text="Layer")
    tree_laminate.heading("#2", text="Thickness, mm")
    tree_laminate.pack(side='left')
    tree_laminate.config(yscrollcommand=sb.set)
    sb.config(command=tree_laminate.yview)
    tk.Label(frame_laminate_structure, text='outer').grid(row=3, column=11, sticky='n')
    tk.Label(frame_laminate_structure, text='inner').grid(row=4, column=11, sticky='s')

    # sheet global strength
    frame_elements_button = tk.Frame(sheet_elements)
    frame_elements_button.pack(side="top", fill='both')

    canvas_elements = tk.Canvas(sheet_elements, borderwidth=0)
    frame_elements = tk.Frame(canvas_elements)
    scroll_elements_vertical = tk.Scrollbar(sheet_elements, orient="vertical", command=canvas_elements.yview)
    canvas_elements.configure(yscrollcommand=scroll_elements_vertical.set)
    scroll_elements_vertical.pack(side="right", fill="y")
    canvas_elements.pack(side="top", fill="both", expand=True)
    canvas_elements.create_window((1, 1), window=frame_elements, anchor="nw")
    frame_elements.bind("<Configure>",
                        lambda event: canvas_elements.configure(scrollregion=canvas_elements.bbox("all")))

    canvas_picture = tk.Canvas(sheet_elements, borderwidth=1)
    canvas_picture.pack(side="top", fill="both", expand=True)
    canvas_picture.create_line(0,0,500,200, fill='green', width=3)
    # buttons and title on strength sheet
    tk.Button(frame_elements_button, text='Add', **button_config, command=add_elements).grid(row=0, column=0,
                                                                                             padx=5, pady=5)
    tk.Button(frame_elements_button, text='Del', **button_config, command=del_elements).grid(row=0, column=1,
                                                                                             padx=5, pady=5)

    title_elements = ['Material', 'Name', 'Angle, deg',  'b, mm', 'h, mm', 'Qty', 'z, mm', 'E, MPa',
                      'F, mm2', 'Fz, mm3', 'Fz2, mm4', 'bh3/12, mm4', 'zna, mm', 'Sig, MPa']
    for title in title_elements:
        tk.Label(frame_elements, width=10, text=title).grid(row=0, column=title_elements.index(title))
    en_elements = {}

    root.mainloop()