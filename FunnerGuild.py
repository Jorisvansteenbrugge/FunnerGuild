#!/usr/bin/env python3
import json
import argparse


class Taxon:
    def __init__(self, name, level, mode, guild, confidence, growthForm, trait, notes):
        self.name = name
        self.level = level
        self.mode = mode
        self.guild = guild
        self.confidence = confidence
        self.growthForm = growthForm
        self.trait = trait
        self.notes = notes

    def __str__(self):
        return f"{self.name}\t{self.level}\t{self.mode}\t{self.guild}\t{self.confidence}\t{self.growthForm}\t{self.trait}\t{self.notes}"


def parse_arguments():
    p = argparse.ArgumentParser()
    p.add_argument("-d", "--database", dest='db', required=True,
                   help="Funguild database in json format")
    p.add_argument('-i', '--otu-table', dest='otu_table', required=True,
                   help='OTU table (comma separated) with a column named "taxonomy"')

    return p.parse_args()


def import_db(database):
    return {taxa_row['taxon']: Taxon(taxa_row['taxon'], taxa_row['taxonomicLevel'], taxa_row['trophicMode'],
                                     taxa_row['guild'], taxa_row['confidenceRanking'], taxa_row['growthForm'],
                                     taxa_row['trait'], taxa_row['notes']) for taxa_row in data}


def read_otus(otu_table, taxa_dict):
    line_sep = ','
    with(open(otu_table)) as f_otutable:
        header = f_otutable.readline().strip().split(line_sep)

        # add new cols to header
        header += ['Taxon', 'TaxonomicLevel', 'TrophicMode', 'Guild', 'ConfidenceRanking', 'growthForm', 'Trait',
                   'Notes']
        print("\t".join(header))

        tax_col = header.index("taxonomy")
        for line in f_otutable:
            if line.startswith('#'):
                continue

            line = line.strip().split(line_sep)
            taxon_val = line[tax_col]
            try:
                taxa_funguild_content = taxa_dict[taxon_val]
                outline = "\t".join(line) + "\t" + str(taxa_funguild_content)
            except KeyError:
                outline = "\t".join(line)
            print(outline)


if __name__ == "__main__":
    options = parse_arguments()
    data = json.load(open(options.db))
    taxa_dict = import_db(data)

    read_otus(options.otu_table, taxa_dict)
