import subprocess
import time
import threading


def run_script(script_path, base_dir, channels, gradual_unzip):
    # Run the script using subprocess.Popen to capture output
    process = subprocess.Popen(['python', script_path, base_dir, str(channels), str(gradual_unzip)],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Capture output and errors
    output, error = process.communicate()

    # Check for errors
    if process.returncode != 0:
        print("Error occurred:", error.decode("utf-8"))
        return None

    # Return the output as a variable
    return output.decode("utf-8")


def parse(script_output):
    idx_channels_num = script_output.find('channels_num:')
    idx_files_num = script_output.find('filse_num:')

    channels_num_rawstr = script_output[idx_channels_num + len('channels_num:'):idx_files_num]
    files_num_rawstr = script_output[idx_files_num + len('filse_num:'):]

    channels_num = int(channels_num_rawstr.strip())
    files_num = int(files_num_rawstr.strip())

    return channels_num, files_num


def run_script_and_check(script_path, base_dir, channels, gradual_unzip=True, counter_list=[]):
    script_output = run_script(script_path, base_dir, channels, gradual_unzip)
    channels_num, files_num = parse(script_output)
    counter_list.append(1)
    max_files_num = channels_num * 10 
    while files_num < max_files_num:
        download_progress = (files_num / max_files_num) * 100  
        print('{} percent of files are downloaded ...'.format(download_progress))
        time.sleep(30)
        script_output = run_script(script_path, base_dir, channels, gradual_unzip)
        _, files_num = parse(script_output)   

    print('All files downloaded successfully!')


def wait_function(counter_list):
    while len(counter_list) == 0:
        time.sleep(1)  # Wait for 1 second before checking again
    print("Length of list is more than zero.")