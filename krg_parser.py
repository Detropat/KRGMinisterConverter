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
        min_list = dict()
        for minKey, minister in ministers:
            pprint(minister)
            min_list['government_type'] = government_type
            min_list['name'] = self.find_minister_name(minKey)
            min_list['ideology'] = self.find_ideology(minKey)

        pprint(min_list)
        exit(0)

    # Find the localised minister name
    def find_minister_name(self, minister_key):
        print('Finding minster: ' + minister_key)
        localisation_file_name = str.replace(self.file, '_ministers.txt', '_l_english.yml')
        minister_name = None

        # Need to search the file, since generally the YML files aren't properly formatted to be parsed
        with open(self.inputDirectoryLocalisation + '\\' + localisation_file_name, 'r', encoding="utf8") as stream:
            for line in stream:
                if (minister_key + ':0') in line:
                    minister_name = line.split(':0')
                    minister_name = str(minister_name[1]).strip()
                    break

        if minister_name is None:
            exit('No minister name found for ' + minister_key)

        return minister_name

    # Map the right ideology
    def find_ideology(self, minister_key):
        ideology = minister_key.split('_')
        ideology = str(ideology[0]).lower()

        if ideology == 'autsoc':
            return 0
        elif ideology == 'socdem':
            return 3
        elif ideology == 'revrep':
            return 2
        elif ideology == 'soclib':
            return 4
        elif ideology == 'marklib':
            return 5
        elif ideology == 'soccon':
            return 6
        elif ideology == 'authdem':
            return 7
        else:
            exit('Missing right ideology mapping')
