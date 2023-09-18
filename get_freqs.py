## FINISHED ##

import yaml
from FreqState import FreqState
import numpy as np

def get_freqs(fmax=1500, fmin=300, U=1):
    '''
    Inputs
    ------
    fmax: float
        maximum frequency to observe in MHz
        default: 1500 MHz
    fmin: float
        minimum frequency to observe in MHz
        default: 300 MHz
    U: int
        upchannelization factor
    '''
    

    # calculations
    coarse_df = 0.586
    df = coarse_df / U

    nfreq = int(np.ceil((fmax - fmin)/df))

    fstate = FreqState()
    fstate.freq = (fmax, fmin, nfreq)
    
    return fstate

yaml_input_file = open("inputs.yaml")
yaml_input = yaml.safe_load(yaml_input_file)
U = yaml_input['frequencies']['U']
fmax = yaml_input['frequencies']['fmax']
fmin = yaml_input['frequencies']['fmin']
output_folder = yaml_input['process']['output_folder']
nside = yaml_input['mapmaking']['nside']
ndays = yaml_input['mapmaking']['ndays']
catalog = yaml_input['process']['catalog']
tsys = yaml_input['telescope']['tsys']
yaml_input_file.close()

fstate = get_freqs(fmax, fmin, U)

# calculating the frequencies for cora maps
nfreqmaps = int(fstate.frequencies.size / U)

with open("outputs.yaml") as istream:
    ymldoc = yaml.safe_load(istream)
    ymldoc['fstate']['f_start'] = float(fstate.frequencies[0])
    ymldoc['fstate']['f_end'] = float(fstate.frequencies[-1])
    ymldoc['fstate']['nfreq'] = fstate.frequencies.size
    ymldoc['frequencies']['fmax'] = fmax
    ymldoc['frequencies']['fmin'] = fmin
    ymldoc['frequencies']['U'] = U
    ymldoc['process']['output_folder'] = output_folder
    ymldoc['process']['catalog'] = catalog
    ymldoc['telescope']['nside'] = nside
    ymldoc['telescope']['ndays'] = ndays
    ymldoc['frequencies']['nfreqmaps'] = nfreqmaps
    ymldoc['telescope']['tsys'] = tsys
istream.close()

with open(output_folder+"outputs.yaml", "w") as ostream:
    yaml.dump(ymldoc, ostream, default_flow_style=False, sort_keys=False)
ostream.close()
