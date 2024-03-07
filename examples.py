"""Get all files in the examples folder, encode and then decode."""

import os
import converter
import json

def list_files(directory):
    """Get a list of all file names in a directory."""
    
    files = os.listdir(directory) # get all contents in the directory
    files = [file for file in files if os.path.isfile(os.path.join(directory, file))] # filter directories
    return files

if True:
    print('encoding files...')
    DIRECTORY = 'examples/'
    for file_name in list_files(DIRECTORY):
        print('- ' + file_name)
        with open(DIRECTORY+file_name) as f:
            data = json.loads(f.read())

        output = converter.encode(data)

        with open(f'{DIRECTORY}encoded/{file_name}.txt', 'w') as f:
            f.writelines([str(o)+'\n' for o in output])

if True:
    print('decoding files...')
    DIRECTORY = 'examples/encoded/'
    for file_name in list_files(DIRECTORY):
        print('- ' + file_name)
        with open(DIRECTORY+file_name) as f:
            data = f.readlines()
            data = [d[0:-1] for d in data] # remove newline

        with open(f'{DIRECTORY}decoded/{file_name}.json', 'w') as f:
            f.write(json.dumps(converter.decode(data), indent=4))