"""
@author: pritesh-mehta
"""

import numpy as np
from pathlib import Path
from argparse import ArgumentParser

import histogram_standardization.nifti_utilities as nutil
import histogram_standardization.histogram_standardization as hs

def hist_train(train_dir, landmarks_dir, cutoff_l=0.01, cutoff_h=0.99, 
          mask_dir=None, extension='.nii.gz'):
    """This function extracts histogram landmarks from a training dataset
    """
    percentiles_database = []
    landmarks_dict = {}    
    paths = nutil.path_generator(train_dir, extension=extension)
    for path in paths:
        name, nii, data = nutil.load(path)
        
        if mask_dir != None:
            ma_path = Path(mask_dir) / name + extension
            ma_name, ma_nii, ma_data = nutil.load(ma_path, dtype=np.bool)
        else:
            ma_data = np.ones_like(data, dtype=np.bool)
        
        cutoff = [cutoff_l, cutoff_h]        
        percentiles = hs.__compute_percentiles(data, ma_data, cutoff)
        percentiles_database.append(percentiles)
    percentiles_database = np.vstack(percentiles_database)
    s1, s2 = hs.create_standard_range()

    landmarks_dict['Data'] = tuple(hs.__averaged_mapping(percentiles_database, s1, s2))
    landmarks_path = Path(landmarks_dir) / 'landmarks.txt'
    hs.write_all_mod_mapping(landmarks_path, landmarks_dict)
    
    return None

def process():
    parser = ArgumentParser()
    parser.add_argument('--train_dir', required=True, type=str)
    parser.add_argument('--landmarks_dir', required=True, type=str)
    parser.add_argument('--cutoff_l', required=False, type=float, default=0.01)
    parser.add_argument('--cutoff_h', required=False, type=float, default=0.99)
    parser.add_argument('--mask_dir', required=False, type=str)
    parser.add_argument('--extension', required=False, type=str, default='.nii.gz')
    
    args = parser.parse_args()
    hist_train(args.train_dir, args.landmarks_dir,
          cutoff_l=args.cutoff_l, cutoff_h=args.cutoff_h, 
          mask_dir=args.mask_dir, extension=args.extension)
    
if __name__ == "__main__":
    process()

