from pyshacl import validate
import sys

filename = sys.argv[1]
print(filename)

try:
    with open(filename, 'r') as file:
        data_graph = file.read()
        # print(f"Contents of {filename}:\n{data_graph}")
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# data_graph = """
# @prefix gkbp:  <https://geokb.wikibase.cloud/wiki/Property:> .
# @prefix owl:   <http://www.w3.org/2002/07/owl#> .
# @prefix dcam:  <http://purl.org/dc/dcam/> .
# @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
# @prefix skos:  <http://www.w3.org/2004/02/skos/core#> .
# @prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
# @prefix geo:   <http://www.opengis.net/ont/geosparql#> .
# @prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
# @prefix sh:    <http://www.w3.org/ns/shacl#> .
# @prefix xml:   <http://www.w3.org/XML/1998/namespace> .
# @prefix dcterms: <http://purl.org/dc/terms/> .
# @prefix gkbi:  <https://geokb.wikibase.cloud/entity/> .
# @prefix mndr:  <https://minmod.isi.edu/resource/> .
# @prefix prov:  <http://www.w3.org/ns/prov#> .
# @prefix ex:  <http://www.w3.org/ns/prov#> .
#
# mndr:Q0 a mndr:MineralSite ;
#     mndr:id "Site103" ;
#     mndr:name "Balmat - Edwards District" ;
#     mndr:mineral_inventory  mndr:Q1, mndr:Q112, mndr:Q113, mndr:Q114;
#     mndr:location_info mndr:Q2 ;
#     mndr:deposit_type "https://minmod.isi.edu/resource/Q380"^^xsd:anyURI .
#
# mndr:Q1 a mndr:MineralInventory ;
#     mndr:id "Inv001" ;
#     mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI ;
#     mndr:category mndr:Indicated ;
#     mndr:ore mndr:Q6 ;
#     mndr:grade mndr:Q7 ;
#     mndr:cutoff_grade mndr:Q71 ;
#     mndr:contained_metal 112128.19 ;
#     mndr:reference mndr:Q8 ;
#     mndr:date "09-19-2017"^^xsd:date .
#
# mndr:Q112 a mndr:MineralInventory ;
#     mndr:id "Inv002" ;
#     mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI ;
#     mndr:category mndr:Indicated ;
#     mndr:ore mndr:Q611 ;
#     mndr:grade mndr:Q711 ;
#     mndr:cutoff_grade mndr:Q71 ;
#     mndr:contained_metal 174604.65 ;
#     mndr:reference mndr:Q8 ;
#     mndr:date "09-19-2017"^^xsd:date .
#
# mndr:Q113 a mndr:MineralInventory ;
#     mndr:id "Inv003" ;
#     mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI ;
#     mndr:category mndr:Measured, mndr:Indicated ;
#     mndr:ore mndr:Q622 ;
#     mndr:grade mndr:Q722 ;
#     mndr:cutoff_grade mndr:Q71 ;
#     mndr:contained_metal 286798.2 ;
#     mndr:reference mndr:Q8 ;
#     mndr:date "09-19-2017"^^xsd:date .
#
# mndr:Q114 a mndr:MineralInventory ;
#     mndr:id "Inv004" ;
#     mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI ;
#     mndr:category mndr:Inferred ;
#     mndr:ore mndr:Q633 ;
#     mndr:grade mndr:Q733 ;
#     mndr:cutoff_grade mndr:Q71 ;
#     mndr:contained_metal 304381.42 ;
#     mndr:reference mndr:Q8 ;
#     mndr:date "09-19-2017"^^xsd:date .
#
# mndr:Q2 a mndr:LocationInfo ;
#     mndr:location "POINT (-75.33292 44.28331)"^^geo:wktLiteral ;
#     mndr:location_source "MRDS_Zinc" ;
#     mndr:crs "NAD83" ;
#     mndr:location_source_record_id "22" ;
#     mndr:country "United States" .
#
# mndr:Q200 a mndr:Unit ;
#     mndr:value "tonnes".
#
# mndr:Q201 a mndr:Unit ;
#     mndr:value "percent".
#
# mndr:Q6 a mndr:Ore ;
#     mndr:ore_unit <https://minmod.isi.edu/resource/Q200> ;
#     mndr:ore_value 850100 .
#
# mndr:Q7 a mndr:Grade ;
#     mndr:grade_unit <https://minmod.isi.edu/resource/Q201> ;
#     mndr:grade_value 13.19 .
#
# mndr:Q71 a mndr:Grade ;
#     mndr:grade_unit <https://minmod.isi.edu/resource/Q201> ;
#     mndr:grade_value 6 .
#
#
#
# mndr:Q611 a mndr:Ore ;
#     mndr:ore_unit <https://minmod.isi.edu/resource/Q200> ;
#     mndr:ore_value 1307900 .
#
# mndr:Q711 a mndr:Grade ;
#     mndr:grade_unit <https://minmod.isi.edu/resource/Q201> ;
#     mndr:grade_value 13.35 .
#
#
#
#
#
# mndr:Q622 a mndr:Ore ;
#     mndr:ore_unit <https://minmod.isi.edu/resource/Q200> ;
#     mndr:ore_value 2158000 .
#
# mndr:Q722 a mndr:Grade ;
#     mndr:grade_unit <https://minmod.isi.edu/resource/Q201> ;
#     mndr:grade_value 13.29 .
#
#
#
#
# mndr:Q633 a mndr:Ore ;
#     mndr:ore_unit <https://minmod.isi.edu/resource/Q200> ;
#     mndr:ore_value 2276600 .
#
# mndr:Q733 a mndr:Grade ;
#     mndr:grade_unit <https://minmod.isi.edu/resource/Q201> ;
#     mndr:grade_value 13.37 .
#
#
#
# mndr:Q8 a mndr:Reference ;
#     mndr:id "Ref001" ;
#     mndr:document mndr:Q9 ;
#     mndr:page_info mndr:Q81 .
#
# mndr:Q81 a mndr:PageInfo ;
#     mndr:page 137 .
#
# mndr:Q9 a mndr:Document ;
#     mndr:title "NI 43-101 PRELIMINARY ECONOMIC ASSESSMENT TECHNICAL REPORT ON THE EMPIRE STATE MINES, GOUVERNEUR, NEW YORK, USA" .
#
# mndr:doi  owl:sameAs gkbp:P74 .
#
# mndr:uri  owl:sameAs gkbp:P136 .
#
# mndr:authors  owl:sameAs gkbp:P102 .
#
#
# mndr:Q10 a mndr:MappableCriteria ;
#     mndr:criteria "The mappable proxy for the source of MVT deposits is dolomitized carbonate platform sequences, particularly those deposited in arid belts.";
#     mndr:theoretical "N/A" ;
#     mndr:potential_dataset "N/A" ;
#     mndr:supporting_references mndr:Q11 .
#
# mndr:Q12 a mndr:Document ;
#     mndr:title "A Deposit Model for Mississippi Valley-Type Lead-Zinc Ores" .
#
# mndr:Q11 a mndr:Reference ;
#     mndr:page_info mndr:Q13 .
#
# mndr:Q13 a mndr:PageInfo ;
#     mndr:page 33 .
#
# mndr:Q14 a mndr:MappableCriteria ;
#     mndr:criteria "The paragraph suggests that extensional faults and dolomitization of limestone are mappable criteria that represent the pathway for the formation and localization of syn-diagenetic Zn-Pb deposits in the MVT deposit type.";
#     mndr:theoretical "N/A" ;
#     mndr:potential_dataset "N/A" ;
#     mndr:supporting_references mndr:Q15 .
#
# mndr:Q15 a mndr:Reference ;
#     mndr:id "SIR10-5070C" ;
#     mndr:document mndr:Q12 ;
#     mndr:page_info mndr:Q16 .
#
# mndr:Q16 a mndr:PageInfo ;
#     mndr:page 46 .
#
# mndr:Q17 a mndr:MappableCriteria ;
#     mndr:criteria "The mappable proxy for the trap of MVT deposits in this paragraph is the presence of pre-ore dissolution collapse features in carbonate platform sequences. These collapse features provide contrasting fluid transmissivity and are important sites for ore deposition and host-rock dissolution. Additionally, the presence of carbonate rocks overlying fractured or faulted crystalline basement rocks can also indicate the potential for ore formation through changes in pH and redox reactions.";
#     mndr:theoretical "N/A" ;
#     mndr:potential_dataset "N/A" ;
#     mndr:supporting_references mndr:Q18 .
#
# mndr:Q18 a mndr:Reference ;
#     mndr:id "SIR10-5070D" ;
#     mndr:document mndr:Q12 ;
#     mndr:page_info mndr:Q19 .
#
# mndr:Q19 a mndr:PageInfo ;
#     mndr:page 16 .
#
# mndr:Q20 a mndr:MappableCriteria ;
#     mndr:criteria  "The mappable proxy for the preservation of MVT deposits is the presence of carbonate host-rock, which provides buffering capacity for acid and results in circum-neutral pH drainage waters with lower concentrations of deposit-related metals compared to other deposit types.";
#     mndr:theoretical "N/A" ;
#     mndr:potential_dataset "N/A" ;
#     mndr:supporting_references mndr:Q21 .
#
# mndr:Q21 a mndr:Reference ;
#     mndr:id "SIR10-5070E" ;
#     mndr:document mndr:Q12 ;
#     mndr:page_info mndr:Q22 .
#
# mndr:Q22 a mndr:PageInfo ;
#     mndr:page 26 .
#
#
# mndr:Q23 a mndr:MineralSystem ;
#     mndr:deposit_type "https://minmod.isi.edu/resource/Q380"^^xsd:anyURI ;
#     mndr:source mndr:Q10;
#     mndr:trap mndr:Q17;
#     mndr:conduit mndr:Q14;
#     mndr:exhumation mndr:Q20.
#
#
#
# mndr:Q10101 a mndr:Grade;
# 	mndr:grade_value 10;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201> .
# mndr:Q10102 a mndr:Grade;
# 	mndr:grade_value 10;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q10103 a mndr:Grade;
# 	mndr:grade_value 10;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q10104 a mndr:Grade;
# 	mndr:grade_value 10;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q10105 a mndr:Grade;
# 	mndr:grade_value 9;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q10106 a mndr:Grade;
# 	mndr:grade_value 9;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q10107 a mndr:Grade;
# 	mndr:grade_value 9;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q10108 a mndr:Grade;
# 	mndr:grade_value 9;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q10109 a mndr:Grade;
# 	mndr:grade_value 8;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101010 a mndr:Grade;
# 	mndr:grade_value 8;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101011 a mndr:Grade;
# 	mndr:grade_value 8;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101012 a mndr:Grade;
# 	mndr:grade_value 8;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101013 a mndr:Grade;
# 	mndr:grade_value 7;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101014 a mndr:Grade;
# 	mndr:grade_value 7;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101015 a mndr:Grade;
# 	mndr:grade_value 7;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101016 a mndr:Grade;
# 	mndr:grade_value 7;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101017 a mndr:Grade;
# 	mndr:grade_value 6;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101018 a mndr:Grade;
# 	mndr:grade_value 6;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101019 a mndr:Grade;
# 	mndr:grade_value 6;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101020 a mndr:Grade;
# 	mndr:grade_value 6;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101021 a mndr:Grade;
# 	mndr:grade_value 5;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101022 a mndr:Grade;
# 	mndr:grade_value 5;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101023 a mndr:Grade;
# 	mndr:grade_value 5;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101024 a mndr:Grade;
# 	mndr:grade_value 5;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101025 a mndr:Grade;
# 	mndr:grade_value 4;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101026 a mndr:Grade;
# 	mndr:grade_value 4;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101027 a mndr:Grade;
# 	mndr:grade_value 4;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101028 a mndr:Grade;
# 	mndr:grade_value 4;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101029 a mndr:Grade;
# 	mndr:grade_value 3;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101030 a mndr:Grade;
# 	mndr:grade_value 3;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101031 a mndr:Grade;
# 	mndr:grade_value 3;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q101032 a mndr:Grade;
# 	mndr:grade_value 3;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q201>
# 	.
# mndr:Q10201 a mndr:Ore;
# 	mndr:ore_value 543000;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10202 a mndr:Ore;
# 	mndr:ore_value 840600;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10203 a mndr:Ore;
# 	mndr:ore_value 1383600;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10204 a mndr:Ore;
# 	mndr:ore_value 1499200;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10205 a mndr:Ore;
# 	mndr:ore_value 617500;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10206 a mndr:Ore;
# 	mndr:ore_value 962500;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10207 a mndr:Ore;
# 	mndr:ore_value 1580000;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10208 a mndr:Ore;
# 	mndr:ore_value 1772600;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10209 a mndr:Ore;
# 	mndr:ore_value 696100;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q102010 a mndr:Ore;
# 	mndr:ore_value 1080000;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q102011 a mndr:Ore;
# 	mndr:ore_value 1776100;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200> .
# mndr:Q102012 a mndr:Ore;
# 	mndr:ore_value 1970400;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200> .
#
# mndr:Q102013 a mndr:Ore;
# 	mndr:ore_value 770200;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200> .
# mndr:Q102014 a mndr:Ore;
# 	mndr:ore_value 1200500;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200> .
#
# mndr:Q102015 a mndr:Ore;
# 	mndr:ore_value 1970700;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q102016 a mndr:Ore;
# 	mndr:ore_value 2100600;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200> .
#
# mndr:Q102017 a mndr:Ore;
# 	mndr:ore_value 850100;
# 	mndr:ore_unit "https://minmod.isi.edu/resource/Q200"^^xsd:anyURI .
#
# mndr:Q102018 a mndr:Ore;
# 	mndr:ore_value 1307900;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200> .
#
# mndr:Q102019 a mndr:Ore;
# 	mndr:ore_value 2158000;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200> .
#
# mndr:Q102020 a mndr:Ore;
# 	mndr:ore_value 2276000;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200> .
#
# mndr:Q102021 a mndr:Ore;
# 	mndr:ore_value 932800;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200> .
#
# mndr:Q102022 a mndr:Ore;
# 	mndr:ore_value 1416700;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200> .
#
# mndr:Q102023 a mndr:Ore;
# 	mndr:ore_value 2349500;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q102024 a mndr:Ore;
# 	mndr:ore_value 2393400;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q102025 a mndr:Ore;
# 	mndr:ore_value 1004900;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q102026 a mndr:Ore;
# 	mndr:ore_value 1524400;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q102027 a mndr:Ore;
# 	mndr:ore_value 2529300;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q102028 a mndr:Ore;
# 	mndr:ore_value 2887100;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q102029 a mndr:Ore;
# 	mndr:ore_value 1074300;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q102030 a mndr:Ore;
# 	mndr:ore_value 1612400;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q102031 a mndr:Ore;
# 	mndr:ore_value 2686700;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q102032 a mndr:Ore;
# 	mndr:ore_value 2824300;
# 	mndr:ore_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10301 a mndr:Grade;
# 	mndr:grade_value 16.15;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10302 a mndr:Grade;
# 	mndr:grade_value 16.27;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10303 a mndr:Grade;
# 	mndr:grade_value 16.22;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10304 a mndr:Grade;
# 	mndr:grade_value 16.02;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10305 a mndr:Grade;
# 	mndr:grade_value 15.34;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10306 a mndr:Grade;
# 	mndr:grade_value 15.42;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10307 a mndr:Grade;
# 	mndr:grade_value 15.39;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10308 a mndr:Grade;
# 	mndr:grade_value 15.01;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10309 a mndr:Grade;
# 	mndr:grade_value 14.57;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103010 a mndr:Grade;
# 	mndr:grade_value 14.67;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103011 a mndr:Grade;
# 	mndr:grade_value 14.63;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103012 a mndr:Grade;
# 	mndr:grade_value 14.36;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103013 a mndr:Grade;
# 	mndr:grade_value 13.89;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103014 a mndr:Grade;
# 	mndr:grade_value 13.96;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103015 a mndr:Grade;
# 	mndr:grade_value 13.93;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103016 a mndr:Grade;
# 	mndr:grade_value 13.94;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103017 a mndr:Grade;
# 	mndr:grade_value 13.19;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103018 a mndr:Grade;
# 	mndr:grade_value 13.35;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103019 a mndr:Grade;
# 	mndr:grade_value 13.29;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103020 a mndr:Grade;
# 	mndr:grade_value 13.37;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103021 a mndr:Grade;
# 	mndr:grade_value 12.51;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103022 a mndr:Grade;
# 	mndr:grade_value 12.76;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103023 a mndr:Grade;
# 	mndr:grade_value 12.66;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103024 a mndr:Grade;
# 	mndr:grade_value 12.98;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103025 a mndr:Grade;
# 	mndr:grade_value 11.94;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103026 a mndr:Grade;
# 	mndr:grade_value 12.18;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103027 a mndr:Grade;
# 	mndr:grade_value 12.08;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103028 a mndr:Grade;
# 	mndr:grade_value 11.88;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103029 a mndr:Grade;
# 	mndr:grade_value 11.39;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103030 a mndr:Grade;
# 	mndr:grade_value 11.7;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103031 a mndr:Grade;
# 	mndr:grade_value 11.58;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q103032 a mndr:Grade;
# 	mndr:grade_value 11.6;
# 	mndr:grade_unit <https://minmod.isi.edu/resource/Q200>
# 	.
# mndr:Q10401 a mndr:MineralInventory;
# 	mndr:category mndr:Measured;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q10101;
# 	mndr:ore mndr:Q10201;
# 	mndr:grade mndr:Q10301;
# 	.
# mndr:Q10402 a mndr:MineralInventory;
# 	mndr:category mndr:Indicated;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q10102;
# 	mndr:ore mndr:Q10202;
# 	mndr:grade mndr:Q10302;
# 	.
# mndr:Q10404 a mndr:MineralInventory;
# 	mndr:category mndr:Inferred;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q10104;
# 	mndr:ore mndr:Q10204;
# 	mndr:grade mndr:Q10304;
# 	.
# mndr:Q10405 a mndr:MineralInventory;
# 	mndr:category mndr:Measured;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q10105;
# 	mndr:ore mndr:Q10205;
# 	mndr:grade mndr:Q10305;
# 	.
# mndr:Q10406 a mndr:MineralInventory;
# 	mndr:category mndr:Indicated;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q10106;
# 	mndr:ore mndr:Q10206;
# 	mndr:grade mndr:Q10306;
# 	.
# mndr:Q10408 a mndr:MineralInventory;
# 	mndr:category mndr:Inferred;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q10108;
# 	mndr:ore mndr:Q10208;
# 	mndr:grade mndr:Q10308;
# 	.
# mndr:Q10409 a mndr:MineralInventory;
# 	mndr:category mndr:Measured;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q10109;
# 	mndr:ore mndr:Q10209;
# 	mndr:grade mndr:Q10309;
# 	.
# mndr:Q104010 a mndr:MineralInventory;
# 	mndr:category mndr:Indicated;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101010;
# 	mndr:ore mndr:Q102010;
# 	mndr:grade mndr:Q103010;
# 	.
# mndr:Q104012 a mndr:MineralInventory;
# 	mndr:category mndr:Inferred;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101012;
# 	mndr:ore mndr:Q102012;
# 	mndr:grade mndr:Q103012;
# 	.
# mndr:Q104013 a mndr:MineralInventory;
# 	mndr:category mndr:Measured;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101013;
# 	mndr:ore mndr:Q102013;
# 	mndr:grade mndr:Q103013;
# 	.
# mndr:Q104014 a mndr:MineralInventory;
# 	mndr:category mndr:Indicated;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101014;
# 	mndr:ore mndr:Q102014;
# 	mndr:grade mndr:Q103014;
# 	.
# mndr:Q104016 a mndr:MineralInventory;
# 	mndr:category mndr:Inferred;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101016;
# 	mndr:ore mndr:Q102016;
# 	mndr:grade mndr:Q103016;
# 	.
# mndr:Q104017 a mndr:MineralInventory;
# 	mndr:category mndr:Measured;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101017;
# 	mndr:ore mndr:Q102017;
# 	mndr:grade mndr:Q103017;
# 	.
# mndr:Q104018 a mndr:MineralInventory;
# 	mndr:category mndr:Indicated;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101018;
# 	mndr:ore mndr:Q102018;
# 	mndr:grade mndr:Q103018;
# 	.
# mndr:Q104020 a mndr:MineralInventory;
# 	mndr:category mndr:Inferred;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101020;
# 	mndr:ore mndr:Q102020;
# 	mndr:grade mndr:Q103020;
# 	.
# mndr:Q104021 a mndr:MineralInventory;
# 	mndr:category mndr:Measured;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101021;
# 	mndr:ore mndr:Q102021;
# 	mndr:grade mndr:Q103021;
# 	.
# mndr:Q104022 a mndr:MineralInventory;
# 	mndr:category mndr:Indicated;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101022;
# 	mndr:ore mndr:Q102022;
# 	mndr:grade mndr:Q103022;
# 	.
# mndr:Q104024 a mndr:MineralInventory;
# 	mndr:category mndr:Inferred;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101024;
# 	mndr:ore mndr:Q102024;
# 	mndr:grade mndr:Q103024;
# 	.
# mndr:Q104025 a mndr:MineralInventory;
# 	mndr:category mndr:Measured;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101025;
# 	mndr:ore mndr:Q102025;
# 	mndr:grade mndr:Q103025;
# 	.
# mndr:Q104026 a mndr:MineralInventory;
# 	mndr:category mndr:Indicated;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101026;
# 	mndr:ore mndr:Q102026;
# 	mndr:grade mndr:Q103026;
# 	.
# mndr:Q104028 a mndr:MineralInventory;
# 	mndr:category mndr:Inferred;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101028;
# 	mndr:ore mndr:Q102028;
# 	mndr:grade mndr:Q103028;
# 	.
# mndr:Q104029 a mndr:MineralInventory;
# 	mndr:category mndr:Measured;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101029;
# 	mndr:ore mndr:Q102029;
# 	mndr:grade mndr:Q103029;
# 	.
# mndr:Q104030 a mndr:MineralInventory;
# 	mndr:category mndr:Indicated;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101030;
# 	mndr:ore mndr:Q102030;
# 	mndr:grade mndr:Q103030;
# 	.
# mndr:Q104032 a mndr:MineralInventory;
# 	mndr:category mndr:Inferred;
# 	mndr:commodity "https://minmod.isi.edu/resource/Q589"^^xsd:anyURI;
# 	mndr:cutoff_grade mndr:Q101032;
# 	mndr:ore mndr:Q102032;
# 	mndr:grade mndr:Q103032;
# 	.
#
# mndr:Measured a mndr:ResourceReserveCategory .
#
# mndr:Indicated a mndr:ResourceReserveCategory .
#
# mndr:Inferred a mndr:ResourceReserveCategory .
#
# mndr:Probable a mndr:ResourceReserveCategory .
#
# mndr:Proven a mndr:ResourceReserveCategory .
#
# mndr:Extracted a mndr:ResourceReserveCategory .
#
# mndr:OriginalResource a mndr:ResourceReserveCategory .
#
# mndr:CumulativeExtracted a mndr:ResourceReserveCategory .
#
# mndr:Q0 mndr:mineral_inventory mndr:Q10401, mndr:Q10402, mndr:Q10404, mndr:Q10405, mndr:Q10406, mndr:Q10408, mndr:Q10409, mndr:Q104010, mndr:Q104012, mndr:Q104013, mndr:Q104014, mndr:Q104016, mndr:Q104017, mndr:Q104018, mndr:Q104020, mndr:Q104021, mndr:Q104022, mndr:Q104024, mndr:Q104025, mndr:Q104026, mndr:Q104028, mndr:Q104029, mndr:Q104030, mndr:Q104032 .
# """

resources = """


mndr:Measured a mndr:ResourceReserveCategory .

mndr:Indicated a mndr:ResourceReserveCategory .

mndr:Inferred a mndr:ResourceReserveCategory .

mndr:Probable a mndr:ResourceReserveCategory .

mndr:Proven a mndr:ResourceReserveCategory .

mndr:Extracted a mndr:ResourceReserveCategory .

mndr:OriginalResource a mndr:ResourceReserveCategory .

mndr:CumulativeExtracted a mndr:ResourceReserveCategory .

"""

data_graph = data_graph + resources


shapes_graph = """
@prefix gkbp:  <https://geokb.wikibase.cloud/wiki/Property:> .
@prefix owl:   <http://www.w3.org/2002/07/owl#> .
@prefix dcam:  <http://purl.org/dc/dcam/> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:  <http://www.w3.org/2004/02/skos/core#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
@prefix geo:   <http://www.opengis.net/ont/geosparql#> .
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix sh:    <http://www.w3.org/ns/shacl#> .
@prefix xml:   <http://www.w3.org/XML/1998/namespace> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix gkbi:  <https://geokb.wikibase.cloud/entity/> .
@prefix mndr:  <https://minmod.isi.edu/resource/> .
@prefix prov:  <http://www.w3.org/ns/prov#> .
@prefix ex:  <http://www.w3.org/ns/prov#> .

mndr:MappableCriteria-https___minmod.isi.edu_resource_criteria
        a        sh:PropertyShape ;
        sh:path  mndr:criteria .

mndr:Ore-https___minmod.isi.edu_resource_ore_value
        a            sh:PropertyShape ;
        sh:or ( [ sh:datatype xsd:decimal ] [ sh:datatype xsd:integer ] ) ;
        sh:path      mndr:ore_value .

mndr:MineralInventory-https___minmod.isi.edu_resource_ore
        a         sh:PropertyShape ;
        sh:class  mndr:Ore ;
        sh:path   mndr:ore .

mndr:MineralSite  a  sh:NodeShape ;
        sh:property  mndr:MineralSite-https___minmod.isi.edu_resource_id , mndr:MineralSite-https___minmod.isi.edu_resource_deposit_type , mndr:MineralSite-https___minmod.isi.edu_resource_location_info , mndr:MineralSite-https___minmod.isi.edu_resource_same_as , mndr:MineralSite-https___minmod.isi.edu_resource_mineral_inventory , mndr:MineralSite-https___minmod.isi.edu_resource_name , mndr:MineralSite-https___minmod.isi.edu_resource_geology_info .

mndr:Grade  a        sh:NodeShape;
        sh:property  mndr:Grade-https___minmod.isi.edu_resource_grade_unit , mndr:Grade-https___minmod.isi.edu_resource_grade_value .

mndr:MineralSystem-https___minmod.isi.edu_resource_deposit_type
        a            sh:PropertyShape ;
        sh:datatype  xsd:anyURI ;
        sh:path      mndr:deposit_type .

mndr:BoundingBox-https___minmod.isi.edu_resource_x_max
        a         sh:PropertyShape ;
        sh:datatype  xsd:decimal ;
        sh:path   mndr:x_max .

mndr:MineralSite-https___minmod.isi.edu_resource_name
        a        sh:PropertyShape ;
        sh:path  mndr:name .

mndr:Document-https___minmod.isi.edu_resource_month
        a        sh:PropertyShape ;
        sh:path  mndr:month .

mndr:GeologyInfo-https___minmod.isi.edu_resource_description
        a        sh:PropertyShape ;
        sh:path  mndr:description .

mndr:Document-https___minmod.isi.edu_resource_id
        a        sh:PropertyShape ;
        sh:path  mndr:id .

mndr:MineralSite-https___minmod.isi.edu_resource_same_as
        a        sh:PropertyShape ;
        sh:path  mndr:same_as .

mndr:MineralSystem-https___minmod.isi.edu_resource_exhumation
        a         sh:PropertyShape ;
        sh:class  mndr:MappableCriteria ;
        sh:path   mndr:exhumation .

mndr:LocationInfo-https___minmod.isi.edu_resource_location_source
        a        sh:PropertyShape ;
        sh:path  mndr:location_source .

mndr:Document-https___minmod.isi.edu_resource_journal
        a        sh:PropertyShape ;
        sh:path  mndr:journal .

mndr:MineralInventory-https___minmod.isi.edu_resource_commodity
        a            sh:PropertyShape ;
        sh:datatype  xsd:anyURI ;
        sh:path      mndr:commodity .

mndr:BoundingBox-https___minmod.isi.edu_resource_y_max
        a         sh:PropertyShape ;
        sh:datatype  xsd:decimal ;
        sh:path   mndr:y_max .

mndr:MineralInventory-https___minmod.isi.edu_resource_date
        a            sh:PropertyShape ;
        sh:datatype  xsd:date ;
        sh:path      mndr:date .

mndr:BoundingBox-https___minmod.isi.edu_resource_x_min
        a         sh:PropertyShape ;
        sh:datatype  xsd:decimal ;
        sh:path   mndr:x_min .

mndr:DepositType-https___minmod.isi.edu_resource_id
        a        sh:PropertyShape ;
        sh:path  mndr:id .

mndr:ResourceReserveCategory  a sh:NodeShape ;
    sh:class mndr:ResourceReserveCategory . 

mndr:Inferred  a  sh:NodeShape ;
     rdfs:subClassOf mndr:ResourceReserveCategory .
         
         
mndr:Indicated  a sh:NodeShape ;
     rdfs:subClassOf mndr:ResourceReserveCategory .
     
mndr:Measured  a sh:NodeShape ;
     sh:subClassOf mndr:ResourceReserveCategory .
     

mndr:category
        a         sh:PropertyShape ;
        sh:class  mndr:ResourceReserveCategory ;
        sh:path   mndr:category .

mndr:GeologyInfo-https___minmod.isi.edu_resource_comments
        a        sh:PropertyShape ;
        sh:path  mndr:comments .

mndr:MineralInventory-https___minmod.isi.edu_resource_cutoff_grade
        a         sh:PropertyShape ;
        sh:class  mndr:Grade ;
        sh:path   mndr:cutoff_grade .

mndr:MineralSystem-https___minmod.isi.edu_resource_dispersion
        a         sh:PropertyShape ;
        sh:class  mndr:MappableCriteria ;
        sh:path   mndr:dispersion .

mndr:MineralSite-https___minmod.isi.edu_resource_location_info
        a         sh:PropertyShape ;
        sh:class  mndr:LocationInfo ;
        sh:path   mndr:location_info .

mndr:MineralSystem-https___minmod.isi.edu_resource_conduit
        a         sh:PropertyShape ;
        sh:class  mndr:MappableCriteria ;
        sh:path   mndr:conduit .

mndr:GeologyInfo-https___minmod.isi.edu_resource_environment
        a        sh:PropertyShape ;
        sh:path  mndr:environment .

mndr:BoundingBox-https___minmod.isi.edu_resource_y_min
        a         sh:PropertyShape ;
        sh:datatype  xsd:decimal ;
        sh:path   mndr:y_min .

mndr:GeologyInfo-https___minmod.isi.edu_resource_age
        a        sh:PropertyShape ;
        sh:path  mndr:age .

mndr:Ore  a          sh:NodeShape;
       sh:property [
                		sh:path mndr:ore_unit ;
                		sh:datatype xsd:anyURI ;
                	] ;
        sh:property [
                		sh:path mndr:ore_value ;
                		sh:or ( [ sh:datatype xsd:decimal ] [ sh:datatype xsd:integer ] ) ;
                	] .
                	
mndr:MineralSystem  a sh:NodeShape ;
        sh:property  mndr:MineralSystem-https___minmod.isi.edu_resource_throttle , mndr:MineralSystem-https___minmod.isi.edu_resource_trigger , mndr:MineralSystem-https___minmod.isi.edu_resource_conduit , mndr:MineralSystem-https___minmod.isi.edu_resource_source_metal , mndr:MineralSystem-https___minmod.isi.edu_resource_direct_detection , mndr:MineralSystem-https___minmod.isi.edu_resource_source_other , mndr:MineralSystem-https___minmod.isi.edu_resource_dispersion , mndr:MineralSystem-https___minmod.isi.edu_resource_exhumation , mndr:MineralSystem-https___minmod.isi.edu_resource_driver , mndr:MineralSystem-https___minmod.isi.edu_resource_source_fluid , mndr:MineralSystem-https___minmod.isi.edu_resource_deposit_type , mndr:MineralSystem-https___minmod.isi.edu_resource_trap , mndr:MineralSystem-https___minmod.isi.edu_resource_source_ligand .

mndr:Document-https___minmod.isi.edu_resource_authors
        a        sh:PropertyShape ;
        sh:path  mndr:authors .


mndr:page_info
        a         sh:PropertyShape ;
        sh:targetClass mndr:PageInfo;
        sh:class  mndr:PageInfo ;
        sh:path   mndr:page_info .


mndr:PageInfo a   sh:NodeShape ;
sh:targetClass mndr:PageInfo;
        sh:property [
                		sh:path mndr:page ;
                		sh:datatype xsd:integer ;
                	] .

#mndr:Reference  a    sh:NodeShape;
#sh:targetClass mndr:Reference;
 #       sh:property  mndr:page_info.

mndr:Q11 a mndr:Reference ;
    mndr:page_info mndr:Q13 .

mndr:Q13 a mndr:PageInfo ;
    mndr:page 33 .



# Define a shape for instances of the class ex:Person
ex:PersonShape
  a sh:NodeShape ;
  sh:property [
    sh:path ex:hasChild ;  # Property path for the hasChild property
    sh:class ex:Person ;   # Expected class for the hasChild property
    sh:severity sh:Violation ;
  ] .

# Data with instances of classes
ex:John
  a ex:Person ;
  ex:hasChild ex:Fido .  # Mistakenly associating hasChild property with an instance of class ex:Animal

ex:Fido
  a ex:Animal .


# mndr:page
        # a         sh:PropertyShape ;
        # sh:datatype  xsd:integer ;
        # sh:path   mndr:page .

mndr:MineralSystem-https___minmod.isi.edu_resource_trap
        a         sh:PropertyShape ;
        sh:class  mndr:MappableCriteria ;
        sh:path   mndr:trap .

mndr:LocationInfo-https___minmod.isi.edu_resource_location
        a         sh:PropertyShape ;
        sh:datatype  geo:wktLiteral ;
        sh:path   mndr:location .

mndr:LocationInfo  a  sh:NodeShape ;
        sh:property  mndr:LocationInfo-https___minmod.isi.edu_resource_state_or_province , mndr:LocationInfo-https___minmod.isi.edu_resource_crs , mndr:LocationInfo-https___minmod.isi.edu_resource_location , mndr:LocationInfo-https___minmod.isi.edu_resource_location_source_record_id , mndr:LocationInfo-https___minmod.isi.edu_resource_location_source , mndr:LocationInfo-https___minmod.isi.edu_resource_country .

mndr:MineralInventory-https___minmod.isi.edu_resource_zone
        a        sh:PropertyShape ;
        sh:path  mndr:zone .

mndr:Document-https___minmod.isi.edu_resource_issue
        a        sh:PropertyShape ;
        sh:path  mndr:issue .

mndr:Document-https___minmod.isi.edu_resource_title
        a        sh:PropertyShape ;
        sh:path  mndr:title .

mndr:Commodity-https___minmod.isi.edu_resource_id
        a        sh:PropertyShape ;
        sh:path  mndr:id .

mndr:Document-https___minmod.isi.edu_resource_year
        a        sh:PropertyShape ;
        sh:path  mndr:year .

mndr:MineralInventory-https___minmod.isi.edu_resource_contained_metal
        a         sh:PropertyShape ;
        sh:datatype  xsd:decimal ;
        sh:path   mndr:contained_metal .

mndr:GeologyInfo-https___minmod.isi.edu_resource_unit_name
        a        sh:PropertyShape ;
        sh:path  mndr:unit_name .

mndr:Document-https___minmod.isi.edu_resource_doi
        a        sh:PropertyShape ;
        sh:path  mndr:doi .

mndr:GeologyInfo-https___minmod.isi.edu_resource_process
        a        sh:PropertyShape ;
        sh:path  mndr:process .

mndr:LocationInfo-https___minmod.isi.edu_resource_crs
        a        sh:PropertyShape ;
        sh:path  mndr:crs .

mndr:Document-https___minmod.isi.edu_resource_volume
        a        sh:PropertyShape ;
        sh:path  mndr:volume .

mndr:DepositType  a  sh:NodeShape  ;
        sh:property  mndr:DepositType-https___minmod.isi.edu_resource_name , mndr:DepositType-https___minmod.isi.edu_resource_id .

mndr:MineralInventory-https___minmod.isi.edu_resource_grade
        a         sh:PropertyShape ;
        sh:class  mndr:Grade ;
        sh:path   mndr:grade .

mndr:MineralSite-https___minmod.isi.edu_resource_mineral_inventory
        a         sh:PropertyShape ;
        sh:class  mndr:MineralInventory ;
        sh:path   mndr:mineral_inventory .

mndr:Document-https___minmod.isi.edu_resource_uri
        a        sh:PropertyShape ;
        sh:path  mndr:uri .

mndr:MineralInventory-https___minmod.isi.edu_resource_id
        a        sh:PropertyShape ;
        sh:path  mndr:id .

mndr:GeologyInfo-https___minmod.isi.edu_resource_lithology
        a        sh:PropertyShape ;
        sh:path  mndr:lithology .

mndr:LocationInfo-https___minmod.isi.edu_resource_country
        a        sh:PropertyShape ;
        sh:path  mndr:country .

mndr:MineralInventory
        a            sh:NodeShape ;
        sh:property  mndr:MineralInventory-https___minmod.isi.edu_resource_grade , mndr:MineralInventory-https___minmod.isi.edu_resource_contained_metal , mndr:MineralInventory-https___minmod.isi.edu_resource_cutoff_grade , mndr:MineralInventory-https___minmod.isi.edu_resource_reference , mndr:MineralInventory-https___minmod.isi.edu_resource_ore , mndr:MineralInventory-https___minmod.isi.edu_resource_zone , mndr:category , mndr:MineralInventory-https___minmod.isi.edu_resource_date , mndr:MineralInventory-https___minmod.isi.edu_resource_id , mndr:MineralInventory-https___minmod.isi.edu_resource_commodity .

mndr:LocationInfo-https___minmod.isi.edu_resource_state_or_province
        a        sh:PropertyShape ;
        sh:path  mndr:state_or_province .

mndr:Commodity-https___minmod.isi.edu_resource_name
        a        sh:PropertyShape ;
        sh:path  mndr:name .

mndr:MineralSystem-https___minmod.isi.edu_resource_driver
        a         sh:PropertyShape ;
        sh:class  mndr:MappableCriteria ;
        sh:path   mndr:driver .

mndr:MineralSite-https___minmod.isi.edu_resource_deposit_type
        a            sh:PropertyShape ;
        sh:datatype  xsd:anyURI ;
        sh:path      mndr:deposit_type .

mndr:MineralSystem-https___minmod.isi.edu_resource_throttle
        a         sh:PropertyShape ;
        sh:class  mndr:MappableCriteria ;
        sh:path   mndr:throttle .

mndr:Document-https___minmod.isi.edu_resource_description
        a        sh:PropertyShape ;
        sh:path  mndr:description .

mndr:MappableCriteria-https___minmod.isi.edu_resource_potential_dataset
        a        sh:PropertyShape ;
        sh:path  mndr:potential_dataset .

mndr:MappableCriteria-https___minmod.isi.edu_resource_supporting_references
        a        sh:PropertyShape ;
        sh:path  mndr:supporting_references .

mndr:BoundingBox  a  sh:NodeShape;
        sh:property  mndr:BoundingBox-https___minmod.isi.edu_resource_x_min , mndr:BoundingBox-https___minmod.isi.edu_resource_y_min , mndr:BoundingBox-https___minmod.isi.edu_resource_x_max , mndr:BoundingBox-https___minmod.isi.edu_resource_y_max .

mndr:MineralSystem-https___minmod.isi.edu_resource_source_fluid
        a         sh:PropertyShape ;
        sh:class  mndr:MappableCriteria ;
        sh:path   mndr:source_fluid .

mndr:Reference-https___minmod.isi.edu_resource_id
        a        sh:PropertyShape ;
        sh:path  mndr:id .

mndr:Ore-https___minmod.isi.edu_resource_ore_unit
        a         sh:PropertyShape ;
        sh:datatype  xsd:anyURI ;
        sh:path   mndr:ore_unit .

mndr:Commodity  a    sh:NodeShape ;
        sh:property  mndr:Commodity-https___minmod.isi.edu_resource_name , mndr:Commodity-https___minmod.isi.edu_resource_id .

mndr:MineralSystem-https___minmod.isi.edu_resource_source_ligand
        a         sh:PropertyShape ;
        sh:class  mndr:MappableCriteria ;
        sh:path   mndr:source_ligand .

mndr:Reference  a    sh:NodeShape ;
        sh:property  mndr:page_info , mndr:Reference-https___minmod.isi.edu_resource_id , mndr:Reference-https___minmod.isi.edu_resource_page .

mndr:MappableCriteria-https___minmod.isi.edu_resource_theoretical
        a        sh:PropertyShape ;
        sh:path  mndr:theoretical .

mndr:DepositType-https___minmod.isi.edu_resource_name
        a        sh:PropertyShape ;
        sh:path  mndr:name .

mndr:GeologyInfo  a sh:NodeShape ;
        sh:property  mndr:GeologyInfo-https___minmod.isi.edu_resource_comments , mndr:GeologyInfo-https___minmod.isi.edu_resource_environment , mndr:GeologyInfo-https___minmod.isi.edu_resource_unit_name , mndr:GeologyInfo-https___minmod.isi.edu_resource_age , mndr:GeologyInfo-https___minmod.isi.edu_resource_process , mndr:GeologyInfo-https___minmod.isi.edu_resource_description , mndr:GeologyInfo-https___minmod.isi.edu_resource_lithology .

mndr:Document  a     sh:NodeShape ;
        sh:property  mndr:Document-https___minmod.isi.edu_resource_title , mndr:Document-https___minmod.isi.edu_resource_id , mndr:Document-https___minmod.isi.edu_resource_issue , mndr:Document-https___minmod.isi.edu_resource_uri , mndr:Document-https___minmod.isi.edu_resource_authors , mndr:Document-https___minmod.isi.edu_resource_description , mndr:Document-https___minmod.isi.edu_resource_doi , mndr:Document-https___minmod.isi.edu_resource_journal , mndr:Document-https___minmod.isi.edu_resource_volume , mndr:Document-https___minmod.isi.edu_resource_year , mndr:Document-https___minmod.isi.edu_resource_month .

mndr:Document  a     sh:NodeShape  ;
        sh:property [
                		sh:path mndr:title ;
                		sh:datatype xsd:string ;
                	] .

mndr:MineralSystem-https___minmod.isi.edu_resource_source_metal
        a         sh:PropertyShape ;
        sh:class  mndr:MappableCriteria ;
        sh:path   mndr:source_metal .

mndr:LocationInfo-https___minmod.isi.edu_resource_location_source_record_id
        a        sh:PropertyShape ;
        sh:path  mndr:location_source_record_id .

mndr:MineralSite-https___minmod.isi.edu_resource_id
        a        sh:PropertyShape ;
        sh:path  mndr:id .

mndr:MappableCriteria
        a            sh:NodeShape ;
        sh:property  mndr:MappableCriteria-https___minmod.isi.edu_resource_supporting_references , mndr:MappableCriteria-https___minmod.isi.edu_resource_theoretical , mndr:MappableCriteria-https___minmod.isi.edu_resource_criteria , mndr:MappableCriteria-https___minmod.isi.edu_resource_potential_dataset .

mndr:MineralSite-https___minmod.isi.edu_resource_geology_info
        a         sh:PropertyShape ;
        sh:class  mndr:GeologyInfo ;
        sh:path   mndr:geology_info .

mndr:Grade-https___minmod.isi.edu_resource_grade_unit
        a         sh:PropertyShape ;
        sh:datatype  xsd:anyURI ;
        sh:path   mndr:grade_unit .

mndr:MineralInventory-https___minmod.isi.edu_resource_reference
        a         sh:PropertyShape ;
        sh:class  mndr:Reference ;
        sh:path   mndr:reference .

mndr:MineralSystem-https___minmod.isi.edu_resource_source_other
        a         sh:PropertyShape ;
        sh:class  mndr:MappableCriteria ;
        sh:path   mndr:source_other .

mndr:MineralSystem-https___minmod.isi.edu_resource_direct_detection
        a         sh:PropertyShape ;
        sh:class  mndr:MappableCriteria ;
        sh:path   mndr:direct_detection .

mndr:MineralSystem-https___minmod.isi.edu_resource_trigger
        a         sh:PropertyShape ;
        sh:class  mndr:MappableCriteria ;
        sh:path   mndr:trigger .

mndr:Reference-https___minmod.isi.edu_resource_page
        a        sh:PropertyShape ;
        sh:path  mndr:page .

mndr:Grade-https___minmod.isi.edu_resource_grade_value
        a         sh:PropertyShape ;
        sh:or ( [ sh:datatype xsd:decimal ] [ sh:datatype xsd:integer ] ) ;
        sh:path   mndr:grade_value .

"""
result = validate(data_graph, shacl_graph=shapes_graph, inference='rdfs', serialize_report_graph=True)

# Check the results
conforms, a, b = result
if not conforms:
    print("Validation does not conform. There are violations.")
    print(b)
else:
    print('This is fine')