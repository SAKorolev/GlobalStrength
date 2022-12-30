import math
import shared as s


def calc_shear_stress(results, mat, zca):
    for name_calculation in results:
        q = results[name_calculation][s.shear]
        fze = calc_first_moment(name_calculation, results, mat, zca)
        ei = results[name_calculation][s.ei_na]
        b = calc_breadth(name_calculation, results, zca)
        shear_stress = q*fze/(ei*b)

def calc_first_moment(name_calculation, results, mat, zca):
    first_moment = 0
    print(zca)
    z_na = results[name_calculation][s.zna]
    for name_element in results[name_calculation][s.section]:
        name_material = results[name_calculation][s.section][name_element][s.material]
        e = float(mat[name_material][s.mod_e])
        z1 = results[name_calculation][s.section][name_element][s.z1]
        z2 = results[name_calculation][s.section][name_element][s.z2]
        z = results[name_calculation][s.section][name_element][s.dist_z]
        b = results[name_calculation][s.section][name_element][s.breadth]
        h = results[name_calculation][s.section][name_element][s.height]
        # alfa = results[name_calculation][s.section][name_element][s.angle]
        # z1 = z-b/2*math.sin(math.radians(alfa))
        # z2 = z+b/2*math.sin(math.radians(alfa))
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
    return first_moment


def calc_breadth(name_calculation, results, zca):
    breadth1 = 0
    breadth2 = 0
    zca1 = zca + 0.5
    zca2 = zca - 0.5
    for name_element in results[name_calculation][s.section]:
        z1 = results[name_calculation][s.section][name_element][s.z1]
        z2 = results[name_calculation][s.section][name_element][s.z2]
        t = results[name_calculation][s.section][name_element][s.height]
        if ((z1>zca1) and (z2<zca1)) or ((z1<zca1) and (z2>zca1)):
            breadth1 += t
        if ((z1>zca2) and (z2<zca2)) or ((z1<zca2) and (z2>zca2)):
            breadth2 += t
    breadth = min(breadth1, breadth2)
    print(breadth)
    return breadth


if __name__ == '__main__':
    pass