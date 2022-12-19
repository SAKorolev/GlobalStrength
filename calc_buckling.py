import shared as s
from math import pi

def calc_buckling(buckling_data_dict, materials, sections, calculations, laminates):
    results = {}
    for name_buckling in buckling_data_dict:
        results[name_buckling] = {}
        name_material = buckling_data_dict[name_buckling][s.material]
        if name_material in materials.keys() and materials[name_material][s.material] == s.list_material[0]:
           results[name_buckling][s.stress_crit] = calc_buckling_metal(name_buckling, buckling_data_dict, materials, sections, calculations)
        else:
            core = False
            for ply in laminates[name_material]:
                if materials[laminates[name_material][ply]][s.material] == s. list_material[2]:
                    core = True
            if core:
                results[name_buckling][s.stress_crit] = calc_buckling_sandwich(buckling_data_dict, materials, sections, calculations)
    return results


def calc_buckling_metal(name_buckling, buckling_data_dict, materials, sections, calculations):
    print(buckling_data_dict)
    a = float(buckling_data_dict[name_buckling][s.length_b])
    b = float(buckling_data_dict[name_buckling][s.breadth_b])
    if a/b <= 1.415:
        k_buck = (1/(a/b)+(a/b)/1)**2
    elif a/b <= 2.45:
        k_buck = (2 / (a / b) + (a / b) / 2) ** 2
    elif a/b <= 3.464:
        k_buck = (3/(a/b)+(a/b)/3)**2
    else:
        k_buck = 4
    E = float(materials[buckling_data_dict[name_buckling][s.material]][s.mod_e])
    mu = float(materials[buckling_data_dict[name_buckling][s.material]][s.poisson])
    name_calculation = buckling_data_dict[name_buckling][s.calc_b]
    name_section = calculations[name_calculation][s.section]
    t = sections[name_section][buckling_data_dict[name_buckling][s.element_b]][s.height]
    sigma_crit = k_buck*E*pi**2/(12*(1-mu**2))*(t/b)**2
    return sigma_crit


def calc_buckling_sandwich(buckling_data_dict, materials, sections, calculations):
    pass

