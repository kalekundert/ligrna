#!/usr/bin/env python3

"""
Consolidate several YAML files into one

Usage:
    consolidate_yaml.py <yml_path> <key> [options]

Arguments:
    <yml_path>
        Path to a YAML file specifying which the locations of YAML files to
        consolidate.

    <key>
        Key of the file in the YAML file list to use as a template for well
        labels in the new consolidated YAML. By default, the first file will
        be used.

Options:
    -o --output <path>
        If an output path is specified, the resulting YAML is written to that
        path.  Dollar signs ($) in the output path are replaced by the base
        name of the given experiment, minus the '.yml' suffix. By default,
        *I'll figure this out later*

    -d --include-discards
        Consolidate all experiments regardless of the discard status

"""
class ConsolidateYAML():
    def __init__(self):
        self.consolidated_yaml = {'plates': {'plates': {}}}
        self.yaml_list = []
        self.template_yaml = None
        self.constituent_yamls = None


    def initialize_yaml_dictionary(self):
        """
        Takes the template YAML file and uses its labels to initialize a
        nested dictionary of plates and labels.
        :return:
        """
        for document in self.template_yaml:
            if 'plates' not in document.keys():
                self.consolidated_yaml[document['label']] = {'label': document['label'],
                                                             'channel': document['channel'],
                                                             'wells': {'apo': [],
                                                                       'holo': []
                                                                       },
                                                             'discard': False
                                                             }


    def populate_yaml(self):
        """
        Append wells to apo and holo for all experiments where discard != True
        :return:
        """
        # For each constituent yaml
        for input_yaml in self.yaml_list:

            print("Currently parsing: {}".format(input_yaml))

            # For each "document" in the constituent yaml
            for document in input_yaml:

                # Add plates to the consolidated yaml plate dictionary
                if 'plates' in document.keys():
                    for plate in document['plates']:
                        self.consolidated_yaml['plates']['plates'][plate] = document['plates'][plate]

                # Add wells to the relevant label if discard != True
                # (not all experiments have discard entries)
                else:
                    if 'discard' not in document.keys():
                        self._add_wells(document)
                    elif 'discard' in document.keys() and document['discard'] == True:
                        if args['--include-discards'] == True:
                            self._add_wells(document)
                    else:
                        self._add_wells(document)

    def _add_wells(self, document):
        for well in document['wells']['apo']:
            if well not in self.consolidated_yaml[document['label']]['wells']['apo']:
                self.consolidated_yaml[document['label']]['wells']['apo'].append(well)
        for well in document['wells']['holo']:
            if well not in self.consolidated_yaml[document['label']]['wells']['holo']:
                self.consolidated_yaml[document['label']]['wells']['holo'].append(well)

    def dump_yaml(self):
        output_YAML = open('Consolidated_YAML.yaml', 'w')

        yaml.dump(werk.consolidated_yaml['plates'], output_YAML)

        yaml_keys = sorted([key for key in werk.consolidated_yaml])

        for document in yaml_keys:
            if document != 'plates':
                output_YAML.write('---\n')
                yaml.dump(werk.consolidated_yaml[document], output_YAML)
        output_YAML.close()


if __name__ == '__main__':
    import docopt
    import yaml
    import pprint
    import collections

    args = docopt.docopt(__doc__)
    werk = ConsolidateYAML()

    werk.constituent_yamls = yaml.load(open(args['<yml_path>'], 'r'), Loader=yaml.Loader)
    werk.template_yaml = yaml.load_all(open(werk.constituent_yamls[int(args['<key>'])], 'r'), Loader=yaml.Loader)

    for file in werk.constituent_yamls:
        werk.yaml_list.append(yaml.load_all(open(werk.constituent_yamls[file], 'r'), Loader=yaml.Loader))

    werk.initialize_yaml_dictionary()
    werk.populate_yaml()
    werk.dump_yaml()

    pprint.pprint(werk.consolidated_yaml['plates'])






