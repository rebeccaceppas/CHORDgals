import yaml

yaml_input_file = open("inputs.yaml")
yaml_input = yaml.safe_load(yaml_input_file)
ndays = yaml_input['mapmaking']['ndays']
grid_ew = yaml_input['telescope']['grid_ew']
grid_ns = yaml_input['telescope']['grid_ns']
spacing_ew = yaml_input['telescope']['spacing_ew']
spacing_ns = yaml_input['telescope']['spacing_ns']
output_folder = yaml_input['process']['output_folder']
yaml_input_file.close()

yaml_output_file = open(output_folder+"/outputs.yaml")
yaml_output = yaml.safe_load(yaml_output_file)
tsys = yaml_output['telescope']['tsys']
elevation = yaml_output['telescope']['elevation']
U = yaml_output['frequencies']['U']
f_start = yaml_output['fstate']['f_start']
f_end = yaml_output['fstate']['f_end']
nfreq = yaml_output['fstate']['nfreq']
nside = yaml_output['telescope']['nside']
yaml_output_file.close()

# beam.yaml
with open("beam.yaml") as istream:
    ymldoc = yaml.safe_load(istream)
    ymldoc['telescope']['freq_start'] = f_start
    ymldoc['telescope']['freq_end'] = f_end
    ymldoc['telescope']['num_freq'] = nfreq
    ymldoc['telescope']['elevation_start'] = elevation
    ymldoc['telescope']['elevation_end'] = elevation
    ymldoc['telescope']['ndays'] = ndays
    ymldoc['telescope']['layout_spec']['grid_ew'] = grid_ew
    ymldoc['telescope']['layout_spec']['grid_ns'] = grid_ns
    ymldoc['telescope']['layout_spec']['spacing_ew'] = spacing_ew
    ymldoc['telescope']['layout_spec']['spacing_ns'] = spacing_ns
    ymldoc['telescope']['beam_spec']['type'] = "airy"
    ymldoc['telescope']['tsys_flat'] = float(tsys)
    ymldoc['config']['output_directory'] = output_folder
istream.close()

with open(output_folder+"/beam.yaml", "w") as ostream:
    yaml.dump(ymldoc, ostream, default_flow_style=False, sort_keys=False)
ostream.close()

# simulate.yaml
with open("simulate.yaml") as istream:
    ymldoc = yaml.safe_load(istream)
    ymldoc['cluster']['directory'] = output_folder+'/simulate_info'
    ymldoc['pipeline']['tasks'][1]['params']['product_directory'] = output_folder
    ymldoc['pipeline']['tasks'][2]['params']['maps'][0]['files'][0] = output_folder+'/Up_Gal.h5'
    ymldoc['pipeline']['tasks'][3]['params']['output_name'] = output_folder+'/sstream.h5'
    ymldoc['pipeline']['tasks'][6]['params']['nside'] = nside
    ymldoc['pipeline']['tasks'][6]['params']['output_name'] = output_folder+'/dirty_map.h5'
istream.close()

    
with open(output_folder+"/simulate.yaml", "w") as ostream:
    yaml.dump(ymldoc, ostream, default_flow_style=False, sort_keys=False)
ostream.close()