#!/usr/bin/env python3

from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.miscmodels.ordinal_model import OrderedModel

import nigsp as ng


def compute_density(vessel_mask, parcel, labels):

    mask = np.isin(parcel, labels)
    total = mask.sum()

    density = 0
    if total > 0:
        density = (vessel_mask * mask).sum() / total

    return density


# stats model linear regression
def run_ols(df, mode):

    model = smf.ols("density ~ C(parcel, Poly)", data=df).fit()

    print("")
    print(f"~~~ OLS {mode}-wise ~~~")
    print("")
    print(model.summary())
    print("")
    print("")


# ordinal logit
def run_oml(df, mode):
    # Fit an ordinal logistic regression model using the logit link function
    model_ordinal = OrderedModel.from_formula("parcel ~ density", data=df, distr="logit").fit()

    print("")
    print(f"~~~ Ordinal logit model {mode}-wise ~~~")
    print("")
    print(model_ordinal.summary())
    print("")
    print("")


# stats model linear regression
def run_tau(df_in, mode):
    df = deepcopy(df_in)
    df["parcel_code"] = df["parcel"].cat.codes

    # Calculate rank correlations
    tau, kendall_p = stats.kendalltau(df["parcel_code"], df["density"])

    print("")
    print(f"~~~ OLS {mode}-wise ~~~")
    print("")
    print(f"Kendall's tau: {tau:.4f} (p-value: {kendall_p:.4f})")
    print("")
    print("")


def plot_ols(df, figname):
    sns.set_theme(style="whitegrid")

    # Initialize the figure
    f, ax = plt.subplots()
    sns.despine(bottom=True, left=True)

    # Show each observation with a scatterplot
    sns.stripplot(
        data=df, x="parcel", y="density", hue="sub",
        dodge=True, alpha=.25, zorder=1, legend=False,
    )

    # Show the conditional means, aligning each pointplot in the
    # center of the strips by adjusting the width allotted to each
    # category (.8 by default) by the number of hue levels
    sns.pointplot(
        data=df, x="parcel", y="density", hue="sub",
        dodge=.8 - .8 / 3, palette="dark", errorbar=None,
        markers="d", markersize=4, linestyle="none",
    )

    # Improve the legend
    # sns.move_legend(
    #     ax, loc="lower right", ncol=3, frameon=True, columnspacing=1, handletextpad=0,
    # )

    plt.tight_layout()
    plt.savefig(figname, dpi=300)
    plt.close()


if __name__ == "__main__":

    roi_labels = {
      'Precuneus': get_ids(range(359, 372), range(389, 411), range(896, 907), range(926, 938)),
    'Parahippocampal_Gyrus': get_ids(range(479, 485), range(975, 979)),
    'Superior_Frontal_Gyrus': get_ids(
        range(253, 260), range(269, 273), range(316, 332), range(346, 359), 
        range(385, 389), range(411, 423), range(445, 468), range(775, 783), 
        range(792, 797), range(843, 855), range(874, 896), range(921, 926), 
        range(938, 948), range(955, 969)
    ),
    'Visual_Cortex': get_ids(range(1, 35), range(501, 540))
    }

    # CRITICAL STEP: Define the true structural hierarchy of your categories
    # (Replace this list with your actual preferred ordering)
   parcel_hierarchy = ["Parahippocampal_Gyrus", "Precuneus", "Superior_Frontal_Gyrus", "Visual_Cortex"]

    ROI_rows = []
    parcel_rows = []

    for sub in range(1, 7):
        sub = f"{sub:02d}"

        vessel_path = f"/data/derivatives/vessels/manualsegready/00.sub-{sub}_ses-7T_part-mag_T2starw_imgavg_preprocessed_vessels.nii.gz"
        _, vessel_mask, _ = ng.io.load_nifti_get_mask(vessel_path, is_mask=True)

        parcel_path = f"/data/derivatives/Anastasija/sub-{sub}_Schaefer.nii.gz"
        parcel, _, _ = ng.io.load_nifti_get_mask(parcel_path, is_mask=True)

        for ROI in roi_labels.keys():
            ROI_density = compute_density(vessel_mask, parcel, roi_labels[ROI])
            ROI_rows.append({"sub": sub, "parcel": ROI, "density": ROI_density})

            for pn in roi_labels[ROI]:
                parcel_density = compute_density(vessel_mask, parcel, [pn])
                parcel_rows.append({"sub": sub, "parcel": pn, "density": parcel_density})

    ROI_table = pd.DataFrame(ROI_rows)
    ROI_table['parcel'] = pd.Categorical(ROI_table['parcel'], categories=parcel_hierarchy, ordered=True)

    parcel_table = pd.DataFrame(parcel_rows)

    ROI_table.to_csv("/data/derivatives/Anastasija/vessel_density_ROI.csv", index=False)
    parcel_table.to_csv("/data/derivatives/Anastasija/vessel_density_parcels.csv", index=False)

    run_tau(ROI_table, "ROI")
    run_tau(parcel_table, "parcel")

    run_ols(ROI_table, "ROI")
    run_ols(parcel_table, "parcel")

    run_oml(ROI_table, "ROI")
    run_oml(parcel_table, "parcel")

    plot_ols(ROI_table, "/data/derivatives/Anastasija/vessel_density_ROI.png")
    plot_ols(parcel_table, "/data/derivatives/Anastasija/vessel_density_parcels.png")

"""
Copyright 2026, Anastasija Krasikova.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
