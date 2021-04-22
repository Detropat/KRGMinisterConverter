import json
import os

from ClauseWizard import cwparse, cwformat

directory = os.path.dirname(os.path.abspath(__file__))
directoryInput = directory + '\\input'
directoryOutput = directory + '\\output'

# Loop through the directory
for filename in os.listdir(directoryInput):
    absoluteFilePath = os.path.join(directoryInput, filename)
    parseResFile = os.path.join(directoryOutput, 'res_' + str.replace(filename, '.txt', '.json'))

    print('Parsing file: ' + absoluteFilePath)

    with open(absoluteFilePath, 'r', encoding='iso-8859-1') as f:
        parsing = cwparse(f.read(), False)
        fileResult = cwformat(parsing)
        with open(parseResFile, 'w', encoding='utf-8') as result:
            print('Outputting result to: ' + parseResFile)
            result.write(json.dumps(fileResult, indent=2, ensure_ascii=False))
