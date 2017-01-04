#!/usr/bin/env python

from setuptools import setup

setup(name='openbmp-mrt',
      version='0.1.0',
      description='OpenBMP MRT',
      author='Tim Evens',
      author_email='tim@openbmp.org',
      url='',
      data_files=[('etc', ['src/etc/openbmp-mrt.yml'])],
      package_dir={'openbmp': 'src/site-packages/openbmp', 'openbmp.mrt': 'src/site-packages/openbmp/mrt'},
      packages=['openbmp', 'openbmp.mrt'],
      scripts=['src/bin/openbmp-mrt']
     )
