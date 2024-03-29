import sys
from netCDF4 import Dataset
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from create_ics import velocities_strains_stress_divergences
import argparse

#--------------------------------------------------------

def integration_weights_triangle(integrationOrder):

    # D. A. Dunavant, High degree efficient symmetrical Gaussian quadrature rules for the triangle,
    # Int. J. Num. Meth. Engng, 21(1985):1129-1148.

    if (integrationOrder == 1):

        nIntegrationPoints = 1

        u = [0.33333333333333]

        v = [0.33333333333333]

        weights = [1.00000000000000]

    elif (integrationOrder == 2):

        nIntegrationPoints = 3

        u = [0.16666666666667, 0.16666666666667, 0.66666666666667]

        v = [0.16666666666667, 0.66666666666667, 0.16666666666667]

        weights = [0.33333333333333, 0.33333333333333, 0.33333333333333]

    elif (integrationOrder == 3):

        nIntegrationPoints = 4

        u = [0.33333333333333, 0.20000000000000, 0.20000000000000, 0.60000000000000]

        v = [0.33333333333333, 0.20000000000000, 0.60000000000000, 0.20000000000000]

        weights = [-0.56250000000000, 0.52083333333333, 0.52083333333333, 0.52083333333333]

    elif (integrationOrder == 4):

        nIntegrationPoints = 6

        u = [0.44594849091597, 0.44594849091597, 0.10810301816807, 0.09157621350977, \
             0.09157621350977, 0.81684757298046]

        v = [0.44594849091597, 0.10810301816807, 0.44594849091597, 0.09157621350977, \
             0.81684757298046, 0.09157621350977]

        weights = [0.22338158967801, 0.22338158967801, 0.22338158967801, 0.10995174365532, \
                   0.10995174365532, 0.10995174365532]

    elif (integrationOrder == 5):

        nIntegrationPoints = 7

        u = [0.33333333333333, 0.47014206410511, 0.47014206410511, 0.05971587178977, \
             0.10128650732346, 0.10128650732346, 0.79742698535309]

        v = [0.33333333333333, 0.47014206410511, 0.05971587178977, 0.47014206410511, \
             0.10128650732346, 0.79742698535309, 0.10128650732346]

        weights = [0.22500000000000, 0.13239415278851, 0.13239415278851, 0.13239415278851, \
                   0.12593918054483, 0.12593918054483, 0.12593918054483]

    elif (integrationOrder == 6):

        nIntegrationPoints = 12

        u = [0.24928674517091, 0.24928674517091, 0.50142650965818, 0.06308901449150, \
             0.06308901449150, 0.87382197101700, 0.31035245103378, 0.63650249912140, \
             0.05314504984482, 0.63650249912140, 0.31035245103378, 0.05314504984482]

        v = [0.24928674517091, 0.50142650965818, 0.24928674517091, 0.06308901449150, \
             0.87382197101700, 0.06308901449150, 0.63650249912140, 0.05314504984482, \
             0.31035245103378, 0.31035245103378, 0.05314504984482, 0.63650249912140]

        weights = [0.11678627572638, 0.11678627572638, 0.11678627572638, 0.05084490637021, \
                   0.05084490637021, 0.05084490637021, 0.08285107561837, 0.08285107561837, \
                   0.08285107561837, 0.08285107561837, 0.08285107561837, 0.08285107561837]

    elif (integrationOrder == 7):

        nIntegrationPoints = 13

        u = [0.33333333333333, 0.26034596607904, 0.26034596607904, 0.47930806784192, \
             0.06513010290222, 0.06513010290222, 0.86973979419557, 0.31286549600487, \
             0.63844418856981, 0.04869031542532, 0.63844418856981, 0.31286549600487, \
             0.04869031542532]

        v = [0.33333333333333, 0.26034596607904, 0.47930806784192, 0.26034596607904, \
             0.06513010290222, 0.86973979419557, 0.06513010290222, 0.63844418856981, \
             0.04869031542532, 0.31286549600487, 0.31286549600487, 0.04869031542532, \
             0.63844418856981]

        weights = [-0.14957004446768, 0.17561525743321, 0.17561525743321, 0.17561525743321, \
                   0.05334723560884, 0.05334723560884, 0.05334723560884, 0.07711376089026, \
                   0.07711376089026, 0.07711376089026, 0.07711376089026, 0.07711376089026, \
                   0.07711376089026]

    elif (integrationOrder == 8):

        nIntegrationPoints = 16

        u = [0.33333333333333, 0.45929258829272, 0.45929258829272, 0.08141482341455, \
             0.17056930775176, 0.17056930775176, 0.65886138449648, 0.05054722831703, \
             0.05054722831703, 0.89890554336594, 0.26311282963464, 0.72849239295540, \
             0.00839477740996, 0.72849239295540, 0.26311282963464, 0.00839477740996]

        v = [0.33333333333333, 0.45929258829272, 0.08141482341455, 0.45929258829272, \
             0.17056930775176, 0.65886138449648, 0.17056930775176, 0.05054722831703, \
             0.89890554336594, 0.05054722831703, 0.72849239295540, 0.00839477740996, \
             0.26311282963464, 0.26311282963464, 0.00839477740996, 0.72849239295540]

        weights = [0.14431560767779, 0.09509163426728, 0.09509163426728, 0.09509163426728, \
                   0.10321737053472, 0.10321737053472, 0.10321737053472, 0.03245849762320, \
                   0.03245849762320, 0.03245849762320, 0.02723031417443, 0.02723031417443, \
                   0.02723031417443, 0.02723031417443, 0.02723031417443, 0.02723031417443]

    elif (integrationOrder == 9):

        nIntegrationPoints = 19

        u = [0.333333333333333, 0.020634961602525, 0.489682519198738, 0.489682519198738, \
             0.125820817014127, 0.437089591492937, 0.437089591492937, 0.623592928761935, \
             0.188203535619033, 0.188203535619033, 0.910540973211095, 0.044729513394453, \
             0.044729513394453, 0.036838412054736, 0.221962989160766, 0.036838412054736, \
             0.741198598784498, 0.221962989160766, 0.741198598784498]

        v = [0.333333333333333, 0.489682519198738, 0.020634961602525, 0.489682519198738, \
             0.437089591492937, 0.125820817014127, 0.437089591492937, 0.188203535619033, \
             0.623592928761935, 0.188203535619033, 0.044729513394453, 0.910540973211095, \
             0.044729513394453, 0.221962989160766, 0.036838412054736, 0.741198598784498, \
             0.036838412054736, 0.741198598784498, 0.221962989160766]

        weights = [0.097135796282799, 0.031334700227139, 0.031334700227139, 0.031334700227139, \
                   0.077827541004774, 0.077827541004774, 0.077827541004774, 0.079647738927210, \
                   0.079647738927210, 0.079647738927210, 0.025577675658698, 0.025577675658698, \
                   0.025577675658698, 0.043283539377289, 0.043283539377289, 0.043283539377289, \
                   0.043283539377289, 0.043283539377289, 0.043283539377289]

    elif (integrationOrder == 10):

        nIntegrationPoints = 25

        u = [0.333333333333333, 0.028844733232685, 0.485577633383657, 0.485577633383657, \
             0.781036849029926, 0.109481575485037, 0.109481575485037, 0.141707219414880, \
             0.307939838764121, 0.141707219414880, 0.550352941820999, 0.307939838764121, \
             0.550352941820999, 0.025003534762686, 0.246672560639903, 0.025003534762686, \
             0.728323904597411, 0.246672560639903, 0.728323904597411, 0.009540815400299, \
             0.066803251012200, 0.009540815400299, 0.923655933587500, 0.066803251012200, \
             0.923655933587500]

        v = [0.333333333333333, 0.485577633383657, 0.028844733232685, 0.485577633383657, \
             0.109481575485037, 0.781036849029926, 0.109481575485037, 0.307939838764121, \
             0.141707219414880, 0.550352941820999, 0.141707219414880, 0.550352941820999, \
             0.307939838764121, 0.246672560639903, 0.025003534762686, 0.728323904597411, \
             0.025003534762686, 0.728323904597411, 0.246672560639903, 0.066803251012200, \
             0.009540815400299, 0.923655933587500, 0.009540815400299, 0.923655933587500, \
             0.066803251012200]

        weights = [0.090817990382754, 0.036725957756467, 0.036725957756467, 0.036725957756467, \
                   0.045321059435528, 0.045321059435528, 0.045321059435528, 0.072757916845420, \
                   0.072757916845420, 0.072757916845420, 0.072757916845420, 0.072757916845420, \
                   0.072757916845420, 0.028327242531057, 0.028327242531057, 0.028327242531057, \
                   0.028327242531057, 0.028327242531057, 0.028327242531057, 0.009421666963733, \
                   0.009421666963733, 0.009421666963733, 0.009421666963733, 0.009421666963733, \
                   0.009421666963733]

    elif (integrationOrder == 12):

        nIntegrationPoints = 33

        u = [0.023565220452390, 0.488217389773805, 0.488217389773805, 0.120551215411079, \
             0.439724392294460, 0.439724392294460, 0.457579229975768, 0.271210385012116, \
             0.271210385012116, 0.744847708916828, 0.127576145541586, 0.127576145541586, \
             0.957365299093579, 0.021317350453210, 0.021317350453210, 0.115343494534698, \
             0.275713269685514, 0.115343494534698, 0.608943235779788, 0.275713269685514, \
             0.608943235779788, 0.022838332222257, 0.281325580989940, 0.022838332222257, \
             0.695836086787803, 0.281325580989940, 0.695836086787803, 0.025734050548330, \
             0.116251915907597, 0.025734050548330, 0.858014033544073, 0.116251915907597, \
             0.858014033544073]

        v = [0.488217389773805, 0.023565220452390, 0.488217389773805, 0.439724392294460, \
             0.120551215411079, 0.439724392294460, 0.271210385012116, 0.457579229975768, \
             0.271210385012116, 0.127576145541586, 0.744847708916828, 0.127576145541586, \
             0.021317350453210, 0.957365299093579, 0.021317350453210, 0.275713269685514, \
             0.115343494534698, 0.608943235779788, 0.115343494534698, 0.608943235779788, \
             0.275713269685514, 0.281325580989940, 0.022838332222257, 0.695836086787803, \
             0.022838332222257, 0.695836086787803, 0.281325580989940, 0.116251915907597, \
             0.025734050548330, 0.858014033544073, 0.025734050548330, 0.858014033544073, \
             0.116251915907597]

        weights = [0.025731066440455, 0.025731066440455, 0.025731066440455, 0.043692544538038, \
                   0.043692544538038, 0.043692544538038, 0.062858224217885, 0.062858224217885, \
                   0.062858224217885, 0.034796112930709, 0.034796112930709, 0.034796112930709, \
                   0.006166261051559, 0.006166261051559, 0.006166261051559, 0.040371557766381, \
                   0.040371557766381, 0.040371557766381, 0.040371557766381, 0.040371557766381, \
                   0.040371557766381, 0.022356773202303, 0.022356773202303, 0.022356773202303, \
                   0.022356773202303, 0.022356773202303, 0.022356773202303, 0.017316231108659, \
                   0.017316231108659, 0.017316231108659, 0.017316231108659, 0.017316231108659, \
                   0.017316231108659]

    return nIntegrationPoints, u, v, weights

#--------------------------------------------------------

def get_real_coords_from_barycentric_coords_coefficients(x1, y1, x2, y2, x3, y3):

    Cx = x1
    Cy = y1

    T11 = x2 - x1
    T21 = y2 - y1

    T12 = x3 - x1
    T22 = y3 - y1

    return T11, T12, T21, T22, Cx, Cy

#--------------------------------------------------------

def get_real_coords_from_barycentric_coords(u, v, T11, T12, T21, T22, Cx, Cy):

    x = T11 * u + T12 * v + Cx

    y = T21 * u + T22 * v + Cy

    return x, y

#--------------------------------------------------------

def get_analytical_stress_divergence_triangle(u, v, T11, T12, T21, T22, Cx, Cy, xMin, yMin):

    x, y = get_real_coords_from_barycentric_coords(u, v, T11, T12, T21, T22, Cx, Cy)

    uVel, vVel, e11, e22, e12, divu, divv = velocities_strains_stress_divergences(x-xMin, y-yMin)

    return divu, divv

#--------------------------------------------------------

def L2_norm_integral_triangle(numerical, nVertices, cellsOnVertex, xCell, yCell, areaTriangle, xMin, yMin, useVertex, divType):

    degreesToRadians = math.pi / 180.0

    L2_norm = 0.0
    Linf_norm = 0.0
    denom = 0.0

    nIntegrationPoints, u, v, weights = integration_weights_triangle(8)

    errors = []

    for iVertex in range(0,nVertices):

        if (useVertex[iVertex]):

            iCell1 = cellsOnVertex[iVertex,0]
            iCell2 = cellsOnVertex[iVertex,1]
            iCell3 = cellsOnVertex[iVertex,2]

            T11, T12, T21, T22, Cx, Cy = \
                get_real_coords_from_barycentric_coords_coefficients(xCell[iCell1], yCell[iCell1], \
                                                                     xCell[iCell2], yCell[iCell2], \
                                                                     xCell[iCell3], yCell[iCell3])

            divuIntegral = 0.0
            divvIntegral = 0.0
            for iWeight in range(0, nIntegrationPoints):

                divu, divv = get_analytical_stress_divergence_triangle(u[iWeight], v[iWeight], T11, T12, T21, T22, Cx, Cy, xMin, yMin)

                divuIntegral += weights[iWeight] * divu
                divvIntegral += weights[iWeight] * divv

            if (divType == "divu"):
                analytical = divuIntegral
            else:
                analytical = divvIntegral

            error = numerical[iVertex] - analytical
            errors.append(error)

            L2_norm = L2_norm + areaTriangle[iVertex] * math.pow(numerical[iVertex] - analytical,2)
            denom   = denom   + areaTriangle[iVertex] * math.pow(analytical,2)

            Linf_norm = max(Linf_norm, math.fabs(numerical[iVertex] - analytical))

        else:

            errors.append(0.0)

    L2_norm = math.sqrt(L2_norm / denom)

    errors = np.array(errors)

    return L2_norm, Linf_norm, errors

#--------------------------------------------------------

def get_norm_integral_triangle(filenameIC, filename, useVertex):

    fileMPAS = Dataset(filename, "r")

    nVertices = len(fileMPAS.dimensions["nVertices"])

    cellsOnVertex = fileMPAS.variables["cellsOnVertex"][:]
    cellsOnVertex[:] = cellsOnVertex[:] - 1
    xCell = fileMPAS.variables["xCell"][:]
    yCell = fileMPAS.variables["yCell"][:]
    xVertex = fileMPAS.variables["xVertex"][:]
    yVertex = fileMPAS.variables["yVertex"][:]
    areaTriangle = fileMPAS.variables["areaTriangle"][:]

    stressDivergenceU = fileMPAS.variables["stressDivergenceU"][0,:]
    stressDivergenceV = fileMPAS.variables["stressDivergenceV"][0,:]

    fileMPAS.close()

    xMin = np.amin(xVertex)
    xMax = np.amax(xVertex)
    yMin = np.amin(yVertex)
    yMax = np.amax(yVertex)

    L2_normU, Linf_normU, errorsU = L2_norm_integral_triangle(stressDivergenceU, nVertices, cellsOnVertex, xCell, yCell, areaTriangle, xMin, yMin, useVertex, "divu")
    L2_normV, Linf_normV, errorsV = L2_norm_integral_triangle(stressDivergenceV, nVertices, cellsOnVertex, xCell, yCell, areaTriangle, xMin, yMin, useVertex, "divv")

    fileMPAS = Dataset(filename, "a")

    try:
        varU = fileMPAS.createVariable("stressDivergenceUError","d",dimensions=["nVertices"])
        varV = fileMPAS.createVariable("stressDivergenceVError","d",dimensions=["nVertices"])
    except:
        varU = fileMPAS.variables["stressDivergenceUError"][:]
        varV = fileMPAS.variables["stressDivergenceVError"][:]
    varU[:] = errorsU[:]
    varV[:] = errorsV[:]

    fileMPAS.close()

    return L2_normU, L2_normV, Linf_normU, Linf_normV

#--------------------------------------------------------

def L2_norm_integral_square(numerical, nVertices, cellsOnVertex, xCell, yCell, areaTriangle, xMin, yMin, useVertex, divType):

    degreesToRadians = math.pi / 180.0

    L2_norm  = 0.0
    Linf_norm = 0.0
    denom = 0.0

    nIntegrationPoints, u, v, weights = integration_weights_triangle(8)

    errors = []

    for iVertex in range(0,nVertices):

        if (useVertex[iVertex]):

            divuIntegral = 0.0
            divvIntegral = 0.0

            # first triangle
            iCell1 = cellsOnVertex[iVertex,0]
            iCell2 = cellsOnVertex[iVertex,1]
            iCell3 = cellsOnVertex[iVertex,2]

            T11, T12, T21, T22, Cx, Cy = \
                get_real_coords_from_barycentric_coords_coefficients(xCell[iCell1], yCell[iCell1], \
                                                                     xCell[iCell2], yCell[iCell2], \
                                                                     xCell[iCell3], yCell[iCell3])

            for iWeight in range(0, nIntegrationPoints):

                divu, divv = get_analytical_stress_divergence_triangle(u[iWeight], v[iWeight], T11, T12, T21, T22, Cx, Cy, xMin, yMin)

                divuIntegral += weights[iWeight] * divu
                divvIntegral += weights[iWeight] * divv

            # second triangle
            iCell1 = cellsOnVertex[iVertex,2]
            iCell2 = cellsOnVertex[iVertex,3]
            iCell3 = cellsOnVertex[iVertex,0]

            T11, T12, T21, T22, Cx, Cy = \
                get_real_coords_from_barycentric_coords_coefficients(xCell[iCell1], yCell[iCell1], \
                                                                     xCell[iCell2], yCell[iCell2], \
                                                                     xCell[iCell3], yCell[iCell3])

            for iWeight in range(0, nIntegrationPoints):

                divu, divv = get_analytical_stress_divergence_triangle(u[iWeight], v[iWeight], T11, T12, T21, T22, Cx, Cy, xMin, yMin)

                divuIntegral += weights[iWeight] * divu
                divvIntegral += weights[iWeight] * divv

            divuIntegral *= 0.5
            divvIntegral *= 0.5

            if (divType == "divu"):
                analytical = divuIntegral
            else:
                analytical = divvIntegral

            error = numerical[iVertex] - analytical
            errors.append(error)

            L2_norm  = L2_norm  + areaTriangle[iVertex] * math.pow(numerical[iVertex] - analytical,2)
            denom    = denom    + areaTriangle[iVertex] * math.pow(analytical,2)

            Linf_norm = max(Linf_norm, math.fabs(numerical[iVertex] - analytical))

        else:

            errors.append(0.0)

    L2_norm = math.sqrt(L2_norm / denom)

    errors = np.array(errors)

    return L2_norm, Linf_norm, errors

#--------------------------------------------------------

def get_norm_integral_square(filenameIC, filename, useVertex):

    fileMPAS = Dataset(filename, "r")

    nVertices = len(fileMPAS.dimensions["nVertices"])

    cellsOnVertex = fileMPAS.variables["cellsOnVertex"][:]
    cellsOnVertex[:] = cellsOnVertex[:] - 1
    xCell = fileMPAS.variables["xCell"][:]
    yCell = fileMPAS.variables["yCell"][:]
    xVertex = fileMPAS.variables["xVertex"][:]
    yVertex = fileMPAS.variables["yVertex"][:]
    areaTriangle = fileMPAS.variables["areaTriangle"][:]

    stressDivergenceU = fileMPAS.variables["stressDivergenceU"][0,:]
    stressDivergenceV = fileMPAS.variables["stressDivergenceV"][0,:]

    fileMPAS.close()

    xMin = np.amin(xVertex)
    xMax = np.amax(xVertex)
    yMin = np.amin(yVertex)
    yMax = np.amax(yVertex)

    L2_normU, Linf_normU, errorsU = L2_norm_integral_square(stressDivergenceU, nVertices, cellsOnVertex, xCell, yCell, areaTriangle, xMin, yMin, useVertex, "divu")
    L2_normV, Linf_normV, errorsV = L2_norm_integral_square(stressDivergenceV, nVertices, cellsOnVertex, xCell, yCell, areaTriangle, xMin, yMin, useVertex, "divv")

    fileMPAS = Dataset(filename, "a")

    try:
        varU = fileMPAS.createVariable("stressDivergenceUError","d",dimensions=["nVertices"])
        varV = fileMPAS.createVariable("stressDivergenceVError","d",dimensions=["nVertices"])
    except:
        varU = fileMPAS.variables["stressDivergenceUError"][:]
        varV = fileMPAS.variables["stressDivergenceVError"][:]
    varU[:] = errorsU[:]
    varV[:] = errorsV[:]

    fileMPAS.close()

    return L2_normU, L2_normV, Linf_normU, Linf_normV

#--------------------------------------------------------

def L2_norm(numerical, analytical, nVertices, areaTriangle, useVertex):

    degreesToRadians = math.pi / 180.0

    #norms  = np.multiply(areaTriangle, np.power(numerical - analytical, 2))
    #denoms = np.multiply(areaTriangle, np.power(analytical, 2))

    L2_norm = 0.0
    Linf_norm = 0.0
    denom = 0.0

    errors = []

    for iVertex in range(0,nVertices):

        if (useVertex[iVertex]):

            error = numerical[iVertex] - analytical[iVertex]
            errors.append(error)

            L2_norm = L2_norm  + areaTriangle[iVertex] * math.pow(numerical[iVertex] - analytical[iVertex],2)
            denom   = denom    + areaTriangle[iVertex] * math.pow(analytical[iVertex],2)

            Linf_norm = max(Linf_norm, math.fabs(numerical[iVertex] - analytical[iVertex]))

        else:

            errors.append(0.0)

    #norm = np.sum(norms[useVertex])
    #denom = np.sum(norms[useVertex])

    L2_norm = math.sqrt(L2_norm / denom)

    errors = np.array(errors)

    return L2_norm, Linf_norm, errors

#--------------------------------------------------------

def get_norm(filenameIC, filename, useVertex):

    fileIC = Dataset(filenameIC, "r")

    stressDivergenceUAnalytical = fileIC.variables["stressDivergenceUAnalytical"][:]
    stressDivergenceVAnalytical = fileIC.variables["stressDivergenceVAnalytical"][:]

    fileIC.close()

    fileMPAS = Dataset(filename, "r")

    nVertices = len(fileMPAS.dimensions["nVertices"])

    latVertex = fileMPAS.variables["latVertex"][:]

    areaTriangle = fileMPAS.variables["areaTriangle"][:]

    stressDivergenceU = fileMPAS.variables["stressDivergenceU"][0,:]
    stressDivergenceV = fileMPAS.variables["stressDivergenceV"][0,:]

    fileMPAS.close()

    L2_normU, Linf_normU, errorsU = L2_norm(stressDivergenceU, stressDivergenceUAnalytical, nVertices, areaTriangle, useVertex)
    L2_normV, Linf_normV, errorsV = L2_norm(stressDivergenceV, stressDivergenceVAnalytical, nVertices, areaTriangle, useVertex)

    fileMPAS = Dataset(filename, "a")

    try:
        varU = fileMPAS.createVariable("stressDivergenceUError","d",dimensions=["nVertices"])
        varV = fileMPAS.createVariable("stressDivergenceVError","d",dimensions=["nVertices"])
    except:
        varU = fileMPAS.variables["stressDivergenceUError"][:]
        varV = fileMPAS.variables["stressDivergenceVError"][:]
    varU[:] = errorsU[:]
    varV[:] = errorsV[:]

    fileMPAS.close()

    return L2_normU, L2_normV, Linf_normU, Linf_normV

#--------------------------------------------------------

def get_resolution(filename, useVertex):

    fileMPAS = Dataset(filename, "r")

    nCells = len(fileMPAS.dimensions["nCells"])
    nEdges = len(fileMPAS.dimensions["nEdges"])

    cellsOnEdge = fileMPAS.variables["cellsOnEdge"][:]
    cellsOnEdge[:] = cellsOnEdge[:] - 1

    degreesToRadians = math.pi / 180.0

    dcEdge = fileMPAS.variables["dcEdge"][:]
    latEdge = fileMPAS.variables["latEdge"][:]

    resolution = 0.0
    denom = 0.0
    for iEdge in range(0,nEdges):
        iCell1 = cellsOnEdge[iEdge,0]
        iCell2 = cellsOnEdge[iEdge,1]
        if (iCell1 != -1 and iCell2 != -1):
            resolution = resolution + dcEdge[iEdge]
            denom = denom + 1.0

    resolution = resolution / denom

    fileMPAS.close()

    return resolution

#--------------------------------------------------------

def get_use_vertex(filenameIn):

    fileIn = Dataset(filenameIn,"r")
    nCells = len(fileIn.dimensions["nCells"])
    nVertices = len(fileIn.dimensions["nVertices"])
    nEdgesOnCell = fileIn.variables["nEdgesOnCell"][:]
    cellsOnCell = fileIn.variables["cellsOnCell"][:]
    cellsOnCell[:] = cellsOnCell[:] - 1
    verticesOnCell = fileIn.variables["verticesOnCell"][:]
    verticesOnCell[:] = verticesOnCell[:] - 1
    interiorCell = fileIn.variables["interiorCell"][0,:]
    fileIn.close()

    useVertex = np.ones(nVertices,dtype="i")
    for iCell in range(0,nCells):
        if (interiorCell[iCell] == 0):
            for iCellOnCell in range(0,nEdgesOnCell[iCell]):
                iCell2 = cellsOnCell[iCell,iCellOnCell]
                if (iCell2 < nCells):
                    for iVertexOnCell in range(0,nEdgesOnCell[iCell2]):
                        iVertex = verticesOnCell[iCell2,iVertexOnCell]
                        useVertex[iVertex] = 0

    return useVertex

#--------------------------------------------------------

def scaling_lines(axis, xMin, xMax, yMin):

    # linear scaling
    scale = yMin / math.pow(xMin,1)
    scaleMinLin = math.pow(xMin,1) * scale
    scaleMaxLin = math.pow(xMax,1) * scale

    # quadratic scaling
    scale = yMin / math.pow(xMin,2)
    scaleMinQuad = math.pow(xMin,2) * scale
    scaleMaxQuad = math.pow(xMax,2) * scale

    axis.loglog([xMin, xMax], [scaleMinLin,  scaleMaxLin],  linestyle=':', color='k')
    axis.loglog([xMin, xMax], [scaleMinQuad, scaleMaxQuad], linestyle=':', color='k')

#--------------------------------------------------------

def stress_divergence_scaling(testName, ignoreWeak=False):

    # options
    if (not ignoreWeak):
        operatorMethods = ["wachspress","pwl","weak"]
    else:
        operatorMethods = ["wachspress","pwl"]

    gridTypes = ["hex","quad"]
    #gridTypes = ["hex"]

    grids = {"hex" :["0082x0094",
                     "0164x0188",
                     "0328x0376",
                     "0656x0752"],
             "quad":["0080x0080",
                     "0160x0160",
                     "0320x0320",
                     "0640x0640"]}
    #grids = {"hex" :["0656x0752"],
    #         "quad":["0640x0640"]}


    # plot options
    lineColours = {"wachspress":"black",
                   "pwl":"grey",
                   "weak":"red"}

    lineStyles = {"hex":"solid",
                  "quad":"dashed"}

    legendLabels = {"wachspress":"Wachs.",
                    "pwl":"PWL",
                    "weak":"FV"}

    markers = {"wachspress":"+",
               "pwl":"x",
               "weak":"^"}


    # scaling lines
    xMin = 2e-3
    xMax = 3.5e-3
    yMin = {"L2":1.5e-3,
            "Linf":5e-1}

    # plot
    cm = 1/2.54  # centimeters in inches
    plt.rc('font', family='Times New Roman', size=8)
    plt.rc('mathtext',fontset="stix")
    SMALL_SIZE = 8
    MEDIUM_SIZE = 8
    BIGGER_SIZE = 8
    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


    fig, axes = plt.subplots(2, 2, figsize=(15*cm,15*cm))

    scaling_lines(axes[0,0], xMin, xMax, yMin["L2"])
    scaling_lines(axes[0,1], xMin, xMax, yMin["L2"])
    scaling_lines(axes[1,0], xMin, xMax, yMin["Linf"])
    scaling_lines(axes[1,1], xMin, xMax, yMin["Linf"])


    for gridType in gridTypes:

        print("Grid type: ", gridType)

        for operatorMethod in operatorMethods:

            print("  Operator Method: ", operatorMethod)

            x = []
            y_L2U = []
            y_L2V = []
            y_LinfU = []
            y_LinfV = []

            for grid in grids[gridType]:

                print("    Grid: ", grid)

                filenameIC = "ic_%s_%s_%s.nc" %(testName, gridType, grid)
                filename = "output_%s_%s_%s_%s/output.2000.nc" %(testName, gridType, operatorMethod, grid)
                print("      ", filename, filenameIC)

                useVertex = get_use_vertex(filename)

                if (gridType == "hex"):
                    #L2_normU, L2_normV, Linf_normU, Linf_normV = get_norm_integral_triangle(filenameIC, filename, useVertex)
                    L2_normU, L2_normV, Linf_normU, Linf_normV = get_norm(filenameIC, filename, useVertex)
                elif (gridType == "quad"):
                    #L2_normU, L2_normV, Linf_normU, Linf_normV = get_norm_integral_square(filenameIC, filename, useVertex)
                    L2_normU, L2_normV, Linf_normU, Linf_normV = get_norm(filenameIC, filename, useVertex)

                x.append(get_resolution(filename, useVertex))
                y_L2U.append(L2_normU)
                y_L2V.append(L2_normV)
                y_LinfU.append(Linf_normU)
                y_LinfV.append(Linf_normV)

            if (gridType == "hex"):
                legendLabel = legendLabels[operatorMethod]
            else:
                legendLabel = "_nolegend_"
            axes[0,0].loglog(x, y_L2U, color=lineColours[operatorMethod], ls=lineStyles[gridType], marker=markers[operatorMethod], markersize=5.0, label=legendLabel)
            axes[0,1].loglog(x, y_L2V, color=lineColours[operatorMethod], ls=lineStyles[gridType], marker=markers[operatorMethod], markersize=5.0, label=legendLabel)
            axes[1,0].loglog(x, y_LinfU, color=lineColours[operatorMethod], ls=lineStyles[gridType], marker=markers[operatorMethod], markersize=5.0, label=legendLabel)
            axes[1,1].loglog(x, y_LinfV, color=lineColours[operatorMethod], ls=lineStyles[gridType], marker=markers[operatorMethod], markersize=5.0, label=legendLabel)


    axes[0,0].legend(frameon=False, loc=2, fontsize=8, handlelength=2)
    axes[0,0].set_xlabel(None)
    axes[0,0].set_ylabel(r"$L_2$ error norm")
    axes[0,0].set_title(r"(a) $(\nabla \cdot \sigma)_u$",loc="left")
    axes[0,0].set_xticks(ticks=[3e-3,4e-3,5e-3,6e-3,7e-3,8e-3,9e-3],minor=True)
    axes[0,0].set_xticklabels(labels=[None,None,None,None,None,None,None],minor=True)
    axes[0,0].set_xticks(ticks=[2e-3,1e-2],minor=False)
    axes[0,0].set_xticklabels(labels=[r'$2\times 10^{-3}$',r'$10^{-2}$'],minor=False)

    axes[0,1].legend(frameon=False, loc=2, fontsize=8, handlelength=2)
    axes[0,1].set_xlabel(None)
    axes[0,1].set_ylabel(None)
    axes[0,1].set_title(r"(b) $(\nabla \cdot \sigma)_v$",loc="left")
    axes[0,1].set_xticks(ticks=[3e-3,4e-3,5e-3,6e-3,7e-3,8e-3,9e-3],minor=True)
    axes[0,1].set_xticklabels(labels=[None,None,None,None,None,None,None],minor=True)
    axes[0,1].set_xticks(ticks=[2e-3,1e-2],minor=False)
    axes[0,1].set_xticklabels(labels=[r'$2\times 10^{-3}$',r'$10^{-2}$'],minor=False)

    axes[1,0].legend(frameon=False, loc=2, fontsize=8, handlelength=2)
    axes[1,0].set_xlabel("Grid resolution")
    axes[1,0].set_ylabel(r"$L_\infty$ error norm")
    axes[1,0].set_title(r"(c) $(\nabla \cdot \sigma)_u$",loc="left")
    axes[1,0].set_xticks(ticks=[3e-3,4e-3,5e-3,6e-3,7e-3,8e-3,9e-3],minor=True)
    axes[1,0].set_xticklabels(labels=[None,None,None,None,None,None,None],minor=True)
    axes[1,0].set_xticks(ticks=[2e-3,1e-2],minor=False)
    axes[1,0].set_xticklabels(labels=[r'$2\times 10^{-3}$',r'$10^{-2}$'],minor=False)

    axes[1,1].legend(frameon=False, loc=2, fontsize=8, handlelength=2)
    axes[1,1].set_xlabel("Grid resolution")
    axes[1,1].set_ylabel(None)
    axes[1,1].set_title(r"(d) $(\nabla \cdot \sigma)_v$",loc="left")
    axes[1,1].set_xticks(ticks=[3e-3,4e-3,5e-3,6e-3,7e-3,8e-3,9e-3],minor=True)
    axes[1,1].set_xticklabels(labels=[None,None,None,None,None,None,None],minor=True)
    axes[1,1].set_xticks(ticks=[2e-3,1e-2],minor=False)
    axes[1,1].set_xticklabels(labels=[r'$2\times 10^{-3}$',r'$10^{-2}$'],minor=False)


    plt.tight_layout(pad=0.2, w_pad=0.6, h_pad=0.2)
    filenameOut = "stress_divergence_scaling_%s.png" %(testName)
    plt.savefig(filenameOut,dpi=300)
    filenameOut = "stress_divergence_scaling_%s.eps" %(testName)
    plt.savefig(filenameOut)

#-------------------------------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-t', dest='testName', help='')
    parser.add_argument('-w', dest='ignoreWeak', action='store_true', help='')

    args = parser.parse_args()

    stress_divergence_scaling(args.testName, args.ignoreWeak)
