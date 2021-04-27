import csv
import os

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
        self.csv_ministers = []

    # Main method
    def main(self):
        # Start parsing
        with open(self.inputDirectory + '\\' + self.file, 'r', encoding='utf-8') as f:
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
                    self.render_ministers(ideas, 'Foreign Minister')
                elif 'economy_minister' == ideaKey:
                    print('Handling economy_minister')
                    self.render_ministers(ideas, 'Economic Minister')
                elif 'interior_minister' == ideaKey:
                    print('Handling interior_minister')
                    self.render_ministers(ideas, 'Interior Minister')
                elif 'justice_minister' == ideaKey:
                    print('Handling justice_minister')
                    self.render_ministers(ideas, 'Justice Minister')
                elif 'head_of_intel' == ideaKey:
                    print('Handling head_of_itenl')
                    self.render_ministers(ideas, 'Head of Intelligence')
                else:
                    print('Invalid sub-level!')

    # Loop through all the available ministers
    def render_ministers(self, ministers, government_type):
        for min_key, ministers in ministers:
            min_list = {}
            self.minister_key = min_key
            self.ministers = ministers
            min_list['government_type'] = government_type
            min_list['name'] = str(self.find_minister_name()).replace('"', '')
            min_list['ideology'] = self.find_ideology()
            min_list['personality'] = self.find_personality()
            min_list['picture_name'] = self.render_picture_name()

            self.csv_ministers.append(min_list)

    # Find the localised minister name
    def find_minister_name(self):
        print('Finding minster: ' + self.minister_key)
        localisation_file_name = str.replace(self.file, '_ministers.txt', '_l_english.yml')
        minister_name = None

        # Need to search the file, since generally the YML files aren't properly formatted to be parsed
        with open(self.inputDirectoryLocalisation + '\\' + localisation_file_name, 'r', encoding="utf-8") as stream:
            for line in stream:
                if (self.minister_key + ':0') in line:
                    minister_name = line.split(':0')
                    minister_name = str(minister_name[1]).strip()
                    break

        if minister_name is None:
            minister_name = ''

        return minister_name

    # Map the right ideology
    def find_ideology(self):
        ideology = self.find_ideology_in_traits()

        if ideology == 'authoritarian_socialist':
            return 0
        elif ideology == 'social_democrat':
            return 3
        elif ideology == 'revolutionary_republican':
            return 2
        elif ideology == 'social_liberal':
            return 4
        elif ideology == 'market_liberal':
            return 5
        elif ideology == 'social_conservative':
            return 6
        elif ideology == 'authoritarian_democrat':
            return 7
        elif ideology == 'paternal_autocrat':
            return 8
        elif ideology == 'radical_socialist':
            return 1
        elif ideology == 'national_populist':
            return 9
        else:
            exit('Missing right ideology mapping')

    # If the ideology is missing in the key, find it on the trait level
    def find_ideology_in_traits(self):
        for k, v in self.ministers:
            if k == 'traits':
                # Clause if the files don't contain enough traits
                if len(v) == 1:
                    return str(v[0][0])
                elif str(self.minister_key).lower() == 'nee_hog_jpk':
                    return str(v[0][0])
                elif str(self.minister_key).lower() == 'maf_otto_rietzsch':
                    return str(v[0][0])
                elif len(v) == 2:
                    return str(v[1][0])
                elif not len(v) == 3:
                    return str(v[1][0])
                else:
                    return str(v[1][0])

    # Find and map the personality
    def find_personality(self):
        personality = None
        for k, v in self.ministers:
            if k == 'traits':
                if not len(v) == 3:
                    print('Invalid amount of traits found')
                personality = str(v[-1][0])

        if not personality:
            exit('No personality was mapped')

        return personality

    # Render the picture name
    def render_picture_name(self):
        picture_name = ''
        for k, m in self.ministers:
            if k == 'picture':
                picture_name = m[0]
                # Fixing annoying missing portaits
                if picture_name == '???':
                    picture_name = ''
                    return picture_name

                # Try to find a matching GFX
                folder = self.inputDirectory + '\\gfx\\' + self.country_tag
                if not os.path.exists(folder):
                    print('No GFX folder. Stop searching')
                    return picture_name

                for filename in os.listdir(folder):
                    search_file = filename.split('.')[0]
                    if picture_name == search_file:
                        filename = filename.split('.')
                        if filename[1] != 'tga':
                            f = '.'
                            new_filename = filename[0] + '.tga'
                            original = f.join(filename)
                            pre, ext = os.path.splitext(folder + '\\' + original)
                            os.rename(folder + '\\' + original, pre + '.tga')
                            return picture_name

        return picture_name

    # Create the country specific CSV file
    def create_csv(self):
        print('Starting CSV creation for ' + self.country_tag)
        with open(self.outputDirectory + '\\' + self.country_tag + '.csv', 'w', newline='\n', encoding="utf-8") as c:
            writer = csv.writer(c)

            # Create the header
            writer.writerow(
                [self.country_tag, 'Ruling Cabinet - Start', 'Name', 'Ideology', 'Personality', 'Picturename'])

            for v in self.csv_ministers:
                writer.writerow(
                    ['x', v['government_type'], v['name'], v['ideology'], v['personality'], v['picture_name']])
