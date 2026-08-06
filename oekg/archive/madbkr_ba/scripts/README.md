# oekg rework folder

## reworkOeoBase.py

- takes path to the latest OEO release .owl file as argument
- queries OEO for subclasses and individuals of sector, sector division, technology, energy carrier, scenario 
- prints them for copying to SHACL
- queries OEO for "oekg" annotated descriptpor tag classes and prints them
- adds triples für subclasses and individuals  to new graph
- outputs graph as output_rework_oekg_step1.ttl

## mainRemodel.py 

- takes path to the old OEKG .ttl file as 1st argument
- takes output_rework_oekg_step1.ttl, the output of reworkOeoBase.py, as second argument
- queries the OEKG for its relevant triples and places them in the new graph
- corrects several mistakes for special places
- replaces classes and predicated
- outputs graph as output_rework_oekg_step2.ttl

## labeler.py

- takes path to the latest OEO release .owl file as first argument
- takes output_rework_oekg_step1.ttl, the output of mainRemodel.py, as second argument
- queries the OEO for labels of any URI in the OEKG
- removes old labels if they exist
- places found labels in the graph
- outputs graph as output_rework_oekg_final.ttl

## hierarchyEXTRA.py

### output_rework_oekg_final.ttl is the final version of the reworked oekg

- this is a variant of reworkOeoBase.py

> **Not usable.** `mode = sys.argv[3]` is a string and `if mode < 2:` therefore raises
> `TypeError` on every invocation, after the graph is parsed and before any work is done.
> It is retired with the other three scripts. Do not treat it as tooling for future
> updates; if OEO-hierarchy refreshing is wanted again, write it deliberately.

- takes path to a data file as first argumennt
- takes the complete IRI of a class as second argument
- take the integer 0, 1 or 2 as third argument
- takes path to an ontology as forth argument if 0 or 1 are used before
- when 0 is chosen queries the inferred(!!!) ontology provided in argument 4 for the subclasses and individuals of the class in argument 2 and places in in the graph of the file given in the first argument
- when 1 is chosen queries the ontology provided in argument 4 for the subclasses and individuals of the class in argument 2 and places in in the graph of the file given in the first argument
- when 2 is chosen queries the data file provided in argument 1 for the subclasses and individuals of the class in argument 2 and removed them from the graph
- outputs the modified graph as output_modified_hierachy.ttl


## input files

The latest version of the input files are provided here:

- oeo-full.owl is the OEO release v2.8.0
- oekg_neu.ttl is the OEKG used for the rework (retrieved in april 2025)
- OEKG_Prep.ttl is a file that gets created by mainRemodel.py as a in-between step
- OEO_Prep.owl is a file that gets created by reworkBase.py as a in-between step
- output_rework_oekg_step1.ttl, output_rework_oekg_step2.ttl, output_rework_oekg_final.ttl are the latest output of the scripts with the input files provided

## documentation.pdf

- explains all the predicates with definitions, domains and ranges




