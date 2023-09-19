## TO DO
## figure out if the order of frequencies I am feeding is correct

from channelization_functions import get_response_matrix, get_fine_freqs
from FreqState import FreqState
import yaml
import numpy as np

yaml_input_file = open("inputs.yaml")
yaml_input = yaml.safe_load(yaml_input_file)
output_folder = yaml_input['process']['output_folder']

yaml_output_file = open(output_folder+"/outputs.yaml")
yaml_output = yaml.safe_load(yaml_output_file)
fmax = yaml_output['frequencies']['fmax']
fmin = yaml_output['frequencies']['fmin']
nfreq = yaml_output['fstate']['nfreq']
U = yaml_output['frequencies']['U']
yaml_output_file.close()

# these are the frequencies we will observe
fstate = FreqState()
fstate.freq = (fmax, fmin, nfreq)
# these are finer frequencies needed to get the response matrix
fine_freqs = get_fine_freqs(fstate.frequencies)

## NEED TO FIGURE OUT IF I'M MEANT TO FLIP THEM OR NOT
## I THINK THEY SHOULD BOTH BE GOING FROM HIGH TO LOW
# getting the response matrix and normalization envelope
R, norm = get_response_matrix(np.flip(fine_freqs), fstate.frequencies, U)

# saving both to disk
np.save(output_folder+'/R.npy', R)
np.save(output_folder+'/norm.npy', norm)