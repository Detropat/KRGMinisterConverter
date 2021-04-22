import json
import os

from ClauseWizard import cwparse, cwformat

directory = os.path.dirname(os.path.abspath(__file__))
directoryInput = directory + '\\input'
directoryOutput = directory + '\\output'

# First do some clean-up in the output folder
print('Starting clean-up process')
for outputFile in os.listdir(directoryOutput):
    absoluteOutputFile = os.path.join(directoryOutput, outputFile)
    print('Removing file: ' + absoluteOutputFile)

# Loop through the directory
print('Start checking input folder')
for filename in os.listdir(directoryInput):
    absoluteFilePath = os.path.join(directoryInput, filename)
    parseResFile = os.path.join(directoryOutput, 'res_' + str.replace(str.lower(filename), '.txt', '.json'))

    print('Parsing file: ' + absoluteFilePath)
    # Start parsing
    with open(absoluteFilePath, 'r', encoding='iso-8859-1') as f:
        parsing = cwparse(f.read(), False)
        # Format the binary output
        fileResult = cwformat(parsing)

        # Finally, store the formatted file into a JSON structure
        with open(parseResFile, 'w', encoding='utf-8') as result:
            print('Outputting result to: ' + parseResFile)
            result.write(json.dumps(fileResult, indent=2, ensure_ascii=False))
