import math

cf_3 = 3.0



def pm2_5_alt(p0_3, p0_5, p1_0, p2_5, cf):
    _cf = float(cf)
    if math.isnan(_cf):
        _cf = cf_3
    m1 = getMass(p0_3 - p0_5, 0.3, 0.5)
    m2 = getMass(p0_5 - p1_0, 0.5, 1.0)
    m3 = getMass(p1_0 - p2_5, 1.0, 2.5)
    pm2_5 = m1 + m2 + m3
    return pm2_5 * _cf

def getMass(countDl, sizeLower, sizeUpper):
    densityGCm3 = 1.0
    geometricMeanUm = math.sqrt(sizeLower * sizeUpper)
    volume = countDl * math.pi * math.pow(geometricMeanUm, 3) / 6.0
    return volume * densityGCm3 / 100.0


pm25 = pm2_5_alt(623, 170, 20, 1, cf_3)
print(pm25)