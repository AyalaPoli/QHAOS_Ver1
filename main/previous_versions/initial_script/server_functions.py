from main.Configuration_files.files_params import *
from main.Configuration_files.files_params import *

#Start server.py on server host

#Start client.py on the client host

def process_experiment_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'a') as outfile:

        for line in infile:
            outfile.write(line)
    return "Done copy test_files"
