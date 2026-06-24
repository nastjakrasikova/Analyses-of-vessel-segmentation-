#!/usr/bin/env bash

mkdir -p /data/derivatives/Anastasija

for sub in $(seq -f %02g 1 6)
do
	anat_reference=/data/derivatives/vessels/sub-${sub}/ses-7T/reg/sub-${sub}_vesselref.nii.gz
	T1w2std_linear=/data/derivatives/vessels/sub-${sub}/ses-02/reg/sub-${sub}_ses-02_UNIT12std0GenericAffine.mat
	std2T1w_warp=/data/derivatives/vessels/sub-${sub}/ses-02/reg/sub-${sub}_ses-02_UNIT12std1InverseWarp.nii.gz
	T1w2T2starw_linear=/data/derivatives/vessels/sub-${sub}/ses-7T/reg/sub-${sub}_ses-02_UNIT12vesselref0GenericAffine.mat

	antsApplyTransforms -d 3 -i /scripts/Schaefer2018_1000Parcels_17Networks_order_FSLMNI152_1mm.nii.gz \
						-r ${anat_reference} \
						-o /data/derivatives/Anastasija/sub-${sub}_Schaefer.nii.gz \
						-n MultiLabel \
						-t ${T1w2T2starw_linear} \
						-t [${T1w2std_linear},1] \
						-t ${std2T1w_warp}
done

# Copyright 2026, Anastasija Krasikova.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
