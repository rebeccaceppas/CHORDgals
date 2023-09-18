import yaml
import sys
from channelization_functions import channelize_catalogue, channelize_map
from FreqState import FreqState

yaml_file = open('outputs.yaml')
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

maps = [map_filepath+'/foregrounds.h5',
        map_filepath+'/synch_map.h5']

if map == 1:
    # upchannelize a sky map
    save_title = norm_filepath+'/Up_Sky.h5'
    channelize_map(U, maps, R_filepath, norm_filepath, fmax, fmin, nfreq, save_title)


else:
    # upchannelize the galaxy catalog profiles
    save_title = norm_filepath+'/Up_Gal.h5'
    channelize_catalogue(U, catalogue_filepath, R_filepath, norm_filepath, fmax, fmin, nfreq, nside, save_title)