from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
#-------------------------------------------------------------------------------

def plot_testcase():

    cm = 1/2.54  # centimeters in inches
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

    ### Air Specific Humidity and Air Temperature
    fig, axis = plt.subplots(figsize=(8*cm,7*cm))

    filein = Dataset("./output/output.2004.nc","r")

    airSpecificHumidity = filein.variables["airSpecificHumidity"][:,0]
    airTemperature = filein.variables["airTemperature"][:,0]

    filein.close()

    line1, = axis.plot(airTemperature,color="green",label="air T")
    axis.set_ylabel("air T (K)")
    axis.set_xlabel("Time step")
    axis.set_title("MPAS_Seaice ISPOL forcing")

    axis2 = axis.twinx()

    line2, = axis2.plot(airSpecificHumidity,color="red",label="airSpecificHumidity")
    axis2.set_ylabel("Spec. Humidity")

    axis2.legend(handles=[line1,line2],loc='lower left')

    plt.tight_layout()
    plt.savefig("single_cell_ispol_airT_humid.eps")
    plt.savefig("single_cell_ispol_airT_humid.png",dpi=300)

    ###  uAirVelocity vAirVelocity
    fig, axis = plt.subplots(figsize=(8*cm,7*cm))

    filein = Dataset("./output/output.2004.nc","r")
    uAirVelocity = filein.variables["uAirVelocity"][:,0]
    vAirVelocity = filein.variables["vAirVelocity"][:,0]

    filein.close()

    line1, = axis.plot(vAirVelocity,color="green",label="air v-vel")
    axis.set_ylabel("v-vel (m s-1)")
    axis.set_xlabel("Time step")
    axis.set_title("MPAS_Seaice ISPOL forcing")

    axis2 = axis.twinx()

    line2, = axis2.plot(uAirVelocity,color="red",label="air u-vel")
    axis2.set_ylabel("u-vel (m s-1)")

    axis2.legend(handles=[line1,line2],loc='lower left')

    plt.tight_layout()
    plt.savefig("single_cell_ispol_u_v_AirVel.eps")
    plt.savefig("single_cell_ispol_u_v_AirVel.png",dpi=300)

    ###  seaSurfaceTemperature seaSurfaceSalinity
    fig, axis = plt.subplots(figsize=(8*cm,7*cm))

    filein = Dataset("./output/output.2004.nc","r")
    seaSurfaceTemperature = filein.variables["seaSurfaceTemperature"][:,0]
    seaSurfaceSalinity = filein.variables["seaSurfaceSalinity"][:,0]

    filein.close()

    line1, = axis.plot(seaSurfaceSalinity,color="green",label="SSS")
    axis.set_ylabel("sss (ppt)")
    axis.set_xlabel("Time step")
    axis.set_title("MPAS_Seaice ISPOL forcing")

    axis2 = axis.twinx()

    line2, = axis2.plot(seaSurfaceTemperature,color="red",label="SST")
    axis2.set_ylabel("T (C)")

    axis2.legend(handles=[line1,line2],loc='upper right')

    plt.tight_layout()
    plt.savefig("single_cell_ispol_sst_sss.eps")
    plt.savefig("single_cell_ispol_sst_sss.png",dpi=300)

    ###  rainfallRate oceanMixedLayerDepth
    fig, axis = plt.subplots(figsize=(8*cm,7*cm))

    filein = Dataset("./output/output.2004.nc","r")
    rainfallRate = filein.variables["rainfallRate"][:,0]
    oceanMixedLayerDepth = filein.variables["oceanMixedLayerDepth"][:,0]

    filein.close()

    line1, = axis.plot(oceanMixedLayerDepth,color="green",label="MLD")
    axis.set_ylabel("MLD (m)")
    axis.set_xlabel("Time step")
    axis.set_title("MPAS_Seaice ISPOL forcing")

    axis2 = axis.twinx()

    line2, = axis2.plot(rainfallRate,color="red",label="rainfall")
    axis2.set_ylabel("rain (kg m-2 s-1)")

    axis2.legend(handles=[line1,line2],loc='lower left')

    plt.tight_layout()
    plt.savefig("single_cell_ispol_mld_rain.eps")
    plt.savefig("single_cell_ispol_mld_rain.png",dpi=300)

    ###  uOceanVelocity vOceanVelocity
    fig, axis = plt.subplots(figsize=(8*cm,7*cm))

    filein = Dataset("./output/output.2004.nc","r")
    uOceanVelocity = filein.variables["uOceanVelocity"][:,0]
    vOceanVelocity = filein.variables["vOceanVelocity"][:,0]

    filein.close()

    line1, = axis.plot(vOceanVelocity,color="green",label="ocean v-vel")
    axis.set_ylabel("v-vel (m s-1)")
    axis.set_xlabel("Time step")
    axis.set_title("MPAS_Seaice ISPOL forcing")

    axis2 = axis.twinx()

    line2, = axis2.plot(uOceanVelocity,color="red",label="ocean u-vel")
    axis2.set_ylabel("u-vel (m s-1)")

    axis2.legend(handles=[line1,line2],loc='lower left')

    plt.tight_layout()
    plt.savefig("single_cell_ispol_u_v_oceanVel.eps")
    plt.savefig("single_cell_ispol_u_v_oceanVel.png",dpi=300)

    ###  seaSurfaceTiltU seaSurfaceTiltV
    fig, axis = plt.subplots(figsize=(8*cm,7*cm))

    filein = Dataset("./output/output.2004.nc","r")
    seaSurfaceTiltU = filein.variables["seaSurfaceTiltU"][:,0]
    seaSurfaceTiltV = filein.variables["seaSurfaceTiltV"][:,0]

    filein.close()

    line1, = axis.plot(seaSurfaceTiltV,color="green",label="sea surface tilt (v)")
    axis.set_ylabel("v-tilt")
    axis.set_xlabel("Time step")
    axis.set_title("MPAS_Seaice ISPOL forcing")

    axis2 = axis.twinx()

    line2, = axis2.plot(seaSurfaceTiltU,color="red",label="sea surface tilt (u)")
    axis2.set_ylabel("u-tilt")

    axis2.legend(handles=[line1,line2],loc='lower left')

    plt.tight_layout()
    plt.savefig("single_cell_ispol_u_v_sstilt.eps")
    plt.savefig("single_cell_ispol_u_v_sstilt.png",dpi=300)

    ###  oceanNitrateConc oceanSilicateConc
    fig, axis = plt.subplots(figsize=(8*cm,7*cm))

    filein = Dataset("./output/output.2004.nc","r")
    oceanNitrateConc = filein.variables["oceanNitrateConc"][:,0]
    oceanSilicateConc = filein.variables["oceanSilicateConc"][:,0]

    filein.close()

    line1, = axis.plot(oceanSilicateConc,color="green",label="ocean SiO3")
    axis.set_ylabel("mmol Si m-3")
    axis.set_xlabel("Time step")
    axis.set_title("MPAS_Seaice ISPOL forcing")

    axis2 = axis.twinx()

    line2, = axis2.plot(oceanNitrateConc,color="red",label="ocean NO3")
    axis2.set_ylabel("mmol NO3 m-3")

    axis2.legend(handles=[line1,line2],loc='lower left')

    plt.tight_layout()
    plt.savefig("single_cell_ispol_ocean_nit_sil.eps")
    plt.savefig("single_cell_ispol_ocean_nit_sil.png",dpi=300)

    ###  shortwaveDown longwaveDown
    fig, axis = plt.subplots(figsize=(8*cm,7*cm))

    filein = Dataset("./output/output.2004.nc","r")
    shortwaveDown = filein.variables["shortwaveDown"][:,0]
    longwaveDown = filein.variables["longwaveDown"][:,0]

    filein.close()

    line1, = axis.plot(longwaveDown,color="green",label="longwave down")
    axis.set_ylabel("Longwave (W m-2)")
    axis.set_xlabel("Time step")
    axis.set_title("MPAS_Seaice ISPOL forcing")

    axis2 = axis.twinx()

    line2, = axis2.plot(shortwaveDown,color="red",label="shortwave down")
    axis2.set_ylabel("Shortwave (W m-2)")

    axis2.legend(handles=[line1,line2],loc='lower left')

    plt.tight_layout()
    plt.savefig("single_cell_ispol_long_shortwave.eps")
    plt.savefig("single_cell_ispol_long_shortwave.png",dpi=300)

#-------------------------------------------------------------------------------

if __name__ == "__main__":

    plot_testcase()
