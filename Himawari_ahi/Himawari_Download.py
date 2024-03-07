import os
import datetime
import himawari_api
from himawari_api import download_latest_files
import sys
parent_dir = os.path.dirname(os.path.abspath(__file__)) # Get the parent directory of the current script
parent_dir = os.path.abspath(os.path.join(parent_dir, ".."))  # Go up one level
sys.path.append(parent_dir) # Add the parent directory to the Python path



from utils import extract_zip_files

#### Define protocol and local directory
base_dir = "./Himawari_ahi/tmp/"
protocol = "s3"

#### Define satellite, product_level and product
satellite = "HIMAWARI-9"
product_level = "L1B"
product = "Rad"

#### Define sector and filtering options
sector = "F"#Full Disc 
scene_abbr = None   # do not specify for Full Disc 
# channels = None     # select all channels
channels = ["C07"]  # select channels subset
filter_parameters = {}
filter_parameters["channels"] = channels
# filter_parameters["scene_abbr"] = scene_abbr

#### Downloading options
n_threads = 20  # n_parallel downloads
force_download = False  # whether to overwrite existing data on disk




# Create the base_dir if it doesn't already exist
if not os.path.exists(base_dir):
    os.makedirs(base_dir)
    print(f"Directory '{base_dir}' created successfully.")
else:
    print(f"Directory '{base_dir}' already exists.")




l_fpaths = download_latest_files(
    base_dir,
    protocol,
    satellite,
    product_level,
    product,
    sector,
    filter_parameters,
    N = 1, 
    check_consistency=True,
    look_ahead_minutes=15, 
    n_threads=20,
    force_download=False,
    check_data_integrity=True,
    progress_bar=True,
    verbose=True,
    fs_args={})



path = list(l_fpaths.values())[0][0]
dir = os.path.dirname(path)
extract_zip_files(dir)