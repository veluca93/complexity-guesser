#!/bin/bash
set -x
./test.py test_single_variable/sizes test_single_variable/constant
./test.py test_single_variable/sizes test_single_variable/linear
./test.py test_single_variable/sizes test_single_variable/nlogn
./test.py test_single_variable/sizes test_single_variable/quadratic
./test.py test_single_variable/sizes test_single_variable/cubic

./test.py test_many_variables/sizes test_many_variables/nlogn
./test.py test_many_variables/sizes test_many_variables/nm
./test.py test_many_variables/sizes test_many_variables/n2m
