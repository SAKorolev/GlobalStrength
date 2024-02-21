import xlwings as xw
import shared as s

def laminates_data_to_template(lam_def, mat_def):
    if not lam_def:
        return
    try:
        f=open('Template.xlsx')
        f.close()
    except FileNotFoundError:
        return
    book = xw.Book('Template.xlsx')
    sheet = book.sheets('Laminates')
    book_new = xw.Book()
    sheet.api.Copy(Before=book_new.sheets(1).api)
    sheet_new = book_new.sheets(1)
    sheet_new.name = 'Laminates'
    i = 5
    for layer in lam_def:
        plies_name = ''
        plies_thickness = ''
        thickness = 0
        sheet_new.range(i, 2).value = layer
        for index in lam_def[layer]:
            plies_name += str(int(index)+1) + ':' + lam_def[layer][index] + '\n'
            plies_thickness += mat_def[lam_def[layer][index]][s.thickness] + '\n'
            thickness += float(mat_def[lam_def[layer][index]][s.thickness])
        sheet_new.range(i, 3).value = plies_name
        sheet_new.range(i, 4).value = plies_thickness
        sheet_new.range(i, 5).value = thickness
        i +=1

    sheet_new.range(str(i) + ':70').delete()
    book.close()

if __name__ == '__main__':
    pass