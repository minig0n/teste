import os
import numpy as np
import simnibs


# Load the simulation result
files = 'filespath'

directoryNames = []
for entry_name in os.listdir(files):
    entry_path = os.path.join(files, entry_name)
    if os.path.isdir(entry_path):
        directoryNames.append(entry_name)

print(directoryNames)

values = np.zeros((32,20))
clusters=["Cluster1_L", "Cluster1_R", "Cluster2_L", "Cluster2_R", "Cluster3_L", "Cluster3_R", "Cluster4_L", 
            "Cluster4_R", "Cluster5_L", "Cluster5_R", "Cluster6_L", "Cluster6_R", "Cluster7_L", "Cluster7_R", 
            "Cluster8_L", "Cluster8_R", "Cluster9_L", "Cluster9_R", "Cluster10_L", "Cluster10_R"]

# clusters = ["Cluster1_L", "Cluster1_R"]

i = 0
for sub in directoryNames:
    os.chdir(str(sub))
    j = 0
    for c in clusters:
        # Read the simulation result
        head_mesh = simnibs.read_msh(os.path.join(str(sub), 'TDCS_1_scalar', str(c), '.msh'))

        # Crop the mesh to have only gray matter volume elements
        gray_matter = head_mesh.crop_mesh(2)

        mask_idx = gray_matter.field['from_volume'][:]

        # Radius
        r = 0.1

        # Define the ROI
        ROI = mask_idx > r

        # Get field and calculate the mean
        field_name='normE'
        efield = gray_matter.field[field_name][:]
        elm_vols = gray_matter.elements_volumes_and_areas()[:]

        avg_field_roi = np.average(efield[ROI], weights=elm_vols[ROI])
        values[i][j] = avg_field_roi

        j += 1
    i += 1

    os.chdir('..')

# lol
