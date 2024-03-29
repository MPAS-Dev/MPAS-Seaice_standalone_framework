from netCDF4 import Dataset
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
import argparse

#--------------------------------------------------------

def L2_norm(numerical, analytical, nVertices, latVertex, areaTriangle, latitudeLimit):

    degreesToRadians = math.pi / 180.0

    L2_norm  = 0.0
    Linf_norm = 0.0
    denom = 0.0

    for iVertex in range(0,nVertices):

        if (math.fabs(latVertex[iVertex]) > latitudeLimit * degreesToRadians):

            L2_norm  = L2_norm  + areaTriangle[iVertex] * math.pow(numerical[iVertex] - analytical[iVertex],2)
            denom    = denom    + areaTriangle[iVertex] * math.pow(analytical[iVertex],2)

            Linf_norm = max(Linf_norm,math.fabs(numerical[iVertex] - analytical[iVertex]))

    L2_norm = math.sqrt(L2_norm / denom)

    return L2_norm, Linf_norm

#--------------------------------------------------------

def get_norm(filenameIC, filename, latitudeLimit):

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

    L2_normU, Linf_normU = L2_norm(stressDivergenceU, stressDivergenceUAnalytical, nVertices, latVertex, areaTriangle, latitudeLimit)
    L2_normV, Linf_normV = L2_norm(stressDivergenceV, stressDivergenceVAnalytical, nVertices, latVertex, areaTriangle, latitudeLimit)

    fileMPAS.close()

    return L2_normU, L2_normV, Linf_normU, Linf_normV

#--------------------------------------------------------

def get_resolution(filename, latitudeLimit):

    fileMPAS = Dataset(filename, "r")

    nCells = len(fileMPAS.dimensions["nCells"])
    nEdges = len(fileMPAS.dimensions["nEdges"])

    degreesToRadians = math.pi / 180.0

    dcEdge = fileMPAS.variables["dcEdge"][:]
    latEdge = fileMPAS.variables["latEdge"][:]

    resolution = 0.0
    denom = 0.0
    for iEdge in range(0,nEdges):
        if (math.fabs(latEdge[iEdge]) > latitudeLimit * degreesToRadians):
            resolution = resolution + dcEdge[iEdge]
            denom = denom + 1.0

    resolution = resolution / denom

    fileMPAS.close()

    return resolution

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

def stress_divergence_scaling(testName):

    resolutions = [2562,10242,40962,163842]

    #methods = ["wachspress", "pwl", "weak", "wachspress_alt", "pwl_alt"]
    methods = ["wachspress", "pwl", "wachspress_alt", "pwl_alt"]


    latitudeLimit = 20.0

    # plot options
    legendLabels = {"wachspress":"Wachs.",
                    "pwl":"PWL",
                    "weak":"Weak",
                    "wachspress_alt":"Wachs. alt",
                    "pwl_alt":"PWL alt."}

    lineColors = {"wachspress":"black",
                  "pwl":"grey",
                  "weak":"red",
                  "wachspress_alt":"black",
                  "pwl_alt":"grey"}

    lineStyles = {"wachspress":"solid",
                  "pwl":"solid",
                  "weak":"solid",
                  "wachspress_alt":"dashed",
                  "pwl_alt":"dashed"}

    markers = {"wachspress":"+",
               "pwl":"x",
               "weak":"^",
               "wachspress_alt":"+",
               "pwl_alt":"x"}

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


    # scaling lines
    xMin = 2.5e-2
    xMax = 5e-2
    yMin_L2 = 2.5e-3
    yMin_Linf = 2e-1

    fig, axes = plt.subplots(2,2,figsize=(15*cm,15*cm))

    scaling_lines(axes[0,0], xMin, xMax, yMin_L2)
    scaling_lines(axes[0,1], xMin, xMax, yMin_L2)
    scaling_lines(axes[1,0], xMin, xMax, yMin_Linf)
    scaling_lines(axes[1,1], xMin, xMax, yMin_Linf)

    for method in methods:

        print("Operator method: ", method)

        x = []
        y_L2U = []
        y_L2V = []
        y_LinfU = []
        y_LinfV = []

        for resolution in resolutions:

            filename = "./output_%s_%s_%i/output.2000.nc" %(testName,method,resolution)
            filenameIC = "./ic_%s.%i.nc" %(testName,resolution)

            print("  ", filename, filenameIC)

            L2_normU, L2_normV, Linf_normU, Linf_normV = get_norm(filenameIC, filename, latitudeLimit)

            x.append(get_resolution(filename, latitudeLimit))
            y_L2U.append(L2_normU)
            y_L2V.append(L2_normV)
            y_LinfU.append(Linf_normU)
            y_LinfV.append(Linf_normV)

        axes[0,0].loglog(x,y_L2U, marker=markers[method], color=lineColors[method], ls=lineStyles[method], markersize=5.0, label=legendLabels[method])
        axes[0,1].loglog(x,y_L2V, marker=markers[method], color=lineColors[method], ls=lineStyles[method], markersize=5.0, label=legendLabels[method])
        axes[1,0].loglog(x,y_LinfU, marker=markers[method], color=lineColors[method], ls=lineStyles[method], markersize=5.0, label=legendLabels[method])
        axes[1,1].loglog(x,y_LinfV, marker=markers[method], color=lineColors[method], ls=lineStyles[method], markersize=5.0, label=legendLabels[method])


    axes[0,0].legend(frameon=False, loc=2, fontsize=8, handlelength=4)
    axes[0,0].set_xlabel(None)
    axes[0,0].set_ylabel(r"$L_2$ error norm")
    axes[0,0].set_title(r'(a) $(\nabla \cdot \sigma)_u$', loc="left")
    axes[0,0].set_xticks(ticks=[9e-3,2e-2,3e-2,4e-2,6e-2,7e-2,8e-2],minor=True)
    axes[0,0].set_xticklabels(labels=[None,None,None,None,None,None,None],minor=True)
    axes[0,0].set_xticks(ticks=[1e-2,5e-2],minor=False)
    axes[0,0].set_xticklabels(labels=[r'$10^{-2}$',r'$5\times10^{-2}$'],minor=False)

    axes[0,1].legend(frameon=False, loc=2, fontsize=8, handlelength=4)
    axes[0,1].set_xlabel(None)
    axes[0,1].set_ylabel(None)
    axes[0,1].set_title(r'(b) $(\nabla \cdot \sigma)_v$', loc="left")
    axes[0,1].set_xticks(ticks=[9e-3,2e-2,3e-2,4e-2,6e-2,7e-2,8e-2],minor=True)
    axes[0,1].set_xticklabels(labels=[None,None,None,None,None,None,None],minor=True)
    axes[0,1].set_xticks(ticks=[1e-2,5e-2],minor=False)
    axes[0,1].set_xticklabels(labels=[r'$10^{-2}$',r'$5\times10^{-2}$'],minor=False)

    axes[1,0].legend(frameon=False, loc=2, fontsize=8, handlelength=4)
    axes[1,0].set_xlabel("Grid resolution")
    axes[1,0].set_ylabel(r"$L_\infty$ error norm")
    axes[1,0].set_title(r'(c) $(\nabla \cdot \sigma)_u$', loc="left")
    axes[1,0].set_xticks(ticks=[9e-3,2e-2,3e-2,4e-2,6e-2,7e-2,8e-2],minor=True)
    axes[1,0].set_xticklabels(labels=[None,None,None,None,None,None,None],minor=True)
    axes[1,0].set_xticks(ticks=[1e-2,5e-2],minor=False)
    axes[1,0].set_xticklabels(labels=[r'$10^{-2}$',r'$5\times10^{-2}$'],minor=False)

    axes[1,1].legend(frameon=False, loc=2, fontsize=8, handlelength=4)
    axes[1,1].set_xlabel("Grid resolution")
    axes[1,1].set_ylabel(None)
    axes[1,1].set_title(r'(d) $(\nabla \cdot \sigma)_v$', loc="left")
    axes[1,1].set_xticks(ticks=[9e-3,2e-2,3e-2,4e-2,6e-2,7e-2,8e-2],minor=True)
    axes[1,1].set_xticklabels(labels=[None,None,None,None,None,None,None],minor=True)
    axes[1,1].set_xticks(ticks=[1e-2,5e-2],minor=False)
    axes[1,1].set_xticklabels(labels=[r'$10^{-2}$',r'$5\times10^{-2}$'],minor=False)

    plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.5)
    plt.savefig("stress_divergence_scaling_%s.png" %(testName),dpi=400)

#-------------------------------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-t', dest='testName', help='')

    args = parser.parse_args()

    stress_divergence_scaling(args.testName)
