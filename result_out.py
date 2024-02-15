import xlwings as xw

def calculation_results_to_xls(dict_results, title_results, section, title_exclude_result, sum_f, sum_ef, sum_efz,
                               sum_eibase, zna, ei_na, moment, shear):
    if not dict_results:
        return
    try:
        f = open('Template.xlsx')
        f.close()
    except FileNotFoundError:
        return
    
    book = xw.Book('Template.xlsx')
    sheet = book.sheets('GIRDER')
    book_new = xw.Book()
    for name_calc in dict_results:
        sheet.api.Copy(Before=book_new.sheets(1).api)
        sheet_new = book_new.sheets(1)
        sheet_new.name = name_calc + section
        i = 8
        j = 1
        for element in dict_results[name_calc][section]:
            for title in title_results:
                if title not in title_exclude_result:
                    sheet_new.range(i,j).value = dict_results[name_calc][section][element][title]
                    j += 1
            i += 1
            j = 1
        # sheet_new.range('C3').value = dict_results[name_calc][section]
        sheet_new.range('G500').value = dict_results[name_calc][sum_f]
        sheet_new.range('K500').value = dict_results[name_calc][sum_ef]
        sheet_new.range('L500').value = dict_results[name_calc][sum_efz]
        sheet_new.range('O500').value = dict_results[name_calc][sum_eibase]
        sheet_new.range('E502').value = dict_results[name_calc][zna]
        sheet_new.range('E503').value = dict_results[name_calc][sum_ef] / dict_results[name_calc][sum_f]
        sheet_new.range('E504').value = dict_results[name_calc][ei_na]
        sheet_new.range('E505').value = dict_results[name_calc][moment]/1000
        sheet_new.range('E506').value = dict_results[name_calc][shear]/1000
        sheet_new.range(str(i)+':498').delete()
    book.close()


if __name__ == '__main__':
    pass