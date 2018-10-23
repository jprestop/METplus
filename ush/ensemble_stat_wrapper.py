#!/usr/bin/env python

'''
Program Name: ensemble_stat_wrapper.py
Contact(s): metplus-dev
Abstract:  Initial template based on grid_stat_wrapper by George McCabe
History Log:  Initial version
Usage: 
Parameters: None
Input Files:
Output Files:
Condition codes: 0 for success, 1 for failure
'''

from __future__ import (print_function, division)

import os
import met_util as util
from compare_ensemble_wrapper import CompareEnsembleWrapper

"""!@namespace EnsembleStatWrapper
@brief Wraps the MET tool ensemble_stat to compare ensemble datasets
@endcode
"""
class EnsembleStatWrapper(CompareEnsembleWrapper):
    """!Wraps the MET tool ensemble_stat to compare ensemble datasets
    """
    def __init__(self, p, logger):
        super(EnsembleStatWrapper, self).__init__(p, logger)
        self.met_install_dir = p.getdir('MET_INSTALL_DIR')
        self.app_path = os.path.join(self.met_install_dir, 'bin/ensemble_stat')
        self.app_name = os.path.basename(self.app_path)

        # create the ensemble stat dictionary.
        self.ce_dict = self.create_ce_dict()

    def create_ce_dict(self):
        """!Create a dictionary containing the values set in the config file
           that are required for running ensemble stat.
           This will make it easier for unit testing.

           Returns:
               @returns A dictionary of the ensemble stat values 
                        from the config file.
        """

        ce_dict = dict()

        # Loop by initialization times 
        ce_dict['LOOP_BY_INIT'] = \
            self.p.getbool('config', 'LOOP_BY_INIT', True)

        # A list of forecast hours from the initialization time that will
        # be processed.
        ce_dict['LEAD_SEQ'] = \
            util.getlistint(self.p.getstr('config', 'LEAD_SEQ', '0'))

        ce_dict['MODEL_TYPE'] = self.p.getstr('config', 'MODEL_TYPE', 'FCST')
        ce_dict['OB_TYPE'] = self.p.getstr('config', 'OB_TYPE', 'OBS')

        ce_dict['CONFIG_DIR'] = \
            self.p.getdir('CONFIG_DIR',
                          self.p.getdir('METPLUS_BASE')+'/parm/met_config')
        ce_dict['CONFIG_FILE'] = \
            self.p.getstr('config', 'ENSEMBLE_STAT_CONFIG',
                          ce_dict['CONFIG_DIR']+'/EnsembleStatConfig_SFC')

        # No Default being set this is REQUIRED TO BE DEFINED in conf file.
        ce_dict['ENSEMBLE_NUMBER_OF_MEMBERS'] = \
            self.p.getstr('config','ENSEMBLE_NUMBER_OF_MEMBERS')

        ce_dict['FCST_IS_PROB'] = self.p.getbool('config', 'FCST_IS_PROB', False)

        ce_dict['OBS_INPUT_DIR'] = \
          self.p.getdir('OBS_ENSEMBLE_STAT_INPUT_DIR')

        # The Observations input files used by ensemble_stat. 
        # This is a raw string and will be interpreted to generate the 
        # filenames.
        ce_dict['OBS_INPUT_TEMPLATE'] = \
          util.getraw_interp(self.p, 'filename_templates',
                               'OBS_INPUT_TEMPLATE')

        # The ensemble forecast files input directory and filename templates
        ce_dict['FCST_INPUT_DIR'] = \
          self.p.getdir('FCST_ENSEMBLE_STAT_INPUT_DIR')

        # This is a raw string and will be interpreted to generate the 
        # ensemble member filenames.
        ce_dict['FCST_INPUT_TEMPLATE'] = \
          util.getraw_interp(self.p, 'filename_templates',
                               'FCST_ENSEMBLE_STAT_INPUT_TEMPLATE')


        ce_dict['OUTPUT_DIR'] =  self.p.getdir('ENSEMBLE_STAT_OUT_DIR')
        ce_dict['INPUT_BASE'] =  self.p.getdir('INPUT_BASE')

        # The max forecast lead in hours.
        ce_dict['FCST_MAX_FORECAST'] = \
            self.p.getint('config', 'FCST_MAX_FORECAST', 24)
        ce_dict['FCST_INIT_INTERVAL'] = \
            self.p.getint('config', 'FCST_INIT_INTERVAL', 12)

        ce_dict['WINDOW_RANGE_BEG'] = \
          self.p.getint('config', 'WINDOW_RANGE_BEG', -3600)
        ce_dict['WINDOW_RANGE_END'] = \
          self.p.getint('config', 'WINDOW_RANGE_END', 3600)
        ce_dict['OBS_EXACT_VALID_TIME'] = \
            self.p.getbool('config','OBS_EXACT_VALID_TIME',True)
        return ce_dict


if __name__ == "__main__":
        util.run_stand_alone("ensemble_stat_wrapper", "EnsembleStat")
