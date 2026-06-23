import numpy as np
import pandas as pd
import nibabel as nib
import statsmodels.api as sm
import statsmodels.formula.api as smf
# import segmentation and parcellation
def run_vascular_analysis():
vessel_nii = nib.load("subject1_session1_refined_vessels.nii.gz")
    vessel_mask = vessel_nii.get_fdata()
# load the Schaefer 2018 Local-Global Atlas
atlas_nii = nib.load("Schaefer2018_LocalGlobal_Parcellation_MNI152_1mm.nii.gz")
    atlas_data = atlas_nii.get_fdata()
# align for the same matrix space 
assert vessel_mask.shape == atlas_data.shape
# region of interests and their labels 
roi_labels = {
        "Precuneus": list(range(389, 411)),          # Labels 389–410
        "Parahippocampal_Gyrus": list(range(479, 485)), # Labels 479–484
        "Superior_Frontal_Gyrus": list(range(921, 926)) # Labels 921–925
    }

    print("--- Computing Regional Vessel Densities ---")
# apply atlas and cumpute density
def apply_atlas(atlas, vessels, labels):
    mask  = np.isin(atlas, list(labels))
    total = mask.sum()
    return ((mask) & (vessels == 1)).sum() / total if total > 0 else 0.0
 brain_mask_path = "/path"
    _, brain_mask, _ = ng.io.load_nifti_get_mask(brain_mask_path, is_mask=True)
    brain_mask_voxels = np.sum(brain_mask)

    vessel_mask_path = "/path"
    _, vessel_mask, _ = ng.io.load_nifti_get_mask(vessel_mask_path, is_mask=True)
    vessel_mask_voxels = np.sum(vessel_mask)

    vascular_density = vessel_mask_voxels / brain_mask_voxels
# stats model linear regression
def run_ols(df):
    model = smf.ols("Vessel_Density ~ C(Region)", data=df).fit()
    print(model.summary())

if __name__ == "__main__":
    df = compute_density()
    df.to_csv(os.path.join(BASE_DIR, "results", "vessel_density_summary.csv"), index=False)
    run_ols(df)
