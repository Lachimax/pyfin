#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-

# Code by Lachlan Marnoch, 2025

from pyfin.portfolio import Portfolio

import os


def main(
        output_dir: str,
        name: str
):
    directory = os.path.join(output_dir, "portfolios", name)
    os.makedirs(directory, exist_ok=True)
    Portfolio.template_yaml(os.path.join(directory, f"{name}.yaml"), product=name)
    

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Create input yaml for a Portfolio simulation."
    )
    parser.add_argument(
        "-o",
        help="Path to output directory.",
        type=str,
        default="."
    )
    parser.add_argument(
        '-n',
        help='Name for sim.',
        type=str,
        default="template"
    )

    args = parser.parse_args()
    output_path = args.o
    main(
        output_dir=output_path,
        name=args.n
    )    


if __name__ == "__main__":
    parse_args()