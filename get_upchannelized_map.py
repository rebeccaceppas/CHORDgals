import yaml
import sys
from channelization_functions import channelize_catalogue, channelize_map, get_fine_freqs
from FreqState import FreqState
import h5py
import numpy as np
from save_galaxy_map import write_map

yaml_input_file = open("inputs.yaml")
input = yaml.safe_load(yaml_input_file)
output_folder = input['process']['output_folder']
yaml_input_file.close()

yaml_file = open(output_folder+'/outputs.yaml')
output = yaml.safe_load(yaml_file)
U = output['frequencies']['U']
R_filepath = output['process']['output_folder'] + '/R.npy'
norm_filepath = output['process']['output_folder'] + '/norm.npy'
map_filepath = output['process']['output_folder']
catalogue_filepath = output['process']['catalog']
fmax = output['frequencies']['fmax']
fmin = output['frequencies']['fmin']
nfreq = output['fstate']['nfreq']
nside = output['telescope']['nside']
yaml_file.close()

fstate = FreqState()
fstate.freq = (fmax, fmin, nfreq)

args = sys.argv
map = args[1]
nfreq_maps = args[2]

f_fg = h5py.File(map_filepath+'/foregrounds.h5')
Map_fg = np.array(f_fg['map'])  # the healpix map
f_fg.close()

f_s = h5py.File(map_filepath+'/synch_map.h5')
Map_s = np.array(f_s['map'])  # the healpix map
f_s.close()

map_freqs = FreqState()
map_freqs.freq(fmax, fmin, nfreq_maps)

sky_map = Map_fg + Map_s

write_map(map_filepath+'/sky_map.h5', sky_map, fstate.frequencies, fstate.freq_width, include_pol=True)

sky_file = map_filepath+'/sky_map.h5'

fine_freqs = get_fine_freqs(fstate.frequencies)

if map == 1:
    # upchannelize a sky map
    save_title = norm_filepath+'/Up_Sky.h5'
    channelize_map(U, fmax, fmin, nfreq, nside, sky_file, R_filepath, norm_filepath, save_title, fine_freqs, map_freqs)

else:
    # upchannelize the galaxy catalog profiles
    save_title = norm_filepath+'/Up_Gal.h5'
    channelize_catalogue(U, catalogue_filepath, R_filepath, norm_filepath, fmax, fmin, nfreq, nside, save_title, fine_freqs)