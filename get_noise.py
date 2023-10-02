from noise import NormalizedNoise, get_manager, get_sstream
import yaml
import numpy as np
from drift.core import manager
from draco.analysis import mapmaker, transform
from save_galaxy_map import write_map
from FreqState import FreqState

yaml_input_file = open("inputs.yaml")
input = yaml.safe_load(yaml_input_file)
output_folder = input['process']['output_folder']
yaml_input_file.close()

yaml_file = open(output_folder+'/outputs.yaml')
output = yaml.safe_load(yaml_file)
tsys = output['telescope']['tsys']
ndays = output['telescope']['ndays']
nside = output['telescope']['nside']
fmax = output['frequencies']['fmax']
fmin = output['frequencies']['fmin']
nfreq = output['fstate']['nfreq']
yaml_file.close()

'''getting normalized noisy visibilities'''
norm = np.load(output_folder+'/norm.npy')

manager = get_manager(output_folder)

noisy = NormalizedNoise()
noisy.setup(manager)

data = get_sstream(output_folder)

noisy_data = noisy.process(data, norm)

'''getting M-modes'''
mmodes = transform.MModeTransform()
mmodes.setup(manager)

Mmodes = mmodes.process(noisy_data)
print(Mmodes)

'''making dirty map'''
dm = mapmaker.DirtyMapMaker()
dm.setup(manager)
m = dm.process(Mmodes)

filename = output_folder+'/dirty_map_norm.h5'
map_ = m['map'][:]
fstate = FreqState()
fstate.freq = (fmax, fmin, nfreq)

write_map(filename, map_, fstate.frequencies, fstate.freq_width, include_pol=True)