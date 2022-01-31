# Histogram-Standardization

This repository contains the NiftyNet implementation of histogram standardization<sup>1</sup>, isolated from NiftyNet for convenience.

## Installation instructions 

1) Clone/download repository.

2) Change directory into repository.

3) Install:
	```
	pip install .
    ```
	
## How to use it 

- Function imports.

- Command line:

	- Training:
		```
		hist_train --train_dir .\sample_data\0_sample_train_t2w --landmarks_dir .\sample_data\0_sample_train_t2w
		```

	- Inference:
		```
		hist_std --infer_dir .\sample_data\0_sample_test_t2w --output_dir .\sample_data\1_standardized_test_t2w --landmarks_path .\sample_data\0_sample_train_t2w\landmarks.txt
		```
	
## References

<sup>1</sup> Nyúl, L.G.; Udupa, J.K.; Zhang, X. New variants of a method of MRI scale standardization. IEEE Trans. Med. Imaging 2000, 19, 143–150, doi:10.1109/42.836373