import argparse
from io import StringIO

import pandas as pd
import requests

# -------- main --------------
# endpoint = "http://dolphin.local:8000"
endpoint = "https://minmod.isi.edu/api/v1/"


def main(args):
    commodity = args.commodity
    output_directory = args.output_directory

    print("Generating grade and tonnage inventory data...")
    # ------------------ Grade and Tonnage Inventory ------------------
    resp = requests.get(
        f"{endpoint}/mineral_site_grade_and_tonnage/{commodity}",
        headers={"Accept": "text/csv"},
    )
    if resp.status_code != 200:
        raise Exception(
            f"Failed to get grade and tonnage inventory data: {resp.status_code} {resp.text}"
        )

    with open(
        f"{output_directory}/{commodity}_mineral_locations_with_grade_tonnage.csv", "w"
    ) as f:
        f.write(resp.text)
    print("Generating deposit type classifications...")
    # ------------------ Deposit Type Classification ------------------
    resp = requests.get(
        f"{endpoint}/mineral_site_deposit_types/{commodity}",
        headers={"Accept": "text/csv"},
    )
    if resp.status_code != 200:
        raise Exception(
            f"Failed to get deposit type classifications: {resp.status_code} {resp.text}"
        )

    with open(
        f"{output_directory}/{commodity}_mineral_locations_with_deposit_types.csv", "w"
    ) as f:
        f.write(resp.text)

    print("Generating mineral site locations...")
    # ------------------ Mineral Site Locations ------------------
    resp = requests.get(
        f"{endpoint}/mineral_site_location/{commodity}",
        headers={"Accept": "text/csv"},
    )
    if resp.status_code != 200:
        raise Exception(
            f"Failed to get deposit type classifications: {resp.status_code} {resp.text}"
        )

    with open(f"{output_directory}/{commodity}_mineral_locations.csv", "w") as f:
        f.write(resp.text)

    print("Generating final Hypersites!")
    # ------------------ Mineral Site Data & Grade and Tonnage Models (Hypersites = aggregated groups of Mineral Locations) ------------------
    resp = requests.get(
        f"{endpoint}/hyper_mineral_sites/{commodity}",
        headers={"Accept": "text/csv"},
    )
    if resp.status_code != 200:
        raise Exception(
            f"Failed to get deposit type classifications: {resp.status_code} {resp.text}"
        )

    df = pd.read_csv(StringIO(resp.text))

    df_mineral_sites_data = df[df["top1_deposit_type"].notna()]
    df_mineral_sites_data.drop(
        columns=["tot_contained_metal", "total_tonnage", "total_grade"],
        axis=1,
        inplace=True,
    )
    df_mineral_sites_data.to_csv(
        f"{output_directory}/{commodity}_mineral_site_data.csv",
        index=False,
        float_format="%.5f",
        mode="w",
    )

    df_grade_tonnage_models = df[df["tot_contained_metal"].notna()]
    df_grade_tonnage_models.to_csv(
        f"{output_directory}/{commodity}_mineral_grade_tonnage_models.csv",
        index=False,
        float_format="%.5f",
        mode="w",
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Generate the TA2 outputs (given a commodity name) from the live MinMod KG using queries"
    )
    parser.add_argument(
        "--commodity",
        type=str,
        default="nickel",
        help="Commodity (default: nickel)",
        required=True,
    )
    parser.add_argument(
        "--output_directory",
        type=str,
        default="output/",
        help="Output directory for TA2 results",
    )

    args = parser.parse_args()
    main(args)
