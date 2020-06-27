#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
'''
SIOgen: Simple Insert Delete Dataset Generator
'''

import random
import csv

# Parameters
ATT = 'att'
INS = 'ins'
DEL = 'del'
FILE = 'file'

# Default parameter values
ATT_DEFAULT = 10
INS_DEFAULT = 10000
DEL_DEFAULT = 1000
FILE_DEFAULT = 'output.csv'


def gen_insertions(par_dict):
    '''
    Generate insertions
    '''
    # Current key
    current_key = 0
    # List of records
    rec_list = []
    # Loop to create insertions
    for _ in range(par_dict[INS]):
        # New record
        new_record = {}
        # List of attributes
        att_list = ['A' + str(number + 1) for number in range(par_dict[ATT])]
        # Generate each attribute value
        for att in att_list:
            new_record[att] = random.randint(0, par_dict[INS])
        # Overwrite the attribute key
        new_record['A1'] = current_key
        # Increase key value
        current_key += 1
        # Insertion flag
        new_record['OP'] = '+'
        # Append record to list
        rec_list.append(new_record)
    return rec_list


def gen_deletions(par_dict):
    '''
    Generate deletions
    '''
    # List of records
    rec_list = []
    # Loop to create insertions
    for _ in range(par_dict[DEL]):
        # New record
        new_record = {}
        # List of attributes
        att_list = ['A' + str(number + 1) for number in range(par_dict[ATT])]
        # Generate each attribute value
        for att in att_list:
            new_record[att] = 0
        # Overwrite the attribute key
        new_record['A1'] = random.randint(0, par_dict[DEL])
        # Deletion flag
        new_record['OP'] = '-'
        # Append record to list
        rec_list.append(new_record)
    return rec_list


def store_records(rec_list, par_dict):
    '''
    Store a record list in into file
    '''
    # Check if record list is empty
    if not rec_list:
        return
    # Build attribute list including operation flag
    att_list = ['OP'] + \
        ['A' + str(number + 1) for number in range(par_dict[ATT])]
    # Open file
    out_file = open(par_dict[FILE], 'w')
    # Create CSV writer
    out_write = csv.DictWriter(out_file, att_list)
    # Write file header
    out_write.writeheader()
    # Write records
    out_write.writerows(rec_list)
    # Close file
    out_file.close()


def gen_data(par_dict):
    '''
    Generate data
    '''
    # Generate insertions
    rec_list = gen_insertions(par_dict)
    # Append deletions
    rec_list += gen_deletions(par_dict)
    # Shuffle
    random.shuffle(rec_list)
    # Store initial list on file
    store_records(rec_list, par_dict)


def get_arguments(print_help=False):
    '''
    Get arguments
    '''
    import argparse
    parser = argparse.ArgumentParser('SIOGen')
    parser.add_argument('-a', '--attributes', action='store', type=int,
                        default=ATT_DEFAULT,
                        help='Number of attributes (default: ' +
                        str(ATT_DEFAULT) + ')')
    parser.add_argument('-i', '--insertions', action='store', type=int,
                        default=INS_DEFAULT,
                        help='Number of insertions (default: ' +
                        str(INS_DEFAULT) + ')')
    parser.add_argument('-d', '--deletions', action='store', type=int,
                        default=DEL_DEFAULT,
                        help='Number of deletions (default: ' +
                        str(DEL_DEFAULT) + ')')
    parser.add_argument('-f', '--filename', action='store', type=str,
                        default=FILE_DEFAULT,
                        help='Output filename (default: ' +
                        FILE_DEFAULT + ')')
    args = parser.parse_args()
    if print_help:
        parser.print_help()
    return args


def main():
    '''
    Main routine
    '''
    # Get arguments
    args = get_arguments()
    # Create dictionary of parameters
    par_dict = {
        ATT: args.attributes,
        INS: args.insertions,
        DEL: args.deletions,
        FILE: args.filename
        }
    # Generate data
    gen_data(par_dict)


if __name__ == '__main__':
    main()
