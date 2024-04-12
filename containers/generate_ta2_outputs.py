import argparse
import pandas as pd
import networkx as nx
from sparql_generate_query import run_minmod_query

# -------- main --------------


def main(args):
    commodity = args.commodity
    output_directory = args.output_directory

    query = ''' SELECT ?ms1 ?ms2
                WHERE {
                    ?ms1 a :MineralSite .
                    ?ms2 a :MineralSite .
    
                    ?ms1 owl:sameAs ?ms2 .
                } '''
    df_all_sites = run_minmod_query(query, values=True)
    G = nx.from_pandas_edgelist(df_all_sites, source='ms1.value', target='ms2.value')

    # Find connected components
    groups = nx.connected_components(G)

    # Create a mapping from value to group ID
    group_mapping = {}
    for group_id, group in enumerate(groups, start=1):
        for value in group:
            group_mapping[value] = group_id

    # Map group IDs to the dataframe
    df_all_sites['group_id'] = df_all_sites['ms1.value'].map(group_mapping)

    # get all deposit types, their confidences for Mineral Sites and aggregated (and transformed) grade-tonnage data
    query = '''
    SELECT 
      ?ms                                              # Mineral Site URI
      ?ms_name                                         # Mineral Site Name
      ?deposit_name                                    # Deposit Type Name
      ?deposit_confidence                              # Deposit Type Confidence
      ?deposit_source
      ?deposit_group
      ?deposit_environment
      ?country                                         # Country
      ?loc_wkt                                         # WKT Geometry
      ?state_or_province
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
        SELECT ?ms ?ms_name ?deposit_name ?deposit_confidence ?country ?loc_wkt ?state_or_province ?deposit_source ?deposit_group ?deposit_environment
               (SUM(?tonnage_measured) AS ?total_tonnage_measured)
               (SUM(?tonnage_indicated) AS ?total_tonnage_indicated)
               (SUM(?tonnage_inferred) AS ?total_tonnage_inferred)
               (SUM(?contained_measured) AS ?total_contained_measured)
               (SUM(?contained_indicated) AS ?total_contained_indicated)
               (SUM(?contained_inferred) AS ?total_contained_inferred)
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
            
            ?ms :location_info ?loc .
            OPTIONAL { ?loc :country ?country . }
            OPTIONAL { ?loc :state_or_province ?state_or_province . }
            OPTIONAL { ?loc :location ?loc_wkt . }
            #FILTER(datatype(?loc_wkt) = geo:wktLiteral)
            
            ?mi :category ?mi_cat .
            ?mi :commodity [ :name ?name ] .
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
        GROUP BY ?ms ?ms_name ?deposit_name ?deposit_confidence ?country ?loc_wkt ?state_or_province ?deposit_group ?deposit_source ?deposit_environment
      }
    }
    ''' % (commodity)
    query_resp_df = run_minmod_query(query, values=True)
    gt_data_df = pd.DataFrame([
        {
            'ms': row['ms.value'],
            'ms_name': row['ms_name.value'] if len(row['ms_name.value']) > 0 else row['ms.value'].split('/')[-1],
            'deposit_type': row['deposit_name.value'],
            'deposit_type_confidence': row['deposit_confidence.value'],
            'deposit_source': row['deposit_source.value'],
            'deposit_group': row['deposit_group.value'],
            'deposit_environment': row['deposit_environment.value'],
            'country': row['country.value'],
            'state_or_province': row['state_or_province.value'],
            'loc_wkt': row['loc_wkt.value'],
            'total_tonnage':float(row['total_tonnage.value']),
            'total_grade': float(row['total_grade.value'])
        }
        for index, row in query_resp_df.iterrows()
    ])

    df_melted = df_all_sites.melt(id_vars=['group_id'], value_vars=['ms1.value', 'ms2.value'], value_name='ms')

    df_all_sites_groups = df_melted[['ms', 'group_id']].drop_duplicates()
    merged_df_all_sites_all_dep = pd.merge(gt_data_df, df_all_sites_groups, how='left', on='ms')

    max_group_id = merged_df_all_sites_all_dep['group_id'].fillna(0).max()
    merged_df_all_sites_all_dep['group_id'] = merged_df_all_sites_all_dep['group_id'].fillna(pd.Series(range(int(max_group_id) + 1, len(merged_df_all_sites_all_dep) + int(max_group_id) + 1)))
    sorted_df_all_sites_all_dep = merged_df_all_sites_all_dep.sort_values(by=['group_id', 'ms_name', 'deposit_type_confidence'])

    # --------- Mineral Site to Grade-Tonnage data  ---------
    gt_df_only = sorted_df_all_sites_all_dep[['ms', 'ms_name', 'country', 'state_or_province', 'loc_wkt', 'total_tonnage', 'total_grade']]
    gt_df_only = gt_df_only.drop_duplicates(subset=['ms', 'ms_name', 'country', 'state_or_province', 'loc_wkt', 'total_tonnage', 'total_grade'])

    # reset index if needed
    newgt_df_only_df = gt_df_only.reset_index(drop=True)
    newgt_df_only_df.to_csv(f'{output_directory}/{commodity}_mineral_sites_to_grade_tonnage.csv', index=False, mode='w')

    # --------- Mineral Site to Deposit Type classification results ---------
    gt_dt_only = sorted_df_all_sites_all_dep[['ms', 'ms_name', 'country', 'state_or_province', 'loc_wkt', 'deposit_type', 'deposit_type_confidence', 'deposit_source', 'deposit_group', 'deposit_environment']]
    gt_dt_only = gt_dt_only.drop_duplicates(subset=['ms', 'ms_name', 'country', 'state_or_province', 'loc_wkt', 'deposit_type', 'deposit_type_confidence', 'deposit_source', 'deposit_group', 'deposit_environment'])

    # reset index if needed
    newgt_dt_only_df = gt_dt_only.reset_index(drop=True)
    duplicates = newgt_dt_only_df.duplicated(subset=['ms'], keep=False)
    if duplicates.any():
        newgt_dt_only_df = newgt_dt_only_df.drop(newgt_dt_only_df[(newgt_dt_only_df['country'] == '') & (newgt_dt_only_df['state_or_province'] == '') & (newgt_dt_only_df['loc_wkt'] == '')].index)
    newgt_dt_only_df.to_csv(f'{output_directory}/{commodity}_mineral_sites_to_deposit_types.csv', index=False, mode='w')

    # --------- Hyper Site (aggregated group of sites) to Mineral Site ---------
    gt_hypersite_only = sorted_df_all_sites_all_dep[['ms', 'group_id', 'ms_name', 'country', 'state_or_province', 'loc_wkt']]
    gt_hypersite_only = gt_hypersite_only.drop_duplicates(subset=['ms', 'group_id', 'ms_name', 'country', 'state_or_province', 'loc_wkt'])

    # reset index if needed
    gt_hypersite_only = gt_hypersite_only.reset_index(drop=True)
    gt_hypersite_only.to_csv(f'{output_directory}/{commodity}_mineral_sites_hypersites.csv', index=False, mode='w')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate the TA2 outputs (given a commodity name) from the live MinMod KG using queries")
    parser.add_argument("--commodity", type=str, default='nickel', help="Commodity (default: nickel)", required=True)
    parser.add_argument("--output_directory", type=str, default='output/', help="Output directory for (mineral site grade-tonnages, deposit types, and mineral sites reconciliation (hypersites)")

    args = parser.parse_args()
    main(args)

