

def show_about():
    mb.showinfo('GlobalStrength', 'Developed by ANMC, 2022 - V1.01.')


def show_ask_exit():
    ask = mb.askyesnocancel('Quit', 'Do you want to save data?')
    if ask:
        save_file()
    elif ask is False:
        root.destroy()


def new_project():
    general.clear()
    mat.clear()
    lam.clear()
    elements.clear()
    wd_material.clear()
    wd_elements.clear()
    en_moment.delete(0, tk.END)
    en_moment.insert(0, 0)
    children = frame_material.winfo_children()
    for child in children:
        child.destroy()
    for title in title_material:
        tk.Label(frame_material, text=title).grid(row=0, column=title_material.index(title))
    children = frame_elements.winfo_children()
    for child in children:
        child.destroy()
    for title in title_elements:
        tk.Label(frame_elements, text=title).grid(row=0, column=title_elements.index(title))
    lb_lam1.delete(0, tk.END)
    lb_lam2.delete(0, tk.END)
    tree_laminate.delete(*tree_laminate.get_children())


def open_file():
    file_types = (("Project file", "*.json"),
                 ("Any", "*"))
    file_name = fd.askopenfilename(title="Open file", initialdir="/", filetypes=file_types)
    if file_name:
        new_project()
        with open(file_name, 'r') as file:
            input_data = json.load(file)
        open_project(input_data)


def open_project(input_data):
    # general
    en_moment.delete(0, tk.END)
    en_moment.insert(0, input_data['general'][moment])
    # materials
    mat.clear()
    for key in input_data['material']:
        row_number = frame_material.grid_size()[1]
        add_material_widgets(row_number)
        mat[key] = {}
        for title in title_material:
            mat[key][title] = input_data['material'][key][title]
            if title == material:
                wd_material[row_number][title].set(mat[key][title])
            else:
                wd_material[row_number][title].delete(0, tk.END)
                wd_material[row_number][title].insert(0, mat[key][title])
    # laminate
    lam.clear()
    for key in input_data['laminates']:
        lb_lam1.insert(tk.END, key)
        lam[key] = {}
        for position in input_data['laminates'][key]:
            lam[key][position] = input_data['laminates'][key][position]

    # elements
    for key in input_data['elements']:
        row_number = frame_elements.grid_size()[1]
        add_elements()
        for title in title_elements:
            if title == material or title == orientation:
                wd_elements[row_number][title].set(input_data['elements'][key][title])
            else:
                wd_elements[row_number][title].delete(0, tk.END)
                wd_elements[row_number][title].insert(0, input_data['elements'][key][title])


def save_file():
    file_types = (("Project file", "*.json"),
                 ("Any", "*"))
    file_name = fd.asksaveasfilename(title="Save file", initialdir="/", filetypes=file_types)

    output_data = dict()

    create_general_dict()
    output_data['general'] = general
    output_data['material'] = mat
    output_data['laminates'] = lam
    create_elements_dict()
    clear_result_element_dict()
    output_data['elements'] = elements

    dict_json = json.dumps(output_data)
    try:
        with open(file_name, "w") as file:
            file.write(dict_json)
    except FileNotFoundError:
        pass


def add_material():
    row_number = frame_material.grid_size()[1]
    add_material_widgets(row_number)
    add_material_dict(row_number)
    print(mat)


def add_material_widgets(row_number):
    wd_material[row_number] = {}
    for title in title_material:
        if title == material:
            wd_material[row_number][title] = ttk.Combobox(frame_material, width=15, values=list_material)
            wd_material[row_number][title].current(1)
            wd_material[row_number][title].grid(row=row_number, column=0)
            wd_material[row_number][title].bind('<<ComboboxSelected>>',
                                                lambda e, i=row_number, t=title: change_material_dict(e, i, t))
        # elif title == name:
        #     wd_material[row_number][title] = tk.Entry(frame_material, width=15)
        #     wd_material[row_number][title].insert(0, 'material ' + str(row_number))
        #     wd_material[row_number][title].grid(row=row_number, column=title_material.index(title), sticky='we')
        else:
            wd_material[row_number][title] = tk.Entry(frame_material, width=15)
            wd_material[row_number][title].insert(0, '0.00')
            wd_material[row_number][title].grid(row=row_number, column=title_material.index(title), sticky='we')
            wd_material[row_number][title].bind('<FocusOut>', lambda e, i=row_number, t=title: change_material_dict(e, i, t))
            wd_material[row_number][title].bind('<Return>', lambda e, i=row_number, t=title: change_material_dict(e, i, t))
    wd_material[row_number][name].delete(0, tk.END)
    wd_material[row_number][name].insert(0, 'material ' + str(row_number))
    wd_material[row_number][name].bind('<FocusIn>', lambda e, i=row_number: current_name_material(e, i))


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


def current_name_material(event, i):
    global current_name
    current_name = wd_material[i][name].get()


def change_material_dict(e, i, t):
    global current_name
    if t == name:
        mat[current_name][t] = wd_material[i][t].get()
        mat[wd_material[i][name].get()] = mat.pop(current_name)
    else:
        mat[wd_material[i][name].get()][t] = wd_material[i][t].get()
    print(mat)


def update_listbox_materials(e):
    lb_lam2.delete(0, tk.END)
    list_material_str.clear()
    for key in mat:
        if mat[key][material] == list_material[1]:
            lb_lam2.insert(tk.END, key)
        else:
            list_material_str.append(key)
    for key in lam:
        list_material_str.append(key)
    for key in wd_elements:
        wd_elements[key][material].configure(value=list_material_str)


def add_laminate():
    lam['laminate ' + str(lb_lam1.index(tk.END))] = {}
    lb_lam1.insert(tk.END, 'laminate ' + str(lb_lam1.index(tk.END)))
    en_laminate_name.delete(0, tk.END)
    en_laminate_name.insert(0, lb_lam1.get(tk.END))
    tree_laminate.delete(*tree_laminate.get_children())
    print(lam)


def del_laminate():
    if lb_lam1.curselection():
        i = lb_lam1.curselection()[0]
        del lam[lb_lam1.get(i)]
        lb_lam1.delete(i)
    print(lam)


def add_layer_in_laminate(e = None):
    if lb_lam2.curselection() and lb_lam1.get(0):
        i = lb_lam2.curselection()[0]
        tree_laminate.insert("", index='end', values=(lb_lam2.get(i), mat[lb_lam2.get(i)]['Thickness, mm']))
        lam[en_laminate_name.get()] = {}
        i = 0
        for child in tree_laminate.get_children():
            lam[en_laminate_name.get()][i] = tree_laminate.item(child)['values'][0]
            i += 1
    print(lam)


def select_laminate(e):
    if lb_lam1.curselection():
        i = lb_lam1.curselection()[0]
        if root.focus_get() == en_laminate_name:
            en_laminate_name.event_generate('<FocusOut>', when='now')
        en_laminate_name.delete(0, tk.END)
        en_laminate_name.insert(0, lb_lam1.get(i))
        tree_laminate.delete(*tree_laminate.get_children())
        for i in lam[lb_lam1.get(i)]:
            tree_laminate.insert("", index='end',
                        values=(lam[en_laminate_name.get()][i], mat[lam[en_laminate_name.get()][i]][thickness]))


def current_name_laminate(event):
    global current_name
    current_name = en_laminate_name.get()



def change_laminate_name(event):
    if lb_lam1.get(0):
        global current_name
        if root.focus_get() != lb_lam1:
            if en_laminate_name.get() != current_name:
                used_name = False
                for laminate in lam:
                    if en_laminate_name.get() == laminate:
                        used_name = True
                if used_name == True:
                    en_laminate_name.delete(0, tk.END)
                    en_laminate_name.insert(0, current_name)
                else:
                    lam[en_laminate_name.get()] = lam.pop(current_name)
                    for elem_name in elements:
                        if elements[elem_name][material] == current_name:
                            elements[elem_name][material] = en_laminate_name.get()
                    current_name = en_laminate_name.get()
                    lb_lam1.delete(0, tk.END)
                    for laminate in lam:
                        lb_lam1.insert(tk.END, laminate)


def del_layer_in_laminate():
    if tree_laminate.selection():
        tree_laminate.delete(tree_laminate.selection()[0])
        lam[en_laminate_name.get()] = {}
        i = 0
        for child in tree_laminate.get_children():
            lam[en_laminate_name.get()][i] = tree_laminate.item(child)['values'][0]
            i += 1
    print(lam)


def up_layer_in_laminate():
    if tree_laminate.selection():
        row = tree_laminate.selection()
        tree_laminate.move(row[0], tree_laminate.parent(row[0]), tree_laminate.index(row[0]) - 1)
        lam[en_laminate_name.get()] = {}
        i = 0
        for child in tree_laminate.get_children():
            lam[en_laminate_name.get()][i] = tree_laminate.item(child)['values'][0]
            i += 1
    print(lam)


def down_layer_in_laminate():
    if tree_laminate.selection():
        row = tree_laminate.selection()
        tree_laminate.move(row[0], tree_laminate.parent(row[0]), tree_laminate.index(row[0]) + 1)
        lam[en_laminate_name.get()] = {}
        i = 0
        for child in tree_laminate.get_children():
            lam[en_laminate_name.get()][i] = tree_laminate.item(child)['values'][0]
            i += 1
    print(lam)


def calc_thickness_lam(lam_name):
    lam_thickness = 0
    for ply in lam[lam_name]:
        lam_thickness += float(mat[lam[lam_name][ply]][thickness])
    return lam_thickness


def calc_E_lam(lam_name):
    lam_thickness = 0
    lam_Ethickness = 0
    for ply in lam[lam_name]:
        lam_thickness += float(mat[lam[lam_name][ply]][thickness])
        lam_Ethickness += float(mat[lam[lam_name][ply]][thickness])*float(mat[lam[lam_name][ply]][mod_e])
    return (lam_Ethickness/lam_thickness)


def add_elements():
    row_number = frame_elements.grid_size()[1]
    wd_elements[row_number] = {}
    for title in title_elements:
        if title == material:
            wd_elements[row_number][title] = ttk.Combobox(frame_elements, width=10, values=list_material_str)
            wd_elements[row_number][title].grid(row=row_number, column=title_elements.index(title), sticky='we')
            wd_elements[row_number][title].bind('<<ComboboxSelected>>',
                                                    lambda e, i=row_number, t=title: change_material_str(e, i, t))
        elif title == orientation:
            wd_elements[row_number][title] = ttk.Combobox(frame_elements, width=10, values=orientation_element)
            wd_elements[row_number][title].current(0)
            wd_elements[row_number][title].grid(row=row_number, column=title_elements.index(title), sticky='we')
            wd_elements[row_number][title].bind('<<ComboboxSelected>>',
                                                lambda e, i=row_number: change_orientation_str(e, i))
        elif title == name:
            wd_elements[row_number][title] = tk.Entry(frame_elements, width=12)
            wd_elements[row_number][title].insert(0, 'element ' + str(row_number))
            wd_elements[row_number][title].grid(row=row_number, column=title_elements.index(title), sticky='we')
        else:
            wd_elements[row_number][title] = tk.Entry(frame_elements, width=12)
            wd_elements[row_number][title].insert(0, 0)
            wd_elements[row_number][title].grid(row=row_number, column=title_elements.index(title), sticky='we')

    wd_elements[row_number][qty].delete(0, tk.END)
    wd_elements[row_number][qty].insert(0, 1)


def del_elements():
    pass


def change_material_str(e, i, t):
    elem_name = wd_elements[i][t].get()
    if elem_name in mat:
        wd_elements[i][mod_e].delete(0, tk.END)
        wd_elements[i][mod_e].insert(0, mat[elem_name][mod_e])
    else:
        wd_elements[i][mod_e].delete(0, tk.END)
        wd_elements[i][mod_e].insert(0, calc_E_lam(elem_name))
        if wd_elements[i][orientation].get() == orientation_element[0]:
            wd_elements[i][height].delete(0, tk.END)
            wd_elements[i][height].insert(0, calc_thickness_lam(elem_name))
        else:
            wd_elements[i][breadth].delete(0, tk.END)
            wd_elements[i][breadth].insert(0, calc_thickness_lam(elem_name))


def change_orientation_str(e, i):
    elem_breadth = wd_elements[i][breadth].get()
    elem_height = wd_elements[i][height].get()
    wd_elements[i][breadth].delete(0, tk.END)
    wd_elements[i][breadth].insert(0, elem_height)
    wd_elements[i][height].delete(0, tk.END)
    wd_elements[i][height].insert(0, elem_breadth)


def calc_sum_column_elements(title):
    sum_elements = 0
    for key in elements:
        sum_elements += float(elements[key][title])
    return sum_elements


def clear_result_element_dict():
    for elem_name in elements:
        for title in title_result:
            elements[elem_name][title] = 0


def create_elements_dict():
    elements.clear()
    for key in wd_elements:
        elem_name = wd_elements[key][name].get()
        elements[elem_name] = {}
        for title in wd_elements[key]:
            if is_digit(wd_elements[key][title].get()):
                elements[elem_name][title] = float(wd_elements[key][title].get())
            else:
                elements[elem_name][title] = wd_elements[key][title].get()


def create_general_dict():
    general.clear()
    general[moment] = float(en_moment.get())


def calculate():
    create_elements_dict()
    create_general_dict()
    for elem_name in elements:
        elements[elem_name][area_f] = elements[elem_name][breadth] * elements[elem_name][height]
        elements[elem_name][ef] = elements[elem_name][area_f] * elements[elem_name][mod_e]
        elements[elem_name][efz] = elements[elem_name][ef] * elements[elem_name][dist_z]
        elements[elem_name][efz2] = elements[elem_name][efz] * elements[elem_name][dist_z]
        elements[elem_name][ebh3] = elements[elem_name][mod_e] * \
                                    elements[elem_name][breadth] * elements[elem_name][height]**3 / 12
    results[zna] = calc_sum_column_elements(efz) / calc_sum_column_elements(ef)
    results[ei_na] = calc_sum_column_elements(efz2) + calc_sum_column_elements(ebh3) - results[zna] **2 * calc_sum_column_elements(ef)
    for key in wd_elements:
        elem_name = wd_elements[key][name].get()
        if (elements[elem_name][dist_z] - results[zna]) >= 0:
            elements[elem_name][dist_zna] = elements[elem_name][dist_z] - results[zna] + elements[elem_name][height]/2
        else:
            elements[elem_name][dist_zna] = elements[elem_name][dist_z] - results[zna] - elements[elem_name][height]/2
        elements[elem_name][sig_act] = general[moment] / results[ei_na] * elements[elem_name][dist_zna] * elements[elem_name][mod_e]
    show_result()


def show_result():
    for key in wd_elements:
        elem_name = wd_elements[key][name].get()
        for title in title_result:
            wd_elements[key][title].delete(0, tk.END)
            wd_elements[key][title].insert(0, f'{elements[elem_name][title]:.3e}')
            en_result_zna.delete(0, tk.END)
            en_result_zna.insert(0, f'{results[zna]:.2f}')
            en_result_ei_na.delete(0, tk.END)
            en_result_ei_na.insert(0, f'{results[ei_na]:.2f}')


def export_results():
    pass


def export_materials():
    pass


def is_digit(string):
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def show_picture():
    canvas_picture.delete(tk.ALL)
    min_z = 0
    max_z = 0
    create_elements_dict()
    for elem_name in elements:
        if elements[elem_name][orientation] == orientation_element[1]:
            coord_z1 = (elements[elem_name][dist_z] - elements[elem_name][height]/2)
            coord_z2 = (elements[elem_name][dist_z] + elements[elem_name][height]/2)
        else:
            coord_z1 = (elements[elem_name][dist_z])
            coord_z2 = (elements[elem_name][dist_z])
        min_z = min(min_z, coord_z1, coord_z2)
        max_z = max(max_z, coord_z1, coord_z2)
    field = 10
    offset = 250
    scale = offset / (max_z - min_z)

    for elem_name in elements:
        if elements[elem_name][orientation] == orientation_element[1]:
            coord_z1 = (elements[elem_name][dist_z] - elements[elem_name][height]/2)*scale * -1 + offset + field
            coord_y1 = (elements[elem_name][dist_y])*scale + field
            coord_z2 = (elements[elem_name][dist_z] + elements[elem_name][height]/2)*scale * -1 + offset + field
            coord_y2 = (elements[elem_name][dist_y])*scale + field
        else:
            coord_z1 = (elements[elem_name][dist_z])*scale * -1 + offset + field
            coord_y1 = (elements[elem_name][dist_y] - elements[elem_name][breadth] / 2)*scale + field
            coord_z2 = (elements[elem_name][dist_z])*scale * -1 + offset + field
            coord_y2 = (elements[elem_name][dist_y] + elements[elem_name][breadth] / 2)*scale + field
        canvas_picture.create_line(coord_y1, coord_z1, coord_y2, coord_z2, fill='green', width=3)


if __name__ == '__main__':
    import tkinter.filedialog as fd
    import tkinter.messagebox as mb
    import tkinter as tk
    import tkinter.ttk as ttk
    import json

    name = 'Name'
    material = 'Material'
    thickness = 'Thickness, mm'
    mod_e = 'E, MPa'
    orientation = 'Orientation'
    qty  = 'Qty'
    breadth = 'b, mm'
    height = 'h, mm'
    dist_z = 'z, mm'
    dist_y = 'y, mm'
    area_f = 'F, mm2'
    ef = 'EF, N'
    efz = 'EFz, Nmm'
    efz2 = 'EFz2, Nmm2'
    ebh3 = 'Eh3/12, Nmm2'
    dist_zna = 'zna, mm'
    sig_act = 'Sig, MPa'
    moment = 'Bending moment'
    zna = 'zna'
    ei_na = 'ei_na'
    title_material = [material, name, mod_e, 'Sig, MPa', 'Tau, MPa', thickness]
    title_elements = [name, material, orientation, breadth, height, qty, dist_y, dist_z, mod_e,
                      area_f, ef,  efz, efz2, ebh3, dist_zna, sig_act]
    title_result = [area_f, ef, efz, efz2, ebh3, dist_zna, sig_act]
    list_material = ['Metal', 'FRP']
    list_material_str = []
    orientation_element = ['horizontal', 'vertical']
    wd_material = {}
    wd_elements = {}
    general = {}
    lam = {}
    mat = {}
    elements = {}
    results = {}
    current_name = ''


    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.title('GlobalStrength')

    main_menu = tk.Menu(root)
    root.config(menu=main_menu)
    file_menu = tk.Menu(main_menu, tearoff=0)
    result_menu = tk.Menu(main_menu, tearoff=0)
    file_menu.add_command(label="New project", command=new_project)
    file_menu.add_separator()
    file_menu.add_command(label="Open project", command=open_file)
    file_menu.add_command(label="Save project", command=save_file)
    file_menu.add_separator()
    result_menu.add_command(label='Export calculation to Excel', command=export_results)
    result_menu.add_command(label='Export materials data to Excel', command=export_materials)
    file_menu.add_command(label="Exit", command=show_ask_exit)
    main_menu.add_cascade(label="File", menu=file_menu)
    main_menu.add_command(label='Calculate', command=calculate)
    main_menu.add_cascade(label='Export title_result', menu=result_menu)
    main_menu.add_command(label='About...', command=show_about)

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
    # sheet general
    frame_general = tk.Frame(sheet_general)
    frame_general.grid(row=0, column=0, sticky='nsew')
    lb_moment = tk.Label(frame_general, text='Bending mement, Nmm')
    lb_moment.grid(row=0, column=0)
    en_moment = tk.Entry(frame_general)
    en_moment.grid(row=0, column=1)
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
        tk.Label(frame_material, anchor='w', width= 15, height=1, relief='solid',
             bd=0.5, text=title).grid(row=0, column=title_material.index(title))

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
        # picture
    canvas_picture = tk.Canvas(sheet_elements, borderwidth=1, bg = 'grey')
    canvas_picture.pack(side="right", fill="both", expand=True)
        # title_result
    frame_elements_result = tk.Frame(sheet_elements, bg='yellow')
    frame_elements_result.pack(side="left", fill='both')
    tk.Label(frame_elements_result, text='Position of neutral axis above base, z0, mm', anchor='w').grid(row=0, column=0)
    en_result_zna = tk.Entry(frame_elements_result)
    en_result_zna.grid(row=0, column=1, padx=10, pady=5)
    tk.Label(frame_elements_result, text='Stiffness EIx about neutral axis, N*mm2', anchor='w').grid(row=1, column=0)
    en_result_ei_na = tk.Entry(frame_elements_result)
    en_result_ei_na.grid(row=1, column=1, padx=10, pady=5)

        # buttons and title on strength sheet
    tk.Button(frame_elements_button, text='Add', **button_config, command=add_elements).grid(row=0, column=0,
                                                                                             padx=5, pady=5)
    tk.Button(frame_elements_button, text='Del', **button_config, command=del_elements).grid(row=0, column=1,
                                                                                             padx=5, pady=5)
    tk.Button(frame_elements_button, text='Show', **button_config, command=show_picture).grid(row=0, column=2,
                                                                                             padx=5, pady=5)
    for title in title_elements:
        tk.Label(frame_elements, anchor='w', width= 12, height=1, relief='solid',
             bd=0.5, text=title).grid(row=0, column=title_elements.index(title))
    en_elements = {}

    root.mainloop()