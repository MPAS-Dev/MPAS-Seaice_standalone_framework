from netCDF4 import Dataset
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

#--------------------------------------------------------

def L2_norm_weak(numerical, analytical, nCells, areaCell, useCell):

    degreesToRadians = math.pi / 180.0

    norm  = 0.0
    denom = 0.0

    for iCell in range(0,nCells):

        if (useCell[iCell]):

            norm  = norm  + areaCell[iCell] * math.pow(numerical[iCell] - analytical[iCell],2)

            denom = denom + areaCell[iCell] * math.pow(analytical[iCell],2)

    norm = math.sqrt(norm / denom)

    return norm

#--------------------------------------------------------

def get_norm_weak(filenameIC, filename):

    fileIC = Dataset(filenameIC, "r")

    strain11CellAnalytical = fileIC.variables["strain11CellAnalytical"][:]
    strain22CellAnalytical = fileIC.variables["strain22CellAnalytical"][:]
    strain12CellAnalytical = fileIC.variables["strain12CellAnalytical"][:]

    fileIC.close()

    fileMPAS = Dataset(filename, "r")

    nCells = len(fileMPAS.dimensions["nCells"])

    areaCell = fileMPAS.variables["areaCell"][:]

    strain11weak = fileMPAS.variables["strain11weak"][0,:]
    strain22weak = fileMPAS.variables["strain22weak"][0,:]
    strain12weak = fileMPAS.variables["strain12weak"][0,:]

    useCell = get_use_cell(filename)

    normE11 = L2_norm_weak(strain11weak, strain11CellAnalytical, nCells, areaCell, useCell)
    normE22 = L2_norm_weak(strain22weak, strain22CellAnalytical, nCells, areaCell, useCell)
    normE12 = L2_norm_weak(strain12weak, strain12CellAnalytical, nCells, areaCell, useCell)

    fileMPAS.close()

    print(normE11, normE22, normE12)
    return normE11, normE22, normE12

#--------------------------------------------------------

def L2_norm_var(numerical, analytical, nCells, nEdgesOnCell, verticesOnCell, areaCell, useCell):

    degreesToRadians = math.pi / 180.0

    norm  = 0.0
    denom = 0.0

    for iCell in range(0,nCells):

        if (useCell[iCell]):

            for iVertexOnCell in range(0,nEdgesOnCell[iCell]):

                iVertex = verticesOnCell[iCell,iVertexOnCell]

                norm  = norm  + areaCell[iCell] * math.pow(numerical[iCell,iVertexOnCell] - analytical[iVertex],2)

                denom = denom + areaCell[iCell] * math.pow(analytical[iVertex],2)

    norm = math.sqrt(norm / denom)

    return norm

#--------------------------------------------------------

def get_norm_var(filenameIC, filename):

    fileIC = Dataset(filenameIC, "r")

    strain11VertexAnalytical = fileIC.variables["strain11VertexAnalytical"][:]
    strain22VertexAnalytical = fileIC.variables["strain22VertexAnalytical"][:]
    strain12VertexAnalytical = fileIC.variables["strain12VertexAnalytical"][:]

    fileIC.close()

    fileMPAS = Dataset(filename, "r")

    nCells = len(fileMPAS.dimensions["nCells"])

    areaCell = fileMPAS.variables["areaCell"][:]

    nEdgesOnCell = fileMPAS.variables["nEdgesOnCell"][:]
    verticesOnCell = fileMPAS.variables["verticesOnCell"][:]
    verticesOnCell[:] = verticesOnCell[:] - 1

    strain11var = fileMPAS.variables["strain11var"][0,:]
    strain22var = fileMPAS.variables["strain22var"][0,:]
    strain12var = fileMPAS.variables["strain12var"][0,:]

    useCell = get_use_cell(filename)

    normE11 = L2_norm_var(strain11var, strain11VertexAnalytical, nCells, nEdgesOnCell, verticesOnCell, areaCell, useCell)
    normE22 = L2_norm_var(strain22var, strain22VertexAnalytical, nCells, nEdgesOnCell, verticesOnCell, areaCell, useCell)
    normE12 = L2_norm_var(strain12var, strain12VertexAnalytical, nCells, nEdgesOnCell, verticesOnCell, areaCell, useCell)

    fileMPAS.close()

    return normE11, normE22, normE12

#--------------------------------------------------------

def L2_norm_var_avg(numerical, analytical, nVertices, areaTriangle, useVertex):

    degreesToRadians = math.pi / 180.0

    norm  = 0.0
    denom = 0.0

    for iVertex in range(0,nVertices):

        if (useVertex[iVertex]):

            norm  = norm  + areaTriangle[iVertex] * math.pow(numerical[iVertex] - analytical[iVertex],2)

            denom = denom + areaTriangle[iVertex] * math.pow(analytical[iVertex],2)

    norm = math.sqrt(norm / denom)

    return norm

#--------------------------------------------------------

def get_norm_var_avg(filenameIC, filename):

    fileIC = Dataset(filenameIC, "r")

    strain11VertexAnalytical = fileIC.variables["strain11VertexAnalytical"][:]
    strain22VertexAnalytical = fileIC.variables["strain22VertexAnalytical"][:]
    strain12VertexAnalytical = fileIC.variables["strain12VertexAnalytical"][:]

    fileIC.close()

    fileMPAS = Dataset(filename, "r")

    nVertices = len(fileMPAS.dimensions["nVertices"])

    areaTriangle = fileMPAS.variables["areaTriangle"][:]

    strain11varAvg = fileMPAS.variables["strain11varAvgVertex"][0,:]
    strain22varAvg = fileMPAS.variables["strain22varAvgVertex"][0,:]
    strain12varAvg = fileMPAS.variables["strain12varAvgVertex"][0,:]

    useVertex = get_use_vertex(filename)

    normE11 = L2_norm_var_avg(strain11varAvg, strain11VertexAnalytical, nVertices, areaTriangle, useVertex)
    normE22 = L2_norm_var_avg(strain22varAvg, strain22VertexAnalytical, nVertices, areaTriangle, useVertex)
    normE12 = L2_norm_var_avg(strain12varAvg, strain12VertexAnalytical, nVertices, areaTriangle, useVertex)

    fileMPAS.close()

    return normE11, normE22, normE12

#--------------------------------------------------------

def L2_norm_weak_avg(numerical, analytical, nVertices, areaTriangle, useVertex):

    norm  = 0.0
    denom = 0.0

    for iVertex in range(0,nVertices):

        if (useVertex[iVertex]):

            norm  += areaTriangle[iVertex] * math.pow(numerical[iVertex] - analytical[iVertex],2)

            denom += areaTriangle[iVertex] * math.pow(analytical[iVertex],2)

    norm = math.sqrt(norm / denom)

    return norm

#--------------------------------------------------------

def get_norm_weak_avg(filenameIC, filename):

    fileIC = Dataset(filenameIC, "r")

    strain11VertexAnalytical = fileIC.variables["strain11VertexAnalytical"][:]
    strain22VertexAnalytical = fileIC.variables["strain22VertexAnalytical"][:]
    strain12VertexAnalytical = fileIC.variables["strain12VertexAnalytical"][:]

    fileIC.close()

    fileMPAS = Dataset(filename, "r")

    nVertices = len(fileMPAS.dimensions["nVertices"])
    nCells = len(fileMPAS.dimensions["nCells"])
    vertexDegree = len(fileMPAS.dimensions["vertexDegree"])

    areaTriangle = fileMPAS.variables["areaTriangle"][:]
    areaCell = fileMPAS.variables["areaCell"][:]

    cellsOnVertex = fileMPAS.variables["cellsOnVertex"][:]
    cellsOnVertex[:] = cellsOnVertex[:] - 1

    strain11weak = fileMPAS.variables["strain11weak"][0,:]
    strain22weak = fileMPAS.variables["strain22weak"][0,:]
    strain12weak = fileMPAS.variables["strain12weak"][0,:]

    strain11weakAvg = np.zeros(nVertices)
    strain22weakAvg = np.zeros(nVertices)
    strain12weakAvg = np.zeros(nVertices)

    for iVertex in range(0,nVertices):

        strain11 = 0.0
        strain22 = 0.0
        strain12 = 0.0
        denominator = 0.0

        for iCellOnVertex in range(0,vertexDegree):
            iCell = cellsOnVertex[iVertex,iCellOnVertex]
            if (iCell < nCells):
                strain11 += areaCell[iCell] * strain11weak[iCell]
                strain22 += areaCell[iCell] * strain22weak[iCell]
                strain12 += areaCell[iCell] * strain12weak[iCell]
                denominator += areaCell[iCell]

        if (denominator > 0.0):
            strain11weakAvg[iVertex] = strain11 / denominator
            strain22weakAvg[iVertex] = strain22 / denominator
            strain12weakAvg[iVertex] = strain12 / denominator

    useVertex = get_use_vertex(filename)

    normE11 = L2_norm_var_avg(strain11weakAvg, strain11VertexAnalytical, nVertices, areaTriangle, useVertex)
    normE22 = L2_norm_var_avg(strain22weakAvg, strain22VertexAnalytical, nVertices, areaTriangle, useVertex)
    normE12 = L2_norm_var_avg(strain12weakAvg, strain12VertexAnalytical, nVertices, areaTriangle, useVertex)

    fileMPAS.close()

    return normE11, normE22, normE12

#--------------------------------------------------------

def get_resolution(filename):

    fileMPAS = Dataset(filename, "r")

    nCells = len(fileMPAS.dimensions["nCells"])
    nEdges = len(fileMPAS.dimensions["nEdges"])

    degreesToRadians = math.pi / 180.0

    cellsOnEdge = fileMPAS.variables["cellsOnEdge"][:]
    cellsOnEdge[:] = cellsOnEdge[:] - 1

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

def get_use_cell(filenameIn):

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

    useCell = np.ones(nCells,dtype="i")
    for iCell in range(0,nCells):
        if (interiorCell[iCell] == 0):
            useCell[iCell] = 0
            for iCellOnCell in range(0,nEdgesOnCell[iCell]):
                iCell2 = cellsOnCell[iCell,iCellOnCell]
                useCell[iCell2] = 0

    return useCell

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

def strain_scaling():

    mpl.rc('font', family='Times New Roman', size=8)
    mpl.rc('text', usetex=True)
    mpl.rcParams['axes.linewidth'] = 0.5

    strains = ["strain11","strain22","strain12"]

    operatorMethods = ["wachspress","pwl","weak","wachspress_avg","pwl_avg","weak_avg"]

    gridTypes = ["hex","quad"]
    #gridTypes = ["quad"]

    grids = {"hex" :["0082x0094",
                     "0164x0188",
                     "0328x0376",
                     "0656x0752"],
             "quad":["0080x0080",
                     "0160x0160",
                     "0320x0320",
                     "0640x0640"]}
    #grids = {"hex" :["0082x0094"],
    #         "quad":["0080x0080"]}


    dirname = {"wachspress":"wachspress",
               "pwl":"pwl",
               "weak":"weak",
               "wachspress_avg":"wachspress",
               "pwl_avg":"pwl",
               "weak_avg":"weak"}

    legendLabels = {"wachspress":"Wachspress",
                    "pwl":"PWL",
                    "weak":"Weak",
                    "wachspress_avg":"Wachs. Avg",
                    "pwl_avg":"PWL Avg",
                    "weak_avg":"Weak Avg"}

    lineColours = {"wachspress":"black",
                   "pwl":"grey",
                   "weak":"red",
                   "wachspress_avg":"blue",
                   "pwl_avg":"green",
                   "weak_avg":"purple"}

    markers = {"wachspress":"o",
               "pwl":"s",
               "weak":"^",
               "wachspress_avg":"o",
               "pwl_avg":"s",
               "weak_avg":"^"}

    lineStyles = {"hex":"solid",
                  "quad":"dashed"}

    strainLabels = {"strain11":r"(a) $\dot{\epsilon}_{11}$",
                    "strain22":r"(b) $\dot{\epsilon}_{22}$",
                    "strain12":r"(c) $\dot{\epsilon}_{12}$"}

    fig, axes = plt.subplots(3,1,figsize=(5,10))

    iStrain = 0
    for strain in strains:

        #xMin = 6e-3
        #xMax = 1e-2
        #yMin = 4e-4
        xMin = 2e-3
        xMax = 3.5e-3
        yMin = 4e-3

        # linear scaling
        scale = yMin / math.pow(xMin,1)
        scaleMinLin = math.pow(xMin,1) * scale
        scaleMaxLin = math.pow(xMax,1) * scale

        # quadratic scaling
        scale = yMin / math.pow(xMin,2)
        scaleMinQuad = math.pow(xMin,2) * scale
        scaleMaxQuad = math.pow(xMax,2) * scale

        axes[iStrain].loglog([xMin, xMax], [scaleMinLin,scaleMaxLin], linestyle=':', color='k')
        axes[iStrain].loglog([xMin, xMax], [scaleMinQuad,scaleMaxQuad], linestyle=':', color='k')

        for gridType in gridTypes:

            print("Grid type: ", gridType)

            iPlot = 0
            for operatorMethod in operatorMethods:

                print("  Operator Method: ", operatorMethod)

                x = []
                y = []

                for grid in grids[gridType]:

                    print("    Grid: ", grid)

                    filenameIC = "ic_%s_%s.nc" %(gridType,grid)
                    filename = "output_%s_%s_%s/output.2000.nc" %(gridType, dirname[operatorMethod], grid)

                    print("      ", filename, filenameIC)

                    if (operatorMethod == "wachspress" or
                        operatorMethod == "pwl"):
                        normE11, normE22, normE12 = get_norm_var(filenameIC, filename)
                    elif (operatorMethod == "weak"):
                        normE11, normE22, normE12 = get_norm_weak(filenameIC, filename)
                    elif (operatorMethod == "wachspress_avg" or
                          operatorMethod == "pwl_avg"):
                        normE11, normE22, normE12 = get_norm_var_avg(filenameIC, filename)
                    elif (operatorMethod == "weak_avg"):
                        normE11, normE22, normE12 = get_norm_weak_avg(filenameIC, filename)

                    x.append(get_resolution(filename))
                    if (strain == "strain11"):
                        y.append(normE11)
                    elif (strain == "strain22"):
                        y.append(normE22)
                    elif (strain == "strain12"):
                        y.append(normE12)

                if (gridType == "hex"):
                    legendLabel = "%s" %(legendLabels[operatorMethod])
                else:
                    legendLabel = "_nolegend_"
                axes[iStrain].loglog(x, y, marker=markers[operatorMethod], color=lineColours[operatorMethod], ls=lineStyles[gridType], markersize=5.0, label=legendLabel)

                iPlot = iPlot + 1

        axes[iStrain].legend(frameon=False, loc=4, fontsize=8, handlelength=4)

        axes[iStrain].set_xlabel("Grid resolution")
        axes[iStrain].set_ylabel(r"$L_2$ error norm")
        axes[iStrain].set_title(strainLabels[strain])

        iStrain = iStrain + 1


    plt.tight_layout()
    plt.savefig("strain_scaling.png", dpi=400)

#-------------------------------------------------------------------------------

if __name__ == "__main__":

    strain_scaling()
