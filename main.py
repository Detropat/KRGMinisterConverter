import json
import os
from pprint import pprint

from ClauseWizard import cwparse, cwformat

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


# Render and map KRG element
def render_krg_element(krg_element):
    # pprint(krg_element)

    for k, v in krg_element:
        for ideaKey, ideas in v:
            if 'head_of_government' == ideaKey:
                print('Handling head_of_government')
                ruling_cabinet = 'Head of Government'
                # Render and map ministers
                render_ministers(ideas, 'Head of Government')
            elif 'foreign_minister' == ideaKey:
                print('Handling foreign_minister')
            elif 'economy_minister' == ideaKey:
                print('Handling economy_minister')
            elif 'interior_minister' == ideaKey:
                print('Handling interior_minister')
            elif 'justice_minister' == ideaKey:
                print('Handling interior_minister')
            elif 'head_of_intel' == ideaKey:
                print('Handling interior_minister')
            else:
                print('Invalid sub-level!')

    exit(0)


# Loop through all the available ministers
def render_ministers(ministers, government_type):
    minList = dict()
    for minKey, minister in ministers:
        minList['government_type'] = government_type
        minList['name'] = find_minister_name(minKey)

    pprint(minList)
    exit(0)


# Find the localised minister name
def find_minister_name(minister_key):
    print('here')


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
        # Start parsing
        with open(absolute_file_path, 'r', encoding='iso-8859-1') as f:
            krg_element = cwparse(f.read(), False)
            # Render the KRG element, after the mapping is done that is according to the CSV mapping
            render_krg_element(krg_element)

            # Format the binary output
            file_result = cwformat(krg_element)

            # Finally, store the formatted file into a JSON structure
            with open(parse_res_file, 'w', encoding='utf-8') as result:
                print('Outputting result to: ' + parse_res_file)
                result.write(json.dumps(file_result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
