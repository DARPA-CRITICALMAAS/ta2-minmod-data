from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

import pandas as pd
from mendeleev import element

"""Helper to calculate the conversion factor between material form & commodity

Requirements: need mendeleev package (https://pypi.org/project/mendeleev/)
"""


def parse(chemical_compound: str):
    cc = chemical_compound
    n = len(chemical_compound)
    i = 0
    split_cc = []
    while i < n:
        # read element
        j = i
        if cc[j].isdigit():
            while j < n and cc[j].isdigit():
                j += 1
            split_cc.append(int(cc[i:j]))
            i = j
        else:
            assert cc[j].isupper()
            j += 1
            while j < n and cc[j].islower():
                j += 1
            if len(split_cc) > 0 and not isinstance(split_cc[-1], int):
                split_cc.append(1)
            split_cc.append(cc[i:j])
            i = j

    assert len(split_cc) > 0 and isinstance(split_cc[0], str)
    if not isinstance(split_cc[-1], int):
        split_cc.append(1)
    assert len(split_cc) % 2 == 0
    out = defaultdict(int)
    for i in range(0, len(split_cc), 2):
        out[split_cc[i]] += split_cc[i + 1]
    return dict(out)


def convert(source: str | dict[str, int], target: str | dict[str, int]):
    if isinstance(source, str):
        source = parse(source)
    if isinstance(target, str):
        target = parse(target)
    print("convert", source, "to", target)
    target_weight = sum(element(e).atomic_weight * n for e, n in target.items())
    source_weight = sum(element(e).atomic_weight * n for e, n in source.items())

    return print("factor", target_weight / source_weight)


def material_to_commodity(material: str | dict[str, int], commodity: str):
    if isinstance(material, str):
        material = parse(material)

    print("how much", commodity, "is in", material)
    target = {commodity: material[commodity]}
    # explain
    # for com in [material, target]:
    #     for e, n in com.items():
    #         print(
    #             "\t",
    #             str(element(e)),
    #             ":",
    #             element(e).atomic_weight,
    #             "x",
    #             n,
    #             "=",
    #             element(e).atomic_weight * n,
    #         )
    target_weight = sum(element(e).atomic_weight * n for e, n in target.items())
    source_weight = sum(element(e).atomic_weight * n for e, n in material.items())
    factor = target_weight / source_weight
    print("factor", factor)
    return factor


df = pd.read_csv(Path(__file__).parent / "material_form.csv")
for ri, row in df.iterrows():
    print(row["formula"], row["commodity"])
    factor = material_to_commodity(row["formula"], row["commodity"])
    df.at[ri, "conversion"] = factor
df.to_csv(Path(__file__).parent / "material_form.csv", index=False)
