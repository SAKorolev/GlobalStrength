import shared as s
from math import pi

def calc_buckling(buckling_data_dict, materials, sections, calculations, laminates, results):
    results_buck = {}
    for name_buckling in buckling_data_dict:
        results_buck[name_buckling] = {}
        name_material = buckling_data_dict[name_buckling][s.material]
        if name_material in materials.keys() and materials[name_material][s.material] == s.list_material[0]:
           results_buck[name_buckling][s.stress_crit] = calc_buckling_metal(name_buckling, buckling_data_dict, materials, sections, calculations)
        else:
            core = False
            for ply in laminates[name_material]:
                if materials[laminates[name_material][ply]][s.material] == s. list_material[2]:
                    core = True
            if core:
                results_buck[name_buckling][s.stress_crit] = calc_buckling_sandwich(name_buckling,
                                                    buckling_data_dict, materials, sections, calculations, laminates)
            else:
                results_buck[name_buckling][s.stress_crit] = calc_buckling_single(name_buckling,
                                                    buckling_data_dict, materials, sections, calculations,laminates)
        results_buck[name_buckling][s.stress_global] = calc_buckling_gs(name_buckling, buckling_data_dict, materials,
                                                                         sections, calculations, results)
    return results_buck


def calc_buckling_metal(name_buckling, buckling_data_dict, materials, sections, calculations):
    a = float(buckling_data_dict[name_buckling][s.length_b])
    b = float(buckling_data_dict[name_buckling][s.breadth_b])
    if buckling_data_dict[name_buckling][s.end_conditions] == s.list_end_conditions[1]:
        if a/b <= 1.415:
            k_buck = (1/(a/b)+(a/b)/1)**2
        elif a/b <= 2.45:
            k_buck = (2 / (a / b) + (a / b) / 2) ** 2
        elif a/b <= 3.464:
            k_buck = (3/(a/b)+(a/b)/3)**2
        else:
            k_buck = 4
    else:
        k_buck = 0
    E = float(materials[buckling_data_dict[name_buckling][s.material]][s.mod_e])
    mu = float(materials[buckling_data_dict[name_buckling][s.material]][s.poisson])
    name_calculation = buckling_data_dict[name_buckling][s.calc_b]
    name_section = calculations[name_calculation][s.section]
    t = sections[name_section][buckling_data_dict[name_buckling][s.element_b]][s.height]
    sigma_crit = round(k_buck*E*pi**2/(12*(1-mu**2))*(t/b)**2, 2)
    return sigma_crit


def calc_buckling_sandwich(name_buckling, buckling_data_dict, materials, sections, calculations, laminates):
    name_lam = buckling_data_dict[name_buckling][s.material]
    b = float(buckling_data_dict[name_buckling][s.breadth_b])
    a = float(buckling_data_dict[name_buckling][s.length_b])
    sum_t = sum_parameter(name_lam, materials, laminates, s.thickness)
    sum_Et = sum_mult_parameter(name_lam, materials, laminates, s.thickness, s.mod_e)
    E = sum_Et / sum_t
    d = sum_t / 2 # assume about average laminate thickness
    h = core_parameter(name_lam, materials, laminates, s.thickness) / 2
    E_core = core_parameter(name_lam, materials, laminates, s.mod_e)
    G_core = core_parameter(name_lam, materials, laminates, s.mod_g)
    poisson_core = core_parameter(name_lam, materials, laminates, s.poisson)
    poisson = 0 # there is not metod of calculation
    D1 = E * d**3 / (12*(1-poisson**2))
    B1 = E * d / (1-poisson**2)
    D_core = 2 * E_core * h**3 / (3*(1-poisson_core**2))
    D = 2 * D1 + D_core + 2 * B1 * (h+d/2)**2
    B_core = 2 * E_core * h /(1-poisson_core**2)
    B0 = 2 * B1 + B_core / 3
    k = pi**2 * B0 * h / (G_core * b**2)
    if buckling_data_dict[name_buckling][s.end_conditions] == s.list_end_conditions[1]:
        mt = 1000
        for m in range(1, 5):
            mt = min(mt, ((m*b/a)+(a/m/b))**2/(1+k*((m*b/a)**2+1)))
    else:
        mt = 0
    T = mt * pi**2 * D / b**2
    print('E ', E)
    print('d ', d)
    print('h ', h)
    print('D1 ', D1)
    print('B1 ', B1)
    print('Dc ', D_core)
    print('D ', D)
    print('B0 ', B0)
    print('k ', k)
    print('mt ', mt)

    sigma_crit = round(T / (2*d), 2)
    return sigma_crit


def calc_buckling_single(name_buckling, buckling_data_dict, materials, sections, calculations, laminates):
    name_lam = buckling_data_dict[name_buckling][s.material]
    b = float(buckling_data_dict[name_buckling][s.breadth_b])
    a = float(buckling_data_dict[name_buckling][s.length_b])
    sum_t = sum_parameter(name_lam, materials, laminates, s.thickness)
    sum_Et = sum_mult_parameter(name_lam, materials, laminates, s.thickness, s.mod_e)
    sum_Gt = sum_mult_parameter(name_lam, materials, laminates, s.thickness, s.mod_g)
    E = sum_Et / sum_t
    G = sum_Gt / sum_t
    t = sum_t
    poisson = 0  # there is not metod of calculation
    if buckling_data_dict[name_buckling][s.end_conditions] == s.list_end_conditions[1]:
        B = 1000000000000
        for m in range(1, 5):
            B = min(B, ((m * b / a)**2 + (a / m / b)**2 + 2*(poisson+2*G/E*(1-poisson**2)))*pi**2 / (12*(1-poisson**2)))
            print(B)
    else:
        B = 0
    sigma_crit = round(E * B * (t / b) ** 2, 2)
    print('E ', E)
    print('t ', t)
    print('B ', B)

    return sigma_crit


def sum_parameter(name_lam, materials, laminates, par1):
    sum_parameter = 0
    for ply in laminates[name_lam]:
        name_ply = laminates[name_lam][ply]
        if materials[name_ply][s.material] != s.list_material[2]:
            sum_parameter += float(materials[name_ply][par1])
    return sum_parameter


def sum_mult_parameter(name_lam, materials, laminates, par1, par2):
    sum_parameter = 0
    for ply in laminates[name_lam]:
        name_ply = laminates[name_lam][ply]
        if materials[name_ply][s.material] != s.list_material[2]:
            sum_parameter += float(materials[name_ply][par1])*float(materials[name_ply][par2])
    return sum_parameter


def core_parameter(name_lam, materials, laminates, par1):
    for ply in laminates[name_lam]:
        name_ply = laminates[name_lam][ply]
        if materials[name_ply][s.material] == s.list_material[2]:
            return float(materials[name_ply][par1])


def calc_buckling_gs(name_buckling, buckling_data_dict, materials, sections, calculations, results):
    name_calc = buckling_data_dict[name_buckling][s.calc_b]
    name_element = buckling_data_dict[name_buckling][s.element_b]
    M = results[name_calc][s.moment]
    EI = results[name_calc][s.ei_na]
    F = 0
    EF = 0
    z = 0
    for row in results[name_calc][s.section]:
        if results[name_calc][s.section][row][s.name] == name_element:
            F += results[name_calc][s.section][row][s.area_f]
            EF += results[name_calc][s.section][row][s.ef]
            z = results[name_calc][s.section][row][s.dist_zna]
    E = EF / F
    sigma_gs = round(M*z*E/EI, 2)
    return sigma_gs
