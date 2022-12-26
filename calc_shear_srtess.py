import math

import shared as s


def calc_shear_stress(results):
    for name_calculation in results:
        for name_element in results[name_calculation][s.section]:
            if s.angle < 45 and s.angle > -45:
                results[name_calculation][s.section][name_element][s.incl_shear] = False
            else:
                results[name_calculation][s.section][name_element][s.incl_shear] = True

def calc_first_moment(results, mat, zca):
    first_moment = 0
    print(zca)
    for name_calculation in results:
        z_na = results[name_calculation][s.zna]
        for name_element in results[name_calculation][s.section]:
            name_material = results[name_calculation][s.section][name_element][s.material]
            e = float(mat[name_material][s.mod_e])
            z = results[name_calculation][s.section][name_element][s.dist_z]
            b = results[name_calculation][s.section][name_element][s.breadth]
            h = results[name_calculation][s.section][name_element][s.height]
            alfa = results[name_calculation][s.section][name_element][s.angle]
            z1 = z-b/2*math.sin(math.radians(alfa))
            z2 = z+b/2*math.sin(math.radians(alfa))
            if (z1>=zca) and (z2>=zca):
                first_moment += e*b*h*(z-z_na)
                print(z1)
                print(z2)
                print(b*h*(z-z_na))
            elif (z1>=zca) and (z2<zca):
                first_moment += e*h*b*(z1-zca)/(z1-z2)*((z1-zca)/2+zca-z_na)
                print(z1)
                print(z2)
                print(h*b*(z1-zca)/(z1-z2)*((z1-zca)/2+zca-z_na))
            elif (z1 < zca) and (z2 >= zca):
                first_moment += e*h * b * (z2 - zca) / (z2 - z1) * ((z2 - zca) / 2 + zca-z_na)
                print(z1)
                print(z2)
                print(h * b * (z2 - zca) / (z2 - z1) * ((z2 - zca) / 2 + zca-z_na))
        print(first_moment)


if __name__ == '__main__':
    pass