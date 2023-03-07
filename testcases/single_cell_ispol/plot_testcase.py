from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
#-------------------------------------------------------------------------------

def plot_testcase():

    cm = 1/2.54  # centimeters in inches
    #plt.rc('font', family="Times")
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

    fig, axis = plt.subplots(figsize=(8*cm,7*cm))

    filein = Dataset("./output/output.2004.nc","r")

    iceVolumeCell = filein.variables["iceVolumeCell"][:,0]
    snowVolumeCell = filein.variables["snowVolumeCell"][:,0]
    surfaceTemperatureCell = filein.variables["surfaceTemperatureCell"][:,0]

    filein.close()

    line1, = axis.plot(surfaceTemperatureCell,color="green",label="surfaceT")
    axis.set_ylabel("Temperature (C)")
    axis.set_xlabel("Time step")
    axis.set_title("MPAS_Seaice ISPOL cell")

    axis2 = axis.twinx()

    line2, = axis2.plot(iceVolumeCell,color="red",label="iceVolume")
    line3, = axis2.plot(snowVolumeCell,color="blue",label="snowVolume")
    axis2.set_ylabel("Thickness (m)")
    axis2.set_ylim(0,None)

    axis2.legend(handles=[line1,line2,line3],loc='lower right')

    plt.tight_layout()
    plt.savefig("single_cell_ispol.eps")
    plt.savefig("single_cell_ispol.png",dpi=300)

    ###  Plot BGC fields
    filein = Dataset("./output/output.2004.nc","r")

    interfaceBiologyGrid = filein.variables["interfaceBiologyGrid"][:]
    verticalNitrateConcCell = filein.variables["verticalNitrateIceCell"][:,0,:]
    verticalAlgaeConcCell = filein.variables["verticalAlgaeIceCell"][:,0,:]
    netBrineHeight = filein.variables["netBrineHeight"][:,0]
    verticalSilicateConcCell = filein.variables["verticalSilicateIceCell"][:,0,:]
    verticalAmmoniumConcCell = filein.variables["verticalAmmoniumIceCell"][:,0,:]
    verticalDONConcCell = filein.variables["verticalDONIceCell"][:,0,:]
    verticalDOCConcCell = filein.variables["verticalDOCIceCell"][:,0,:]
    verticalDICConcCell = filein.variables["verticalDICIceCell"][:,0,:]
    verticaldFeConcCell = filein.variables["verticalDissolvedIronIceCell"][:,0,:]

    nTime1 = filein.dimensions["Time"]
    nTime = nTime1.size

    nBiogrid1 = filein.dimensions["nBioLayersP1"]
    nBioLayersP1 = nBiogrid1.size
    filein.close()

    totNitrate = np.linspace(1,nTime,nTime,dtype=float)*0
    totSilicate = np.linspace(1,nTime,nTime,dtype=float)*0
    totAmmonium= np.linspace(1,nTime,nTime,dtype=float)*0
    totAlgalN = np.linspace(1,nTime,nTime,dtype=float)*0
    algae1  = np.linspace(1,nBioLayersP1,nBioLayersP1,dtype=float)*0
    algae2  = np.linspace(1,nBioLayersP1,nBioLayersP1,dtype=float)*0
    totalalgae = np.linspace(1,nBioLayersP1,nBioLayersP1,dtype=float)*0

    DOC1  = np.linspace(1,nBioLayersP1,nBioLayersP1,dtype=float)*0
    DOC2  = np.linspace(1,nBioLayersP1,nBioLayersP1,dtype=float)*0
    totDOCtmp = np.linspace(1,nBioLayersP1,nBioLayersP1,dtype=float)*0
    totDOC = np.linspace(1,nTime,nTime,dtype=float)*0
    totDON = np.linspace(1,nTime,nTime,dtype=float)*0
    totDIC = np.linspace(1,nTime,nTime,dtype=float)*0
    totdFe = np.linspace(1,nTime,nTime,dtype=float)*0

    for cnt in range(0,nTime):
        bgrid = interfaceBiologyGrid[:] * netBrineHeight[cnt]
        totNitrate[cnt] = np.nansum(verticalNitrateConcCell[cnt,:]*bgrid[:])
        totSilicate[cnt] = np.nansum(verticalSilicateConcCell[cnt,:]*bgrid[:])
        totAmmonium[cnt] = np.nansum(verticalAmmoniumConcCell[cnt,:]*bgrid[:])
        algae1[:] = verticalAlgaeConcCell[cnt,0:nBioLayersP1]
        algae2[:] = verticalAlgaeConcCell[cnt,nBioLayersP1:2*nBioLayersP1]
        DOC1[:] = verticalDOCConcCell[cnt,0:nBioLayersP1]
        DOC2[:] = verticalDOCConcCell[cnt,nBioLayersP1:2*nBioLayersP1]
        totDOCtmp[:] = DOC1[:] + DOC2[:]
        totDOC[cnt] = np.nansum(totDOCtmp[:]*bgrid[:])
        totDON[cnt] = np.nansum(verticalDONConcCell[cnt,:]*bgrid[:])
        totDIC[cnt] = np.nansum(verticalDICConcCell[cnt,:]*bgrid[:])
        totdFe[cnt] = np.nansum(verticaldFeConcCell[cnt,:]*bgrid[:])
        totalgae = algae1[:] + algae2[:]
        totAlgalN[cnt] = np.nansum(totalgae[:]*bgrid[:])

    ###  total Algal Nitrogen, total Silicate, total Ammonium, total Nitrate
    fig, axis = plt.subplots(figsize=(8*cm,7*cm))

    line1, = axis.plot(totAlgalN,color="green",label="tot Algal N")
    axis.set_ylabel("Algae (mmol N m-2)")
    axis.set_xlabel("Time step")
    axis.set_title("MPAS_Seaice ISPOL BGC")

    axis2 = axis.twinx()

    line2, = axis2.plot(totNitrate,color="red",label="Nitrate")
    line3, = axis2.plot(totSilicate,color="blue",label="Silicate")
    line4, = axis2.plot(totAmmonium,color="cyan",label="Ammonium")
    axis2.set_ylabel("(mmol m-3)")
    axis2.set_ylim(0,None)

    axis2.legend(handles=[line1,line2,line3,line4],loc='upper right')

    plt.tight_layout()
    plt.savefig("single_cell_ispol_bgc.eps")
    plt.savefig("single_cell_ispol_bgc.png",dpi=300)

    ### total dissolved organic carbon (minus proteins), total dissolved organic nitrogen
    fig, axis = plt.subplots(figsize=(8*cm,7*cm))

    line1, = axis.plot(totDOC,color="green",label="DOC (minus proteins)")
    axis.set_ylabel("DOC (mmol C m-2)")
    axis.set_xlabel("Time step")
    axis.set_title("MPAS_Seaice ISPOL BGC")

    axis2 = axis.twinx()

    line2, = axis2.plot(totDON,color="red",label="DON")
    axis2.set_ylabel("DON (mmol N m-2)")

    axis2.legend(handles=[line1,line2],loc='upper right')

    plt.tight_layout()
    plt.savefig("single_cell_ispol_DOC_DON.eps")
    plt.savefig("single_cell_ispol_DOC_DON.png",dpi=300)

    ###  DIC, dissolved iron
    fig, axis = plt.subplots(figsize=(8*cm,7*cm))

    line1, = axis.plot(totDIC,color="green",label="DIC")
    axis.set_ylabel("DIC (mmol C m-2)")
    axis.set_xlabel("Time step")
    axis.set_title("MPAS_Seaice ISPOL BGC")

    axis2 = axis.twinx()

    line2, = axis2.plot(totdFe,color="red",label="dissolve Fe")
    axis2.set_ylabel("dFe (mmol Fe m-2)")

    axis2.legend(handles=[line1,line2],loc='lower right')

    plt.tight_layout()
    plt.savefig("single_cell_ispol_DIC_dfe.eps")
    plt.savefig("single_cell_ispol_DIC_dfe.png",dpi=300)

#-------------------------------------------------------------------------------

if __name__ == "__main__":

    plot_testcase()
