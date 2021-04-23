from pprint import pprint

from ClauseWizard import cwparse


class KRGParser:
    # Constructor
    def __init__(self, file, input_directory):
        self.file = file
        self.krg_element = None
        self.inputDirectory = input_directory
        self.inputDirectoryLocalisation = self.inputDirectory + '\\localisation'

    # Main method
    def main(self):
        print(self.file)
        # Start parsing
        with open(self.inputDirectory + '\\' + self.file, 'r', encoding='iso-8859-1') as f:
            self.krg_element = cwparse(f.read(), False)
            # Render the KRG element, after the mapping is done that is according to the CSV mapping
            self.render_krg_element()

    # Render and map KRG element
    def render_krg_element(self):
        # pprint(krg_element)
        for k, v in self.krg_element:
            for ideaKey, ideas in v:
                if 'head_of_government' == ideaKey:
                    print('Handling head_of_government')
                    self.render_ministers(ideas, 'Head of Government')
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
    def render_ministers(self, ministers, government_type):
        minList = dict()
        for minKey, minister in ministers:
            minList['government_type'] = government_type
            minList['name'] = self.find_minister_name(minKey)

        pprint(minList)
        exit(0)

    # Find the localised minister name
    def find_minister_name(self, minister_key):
        print('Finding the minster: ' + minister_key)
        localisation_file_name = str.replace(self.file, '_ministers.txt', '_l_english.yml')
        yml_file = None
        with open(self.inputDirectoryLocalisation + '\\' + localisation_file_name, 'r', encoding="utf8") as stream:
            for line in stream:
                if line.find(minister_key + ':0'):
                    print('found him!')

        pprint(yml_file)
        exit(0)
