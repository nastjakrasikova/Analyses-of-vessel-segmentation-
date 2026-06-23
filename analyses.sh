antsApplyTransforms -d 3 -i ${std_in}.nii.gz \
					-r ${anat_reference}.nii.gz -o ${std}2anat.nii.gz \
					-n GenericLabel -t [${anat}2std0GenericAffine.mat,1] -t ${anat}2std1InverseWarp.nii.gz
