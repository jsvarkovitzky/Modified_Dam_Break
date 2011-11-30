#!/usr/bin/env python
# encoding: utf-8
r"""
Contains all test suites for the 1d multi-layer code

Can run a particular test by giving the number of the test at the comand line

:Authors:
    Kyle Mandli (2011-05-11) Initial version
"""
# ============================================================================
#      Copyright (C) 2011 Kyle Mandli <mandli@amath.washington.edu>
#
#  Distributed under the terms of the Berkeley Software Distribution (BSD) 
#  license
#                     http://www.opensource.org/licenses/
# ============================================================================

import os
import sys
import numpy as np

import pyclaw.geotools.topotools as tt
import test_runs
import maketopo


tests = []

    
# Cases A & C Tester
class BenchmarkBaseTest(test_runs.Test):
    
    def __init__(self, test = "A"):
        super(BenchmarkBaseTest,self).__init__()
        
        import setrun
        self.run_data = setrun.setrun()

        self.name = "TestOutput"
        self.test = test
       
        if test == "A":
            self.run_data.clawdata.nout = 22
        elif test == "C":
            self.run_data.clawdata.nout = 28

    # Convert angle to degrees for the label
        self.prefix = "Case%s" % test
                     
    #Outputs settings from setrun.py    
    def __str__(self):
        output = super(BenchmarkBaseTest,self).__str__()
        output += "\nRundata:    \n%s" % self.run_data
        return output
        
    def write_data_objects(self):
        self.run_data.write()
        maketopo.generatetopo(self.test)

tests = []
tests.append(BenchmarkBaseTest("A"))   
tests.append(BenchmarkBaseTest("C"))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == 'all':
            tests_to_be_run = tests
        else:
            tests_to_be_run = []
            for test in sys.argv[1:]:
                tests_to_be_run.append(tests[int(test)])
        
        test_runs.run_tests(tests_to_be_run,parallel=False)
    
    else:
        test_runs.print_tests(tests)
