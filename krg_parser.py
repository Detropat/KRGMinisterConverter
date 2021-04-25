import csv
from pprint import pprint

from ClauseWizard import cwparse


class KRGParser:
    # Constructor
    def __init__(self, file, input_directory, output_directory):
        self.file = file
        self.krg_element = None
        self.minister_key = None
        self.ministers = None
        self.inputDirectory = input_directory
        self.outputDirectory = output_directory
        self.inputDirectoryLocalisation = self.inputDirectory + '\\localisation'
        self.country_tag = None
        self.csv_ministers = None

    # Main method
    def main(self):
        # Start parsing
        with open(self.inputDirectory + '\\' + self.file, 'r', encoding='iso-8859-1') as f:
            self.krg_element = cwparse(f.read(), False)
            # Render the KRG element, after the mapping is done that is according to the CSV mapping
            self.country_tag = self.file.split('_')[1]
            self.render_krg_element()

            # Once here, it's time to create the CSV file
            self.create_csv()

    # Render and map KRG element
    def render_krg_element(self):
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

    # Loop through all the available ministers
    def render_ministers(self, ministers, government_type):
        min_list = dict()
        for min_key, ministers in ministers:
            self.minister_key = min_key
            self.ministers = ministers
            min_list['government_type'] = government_type
            min_list['name'] = self.find_minister_name()
            min_list['ideology'] = self.find_ideology()
            min_list['personality'] = self.find_personality()
            min_list['picture_name'] = self.render_picture_name()

            self.csv_ministers = min_list

    # Find the localised minister name
    def find_minister_name(self):
        print('Finding minster: ' + self.minister_key)
        localisation_file_name = str.replace(self.file, '_ministers.txt', '_l_english.yml')
        minister_name = None

        # Need to search the file, since generally the YML files aren't properly formatted to be parsed
        with open(self.inputDirectoryLocalisation + '\\' + localisation_file_name, 'r', encoding="utf8") as stream:
            for line in stream:
                if (self.minister_key + ':0') in line:
                    minister_name = line.split(':0')
                    minister_name = str(minister_name[1]).strip()
                    break

        if minister_name is None:
            exit('No minister name found for ' + self.minister_key)

        return minister_name

    # Map the right ideology
    def find_ideology(self):
        ideology = self.minister_key.split('_')
        ideologyTmp = str(ideology[0]).lower()

        # Special clause for country specific mapping
        if ideologyTmp == 'chi' or ideologyTmp == 'eng' or ideologyTmp == 'ger':
            ideology = str(ideology[2]).lower()
        # Special clause for the DNF mapping
        elif ideologyTmp == 'dnf':
            ideology = str(ideology[-1]).lower()
        else:
            ideology = ideologyTmp

        pprint(ideology)

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
        elif ideology == 'pataut':
            return 8
        else:
            exit('Missing right ideology mapping')

    # Find and map the personality
    def find_personality(self):
        personality = None
        for k, v in self.ministers:
            if k == 'traits':
                if not len(v) == 3:
                    exit('Invalid amount of traits found')
                personality = str(v[-1][0])

        if not personality:
            exit('No personality was mapped')

        return personality

    # Render the picture name
    def render_picture_name(self):
        picture_name = self.minister_key.split('_')
        picture_name = self.country_tag + '_' + picture_name[1] + '_' + picture_name[2]

        return picture_name

    # Create the country specific CSV file
    def create_csv(self):
        print('Starting CSV creation for ' + self.country_tag)
        with open(self.outputDirectory + '\\' + self.country_tag + '.csv', 'w') as c:
            writer = csv.writer(c)

            # Create the header
            writer.writerow(
                [self.country_tag, 'Ruling Cabinet - Start', 'Name', 'Ideology', 'Personality', 'Picturename'])
            # Insert the empty row. No clue why, just following the example
            writer.writerow(['', '', '', '', '', ''])
