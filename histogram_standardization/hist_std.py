"""
@author: Pritesh Mehta
"""

import os
import numpy as np
import numpy.ma as ma
from pathlib import Path
from argparse import ArgumentParser

import histogram_standardization.nifti_utilities as nutil
import histogram_standardization.histogram_standardization as hs

def hist_std(data, landmarks_path, cutoff_l=0.01, cutoff_h=0.99,
                    norm_type='percentile', post_whitening=False, mask_data=None):
    # histogram landmarks
    landmarks_path = os.path.abspath(landmarks_path)
    mapping = hs.read_mapping_file(landmarks_path)
    mapping = mapping['Data']
    
    if mask_data is None:
        mask_data = np.ones_like(data, dtype=np.bool)
        
    # perform standardisation
    cutoff = [cutoff_l, cutoff_h]
    std_data = hs.transform_by_mapping(data, mask_data, mapping, cutoff, type_hist=norm_type)
        
    # perform whitening
    if post_whitening == True:
        masked_data = ma.masked_array(std_data, np.logical_not(mask_data))
        std_data = (std_data - masked_data.mean()) / max(masked_data.std(), 1e-5)
        
    return std_data
    
def hist_std_dir(infer_dir, output_dir, landmarks_path, 
                 cutoff_l=0.01, cutoff_h=0.99, norm_type='percentile', 
                 mask_dir=None, post_whitening=False, 
                 extension='nii.gz'):
        
    # histogram landmarks
    landmarks_path = os.path.abspath(landmarks_path)
    mapping = hs.read_mapping_file(landmarks_path)
    mapping = mapping['Data']
    
    # standardise images
    paths = nutil.path_generator(infer_dir, extension=extension)
    for path in paths:
        name, nii, data = nutil.load(path)
        print("Processing:", name)
        
        if mask_dir != None:
            mask_path = Path(mask_dir) / name + extension
            mask_name, mask_nii, mask_data = nutil.load(mask_path, dtype=np.bool)
        else:
            mask_data = np.ones_like(data, dtype=np.bool)
        
        # perform standardisation
        cutoff = [cutoff_l, cutoff_h]
        std_data = hs.transform_by_mapping(data, mask_data, mapping, cutoff, type_hist=norm_type)
        
        # perform whitening
        if post_whitening == True:
            masked_data = ma.masked_array(std_data, np.logical_not(mask_data))
            std_data = (std_data - masked_data.mean()) / max(masked_data.std(), 1e-5)
        
        output_path = Path(output_dir) / name
        nutil.save(output_path, nii, std_data)
            
    return None

def process():
    parser = ArgumentParser()
    parser.add_argument('--infer_dir', required=True, type=str)
    parser.add_argument('--output_dir', required=True, type=str)
    parser.add_argument('--landmarks_path', required=True, type=str)
    parser.add_argument('--cutoff_l', required=False, type=float, default=0.01)
    parser.add_argument('--cutoff_h', required=False, type=float, default=0.99)
    parser.add_argument('--norm_type', required=False, type=str, default='percentile')
    parser.add_argument('--mask_dir', required=False, type=str)
    parser.add_argument('--post_whitening', required=False, action="store_true")
    parser.add_argument('--extension', required=False, type=str, default='nii.gz')
    
    args = parser.parse_args()
    hist_std_dir(args.infer_dir, args.output_dir,
                    args.landmarks_path, cutoff_l=args.cutoff_l, cutoff_h=args.cutoff_h, norm_type=args.norm_type,
                    mask_dir=args.mask_dir, post_whitening=args.post_whitening,
                    extension=args.extension)
    
if __name__ == "__main__":
    process()
