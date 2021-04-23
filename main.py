import os

from krg_parser import KRGParser

directory = os.path.dirname(os.path.abspath(__file__))
directoryInput = directory + '\\input'
directoryInputLocalisation = directoryInput + '\\localisation'
directoryOutput = directory + '\\output'


# Remove previously generated files
def cleanup():
    print('Starting clean-up process')
    for outputFile in os.listdir(directoryOutput):
        absolute_output_file = os.path.join(directoryOutput, outputFile)
        os.unlink(absolute_output_file)


# Main function
def main():
    # First do some clean-up in the output folder
    # cleanup()
    # Loop through the directory
    print('Start checking input folder')
    for filename in os.listdir(directoryInput):
        # Only handle .txt files
        if not (filename.endswith('.txt')):
            continue

        absolute_file_path = os.path.join(directoryInput, filename)
        parse_res_file = os.path.join(directoryOutput, 'res_' + str.replace(str.lower(filename), '.txt', '.json'))

        print('Parsing file: ' + absolute_file_path)
        KRGParser(filename, directoryInput).main()


if __name__ == "__main__":
    main()
