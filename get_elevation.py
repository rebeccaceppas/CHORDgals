## FINISHED ##

import yaml

def get_elevation(center_dec):
    
    '''make sure this is negative if south of zenihth and positive otherwise
    
    elevation_start: :py:class:`caput.config.Property(proptype=float)`
        Start point of the elevation offset pointings, relative to zenith in degrees.
        Positive is north of zenith, negative is south of zenith.
        Default: -10 [degrees]
    
    '''
    
    # making negative if south of zenith
    elevation = center_dec - 49.3207092194
    
    return elevation

yaml_input_file = open("inputs.yaml")
yaml_input = yaml.safe_load(yaml_input_file)
center_dec = yaml_input['telescope']['observing_dec']

elevation = get_elevation(center_dec)

with open("outputs.yaml") as istream:
    ymldoc = yaml.safe_load(istream)
    ymldoc['telescope']['elevation'] = float(elevation)
istream.close()

with open("outputs.yaml", "w") as ostream:
    yaml.dump(ymldoc, ostream, default_flow_style=False, sort_keys=False)
ostream.close()