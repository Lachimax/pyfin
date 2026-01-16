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
        path_csv: str
):
    try:
        portfolio = Portfolio.from_file(path)
    except FileNotFoundError:
        print(f"No file {path} found. Make sure you're providing the correct Portfolio path using -f.")
        exit()
    portfolio.load_etfs()
    try:
        portfolio.add_etf_units_csv(path_csv, skip_existing=True)
    except FileNotFoundError:
        print(f"No file {path_csv} found. Make sure you're providing the correct CSV path using -c.")
        exit()
        
    portfolio.write_etfs()
    portfolio.tabulate()

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Create input yaml for ETF units."
    )
    parser.add_argument(
        "-f",
        help="Path to Portfolio input file.",
        type=str,
        default="./main.yaml"
    )
    
    parser.add_argument(
        "-c",
        help="Path to CSV file.",
        type=str,
    )

    args = parser.parse_args()
    main(
        path=args.f,
        path_csv=args.c,
    )


if __name__ == "__main__":
    parse_args()