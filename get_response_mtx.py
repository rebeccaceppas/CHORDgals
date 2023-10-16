## TO DO
## figure out if the order of frequencies I am feeding is correct

from channelization_functions import get_response_matrix, get_fine_freqs
import yaml
import numpy as np
from FreqState import FreqState

yaml_input_file = open("inputs.yaml")
yaml_input = yaml.safe_load(yaml_input_file)
output_folder = yaml_input['process']['output_folder']

yaml_output_file = open(output_folder+"/outputs.yaml")
yaml_output = yaml.safe_load(yaml_output_file)
f_start = yaml_output['fstate']['f_start']
f_end = yaml_output['fstate']['f_end']
nfreq = yaml_output['fstate']['nfreq']
U = yaml_output['frequencies']['U']
fmax = yaml_output['frequencies']['fmax']
fmin = yaml_output['frequencies']['fmin']
yaml_output_file.close()


# these are finer frequencies needed to get the response matrix
fstate = FreqState()
fstate.freq = (f_start, f_end, nfreq)
fine_freqs = get_fine_freqs(fstate.frequencies)

# getting the response matrix and normalization envelope
#R, norm = get_response_matrix(fine_freqs, fmax, fmin, U)

R, chans, norm = get_response_matrix(fine_freqs, U, min_obs_freq=fmin, max_obs_freq=fmax, viewmatrix=False)

# saving both to disk
np.save(output_folder+'/R.npy', R)
np.save(output_folder+'/norm.npy', norm)