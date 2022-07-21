

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
    sections.clear()
    calculations.clear()
    wd_material.clear()
    wd_elements.clear()
    wd_calculation.clear()

    children = frame_material.winfo_children()
    for child in children:
        if child.winfo_class() != 'Label':
            child.destroy()
    children = frame_elements.winfo_children()
    for child in children:
        if child.winfo_class() != 'Label':
            child.destroy()
    children = frame_calculation.winfo_children()
    for child in children:
        if child.winfo_class() != 'Label':
            child.destroy()
    lb_lam1.delete(0, tk.END)
    lb_lam2.delete(0, tk.END)
    lb_section.delete(0, tk.END)
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
    # en_moment.delete(0, tk.END)
    # en_moment.insert(0, input_data['general'][moment])
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
    update_listbox_materials()

    # sections
    for name_section in input_data['sections']:
        wd_elements[name_section] = {}
        en_section_name.delete(0, tk.END)
        en_section_name.insert(0, name_section)

        lb_section.insert(tk.END, name_section)

        for key in input_data['sections'][name_section]:
            row_number = frame_elements.grid_size()[1]
            add_elements()
            for title in title_elements:
                if title == material or title == orientation or title == location:
                    wd_elements[name_section][row_number][title].set(input_data['sections'][name_section][key][title])
                elif title == name:
                    wd_elements[name_section][row_number][title].delete(0, tk.END)
                    wd_elements[name_section][row_number][title].insert(0, input_data['sections'][name_section][key][title])
                else:
                    wd_elements[name_section][row_number][title].delete(0, tk.END)
                    wd_elements[name_section][row_number][title].insert(0, f"{input_data['sections'][name_section][key][title]:.3f}")
        clear_element_widgets()

    # calculation
    for name_calc in input_data['calculations']:
        row_number = frame_calculation.grid_size()[1]
        add_calculation()

        for title in title_calculation:
            if title == section:
                wd_calculation[row_number][title].set(input_data['calculations'][name_calc][title])
            else:
                wd_calculation[row_number][title].delete(0, tk.END)
                wd_calculation[row_number][title].insert(0, input_data['calculations'][name_calc][title])


def save_file():
    file_types = (("Project file", "*.json"),
                 ("Any", "*"))
    file_name = fd.asksaveasfilename(title="Save file", initialdir="/", filetypes=file_types)

    output_data = dict()

    create_general_dict()
    output_data['general'] = general
    output_data['material'] = mat
    output_data['laminates'] = lam
    create_sections_dict()
    output_data['sections'] = sections
    create_calculation_dict()
    output_data['calculations'] = calculations

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


def update_listbox(event):
    update_listbox_materials()
    update_listbox_calculation()


def update_listbox_materials(event=None):
    lb_lam2.delete(0, tk.END)
    list_material_calc.clear()
    for key in mat:
        if mat[key][material] == list_material[1]:
            lb_lam2.insert(tk.END, key)
        else:
            list_material_calc.append(key)
    for key in lam:
        list_material_calc.append(key)
    for name_section in wd_elements:
        for key in wd_elements[name_section]:
            wd_elements[name_section][key][material].configure(value=list_material_calc)


def update_listbox_calculation(event=None):
    list_section = []
    for key in wd_elements:
        list_section.append(key)
    for key in wd_calculation:
        wd_calculation[key][section].configure(value=list_section)


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
                    for elem_name in sections:
                        if sections[elem_name][material] == current_name:
                            sections[elem_name][material] = en_laminate_name.get()
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


def add_section():
    name_section = 'section' + str(lb_section.index(tk.END))
    en_section_name.delete(0, tk.END)
    en_section_name.insert(0, name_section)
    clear_element_widgets()
    lb_section.insert(tk.END, name_section)
    lb_section.select_clear(0, tk.END)
    lb_section.select_set(tk.END)
    # sections[name_section] = {}
    wd_elements[name_section] = {}


def del_section():
    if lb_section.curselection():
        clear_element_widgets()
        i = lb_section.curselection()[0]
        name_section = lb_section.get(i)
        # del sections[name_section]
        del wd_elements[name_section]
        en_section_name.delete(0, tk.END)
        lb_section.delete(i)
    print(wd_elements)


def select_section(event):
    if lb_section.curselection():

        clear_element_widgets()
        i = lb_section.curselection()[0]
        name_section = lb_section.get(i)
        for row_number in wd_elements[name_section]:
            for title in title_elements:
                wd_elements[name_section][row_number][title].grid(row=row_number, column=title_elements.index(title), sticky='we')
        en_section_name.delete(0, tk.END)
        en_section_name.insert(0, name_section)
        show_picture()
    # print(sections)


def clear_element_widgets():
    children = frame_elements.winfo_children()
    for child in children:
        if child.winfo_class() != 'Label':
            child.grid_forget()


def add_elements():
    row_number = frame_elements.grid_size()[1]
    name_section = en_section_name.get()
    wd_elements[name_section][row_number] = {}
    for title in title_elements:
        if title == material:
            wd_elements[name_section][row_number][title] = ttk.Combobox(frame_elements, width=10, values=list_material_calc)
            wd_elements[name_section][row_number][title].grid(row=row_number, column=title_elements.index(title), sticky='we')
            wd_elements[name_section][row_number][title].bind('<<ComboboxSelected>>',
                                                    lambda e, i=row_number, t=title: change_material_str(e, i, t))
        elif title == orientation:
            wd_elements[name_section][row_number][title] = ttk.Combobox(frame_elements, width=10, values=orientation_element)
            wd_elements[name_section][row_number][title].current(0)
            wd_elements[name_section][row_number][title].grid(row=row_number, column=title_elements.index(title), sticky='we')
            wd_elements[name_section][row_number][title].bind('<<ComboboxSelected>>',
                                                lambda e, i=row_number: change_orientation_str(e, i))
        elif title == location:
            wd_elements[name_section][row_number][title] = ttk.Combobox(frame_elements, width=10, values=list_location)
            wd_elements[name_section][row_number][title].current(0)
            wd_elements[name_section][row_number][title].grid(row=row_number, column=title_elements.index(title), sticky='we')

        elif title == name:
            wd_elements[name_section][row_number][title] = tk.Entry(frame_elements, width=12)
            wd_elements[name_section][row_number][title].insert(0, 'element ' + str(row_number))
            wd_elements[name_section][row_number][title].grid(row=row_number, column=title_elements.index(title), sticky='we')
        else:
            wd_elements[name_section][row_number][title] = tk.Entry(frame_elements, width=12)
            wd_elements[name_section][row_number][title].insert(0, f'{0:.3f}')
            wd_elements[name_section][row_number][title].grid(row=row_number, column=title_elements.index(title), sticky='we')

    wd_elements[name_section][row_number][qty].delete(0, tk.END)
    wd_elements[name_section][row_number][qty].insert(0, f'{1:.3f}')


def del_elements():
    children = frame_elements.winfo_children()
    widget = frame_elements.focus_get()
    if widget in children:
        i = widget.grid_info()['row']
        name_section = en_section_name.get()
        for widget1 in children:
            print(widget1.grid_info())
            if widget1.grid_info() != {} and int(widget1.grid_info()['row']) == i:
                widget1.destroy()
        del wd_elements[name_section][i]


def change_material_str(e, i, t):
    name_section = en_section_name.get()
    elem_name = wd_elements[name_section][i][t].get()
    if elem_name not in mat:
        if wd_elements[name_section][i][orientation].get() == orientation_element[0]:
            wd_elements[name_section][i][height].delete(0, tk.END)
            wd_elements[name_section][i][height].insert(0, f'{calc_thickness_lam(elem_name):.3f}')
        else:
            wd_elements[i][breadth].delete(0, tk.END)
            wd_elements[i][breadth].insert(0, f'{calc_thickness_lam(elem_name):.3f}')


def change_orientation_str(e, i):
    name_section = en_section_name.get()
    elem_breadth = wd_elements[name_section][i][breadth].get()
    elem_height = wd_elements[name_section][i][height].get()
    wd_elements[name_section][i][breadth].delete(0, tk.END)
    wd_elements[name_section][i][breadth].insert(0, elem_height)
    wd_elements[name_section][i][height].delete(0, tk.END)
    wd_elements[name_section][i][height].insert(0, elem_breadth)


def calc_sum_column_elements(name_calc, title):
    sum_elements = 0
    for key in results[name_calc][section]:
        sum_elements += float(results[name_calc][section][key][title])
    return float(sum_elements)


def clear_result_element_dict():
    for elem_name in sections:
        for title in title_result:
            sections[elem_name][title] = 0


def add_calculation():
    row_number = frame_calculation.grid_size()[1]
    wd_calculation[row_number] = {}
    for title in title_calculation:
        if title == section:
            wd_calculation[row_number][title] = ttk.Combobox(frame_calculation, width=15)
            # wd_calculation[row_number][title].current(0)
            wd_calculation[row_number][title].grid(row=row_number, column=title_calculation.index(title))
        else:
            wd_calculation[row_number][title] = tk.Entry(frame_calculation, width=15)
            wd_calculation[row_number][title].insert(0, '0.00')
            wd_calculation[row_number][title].grid(row=row_number, column=title_calculation.index(title), sticky='we')
    wd_calculation[row_number][name].delete(0, tk.END)
    wd_calculation[row_number][name].insert(0, 'calculation ' + str(row_number))
    update_listbox_calculation()


def del_calculation():
    children = frame_calculation.winfo_children()
    widget = frame_calculation.focus_get()
    if widget in children:
        i = widget.grid_info()['row']
        for widget1 in children:
            if int(widget1.grid_info()['row']) == i:
                widget1.destroy()
        del wd_calculation[i]


def create_sections_dict():
    sections.clear()
    for name_section in wd_elements:
        sections[name_section] = {}
        for key in wd_elements[name_section]:
            elem_name = wd_elements[name_section][key][name].get()
            sections[name_section][elem_name] = {}
            for title in title_elements:
                if is_digit(wd_elements[name_section][key][title].get()):
                    sections[name_section][elem_name][title] = float(wd_elements[name_section][key][title].get())
                else:
                    sections[name_section][elem_name][title] = wd_elements[name_section][key][title].get()


def create_calculation_dict():
    calculations.clear()
    for key in wd_calculation:
        name_calc = wd_calculation[key][name].get()
        calculations[name_calc] = {}
        for title in title_calculation:
            if is_digit(wd_calculation[key][title].get()):
                calculations[name_calc][title] = float(wd_calculation[key][title].get())
            else:
                calculations[name_calc][title] = wd_calculation[key][title].get()


def create_results_dict():
    results.clear()
    for name_calc in calculations:
        results[name_calc] = {}
        for title in title_calculation:
            results[name_calc][title] = calculations[name_calc][title]
        name_section = results[name_calc][section]
        results[name_calc][section] = {}
        for key in wd_elements[name_section]:
            elem_name = wd_elements[name_section][key][name].get()
            wd_elements[name_section][key][material].get()
            if wd_elements[name_section][key][material].get() in lam:
                name_lam = wd_elements[name_section][key][material].get()
                for ply in lam[name_lam]:
                    new_name = elem_name+' ply '+ply+' '+lam[name_lam][ply]
                    results[name_calc][section][new_name] = {}
                    for title in title_result:
                        if title in title_elements:
                            if is_digit(wd_elements[name_section][key][title].get()):
                                results[name_calc][section][new_name][title] = float(wd_elements[name_section][key][title].get())
                            else:
                                results[name_calc][section][new_name][title] = wd_elements[name_section][key][title].get()
                        else:
                            results[name_calc][section][new_name][title] = 0
                    results[name_calc][section][new_name][mod_e] = float(mat[lam[name_lam][ply]][mod_e])
                    if results[name_calc][section][new_name][orientation] == orientation_element[0]:
                        results[name_calc][section][new_name][height] = float(mat[lam[name_lam][ply]][thickness])
                    else:
                        results[name_calc][section][new_name][breadth] = float(mat[lam[name_lam][ply]][thickness])
            else:
                results[name_calc][section][elem_name] = {}
                for title in title_result:
                    if title in title_elements:
                        if is_digit(wd_elements[name_section][key][title].get()):
                            results[name_calc][section][elem_name][title] = float(wd_elements[name_section][key][title].get())
                        else:
                            results[name_calc][section][elem_name][title] = wd_elements[name_section][key][title].get()
                    else:
                        results[name_calc][section][elem_name][title] = 0
                results[name_calc][section][elem_name][mod_e] = float(mat[results[name_calc][section][elem_name][material]][mod_e])
    print(results)


def create_general_dict():
    general.clear()


def calculate():
    create_calculation_dict()
    create_results_dict()

    for name_calc in results:
        for elem_name in results[name_calc][section]:
            results[name_calc][section][elem_name][area_f] = results[name_calc][section][elem_name][breadth] * results[name_calc][section][elem_name][height]
            results[name_calc][section][elem_name][ef] = results[name_calc][section][elem_name][area_f] * results[name_calc][section][elem_name][mod_e]
            results[name_calc][section][elem_name][efz] = results[name_calc][section][elem_name][ef] * results[name_calc][section][elem_name][dist_z]
            results[name_calc][section][elem_name][efz2] = results[name_calc][section][elem_name][efz] * results[name_calc][section][elem_name][dist_z]
            results[name_calc][section][elem_name][ebh3] = results[name_calc][section][elem_name][mod_e] * \
                                        results[name_calc][section][elem_name][breadth] * results[name_calc][section][elem_name][height] ** 3 / 12

        results[name_calc][zna] = calc_sum_column_elements(name_calc, efz) / calc_sum_column_elements(name_calc, ef)
        results[name_calc][ei_na] = calc_sum_column_elements(name_calc, efz2) + calc_sum_column_elements(name_calc, ebh3) - results[name_calc][zna] **2 * calc_sum_column_elements(name_calc, ef)

        for elem_name in results[name_calc][section]:
            if (results[name_calc][section][elem_name][dist_z] - results[name_calc][zna]) >= 0:
                results[name_calc][section][elem_name][dist_zna] = results[name_calc][section][elem_name][dist_z] - results[name_calc][zna] + results[name_calc][section][elem_name][height] / 2
            else:
                results[name_calc][section][elem_name][dist_zna] = results[name_calc][section][elem_name][dist_z] - results[name_calc][zna] - results[name_calc][section][elem_name][height] / 2
            results[name_calc][section][elem_name][sig_act] = calculations[name_calc][moment] / results[name_calc][ei_na] * results[name_calc][section][elem_name][dist_zna] * results[name_calc][section][elem_name][mod_e]
        print(results)
        # show_result()


def show_result():
    for key in wd_elements:
        elem_name = wd_elements[key][name].get()
        for title in title_result:
            wd_elements[key][title].delete(0, tk.END)
            wd_elements[key][title].insert(0, f'{sections[elem_name][title]:.3e}')
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
    create_sections_dict()
    name_section = en_section_name.get()
    for elem_name in sections[name_section]:
        if sections[name_section][elem_name][orientation] == orientation_element[1]:
            coord_z1 = (sections[name_section][elem_name][dist_z] - sections[name_section][elem_name][height] / 2)
            coord_z2 = (sections[name_section][elem_name][dist_z] + sections[name_section][elem_name][height] / 2)
        else:
            coord_z1 = (sections[name_section][elem_name][dist_z])
            coord_z2 = (sections[name_section][elem_name][dist_z])
        min_z = min(min_z, coord_z1, coord_z2)
        max_z = max(max_z, coord_z1, coord_z2)
    field = 10
    offset = 250
    scale = offset / (max_z - min_z)

    for elem_name in sections[name_section]:
        if sections[name_section][elem_name][orientation] == orientation_element[1]:
            coord_z1 = (sections[name_section][elem_name][dist_z] - sections[name_section][elem_name][height] / 2) * scale * -1 + offset + field
            coord_y1 = (sections[name_section][elem_name][dist_y]) * scale + field
            coord_z2 = (sections[name_section][elem_name][dist_z] + sections[name_section][elem_name][height] / 2) * scale * -1 + offset + field
            coord_y2 = (sections[name_section][elem_name][dist_y]) * scale + field
        else:
            coord_z1 = (sections[name_section][elem_name][dist_z]) * scale * -1 + offset + field
            coord_y1 = (sections[name_section][elem_name][dist_y] - sections[name_section][elem_name][breadth] / 2) * scale + field
            coord_z2 = (sections[name_section][elem_name][dist_z]) * scale * -1 + offset + field
            coord_y2 = (sections[name_section][elem_name][dist_y] + sections[name_section][elem_name][breadth] / 2) * scale + field
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
    shear = 'Shear force'
    section = 'Section'
    zna = 'zna'
    ei_na = 'ei_na'
    location = 'Location'
    title_material = [material, name, mod_e, 'Sig, MPa', 'Tau, MPa', thickness]
    title_elements = [name, location, material, orientation, breadth, height, qty, dist_y, dist_z]
    title_result = [name, location, material, orientation, breadth, height, qty, dist_y, dist_z, mod_e,
                      area_f, ef,  efz, efz2, ebh3, dist_zna, sig_act]
    # title_result = [area_f, ef, efz, efz2, ebh3, dist_zna, sig_act]
    title_calculation = [name, section, moment, shear]
    list_location = ['bottom', 'side below WL', 'side above WL', 'deck', 'bulkhead', 'superstructure']
    list_material = ['Metal', 'FRP']
    list_material_calc = []
    orientation_element = ['horizontal', 'vertical']
    wd_material = {}
    wd_elements = {}
    wd_calculation = {}
    general = {}
    lam = {}
    mat = {}
    sections = {}
    calculations = {}
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
    sheet.add(sheet_elements,text='Sections')
    sheet_calculation = ttk.Frame(sheet)
    sheet.add(sheet_calculation, text='Calculate')
    sheet.grid(row=0, column=0, sticky='snwe')
    sheet.bind('<<NotebookTabChanged>>', update_listbox)
    # sheet general
    frame_general = tk.Frame(sheet_general)
    frame_general.grid(row=0, column=0, sticky='nsew')
    lb_moment = tk.Label(frame_general, text='Project :')
    lb_moment.grid(row=0, column=0)
    en_project_name = tk.Entry(frame_general)
    en_project_name.grid(row=0, column=1)
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

    # sheet sections
    sheet_elements.columnconfigure(1, weight=1)
    sheet_elements.rowconfigure(1, weight=1)
        # section listbox
    frame_elements_section = tk.LabelFrame(sheet_elements, text='Sections')
    frame_elements_section.grid(row=0, column=0, sticky='wn')
    frame_elements_section_button = tk.Frame(frame_elements_section)
    frame_elements_section_button.grid(row=0, column=0, sticky='nw')

    tk.Button(frame_elements_section_button, text='Add', **button_config, command=add_section).grid(row=0, column=0,
                                                                            padx=5, pady=5)
    tk.Button(frame_elements_section_button, text='Del', **button_config, command=del_section).grid(row=0, column=1,
                                                                                             padx=5, pady=5)
    lb_section = tk.Listbox(frame_elements_section, height=20, width=40)
    lb_section.grid(row=1, column=0)
    lb_section.bind('<<ListboxSelect>>', select_section)
        # picture
    frame_canvas_picture = tk.LabelFrame(sheet_elements, text='Picture')
    frame_canvas_picture.grid(row=0, column=1, sticky='wn')
    canvas_picture = tk.Canvas(frame_canvas_picture, borderwidth=1, bg='light grey', height=356)
    canvas_picture.grid(row=0, column=0, sticky='wn')
        # sections
    frame_elements_global = tk.LabelFrame(sheet_elements, text='Elements')
    frame_elements_global.grid(row=1, column=0, columnspan=2, sticky='nwe')
    frame_elements_global.columnconfigure(0, weight=1)
    frame_elements_global.rowconfigure(1, weight=1)

    frame_elements_button = tk.Frame(frame_elements_global)
    frame_elements_button.grid(row=0, column=0, sticky='we')

    frame_canvas_elements = tk.Frame(frame_elements_global)
    frame_canvas_elements.grid(row=1, column=0, sticky='we')
    frame_canvas_elements.rowconfigure(0, weight=1)
    canvas_elements = tk.Canvas(frame_canvas_elements, borderwidth=0)
    frame_elements = tk.Frame(canvas_elements)
    scroll_elements_vertical = tk.Scrollbar(frame_canvas_elements, orient="vertical", command=canvas_elements.yview)
    scroll_elements_horizontal = tk.Scrollbar(frame_canvas_elements, orient="horizontal", command=canvas_elements.xview)
    canvas_elements.configure(yscrollcommand=scroll_elements_vertical.set)
    canvas_elements.configure(xscrollcommand=scroll_elements_horizontal.set)
    scroll_elements_vertical.pack(side="right", fill="y")
    scroll_elements_horizontal.pack(side="bottom", fill="x")
    canvas_elements.pack(side="top", fill="both", expand=True)
    canvas_elements.create_window((1, 1), window=frame_elements, anchor="nw")
    frame_elements.bind("<Configure>",
                        lambda event: canvas_elements.configure(scrollregion=canvas_elements.bbox("all")))
        # buttons and title on strength sheet
    tk.Button(frame_elements_button, text='Add', **button_config, command=add_elements).grid(row=0, column=0,
                                                                                             padx=5, pady=5)
    tk.Button(frame_elements_button, text='Del', **button_config, command=del_elements).grid(row=0, column=1,
                                                                                             padx=5, pady=5)
    tk.Button(frame_elements_button, text='Show', **button_config, command=show_picture).grid(row=0, column=2,
                                                                                             padx=5, pady=5)
    tk.Label(frame_elements_button, text='Label: ').grid(row=0, column=3)
    en_section_name = tk.Entry(frame_elements_button)
    en_section_name.grid(row=0, column=4)
    for title in title_elements:
        tk.Label(frame_elements, anchor='w', width= 12, height=1, relief='solid',
             bd=0.5, text=title).grid(row=0, column=title_elements.index(title))
    en_elements = {}

    # sheet calculation
    sheet_calculation.rowconfigure(1, weight=1)
    sheet_calculation.columnconfigure(1, weight=1)
        # tree results
    frame_calculation_tree = tk.LabelFrame(sheet_calculation, text='Results')
    frame_calculation_tree.grid(row=1, column=0, columnspan=2, sticky='nwe')
    frame_calculation_tree.columnconfigure(0, weight=1)
    frame_calculation_tree.rowconfigure(0, weight=1)
    tree_result = ttk.Treeview(frame_calculation_tree, height=20)
    tree_result.grid(row=0, column=0, sticky='nwes')
    sb_result = ttk.Scrollbar(frame_calculation_tree, orient='vertical')
    sb_result.grid(row=0, column=1 ,sticky='ns')

        # general results
    frame_calculation_result = tk.LabelFrame(sheet_calculation, text='Results')
    frame_calculation_result.grid(row=0, column=1, sticky='nwes')
    tk.Label(frame_calculation_result, text='Position of neutral axis above base, z0, mm', anchor='w').grid(row=0,
                                                                                                column=0, sticky='w')
    en_result_zna = tk.Entry(frame_calculation_result)
    en_result_zna.grid(row=0, column=1, padx=10, pady=5)
    tk.Label(frame_calculation_result, text='Stiffness EIx about neutral axis, N*mm2', anchor='w').grid(row=1,
                                                                                                column=0, sticky='w')
    en_result_ei_na = tk.Entry(frame_calculation_result)
    en_result_ei_na.grid(row=1, column=1, padx=10, pady=5)

        # calculation data
    frame_calculation_data = tk.LabelFrame(sheet_calculation, text='Data')
    frame_calculation_data.grid(row=0, column=0)
    # frame_calculation_data.columnconfigure(0, weight=1)

    frame_calculation_button = tk.Frame(frame_calculation_data)
    frame_calculation_button.pack(side="top", fill='both')

    frame_canvas_calculation = tk.Frame(frame_calculation_data)
    frame_canvas_calculation.pack(side="top", fill='both')
    canvas_calculation = tk.Canvas(frame_canvas_calculation, borderwidth=0, width=500)
    frame_calculation = tk.Frame(canvas_calculation)
    scroll_calculation_vertical = tk.Scrollbar(frame_canvas_calculation, orient="vertical", command=canvas_calculation.yview)
    scroll_calculation_horizontal = tk.Scrollbar(frame_canvas_calculation, orient="horizontal", command=canvas_calculation.xview)
    canvas_calculation.configure(yscrollcommand=scroll_calculation_vertical.set)
    canvas_calculation.configure(xscrollcommand=scroll_calculation_horizontal.set)
    scroll_calculation_vertical.pack(side="right", fill="y")
    scroll_calculation_horizontal.pack(side="bottom", fill="x")
    canvas_calculation.pack(side="top", fill="both", expand=True)
    canvas_calculation.create_window((1, 1), window=frame_calculation, anchor="nw")
    frame_calculation.bind("<Configure>",
                        lambda event: canvas_calculation.configure(scrollregion=canvas_calculation.bbox("all")))

        # buttons and title on calculation sheet
    tk.Button(frame_calculation_button, text='Add', **button_config, command=add_calculation).grid(row=0, column=0,
                                                                                             padx=5, pady=5)
    tk.Button(frame_calculation_button, text='Del', **button_config, command=del_calculation).grid(row=0, column=1,
                                                                                             padx=5, pady=5)
    for title in title_calculation:
        tk.Label(frame_calculation, anchor='w', width=15, height=1, relief='solid',
                 bd=0.5, text=title).grid(row=0, column=title_calculation.index(title))

    root.mainloop()