import os

from krg_parser import KRGParser

directory = os.path.dirname(os.path.abspath(__file__))
directory_input = directory + '\\input'
directory_input_localisation = directory_input + '\\localisation'
directory_output = directory + '\\output'


# Remove previously generated files
def cleanup():
    print('Starting clean-up process')
    for outputFile in os.listdir(directory_output):
        absolute_output_file = os.path.join(directory_output, outputFile)
        os.unlink(absolute_output_file)


# Main function
def main():
    # First do some clean-up in the output folder
    # cleanup()
    # Loop through the directory
    print('Start checking input folder')
    for filename in os.listdir(directory_input):
        # Only handle .txt files
        if not (filename.endswith('.txt')):
            continue

        absolute_file_path = os.path.join(directory_input, filename)
        parse_res_file = os.path.join(directory_output, 'res_' + str.replace(str.lower(filename), '.txt', '.json'))

        print('Parsing file: ' + absolute_file_path)
        KRGParser(filename, directory_input, directory_output).main()


if __name__ == "__main__":
    main()
