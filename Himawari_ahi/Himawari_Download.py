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
if len(sys.argv) > 1:
    base_dir = sys.argv[1]

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
if len(sys.argv) > 1:
    channels = eval(sys.argv[2])
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
    progress_bar=False,
    verbose=False,
    fs_args={})



path = list(l_fpaths.values())[0][0]
dir = os.path.dirname(path)


# number of channels
channels_num = 16 if channels is None else len(channels)
print('channels_num:{}'.format(channels_num))
# number of files
files_num = len([name for name in os.listdir(dir) if name.endswith('.bz2') and os.path.isfile(os.path.join(dir, name))])
print('filse_num:{}'.format(files_num))

max_files_num = channels_num * 10  
if eval(sys.argv[3]) == True or files_num == max_files_num:
    extract_zip_files(dir, verbosity=-1)
