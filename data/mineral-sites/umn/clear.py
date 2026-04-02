import json
import os

for i in os.listdir("./mrdata_mrds"):
    input_json = os.path.join("./mrdata_mrds", i)
    output_json = input_json

    dep_ids_text = """
    10122077
    10243704
    10192132
    10219651
    10267662
    10122520
    10243207
    10268147
    10143828
    10170395
    10146250
    10254470
    10181270
    10185010
    10265072
    10146736
    10298975
    10223863
    10181288
    10195120
    10195423
    10264747
    10265343
    10178244
    10266247
    10170551
    10208860
    10243156
    10126767
    10268094
    10266708
    10250945
    10168857
    10129890
    10243044
    10240957
    10122301
    10168135
    10193495
    10138664
    10195450
    10122475
    10281629
    10289247
    10219561
    10144218
    10184653
    10122296
    10280185
    10257779
    10219607
    10215722
    10268275
    10122019
    10191597
    10145991
    10178671
    10257900
    10160671
    10119023
    10122565
    10182920
    10243727
    10284005
    10146138
    10170365
    10195454
    10168245
    10194792
    10122286
    10281981
    10219595
    10200764
    10170921
    10265775
    10171279
    10159723
    10233509
    10259285
    10283015
    10265191
    10257901
    10162119
    10243597
    10281755
    10192117
    10173427
    10191836
    10195017
    10118979
    10292248
    10200140
    10118999
    10216001
    10291957
    10118836
    10171011
    10171016
    10233262
    10304195
    10146607
    10289938
    10268035
    10233074
    10119938
    10280220
    10146463
    10142833
    10201748
    10156790
    10291922
    10245135
    10122463
    10284070
    10126574
    10169064
    10146446
    10140183
    10136316
    10211505
    10146591
    10170742
    10227392
    10219658
    10119453
    10168555
    10219592
    10283840
    10170426
    10113433
    10243749
    10243757
    10233145
    10243724
    10160653
    10170983
    10194871
    10118737
    10121884
    10195044
    10292536
    10119148
    10143361
    10195538
    10292453
    10292366
    10178807
    10202152
    10111926
    10203466
    10243143
    10275081
    10218884
    10219226
    10255860
    10289174
    10142838
    10267612
    10192278
    10111857
    10153190
    10161331
    10170464
    10289094
    10136338
    10218964
    10300232
    10268081
    10191796
    10137326
    10303516
    10281984
    10219107
    10122579
    10216324
    10257364
    10284202
    10215971
    10268319
    10289097
    10195345
    10142835
    10216990
    10274934
    10122099
    10195025
    10203995
    10146304
    10292301
    10254118
    10195492
    10274357
    10180398
    10268188
    10135152
    10170725
    10267959
    10279152
    10185686
    10240822
    10268287
    10292048
    10209072
    10302519
    10243163
    10169984
    10216043
    10219422
    10219408
    10119370
    10191651
    10152462
    10264424
    10209385
    10283424
    """

    commods = "FLanthanum; Praseodymium; Samarium; Gadolinium; Thulium; Holmium; Cerium; Europium; Ytterbium; Erbium; Yttrium; Neodymium; Terbium; Dysprosium; Lutetium"

    dep_ids = {line.strip() for line in dep_ids_text.splitlines() if line.strip()}
    target_commodities = {c.strip() for c in commods.split(";") if c.strip()}

    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    removed_count = 0
    changed_record_ids = []

    for record in data:
        record_id = str(record.get("record_id", "")).strip()

        if record_id not in dep_ids:
            continue

        mineral_inventory = record.get("mineral_inventory")
        if not isinstance(mineral_inventory, list):
            continue

        original_len = len(mineral_inventory)

        filtered_inventory = []
        for item in mineral_inventory:
            observed_name = (
                item.get("commodity", {}).get("observed_name")
                if isinstance(item, dict) else None
            )

            if observed_name in target_commodities:
                removed_count += 1
                continue

            filtered_inventory.append(item)

        if len(filtered_inventory) != original_len:
            changed_record_ids.append(record_id)

        if filtered_inventory:
            record["mineral_inventory"] = filtered_inventory
        else:
            record.pop("mineral_inventory", None)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Done. Removed {removed_count} mineral_inventory entries.")
    print(f"Changed {len(changed_record_ids)} records.")