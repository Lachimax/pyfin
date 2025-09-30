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
):
    Portfolio.template_yaml()
    

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Template script."
    )
    parser.add_argument(
        "-o",
        help="Path to output directory.",
        type=str,
        default="."
    )

    args = parser.parse_args()
    output_path = args.o
    main(
        output_dir=output_path,
    )    


if __name__ == "__main__":
    parse_args()