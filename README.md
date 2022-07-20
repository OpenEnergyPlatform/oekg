
# Open Energy Knowledge Graph (OEKG) 

**Disclaimer:** This repository is currently under development.

This repository aims at providing some guidelines for energy experts on how to make an RDF document. RDF is a standard for exchanging data. If you want to learn about the RDF standard, please check out [this page](https://www.w3.org/RDF/) for more details. The Open Energy Knowledge Graph (OEKG) is based on the RDF standard and we use the [Turtle](https://www.w3.org/TR/turtle/) format for storing its facts. Fundamentally, we use the [OEO ontology](https://github.com/OpenEnergyPlatform/ontology) as the schema for our knowledge graph. It means, the OEKG is under development according to the OEO conceptualization. [This post](https://github.com/OpenEnergyPlatform/oekg/issues/7) shows the latest version of the OEKG template. As the OEO evolves, this template may change accordingly. 


We are actively creating RDF graphs from energy study reports. For example, [this report](https://www.oeko.de/publikationen/p-details/klimaschutzszenario-2050-2-endbericht) contains information about the energy scenarios, spatial regions, sectors, and the models used in a study. Instead of conveying these terms in a natural language, we aim at expressing these concepts and their relations in an RDF graph according to the OEO conceptualizations. For this reason, we use some intermediate data structures called [placeholders](https://github.com/OpenEnergyPlatform/oekg/tree/main/Place-holders)  which are  .JSON files with a simple structure. Through [this Google Colab notebook](https://github.com/OpenEnergyPlatform/oekg/blob/main/How-to-develop-OEKG/How_to_develop_OEPKG.ipynb), you can find a guideline about how to read these placeholders and convert them to a single RDF document using the [rdflib](https://github.com/RDFLib/rdflib) library. Indeed, the OEKG is a big RDF graph containing information about energy studies. It enables interoperability among energy studies. [Here](https://github.com/OpenEnergyPlatform/oekg/blob/main/OEKG_in_Turtle/OEKG_With_Datasets.ttl), you can find the latest version of the OEKG in Turtle format. It contains 948 facts (or triples). You can also load this Turtle file with the [Apache Jena](https://jena.apache.org/) and run SPARQL queries on it.

Also, to express study reports using the RDF standard (according to the OEO conceptualizaion), you may find it easier to write Turtle files from scratch and avoid using the placeholders as an intermediate step. The main purpose of the placeholders, [this Google Colab notebook](https://github.com/OpenEnergyPlatform/oekg/blob/main/How-to-develop-OEKG/How_to_develop_OEPKG.ipynb) and the [rdflib](https://github.com/RDFLib/rdflib) library is to make it easier to develop an RDF document.


If you are interested in the knowledge graphs, [here](https://neo4j.com/knowledge-graphs-data-in-context-for-responsive-businesses/?utm_program=emea-prospecting&utm_source=google&utm_medium=cpc&utm_campaign=emea-search-offers&utm_adgroup=ebook-knowledge-graphs&utm_content=ebook-knowledge-graphs&utm_placement=&utm_keyword=define%20knowledge%20graph&utm_network=g&gclid=Cj0KCQjw1tGUBhDXARIsAIJx01mim5CuQ2uQoiLpzYmnlrsYzZk0virUTkGKFEsoqKYxNCQMEyYHbZUaAhiZEALw_wcB) and
[here](https://www.ibm.com/cloud/learn/knowledge-graph#:~:text=A%20knowledge%20graph%2C%20also%20known,the%20term%20knowledge%20%E2%80%9Cgraph.%E2%80%9D) are some useful resources for more details.

We are actively creating RDF graphs from energy study reports. 
Currently, the [OEKG](https://github.com/OpenEnergyPlatform/oekg/blob/main/OEKG_in_Turtle/OEKG_With_Datasets.ttl) has 1681 facts. 

