import argparse

import networkx as nx
import pandas as pd
from sparql_generate_query import (
    adjust_lists,
    merge_wkt,
    run_minmod_query,
    sort_strings,
)

# -------- main --------------


def main(args):
    commodity = args.commodity
    output_directory = args.output_directory

    query = """ SELECT ?ms1 ?ms2
                WHERE {
                    ?ms1 a :MineralSite .
                    ?ms2 a :MineralSite .
    
                    ?ms1 owl:sameAs ?ms2 .
                } """
    df_all_sites = run_minmod_query(query, values=True)
    G = nx.from_pandas_edgelist(df_all_sites, source="ms1.value", target="ms2.value")

    # Find connected components
    groups = nx.connected_components(G)

    # Create a mapping from value to group ID
    group_mapping = {}
    for group_id, group in enumerate(groups, start=1):
        for value in group:
            group_mapping[value] = group_id

    # Map group IDs to the dataframe
    df_all_sites["group_id"] = df_all_sites["ms1.value"].map(group_mapping)

    print("Generating grade and tonnage inventory data...")
    # ------------------ Grade and Tonnage Inventory ------------------
    query = """
    SELECT 
      ?ms                                              # Mineral Site URI
      ?ms_name                                         # Mineral Site Name
      ?country                                         # Country
      ?loc_crs                                         # WKT CRS
      ?loc_wkt                                         # WKT Geometry
      ?state_or_province
      ?doc
      ?total_tonnage_measured
      ?total_tonnage_indicated
      ?total_tonnage_inferred
      ?total_contained_measured
      ?total_contained_indicated
      ?total_contained_inferred
      (?total_tonnage_measured + ?total_tonnage_indicated + ?total_tonnage_inferred AS ?total_tonnage)                     # Total Tonnage [million tonnes]
      (?total_contained_measured + ?total_contained_indicated + ?total_contained_inferred AS ?total_contained_metal)
      (IF(?total_tonnage > 0, ?total_contained_metal / ?total_tonnage, 0) AS ?total_grade)                                 # Total Grade
    WHERE {
      {
        SELECT ?ms ?ms_name ?country ?loc_crs ?loc_wkt ?state_or_province ?doc
               (SUM(?tonnage_measured) AS ?total_tonnage_measured)
               (SUM(?tonnage_indicated) AS ?total_tonnage_indicated)
               (SUM(?tonnage_inferred) AS ?total_tonnage_inferred)
               (SUM(?contained_measured) AS ?total_contained_measured)
               (SUM(?contained_indicated) AS ?total_contained_indicated)
               (SUM(?contained_inferred) AS ?total_contained_inferred)
        WHERE {

            ?ms :mineral_inventory ?mi .
            OPTIONAL { ?ms rdfs:label|:name ?ms_name . FILTER (STR(?ms_name) != "") }

            OPTIONAL { ?ms :location_info ?loc .

            OPTIONAL { ?loc :country ?country . FILTER (STR(?country) != "") }
            OPTIONAL { ?loc :state_or_province ?state_or_province . FILTER (STR(?state_or_province) != "") }
            OPTIONAL { ?loc :crs ?loc_crs . FILTER (STR(?loc_crs) != "") }
            OPTIONAL { ?loc :location ?loc_wkt . FILTER (STR(?loc_wkt) != "") }

            }

            ?mi :category ?mi_cat .
            ?mi :commodity [ :name ?name ] .
            OPTIONAL { ?mi :reference/:document ?doc . }
            FILTER(LCASE(STR(?name)) = "%s")

            {
                SELECT ?mi (MAX(?ore_val) AS ?max_ore_val) (SAMPLE(?grade_val) AS ?matched_grade_val)
                WHERE {
                    ?mi :ore [ :ore_value ?ore_val_raw; :ore_unit ?ore_unit] .
                    OPTIONAL { ?mi :grade [ :grade_value ?grade_val; :grade_unit ?grade_unit] . }
                    BIND(IF(bound(?ore_val_raw), ?ore_val_raw, 0) AS ?ore_val_pre)
                    BIND(IF(?ore_unit = <https://minmod.isi.edu/resource/Q202>, ?ore_val_pre, IF(?ore_unit = <https://minmod.isi.edu/resource/Q200>, ?ore_val_pre / 1e6, ?ore_val_pre)) AS ?ore_val)
                }
                GROUP BY ?mi
            }

            BIND(IF(CONTAINS(LCASE(STR(?mi_cat)), "measured"), ?max_ore_val, 0) AS ?tonnage_measured)
            BIND(IF(CONTAINS(LCASE(STR(?mi_cat)), "indicated"), ?max_ore_val, 0) AS ?tonnage_indicated)
            BIND(IF(CONTAINS(LCASE(STR(?mi_cat)), "inferred"), ?max_ore_val, 0) AS ?tonnage_inferred)

            BIND(IF(CONTAINS(LCASE(STR(?mi_cat)), "measured") && ?matched_grade_val > 0, ?max_ore_val * ?matched_grade_val, 0) AS ?contained_measured)
            BIND(IF(CONTAINS(LCASE(STR(?mi_cat)), "indicated") && ?matched_grade_val > 0, ?max_ore_val * ?matched_grade_val, 0) AS ?contained_indicated)
            BIND(IF(CONTAINS(LCASE(STR(?mi_cat)), "inferred") && ?matched_grade_val > 0, ?max_ore_val * ?matched_grade_val, 0) AS ?contained_inferred)

        }
        GROUP BY ?ms ?ms_name ?country ?loc_crs ?loc_wkt ?state_or_province ?doc
      }
    }
    """ % (
        commodity
    )
    query_resp_df = run_minmod_query(query, values=True)
    if not query_resp_df.empty:
        gt_data_df = pd.DataFrame(
            [
                {
                    "ms": row["ms.value"],
                    "ms_name": (
                        row["ms_name.value"]
                        if len(str(row["ms_name.value"])) > 0
                        else row["ms.value"].split("/")[-1]
                    ),
                    "country": row.get("country.value", None),
                    "state_or_province": row.get("state_or_province.value", None),
                    "loc_crs": row.get("loc_crs.value", None),
                    "loc_wkt": row.get("loc_wkt.value", None),
                    "tot_tonnage_measured": float(row["total_tonnage_measured.value"]),
                    "tot_tonnage_indicated": float(
                        row["total_tonnage_indicated.value"]
                    ),
                    "tot_tonnage_inferred": float(row["total_tonnage_inferred.value"]),
                    "tot_contained_measured": float(
                        row["total_contained_measured.value"]
                    ),
                    "tot_contained_indicated": float(
                        row["total_contained_indicated.value"]
                    ),
                    "tot_contained_inferred": float(
                        row["total_contained_inferred.value"]
                    ),
                    "tot_contained_metal": float(row["total_contained_metal.value"]),
                    "total_tonnage": float(row["total_tonnage.value"]),
                    "total_grade": float(row["total_grade.value"]),
                    "internal_document_reference": row.get("doc.value", None),
                }
                for index, row in query_resp_df.iterrows()
            ]
        )

        gt_df_only = gt_data_df.drop_duplicates()
        gt_df_only.reset_index(drop=True, inplace=True)
        gt_df_only.set_index("ms", inplace=True)
        gt_df_only["info_count"] = gt_df_only[
            ["country", "state_or_province", "loc_crs", "loc_wkt"]
        ].apply(lambda x: ((x != "") & (x.notna())).sum(), axis=1)
        gt_df_only = gt_df_only.sort_values(by="info_count", ascending=False)
        gt_df_only = gt_df_only[~gt_df_only.index.duplicated(keep="first")]
        gt_df_only.drop(columns=["info_count"], inplace=True)
        gt_df_only.to_csv(
            f"{output_directory}/{commodity}_mineral_locations_with_grade_tonnage.csv",
            index=True,
            float_format="%.5f",
            mode="w",
        )

    print("Generating deposit type classifications...")
    # ------------------ Deposit Type Classification ------------------
    query = """
       SELECT ?ms ?ms_name ?deposit_name ?deposit_source ?deposit_confidence ?deposit_group ?deposit_environment ?country ?loc_crs ?loc_wkt ?state_or_province
       WHERE {

           ?ms :deposit_type_candidate ?deposit_candidate_uri .
           ?deposit_candidate_uri :source ?deposit_source .
           ?deposit_candidate_uri :confidence ?deposit_confidence .
           ?deposit_candidate_uri :normalized_uri [
               rdfs:label ?deposit_name ;
               :deposit_group ?deposit_group ;
               :environment ?deposit_environment ] .

           ?ms :mineral_inventory ?mi .
           OPTIONAL { ?ms rdfs:label|:name ?ms_name . }

           OPTIONAL { 
           ?ms :location_info ?loc .
           OPTIONAL { ?loc :country ?country . }
           OPTIONAL { ?loc :state_or_province ?state_or_province . }
           OPTIONAL { ?loc :crs ?loc_crs . }
           OPTIONAL { ?loc :location ?loc_wkt . }
           }


           ?mi :commodity [ :name ?name ] .
           FILTER(LCASE(STR(?name)) = "%s")
       }
       """ % (
        commodity
    )
    query_resp_df = run_minmod_query(query, values=True)
    if not query_resp_df.empty:
        deposits_data = pd.DataFrame(
            [
                {
                    "ms": row["ms.value"],
                    "ms_name": (
                        row["ms_name.value"]
                        if len(str(row["ms_name.value"])) > 0
                        else row["ms.value"].split("/")[-1]
                    ),
                    "country": row.get("country.value", None),
                    "state_or_province": row.get("state_or_province.value", None),
                    "loc_crs": row.get("loc_crs.value", None),
                    "loc_wkt": row.get("loc_wkt.value", None),
                    "deposit_type": row.get("deposit_name.value", None),
                    "deposit_group": row.get("deposit_group.value", None),
                    "deposit_environment": row.get("deposit_environment.value", None),
                    "deposit_classification_confidence": row.get(
                        "deposit_confidence.value", None
                    ),
                    "deposit_classification_source": row.get(
                        "deposit_source.value", None
                    ),
                }
                for index, row in query_resp_df.iterrows()
            ]
        )

        deposits_df = deposits_data.drop_duplicates()
        deposits_df.reset_index(drop=True, inplace=True)
        deposits_df.set_index(["ms", "deposit_type"], inplace=True)
        # deposits_df['info_count'] = deposits_df[['country', 'state_or_province', 'loc_crs', 'loc_wkt']].apply(lambda x: ((x != '') & (x.notna())).sum(), axis=1)
        deposits_df["info_count"] = deposits_df[
            [
                "country",
                "state_or_province",
                "loc_crs",
                "loc_wkt",
                "deposit_classification_confidence",
            ]
        ].apply(
            lambda x: (((x[:-1] != "") & (x[:-1].notna())).sum(), float(x[-1])), axis=1
        )
        deposits_df_ordered = deposits_df.sort_values(by="info_count", ascending=False)
        deposits_df_ordered = deposits_df_ordered[
            ~deposits_df_ordered.index.duplicated(keep="first")
        ]
        deposits_df_ordered.drop(columns=["info_count"], inplace=True)
        deposits_df_ordered["deposit_classification_confidence"] = deposits_df_ordered[
            "deposit_classification_confidence"
        ].astype(float)
        deposits_df_ordered.reset_index(inplace=True)

        grouped = deposits_df_ordered.groupby("ms")
        results = []
        for name, group in grouped:
            # Sort by 'deposit_classification_confidence'
            unique_group = group.drop_duplicates(
                subset=[
                    "deposit_type",
                    "deposit_group",
                    "deposit_environment",
                    "deposit_classification_confidence",
                    "deposit_classification_source",
                ]
            )
            sorted_group = unique_group.sort_values(
                "deposit_classification_confidence", ascending=False
            )
            top_5 = sorted_group.head(5)

            result_row = {"ms": name}
            for i, row in enumerate(top_5.itertuples(index=False), start=1):
                result_row[f"top{i}_deposit_type"] = row.deposit_type
                result_row[f"top{i}_deposit_group"] = row.deposit_group
                result_row[f"top{i}_deposit_environment"] = row.deposit_environment
                result_row[f"top{i}_deposit_classification_confidence"] = (
                    row.deposit_classification_confidence
                )
                result_row[f"top{i}_deposit_classification_source"] = (
                    row.deposit_classification_source
                )

            results.append(result_row)

        final_df = pd.DataFrame(results)
        unique_ms_data = deposits_df_ordered[
            ["ms", "ms_name", "country", "state_or_province", "loc_crs", "loc_wkt"]
        ].drop_duplicates(subset=["ms"])
        merged_deposits_df = pd.merge(unique_ms_data, final_df, on="ms", how="left")
        merged_deposits_df.to_csv(
            f"{output_directory}/{commodity}_mineral_locations_with_deposit_types.csv",
            index=False,
            float_format="%.5f",
            mode="w",
        )

    print("Generating mineral site locations...")
    # ------------------ Mineral Site Locations ------------------
    query = """
    SELECT ?ms ?ms_name ?ms_type ?ms_rank ?country ?loc_crs ?loc_wkt ?state_or_province
    WHERE {

        ?ms :mineral_inventory ?mi .
        OPTIONAL { ?ms rdfs:label|:name ?ms_name . FILTER (STR(?ms_name) != "") }
        OPTIONAL { ?ms :site_type ?ms_type . FILTER (STR(?ms_type) != "") }
        OPTIONAL { ?ms :site_rank ?ms_rank . FILTER (STR(?ms_rank) != "") }

        OPTIONAL { ?ms :location_info ?loc . 
        OPTIONAL { ?loc :country ?country . FILTER (STR(?country) != "") }
        OPTIONAL { ?loc :state_or_province ?state_or_province . FILTER (STR(?state_or_province) != "") }
        OPTIONAL { ?loc :crs ?loc_crs . FILTER (STR(?loc_crs) != "") }
        OPTIONAL { ?loc :location ?loc_wkt . FILTER (STR(?loc_wkt) != "") }
        }

        OPTIONAL { ?mi :category ?mi_cat . }
        ?mi :commodity [ :name ?name ] .
        FILTER(LCASE(STR(?name)) = "%s")
    }
    """ % (
        commodity
    )
    query_resp_df = run_minmod_query(query, values=True)
    if not query_resp_df.empty:
        sites_df = pd.DataFrame(
            [
                {
                    "ms": row["ms.value"],
                    "ms_name": (
                        row["ms_name.value"]
                        if len(str(row["ms_name.value"])) > 0
                        else row["ms.value"].split("/")[-1]
                    ),
                    "ms_type": (
                        row["ms_type.value"]
                        if len(str(row["ms_type.value"])) > 0
                        else ""
                    ),
                    "ms_rank": (
                        row["ms_rank.value"]
                        if len(str(row["ms_rank.value"])) > 0
                        else ""
                    ),
                    "country": row.get("country.value", None),
                    "state_or_province": row.get("state_or_province.value", None),
                    "loc_crs": row.get("loc_crs.value", None),
                    "loc_wkt": row.get("loc_wkt.value", None),
                }
                for index, row in query_resp_df.iterrows()
            ]
        )
        sites_df.dropna(
            subset=["country", "state_or_province", "loc_crs", "loc_wkt"],
            how="all",
            inplace=True,
        )

        df_melted = df_all_sites.melt(
            id_vars=["group_id"], value_vars=["ms1.value", "ms2.value"], value_name="ms"
        )

        df_all_sites_groups = df_melted[["ms", "group_id"]].drop_duplicates()
        merged_df_all_sites = pd.merge(
            sites_df, df_all_sites_groups, how="left", on="ms"
        )

        max_group_id = merged_df_all_sites["group_id"].fillna(0).max()
        merged_df_all_sites["group_id"] = merged_df_all_sites["group_id"].fillna(
            pd.Series(
                range(
                    int(max_group_id) + 1,
                    len(merged_df_all_sites) + int(max_group_id) + 1,
                )
            )
        )
        sorted_df_all_sites_all_dep = merged_df_all_sites.sort_values(
            by=["group_id", "ms_name"]
        )

        sorted_df_all_sites_all_dep.reset_index(drop=True, inplace=True)
        sorted_df_all_sites_all_dep.set_index("ms", inplace=True)
        sorted_df_all_sites_all_dep["info_count"] = sorted_df_all_sites_all_dep[
            ["country", "state_or_province", "loc_crs", "loc_wkt"]
        ].apply(lambda x: ((x != "") & (x.notna())).sum(), axis=1)
        sorted_df_all_sites_all_dep = sorted_df_all_sites_all_dep.sort_values(
            by="info_count", ascending=False
        )
        sorted_df_all_sites_all_dep = sorted_df_all_sites_all_dep[
            ~sorted_df_all_sites_all_dep.index.duplicated(keep="first")
        ]
        sorted_df_all_sites_all_dep.drop(columns=["info_count"], inplace=True)
        sorted_df_all_sites_all_dep["group_id"] = sorted_df_all_sites_all_dep[
            "group_id"
        ].astype(int)
        sorted_df_all_sites_all_dep.reset_index(inplace=True)
        sorted_df_all_sites_all_dep.to_csv(
            f"{output_directory}/{commodity}_mineral_locations.csv",
            index=False,
            float_format="%.5f",
            mode="w",
        )

        print("Generating final Hypersites!")
        # ------------------ Mineral Site Data & Grade and Tonnage Models (Hypersites = aggregated groups of Mineral Locations) ------------------

        # ---- 1. find top grade-tonnage per each hypersite ----
        gt_df_only.reset_index(inplace=True)
        detailed_df_w_gt = pd.merge(
            gt_df_only,
            sorted_df_all_sites_all_dep[["ms", "group_id"]],
            on="ms",
            how="left",
        )
        detailed_df_w_gt = detailed_df_w_gt[~detailed_df_w_gt["group_id"].isna()]
        # ensure 'tot_contained_metal' is float and handle errors
        detailed_df_w_gt["tot_contained_metal"] = pd.to_numeric(
            detailed_df_w_gt["tot_contained_metal"], errors="coerce"
        )
        # remove rows where 'tot_contained_metal' is still NaN
        detailed_df_w_gt = detailed_df_w_gt[
            detailed_df_w_gt["tot_contained_metal"].notna()
        ]
        # group by 'group_id' and find the entry with the highest 'tot_contained_metal'
        merged_gt_df_max_idx = detailed_df_w_gt.groupby("group_id")[
            "tot_contained_metal"
        ].idxmax()
        # select the rows with the highest confidence for each group
        best_gt_df = detailed_df_w_gt.loc[
            merged_gt_df_max_idx,
            ["group_id", "tot_contained_metal", "total_tonnage", "total_grade"],
        ]

        # ---- 2. find top grade-tonnage per each hypersite ----
        detailed_df = pd.merge(
            merged_deposits_df,
            sorted_df_all_sites_all_dep[["ms", "group_id"]],
            on="ms",
            how="left",
        )
        detailed_df = detailed_df[~detailed_df["group_id"].isna()]
        detailed_df["top1_deposit_classification_confidence"] = pd.to_numeric(
            detailed_df["top1_deposit_classification_confidence"], errors="coerce"
        )
        detailed_df = detailed_df[
            detailed_df["top1_deposit_classification_confidence"].notna()
        ]
        merged_deposits_df_max_idx = detailed_df.groupby("group_id")[
            "top1_deposit_classification_confidence"
        ].idxmax()
        best_deposits_df = detailed_df.loc[
            merged_deposits_df_max_idx,
            [
                "group_id",
                "top1_deposit_type",
                "top1_deposit_group",
                "top1_deposit_environment",
                "top1_deposit_classification_confidence",
                "top1_deposit_classification_source",
            ],
        ]

        # ---- 3. squash into single-row hypersites ----
        new_result_df = (
            sorted_df_all_sites_all_dep.groupby("group_id")
            .agg(
                {
                    "group_id": "first",  # take the first (or any since all are the same within a group)
                    "ms": lambda x: set(x),
                    "ms_name": sort_strings,  # sort by string length after converting to set
                    "ms_type": sort_strings,
                    "ms_rank": sort_strings,
                    "country": sort_strings,
                    "state_or_province": sort_strings,
                    "loc_crs": sort_strings,
                    "loc_wkt": merge_wkt,
                }
            )
            .reset_index(drop=True)
        )
        for column in new_result_df.columns:
            new_result_df[column] = new_result_df[column].apply(adjust_lists)

        new_result_df = pd.merge(new_result_df, best_gt_df, on="group_id", how="left")
        new_result_df = pd.merge(
            new_result_df, best_deposits_df, on="group_id", how="left"
        )

        df_mineral_sites_data = new_result_df[
            new_result_df["top1_deposit_type"].notna()
        ]
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

        df_grade_tonnage_models = new_result_df[
            new_result_df["tot_contained_metal"].notna()
        ]
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
