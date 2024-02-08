import numpy as np
from scipy import integrate

# helper function
def draw_sample(bins, heights, n):
    # cumulatively integrating 
    y_cumulative = integrate.cumtrapz(heights, initial = 0)
    draws = []

    # randomly sampling based on original probability
    for i in range(n):
        choice = np.random.uniform(low = 0, high = 1)
        draw = np.interp(choice, y_cumulative, bins)
        draws.append(draw)

    return np.array(draws)


# wrapper function
def draw_random_errors(phase_bins, phase_heights, amp_bins, amp_heights, output_shape):

    # normalizing the input heights to make it into a probability distribution
    phase_heights = phase_heights / integrate.trapz(np.abs(phase_heights))
    amp_heights = amp_heights / integrate.trapz(np.abs(amp_heights))
    
    # getting total random errors needed to populate the result matrix
    n = np.prod(output_shape)

    # getting phase errors for each matrix
    phase_draws = draw_sample(phase_bins, phase_heights, n).reshape(output_shape)
    amp_draws = draw_sample(amp_bins, amp_heights, n).reshape(output_shape)
    
    return phase_draws, amp_draws


# wrapper function for once we have the file 
def get_calibration_errors(output_shape, filename = 'generic file name - change once imported to pipeline'):
    
    phase_bins, phase_heights, amp_bins, amp_heights = filename # change to however the file should be opened
    phase_draws, amp_draws = draw_random_errors(phase_bins, phase_heights, amp_bins, amp_heights, output_shape)
    
    return phase_draws, amp_draws