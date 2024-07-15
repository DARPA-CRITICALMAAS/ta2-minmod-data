# MinMod Knowledge Graph

This repository contains the datasets used to create the mineral site knowledge graph (KG), and some examples on how to fetch & manipulate the data in the KG. The KG integrates heterogeneous data sources including mineral site reports (National Instrument 43-101), scholarly articles, geo databases, and structured tables to provide a rich, queryable graph of mineral site information.

## Repository Structure

- `/data` (see designated [README](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/tree/main/data#readme)): This directory contains all the raw data used to build the MinMod knowledge graph.
  - Under `data`, `json` files within the folders `umn`, `inferlink`, `sri`, and `usc` are semantically modeled to materialize the data from the respective sources.
  <!-- - `/sandbox` (see designated [README](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/tree/main/sandbox#readme)): This directory holds the "sandbox", a `jupyter notebook` with a collection of example `SPARQL` queries & `python` code to manipulate the KG data & to build **Grade & Tonnage models** & interactively navigate the results! -->
- `/containers` (see designated [README](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/tree/main/containers#readme)): This directory contains necessary `Dockerfile`, code & scripts to build the Docker image to generate the TA2 outputs (`csv` files) from the **live** MinMod KG using queries.
<!-- - `/scripts`: This directory contains scripts used for internal use -->

## Schema

The data in this knowledge graph adhere to this [schema](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-kg/tree/main/schema/README.md).

## Deployment

The final `RDF` data (triples) are deployed & can be queried directly from our online & public `SPARQL` endpoint: [SPARQL Endpoint](https://minmod.isi.edu/sparql). You can also explore the data via our [Mineral Data Browser](https://minmod.isi.edu/).
