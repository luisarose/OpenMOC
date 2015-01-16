## Currently imports 'materials-test.py' which is a copy of 'c5g7-materials.py'
## and tests the materialize module by comparing the inputted values for all
## parameters to the values stored when the Material instance is created.

## Test cases from c5g7-materials:
##  UO2
##  MOX-4.3%
##  MOX-7%
##  MOX-8.7%
##  Fission Chamber

## Can also add tests for Guide Tube, Water, and Control Rod if that would be useful.
## Add water (don't need all fuels)

## make sure we get an error if we try energy group = 0
## test isFissionable

## This DOES NOT currently test the following modules because they aren't included in the test input file:
##  getDifCoefByGroup, getBucklingByGroup, getDifHat, getDifTilde

## This DOES NOT test the case where the filename is not a string

## This DOES NOT test the case where the filetype is unsupported.


    # test with H5/HDF5 data files:
        # check if filename has 'Energy Groups' attribute (an int/fl)
        # material_names = list(f) :: list version of the file
        # for name, should print INFO-level: Importing material (strname)
        # for each, generates a material instance and assigns the num Energy Groups to it
        # checks name of each and sets known values

import openmoc.materialize as materialize
import unittest
import imp
import sys
import optparse
import os

curpath = os.getcwd()
if 'test_materialize' in curpath:
    location = 'materials_test.py'
else:
    location = 'test_materialize/materials_test.py'

class test_python_files(unittest.TestCase):

    ## Test the materialize.py module for when the input is a
    ## .py file.

    @classmethod
    def setUpClass(cls):
        
        # Stores the input filename, the imported file,
        # and the output dictionary in the test class.
        
        cls._input = location
        cls._import = imp.load_source(cls._input, cls._input).dataset
        cls._output = materialize.materialize(cls._input)


        ########### importing the file fails when running the full suite
    
    def test_energy_group(self):

        # Asserts the number of energy groups is 7 (from file)
        
        data = self._import
        num_groups = data['Energy Groups']
        self.assertEqual(num_groups, 7)

    def test_num_of_materials(self):

        # Asserts the number of materials is the same in the data
        # and in the processed list
        
        data = self._import
        data = data['Materials']
        output = self._output
        self.assertEqual(len(data), len(output))

    def test_names_of_materials(self):

        # Makes sure every material in the imported file
        # is present in the output file.
        
        list_of_results = []
        list_of_true = []
        data = self._import
        data = data['Materials']
        output = self._output
        for material in data.keys():
            list_of_results.append(material in output)
            list_of_true.append(True)
        self.assertEqual(list_of_results, list_of_true)



##################################################################################
################################   Test Case: UO2   ##############################
##################################################################################

class test_UO2(unittest.TestCase):

    ## Test the assigned values to UO2 match those in the input file.

    @classmethod
    def setUpClass(cls):
        cls._input = location
        cls._import = imp.load_source(cls._input, cls._input).dataset
        cls._output = materialize.materialize(cls._input)
        data = cls._import
        cls._data = data['Materials']
        cls._UO2_input = cls._data['UO2']
        cls._UO2_output = cls._output['UO2']

    def test_UO2_totalXS(self):

        UO2_input = self._UO2_input
        UO2_output = self._UO2_output
        UO2_TotalXS_input = UO2_input['Total XS']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for energy_group in xrange(1, len(UO2_TotalXS_input)+1):

            # identify what was passed in for SigmaT here
            SigmaT = UO2_TotalXS_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(UO2_output.getSigmaTByGroup(energy_group) - SigmaT) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_UO2_scatteringXS(self):

        # The input is a list of num_groups**2 values that should be mapped as follows:
        # list[0] = getSigmaSByGroup(1,1)
        # list[1] = getSigmaSByGroup(2,1)
        # list[2] = getSigmaSByGroup(3,1), etc.


        UO2_input = self._UO2_input
        UO2_output = self._UO2_output
        UO2_Scattering_input = UO2_input['Scattering XS']
        list_of_results = []
        list_of_true = []
        num_energy_groups = int((len(UO2_Scattering_input))**0.5)

        #print len(UO2_Scattering_input)
        #print UO2_Scattering_input
        
        input_list_index = 0
        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for group2 in xrange(1, num_energy_groups + 1):

            for group1 in xrange(1, num_energy_groups + 1):
            
                # identify what was passed in for SigmaS at this point
                SigmaS = UO2_Scattering_input[input_list_index]
                input_list_index += 1           
                list_of_true.append(True)
                list_of_results.append(abs(UO2_output.getSigmaSByGroup(group1, group2) - SigmaS) < 0.05)

                # debugging code
                if abs(UO2_output.getSigmaSByGroup(group1, group2) - SigmaS) >= 0.05:
                    print 'PROBLEM AREA!!!!', group1, group2
                    print 'We expected:', SigmaS, 'We got:', UO2_output.getSigmaSByGroup(group1, group2)

        len(list_of_results)
        self.assertEqual(list_of_results, list_of_true)

    def test_UO2_fissionXS(self):

        UO2_input = self._UO2_input
        UO2_output = self._UO2_output
        UO2_FissionXS_input = UO2_input['Fission XS']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for energy_group in xrange(1, len(UO2_FissionXS_input)+1):

            # identify what was passed in for SigmaT here
            SigmaF = UO2_FissionXS_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(UO2_output.getSigmaFByGroup(energy_group) - SigmaF) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_UO2_nu_fissionXS(self):

        UO2_input = self._UO2_input
        UO2_output = self._UO2_output
        UO2_NuFissionXS_input = UO2_input['Nu Fission XS']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for energy_group in xrange(1, len(UO2_NuFissionXS_input)+1):

            # identify what was passed in for SigmaT here
            NuSigmaF = UO2_NuFissionXS_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(UO2_output.getNuSigmaFByGroup(energy_group) - NuSigmaF) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_UO2_chi(self):

        UO2_input = self._UO2_input
        UO2_output = self._UO2_output
        UO2_Chi_input = UO2_input['Chi']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for energy_group in xrange(1, len(UO2_Chi_input)+1):

            # identify what was passed in for SigmaT here
            Chi = UO2_Chi_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(UO2_output.getChiByGroup(energy_group) - Chi) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_UO2_absorptionXS(self):

        UO2_input = self._UO2_input
        UO2_output = self._UO2_output
        UO2_AbsorptionXS_input = UO2_input['Absorption XS']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaA to the assigned value.
        for energy_group in xrange(1, len(UO2_AbsorptionXS_input)+1):

            # identify what was passed in for SigmaA here
            SigmaA = UO2_AbsorptionXS_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(UO2_output.getSigmaAByGroup(energy_group) - SigmaA) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_UO2_is_fissionable(self):
        UO2_output = self._UO2_output
        self.assertTrue(UO2_output.isFissionable())


#############################################################################################
################################   Test Case: Fission Chamber  ##############################
#############################################################################################


class test_fission_chamber(unittest.TestCase):

    ## Test the assigned values to UO2 match those in the input file.

    @classmethod
    def setUpClass(cls):
        
        # pass in directory in input (default - empty, pass in directory if outside immediate directory)

        cls._input = location
        cls._import = imp.load_source(cls._input, cls._input).dataset
        cls._output = materialize.materialize(cls._input)
        data = cls._import
        cls._data = data['Materials']
        cls._FissionChamber_input = cls._data['Fission Chamber']
        cls._FissionChamber_output = cls._output['Fission Chamber']

    def test_FC_totalXS(self):

        FC_input = self._FissionChamber_input
        FC_output = self._FissionChamber_output
        FC_TotalXS_input = FC_input['Total XS']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for energy_group in xrange(1, len(FC_TotalXS_input)+1):

            # identify what was passed in for SigmaT here
            SigmaT = FC_TotalXS_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(FC_output.getSigmaTByGroup(energy_group) - SigmaT) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_FC_scatteringXS(self):

        # The input is a list of num_groups**2 values that should be mapped as follows:
        # list[0] = getSigmaSByGroup(1,1)
        # list[1] = getSigmaSByGroup(2,1)
        # list[2] = getSigmaSByGroup(3,1), etc.

        FC_input = self._FissionChamber_input
        FC_output = self._FissionChamber_output
        FC_ScatteringXS_input = FC_input['Scattering XS']
        list_of_results = []
        list_of_true = []
        
        num_energy_groups = int((len(FC_ScatteringXS_input))**0.5)
        
        input_list_index = 0
        
        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for group1 in xrange(1, num_energy_groups + 1):

            for group2 in xrange(1, num_energy_groups + 1):
            
                # identify what was passed in for SigmaS at this point
                SigmaS = FC_ScatteringXS_input[input_list_index]
                input_list_index += 1           
                list_of_true.append(True)
                list_of_results.append(abs(FC_output.getSigmaSByGroup(group1, group2) - SigmaS) < 0.05)

                # debugging code
##                if abs(FC_output.getSigmaSByGroup(group1, group2) - SigmaS) >= 0.05:
##                    print 'PROBLEM AREA!!!!', group1, group2
##                    print FC_output.getSigmaSByGroup(group1, group2), ' should be ', SigmaS

        len(list_of_results)
        self.assertEqual(list_of_results, list_of_true)

    def test_FC_fissionXS(self):

        FC_input = self._FissionChamber_input
        FC_output = self._FissionChamber_output
        FC_FissionXS_input = FC_input['Fission XS']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for energy_group in xrange(1, len(FC_FissionXS_input)+1):

            # identify what was passed in for SigmaT here
            SigmaF = FC_FissionXS_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(FC_output.getSigmaFByGroup(energy_group) - SigmaF) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_FC_nu_fissionXS(self):

        FC_input = self._FissionChamber_input
        FC_output = self._FissionChamber_output
        FC_NuFissionXS_input = FC_input['Nu Fission XS']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for energy_group in xrange(1, len(FC_NuFissionXS_input)+1):

            # identify what was passed in for SigmaT here
            NuSigmaF = FC_NuFissionXS_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(FC_output.getNuSigmaFByGroup(energy_group) - NuSigmaF) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_FC_chi(self):

        FC_input = self._FissionChamber_input
        FC_output = self._FissionChamber_output
        FC_Chi_input = FC_input['Chi']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for energy_group in xrange(1, len(FC_Chi_input)+1):

            # identify what was passed in for SigmaT here
            Chi = FC_Chi_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(FC_output.getChiByGroup(energy_group) - Chi) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_FC_absorptionXS(self):

        FC_input = self._FissionChamber_input
        FC_output = self._FissionChamber_output
        FC_AbsorptionXS_input = FC_input['Absorption XS']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaA to the assigned value.
        for energy_group in xrange(1, len(FC_AbsorptionXS_input)+1):

            # identify what was passed in for SigmaA here
            SigmaA = FC_AbsorptionXS_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(FC_output.getSigmaAByGroup(energy_group) - SigmaA) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_FC_is_fissionable(self):
        FC_output = self._FissionChamber_output
        self.assertTrue(FC_output.isFissionable())


################################################################################
#############################   Test Case: Water  ##############################
################################################################################


class test_water(unittest.TestCase):

    ## Test the assigned values to UO2 match those in the input file.

    @classmethod
    def setUpClass(cls):
        cls._input = location
        cls._import = imp.load_source(cls._input, cls._input).dataset
        cls._output = materialize.materialize(cls._input)
        data = cls._import['Materials']
        cls._Water_input = data['Water']
        cls._Water_output = cls._output['Water']

    def test_water_totalXS(self):

        Water_input = self._Water_input
        Water_output = self._Water_output
        Water_TotalXS_input = Water_input['Total XS']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for energy_group in xrange(1, len(Water_TotalXS_input)+1):

            # identify what was passed in for SigmaT here
            SigmaT = Water_TotalXS_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(Water_output.getSigmaTByGroup(energy_group) - SigmaT) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_water_scatteringXS(self):

        # The input is a list of num_groups**2 values that should be mapped as follows:
        # list[0] = getSigmaSByGroup(1,1)
        # list[1] = getSigmaSByGroup(1,2)
        # list[2] = getSigmaSByGroup(1,3), etc.

        Water_input = self._Water_input
        Water_output = self._Water_output
        Water_ScatteringXS_input = Water_input['Scattering XS']
        list_of_results = []
        list_of_true = []
        
        num_energy_groups = int((len(Water_ScatteringXS_input))**0.5)
        
        input_list_index = 0
        
        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for group1 in xrange(1, num_energy_groups + 1):

            for group2 in xrange(1, num_energy_groups + 1):
            
                # identify what was passed in for SigmaS at this point
                SigmaS = Water_ScatteringXS_input[input_list_index]
                input_list_index += 1           
                list_of_true.append(True)
                list_of_results.append(abs(Water_output.getSigmaSByGroup(group1, group2) - SigmaS) < 0.05)

        self.assertEqual(list_of_results, list_of_true)

    def test_water_fissionXS(self):

        Water_input = self._Water_input
        Water_output = self._Water_output
        Water_FissionXS_input = Water_input['Fission XS']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for energy_group in xrange(1, len(Water_FissionXS_input)+1):

            # identify what was passed in for SigmaT here
            SigmaF = Water_FissionXS_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(Water_output.getSigmaFByGroup(energy_group) - SigmaF) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_water_nu_fissionXS(self):

        Water_input = self._Water_input
        Water_output = self._Water_output
        Water_NuFissionXS_input = Water_input['Nu Fission XS']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for energy_group in xrange(1, len(Water_NuFissionXS_input)+1):

            # identify what was passed in for SigmaT here
            NuSigmaF = Water_NuFissionXS_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(Water_output.getNuSigmaFByGroup(energy_group) - NuSigmaF) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_water_chi(self):

        Water_input = self._Water_input
        Water_output = self._Water_output
        Water_Chi_input = Water_input['Chi']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaT to the assigned value.
        for energy_group in xrange(1, len(Water_Chi_input)+1):

            # identify what was passed in for SigmaT here
            Chi = Water_Chi_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(Water_output.getChiByGroup(energy_group) - Chi) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_water_absorptionXS(self):

        Water_input = self._Water_input
        Water_output = self._Water_output
        Water_AbsorptionXS_input = Water_input['Absorption XS']
        list_of_results = []
        list_of_true = []

        # for each energy group, compare the value that SHOULD be SigmaA to the assigned value.
        for energy_group in xrange(1, len(Water_AbsorptionXS_input)+1):

            # identify what was passed in for SigmaA here
            SigmaA = Water_AbsorptionXS_input[energy_group - 1]
            
            list_of_true.append(True)
            list_of_results.append(abs(Water_output.getSigmaAByGroup(energy_group) - SigmaA) < 0.05)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_water_is_fissionable(self):
        Water_output = self._Water_output
        self.assertFalse(Water_output.isFissionable())

class test_material_file(unittest.TestCase):

    ## Runs basic tests (num energy groups, num materials, names of materials) on an input file
    ## and the Material() object created from that file.

    ## TODO: Create a framework that would also test the values for each material
    ## in the input file.

    def __init__(filename):
        self._input = filename
        
    @classmethod
    def setUpClass(cls):

        cls._import = imp.load_source(cls._input, cls._input).dataset
        cls._output = materialize.materialize(cls._input)

    def test_energy_group(self):

        # Asserts the number of energy groups is the same as the lengths of the cross-section lists
        
        data = self._import
        num_groups = data['Energy Groups']
        list_of_results = []
        list_of_true = []

        for material in data['Materials']:
            for attribute in material:
                if attribute != 'Scattering XS':
                    list_of_results.append(len(attribute) == num_groups)
                list_of_true.append(True)
        
        self.assertEqual(list_of_results, list_of_true)

    def test_num_of_materials(self):

        # Asserts the number of materials is the same in the data
        # and in the processed list
        
        data = self._import
        data = data['Materials']
        output = self._output
        self.assertEqual(len(data), len(output))

    def test_names_of_materials(self):

        # Makes sure every material in the imported file
        # is present in the output file.
        
        list_of_results = []
        list_of_true = []
        data = self._import
        data = data['Materials']
        output = self._output
        for material in data.keys():
            list_of_results.append(material in output)
            list_of_true.append(True)
        self.assertEqual(list_of_results, list_of_true)


    

    

test_materials_py_suite = unittest.TestSuite()
test_materials_py_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_python_files))
test_materials_py_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_UO2))
test_materials_py_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_fission_chamber))
test_materials_py_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_water))


## Currently all the _getValueByGroup methods are broken -- update

## this is just playing around with command line stuff. please ignore for now
##
##p = optparse.OptionParser()
##p.add_option('--custom', '-c')
##opts, arguments = p.parse_args()
##if '--custom' in opts or '-c' in opts:
##    print 'success'
##    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMaterialFile))
##    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCustomMaterials))


## if sys.argv says to use custom one:
##  for attr in input_attributes:
##      add test case

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_materials_py_suite)

