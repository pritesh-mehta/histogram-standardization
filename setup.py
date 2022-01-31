"""
@author: pritesh-mehta
"""

from setuptools import setup, find_packages

setup(name='histogram_standardization',
      version='1.0',
      description='Histogram standardization (Nyul et al)',
      url='https://github.com/pritesh-mehta/histogram_standardization',
      python_requires='>=3.6',
      author='Pritesh Mehta',
      author_email='pritesh.mehta@kcl.ac.uk',
      license='Apache 2.0',
      zip_safe=False,
      install_requires=[
      'numpy',
      'pathlib',
      'argparse',
      'nibabel',
      'six',
      ],
      entry_points={
        'console_scripts': [
            'hist_train=histogram_standardization.hist_train:process',
            'hist_std=histogram_standardization.hist_std:process',
            ],
      },
      packages=find_packages(include=['histogram_standardization']),
      classifiers=[
          'Intended Audience :: Science/Research',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
      ]
      )