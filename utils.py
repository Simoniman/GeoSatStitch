import os
import patoolib
from pyresample import create_area_def


def find_format(directory, format_list=['nc', 'DAT', 'nat']):
    """
    Search for files with specified formats in the given directory.

    Parameters:
    - directory (str): The path to the directory to search.
    - format_list (list): A list of strings representing file formats to search for. Default is set to ['nc', 'dat', 'nat'].

    Returns:
    - str or None: The format of the first file found with a matching format from format_list.
                  Returns None if no matching file is found.

    Example:
    >>> directory = '/path/to/your/directory'
    >>> format_list = ['nc', 'dat', 'nat']
    >>> found_format = find_format(directory, format_list)
    >>> print(found_format)
    'nc'

    Note:
    - This function stops iteration and returns the format of the first matching file found.
    - If the directory does not exist or is empty, or if format_list is empty, None is returned.
    """
    # Loop through the files in the directory
    for file in os.listdir(directory):
        # Check if the file has one of the specified formats
        for format in format_list:
            if file.endswith(f'.{format}'):
                return format  # Return the format as soon as a match is found
    
    # Return None if no match is found
    return None


def find_reader(filenames_format):
    """
    Map file formats to reader names.

    Parameters:
    - filenames_format (str): The file format to map to a reader name.
                             Should be one of 'nc', 'DAT', or 'nat'.

    Returns:
    - str: The reader name corresponding to the input file format.

    Raises:
    - ValueError: If the input file format is not in the ['nc', 'DAT', 'nat'] list.

    Example:
    >>> reader = find_reader('nc')
    >>> print(reader)
    'abi_l1b'

    Note:
    - This function maps file formats to reader names based on a predefined mapping.
    """
    if filenames_format == 'nc':
        reader = 'abi_l1b'
    elif filenames_format == 'nat':
        reader = 'seviri_l1b_native'
    elif filenames_format == 'DAT':
        reader = 'ahi_hsd'
    else:
        raise ValueError("Data format is not in the ['nc', 'DAT', 'nat'] list. Please check it again.")
    return reader


def geo_area_def(scene):
    """
    Generate an appropriate AreaDefinition object based on the platform of the satellite imagery.

    Parameters:
    - scene (Scene): The satellite scene object containing the imagery.

    Returns:
    - geo_area_def(AreaDefinition): The AreaDefinition object representing the geographic area covered by the imagery in the destination projection system.

    Raises:
    - ValueError: If there are no datasets in the scene directory or if the platform type does not match with any predefined ones.

    Note:
    - The function determines the platform of the satellite imagery from the scene metadata and selects the appropriate AreaDefinition object accordingly.
    """
    # Projection systems 
    web_mercator_default = {'a': '6378137', 'b': '6378137', 'k': '1', 'lat_ts': '0', 'lon_0': '0', 'nadgrids': '@null', 'no_defs': 'None', 'proj': 'merc', 'type': 'crs', 'units': 'm', 'wktext': 'None', 'x_0': '0', 'y_0': '0'}
    web_mercator_180deg = {'a': '6378137', 'b': '6378137', 'k': '1', 'lat_ts': '0', 'lon_0': '180', 'nadgrids': '@null', 'no_defs': 'None', 'proj': 'merc', 'type': 'crs', 'units': 'm', 'wktext': 'None', 'x_0': '0', 'y_0': '0'}
    
    # Dictionary mapping platform names to corresponding AreaDefinition objects. 
    geo_area_defs = {
        'Goes_West': create_area_def('Goes_West', web_mercator_180deg, resolution=2000, area_extent=[-3339000, -11069000, 13359000, 11069000], units='meters'), #[+150, -70, -60, 70]
        'Goes_East': create_area_def('Goes_East', web_mercator_default, resolution=2000, area_extent=[-16698000, -11069000, 0.0, 11069000], units='meters'), #[-150, -70, 0, 70]
        'Meteo_Prime': create_area_def('Meteo_Prime', web_mercator_default, resolution=2000, area_extent=[-8350000, -11069000, 8350000, 11069000], units='meters'), #[-75, -70, 75, 70]
        'Meteo_IndOcean': create_area_def('Meteo_IndOcean', web_mercator_default, resolution=2000, area_extent=[-3898000, -11069000, 12802000, 11069000], units='meters'), #[-35, -70, 115, 70]
        'Himawari': create_area_def('Himawari', web_mercator_180deg, resolution=2000, area_extent=[-12802000, -11069000, 3898000, 11069000], units='meters') #[+65, -70, -145, 70]
    }

    # Check if there are any datasets in the scene directory
    available_dataset_names = scene.available_dataset_names()
    if len(available_dataset_names) == 0:
        raise ValueError("There are no datasets in the directory.")

    # Get the platform name from the scene metadata
    if len(scene.keys()) == 0:
        dataset_name = available_dataset_names[0]
    else : 
        dataset_name = scene.keys()[0]['name']
    scene.load([dataset_name])
    platform_name = scene[dataset_name].attrs['platform_name']

    # Select the appropriate AreaDefinition object based on the platform type
    if platform_name in ['GOES-18']:
        geo_area_def = geo_area_defs['Goes_West']
    elif platform_name in ['GOES-16']:
        geo_area_def = geo_area_defs['Goes_East']
    elif platform_name in ['Meteosat-10']:
        geo_area_def = geo_area_defs['Meteo_Prime']
    elif platform_name in ['Meteosat-9']:
        geo_area_def = geo_area_defs['Meteo_IndOcean']
    elif platform_name in ['Himawari-9', 'Himawari-8']:
        geo_area_def = geo_area_defs['Himawari']
    else:
        raise ValueError("Platform type does not match with any predefined ones.")

    return geo_area_def


def extract_zip_files(directory, zip_formats=('.zip','.bz2')):
    """
    Extracts files with specified zip formats from a directory using patoolib.

    Parameters:
    - directory (str): The directory path containing the zip files to be extracted.
    - zip_formats (tuple): Tuple containing file extensions of the zip formats to be extracted (default: ('.zip', '.bz2')).

    Returns:
    - None

    Note:
    - This function extracts files with specified zip formats using patoolib.extract_archive function from the patoolib library.
    - If extraction fails for any file, it prints an error message indicating the failure.
    """
    # List all files in the directory
    files = os.listdir(directory)
    
    # Filter files based on specified zip formats
    zip_files = [file for file in files if file.endswith(zip_formats)]

    # Extract each zip file using patoolib
    for zip_file in zip_files:
        zip_file_path = os.path.join(directory, zip_file)
        try:
            patoolib.extract_archive(zip_file_path, outdir=directory)
            print(f"{zip_file} extracted successfully.")
        except patoolib.util.PatoolError as e:
            print(f"Error: Failed to extract {zip_file}: {e}")