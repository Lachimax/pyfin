#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-

# Code by Lachlan Marnoch, 2025

from astropy.units import yr

from pyfin.portfolio import Portfolio
from pyfin import utils

import os


def main(
        path: str,
):
    try:
        portfolio = Portfolio.from_file(path)
    except FileNotFoundError:
        print(f"No file {path} found. Make sure you're providing the correct path using -f.")
        exit()
    portfolio.load_etfs()
    portfolio.tabulate()

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Create input yaml for ETF units."
    )
    parser.add_argument(
        "-f",
        help="Path to input file.",
        type=str,
        default="./main.yaml"
    )

    args = parser.parse_args()
    main(
        path=args.f,
    )


if __name__ == "__main__":
    parse_args()