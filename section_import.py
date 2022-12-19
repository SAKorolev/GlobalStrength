

def open_file_import():
    import tkinter.filedialog as fd
    file_types = (("File", "*.xls"),
                 ("Any", "*"))
    file_name = fd.askopenfilename(title="Open file", initialdir="/", filetypes=file_types)
    if file_name:
        return file_name


def import_section_xls(section_name, angle, breadth, dist_z, dist_y):

    import xlwings as xw
    from math import atan, degrees

    file_import = open_file_import()
    app = xw.App(visible = False)
    book = xw.Book(file_import)
    sheet = xw.sheets[0]
    row_max = sheet.range(1, 1).end('down').row
    section_dict = {}
    section_dict[section_name]={}
    for i in range(2, row_max+1):
        start_y = float(sheet.range('E'+ str(i)).value)
        start_z = float(sheet.range('F'+ str(i)).value)
        finish_y = float(sheet.range('C'+ str(i)).value)
        finish_z = float(sheet.range('D'+ str(i)).value)
        section_dict[section_name][i-1] = {}
        section_dict[section_name][i-1][breadth] = round(((finish_z-start_z)**2+(finish_y-start_y)**2)**0.5, 3)
        section_dict[section_name][i-1][dist_z] = round((finish_z+start_z)/2, 3)
        section_dict[section_name][i-1][dist_y] = round((finish_y+start_y)/2, 3)
        if finish_y == start_y:
            section_dict[section_name][i-1][angle] = 90
        else:
            section_dict[section_name][i-1][angle] = round(degrees(atan((finish_z-start_z)/(finish_y-start_y))), 3)
        # print(section_dict[section_name][i])

    # book.close()
    app.quit()
    return section_dict


if __name__ == '__main__':
    import_section_xls('section1', 'angle', 'breadth', 'z', 'y')