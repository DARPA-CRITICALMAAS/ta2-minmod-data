# MinMod Knowledge Graph

This repository contains the datasets used to create the mineral site knowledge graph. The knowledge graph integrates heterogeneous data sources including scholarly articles, geolocation databases, and structured tables to provide a rich, queryable graph of mineral site information.

## Repository Structure

- `/data` (see designated [README](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/tree/main/data#readme)): This directory contains all the raw data used to build the MinMod knowledge graph.
  - Under data umn, inferlink and usc folder contain the data from respective sources
- `/sandbox` (see designated [README](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/tree/main/sandbox#readme)): This directory holds the sandbox, a collection of example queries & code to manipulate the KG data & build **Grade & Tonnage models**!

## Schema

The data in this knowledge graph adhere to this [schema](https://github.com/DARPA-CRITICALMAAS/schemas/blob/main/ta2/README.md).

## Deployment

The final RDF data (triples) are deployed & can be queried at our online SPARQL endpoint: [SPARQL Endpoint](https://minmod.isi.edu/sparql). You can also explore the data via our [Mineral Data Browser](https://minmod.isi.edu/).