#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-

# Code by Lachlan Marnoch, 2025

import pyfin.utils as utils
from pyfin.portfolio import Portfolio
from pyfin.etf.product import ETFProduct
from pyfin.etf.unit import ETFUnit

import os


def main(
        output_dir: str,
        name: str
):
    if name is None:
        name = utils.user_input("What do you want to call this portfolio?")
    
    
    portfolio_directory = os.path.join(output_dir, "portfolios", name)
    print(f"Generating directory for this Portfolio at {name}")
    os.makedirs(portfolio_directory, exist_ok=True)
    Portfolio.template_yaml(os.path.join(portfolio_directory, f"{name}.yaml"))

    if utils.select_yn_exit("Does this Portfolio include ETFs?"):
        
        etf_name = utils.user_input("Please enter a code for one ETF included in the Portfolio.")

        product_directory = os.path.join(portfolio_directory, "etf", "products")
        os.makedirs(product_directory, exist_ok=True)
        ETFProduct.template_yaml(os.path.join(product_directory, f"{etf_name}.yaml"), code=name)

        unit_directory = os.path.join(portfolio_directory, "etf", "units", etf_name)
        os.makedirs(unit_directory, exist_ok=True)
        ETFUnit.template_yaml(os.path.join(unit_directory, "unit_template.yaml"), product=name)


    

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Create input directory and yaml for a Portfolio."
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
        default=None
    )

    args = parser.parse_args()
    output_path = args.o
    main(
        output_dir=output_path,
        name=args.n
    )    


if __name__ == "__main__":
    parse_args()