from sparql_generate_query import run_minmod_query
import pandas as pd
import sys

input_csv_file = sys.argv[1]   # input  cols: source_id, record_id, GroupID
output_csv_file = sys.argv[2]  # output cols: ms_uri_1, ms_uri_2

df_er_results = pd.read_csv(input_csv_file)
df_er_results.dropna(inplace=True)
df_er_results = df_er_results.drop_duplicates(subset=['source_id', 'record_id'])


query = ''' SELECT ?ms ?ms_record_id ?ms_source_id
            WHERE {
                ?ms a :MineralSite .
                ?ms :record_id ?ms_record_id .
                ?ms :source_id ?ms_source_id .
            } '''
df_all_sites = run_minmod_query(query, values=True)
df_all_sites.dropna(inplace=True)
df_all_sites = df_all_sites.drop_duplicates(subset=['ms_source_id.value', 'ms_record_id.value'])

merged_df = df_er_results.merge(df_all_sites, how='left', left_on=['source_id', 'record_id'], right_on=['ms_source_id.value', 'ms_record_id.value'])
url_pred_results_df = merged_df[['GroupID', 'ms.value']]

# self-join on 'GroupID' column
paired_df = pd.merge(url_pred_results_df, url_pred_results_df, on='GroupID')
# filter out pairs that are the same 
paired_df = paired_df[paired_df['ms.value_x'] != paired_df['ms.value_y']]

paired_df.rename(columns={'ms.value_x': 'ms_uri_1', 'ms.value_y': 'ms_uri_2'}, inplace=True)
paired_df.drop(columns='GroupID', inplace=True)

paired_df.to_csv(output_csv_file, index=False)