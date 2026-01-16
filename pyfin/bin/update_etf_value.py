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
        print(f"No file {path} found. Make sure you're providing the correct Portfolio path using -f.")
        exit()
    portfolio.load_etfs()
    portfolio.update_etf_values_ui()
    portfolio.write_etfs()
    portfolio.tabulate()
    # This currently doesn't save the new value in any meaningful way (the ETF units have it, but that will get wiped the next time it loads.)
    # Need a way of saving records to get loaded.
    

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

    args = parser.parse_args()
    main(
        path=args.f,
    )


if __name__ == "__main__":
    parse_args()