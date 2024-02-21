import xlwings as xw
import shared as s

def materials_data_to_template(layers_def):
    if not layers_def:
        return
    try:
        f=open('Template.xlsx')
        f.close()
    except FileNotFoundError:
        return
    book = xw.Book('Template.xlsx')
    sheet = book.sheets('Materials')
    book_new = xw.Book()
    sheet.api.Copy(Before=book_new.sheets(1).api)
    sheet_new = book_new.sheets(1)
    sheet_new.name = 'Layers'

    i = 5
    for layer in layers_def:
        sheet_new.range(i, 2).value = layers_def[layer][s.name]
        sheet_new.range(i, 3).value = layers_def[layer][s.material]
        sheet_new.range(i, 4).value = layers_def[layer][s.mod_e]
        sheet_new.range(i, 5).value = layers_def[layer][s.mod_g]
        sheet_new.range(i, 6).value = layers_def[layer][s.sig_ten]
        sheet_new.range(i, 7).value = layers_def[layer][s.sig_comp]
        sheet_new.range(i, 8).value = layers_def[layer][s.tau]
        sheet_new.range(i, 9).value = layers_def[layer][s.poisson]
        sheet_new.range(i, 10).value = layers_def[layer][s.thickness]
        i +=1

    sheet_new.range(str(i) + ':34').delete()
    book.close()

if __name__ == '__main__':
    pass