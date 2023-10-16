## FINISHED ##

import yaml
from FreqState import FreqState
import numpy as np
import channelization_functions as cf

with open("inputs.yaml") as inp:
    yaml_input = yaml.safe_load(inp)
    U = yaml_input['frequencies']['U']
    fmax = yaml_input['frequencies']['fmax']
    fmin = yaml_input['frequencies']['fmin']
    output_folder = yaml_input['process']['output_folder']
    nside = yaml_input['mapmaking']['nside']
    ndays = yaml_input['mapmaking']['ndays']
    catalog = yaml_input['process']['catalog']
    tsys = yaml_input['telescope']['tsys']
inp.close()

# saving an input file in the output directory
with open(output_folder+"/inputs.yaml", "w") as inp_save:
    yaml.dump(yaml_input, inp_save, default_flow_style=False, sort_keys=False)
inp_save.close()

# getting coarse channels
chans1 = cf.get_chans(fmin, fmax)

# getting min and max and required df for chosen U
use_max = cf.freq_unit_add(np.arange(chans1.min()-0.5 + 1/(2*U), chans1.max()+0.5, 1/U).max())
use_min = cf.freq_unit_add(np.arange(chans1.min()-0.5 + 1/(2*U), chans1.max()+0.5, 1/U).min())
df = (use_max - use_min) / (chans1.size*U -1)
size_freqs = chans1.size*U

# calculating the frequencies for cora maps
nfreqmaps = int(size_freqs / U)

with open("outputs.yaml") as istream:
    ymldoc = yaml.safe_load(istream)
    ymldoc['fstate']['f_start'] = float(use_max)
    ymldoc['fstate']['f_end'] = float(use_min-df)
    ymldoc['fstate']['nfreq'] = int(size_freqs)
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

with open(output_folder+"/outputs.yaml", "w") as ostream:
    yaml.dump(ymldoc, ostream, default_flow_style=False, sort_keys=False)
ostream.close()
