#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-

# Code by Lachlan Marnoch, 2025

from astropy.units import yr

from pyfin.portfolio import Portfolio

import os


def main(
        path: str,
        time: float
): 
    time *= yr
    portfolio = Portfolio.from_file(path)
    portfolio.load_etfs()
    portfolio.simulate(length=time)
    

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Create input yaml for an ETF product."
    )
    parser.add_argument(
        "-f",
        help="Path to input file.",
        type=str,
        default="./main.yaml"
    )
    parser.add_argument(
        '-t',
        help='Number of years to run for.',
        type=float,
        default=10.
    )

    args = parser.parse_args()
    main(
        path=args.f,
        time=args.t,
    )    


if __name__ == "__main__":
    parse_args()