#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-

# Code by Lachlan Marnoch, 2025

from pyfin.etf.product import ETFProduct
from pyfin.etf.unit import ETFUnit

import os


def main(
        output_dir: str,
        name: str
):
    directory = os.path.join(output_dir, "etf", "products")
    os.makedirs(directory, exist_ok=True)
    ETFProduct.template_yaml(os.path.join(directory, f"{name}.yaml"), code=name)

    directory = os.path.join(output_dir, "etf", "units", name)
    os.makedirs(directory, exist_ok=True)
    ETFUnit.template_yaml(os.path.join(directory, "unit_template.yaml"), product=name)
    

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Create input yaml for an ETF product."
    )
    parser.add_argument(
        "-o",
        help="Path to output directory.",
        type=str,
        default="."
    )
    parser.add_argument(
        '-n',
        help='Code for product.',
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