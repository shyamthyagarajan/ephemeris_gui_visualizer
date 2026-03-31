import numpy as np
from astroquery.jplhorizons import Horizons

def fetch_horizons_data(satellite_id_list, start_time, stop_time, step_val):
  """
    Fetches heliocentric position vectors for a list of solar system bodies
    from the JPL Horizons API.

    Parameters:
        satellite_id_list (list): List of JPL Horizons body IDs (e.g. ['99942', '-64'])
        start_time (str): Start date in 'YYYY-MM-DD' format
        stop_time (str): Stop date in 'YYYY-MM-DD' format
        step_val (str): Time step between data points (e.g. '1h', '30m', '1d')

    Returns:
        dict: Map of body ID -> (datetime_jd, x, y, z) arrays in AU,
              all positions relative to the Sun (@sun)
  """
  data_map = {}
  for satellite in satellite_id_list:
    position_time_obj = Horizons(id=satellite,location = '@sun', \
    epochs={'start':start_time, 'stop': stop_time, 'step': step_val})
    position_time_data = position_time_obj.vectors()

    data_map[satellite] = (np.array(position_time_data['datetime_jd']), \
        np.array(position_time_data['x']), np.array(position_time_data['y']), \
        np.array(position_time_data['z']))

  return data_map

if __name__ == "__main__":
    result = fetch_horizons_data(['99942','-64'], '2026-03-20', '2026-03-21', '1h')
    print(result)