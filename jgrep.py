#!/usr/bin/env python

import argparse
import re
import sys

junos_sections = ["system", "chassis", "interfaces", "routing-options",
                  "protocols", "policy-options", "firewall", "routing-instances"]
section_choices = list(junos_sections) #full copy of list
section_choices.append("all_sections")

parser = argparse.ArgumentParser()
parser.add_argument(
    'section', help='section to grep from config', choices=section_choices)
parser.add_argument('infile', help='config file to grep from')
parser.add_argument('--outfile', '-o', action='store_true')
args = parser.parse_args()

END_RE = re.compile(r"^}")


def section_from_bounds(section, config):
    """
    Finds and returns full top-level section including start & end line
    """
    start_re = re.compile(section + r" {")
    within_section = False
    desired_config = ""
    for line in config:
        if start_re.search(line):
            within_section = True
        if within_section:
            desired_config += line
        if END_RE.search(line):
            within_section = False
    return(desired_config)


def main():
    """
    Retrieves config sections from regular-style junos config files
    With 'all_sections' section and '-o'; can split into a file per section
    Else prints out section, which could be piped to another input.

    Example usage for multiple input files:

    for file in junos_complete* ; do jgrep.py all_sections "$file" -o ; done

    Created file: system_junos_complete.conf
    Created file: chassis_junos_complete.conf
    Created file: interfaces_junos_complete.conf
    Created file: routing-options_junos_complete.conf
    Created file: protocols_junos_complete.conf
    Created file: policy-options_junos_complete.conf
    Created file: firewall_junos_complete.conf
    Created file: routing-instances_junos_complete.conf
    Created file: system_junos_complete_1.conf
    Created file: chassis_junos_complete_1.conf
    Created file: interfaces_junos_complete_1.conf
    Created file: routing-options_junos_complete_1.conf
    Created file: protocols_junos_complete_1.conf
    Created file: policy-options_junos_complete_1.conf
    Created file: firewall_junos_complete_1.conf
    Created file: routing-instances_junos_complete_1.conf
    """

    
    infile = args.infile.rstrip('\n')
    with open(infile) as in_fh:
        config = in_fh.readlines()
    if args.section == "all_sections":
        find_sections = junos_sections
    else:
        find_sections = [args.section]

    for section_name in find_sections:
        found_section = section_from_bounds(section_name, config)
        if found_section == "":
            print("MISSING: {} not found in config".format(section))
            continue
        if args.outfile:
            outfile_name = "{}_{}".format(section_name, infile)
            with open(outfile_name, 'w') as out_fh:
                out_fh.write(found_section)
            print("Created file: {}".format(outfile_name))
        else:
            print(found_section)

if __name__ == "__main__":
    main()
