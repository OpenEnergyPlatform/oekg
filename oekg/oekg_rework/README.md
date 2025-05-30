# oekg rework folder

## reworkOeoBase.py

- takes path to the latest OEO release .owl file as argument
- queries OEO for subclasses and individuals of sector, sector division, technology, energy carrier, scenario 
- prints them for copying to SHACL
- queries OEO for "oekg" annotated descriptpor tag classes and prints them
- adds triples für subclasses and individuals  to new graph
- outputs graph as rework1.ttl

## mainRemodel.py 

- takes path to the old OEKG .ttl file as 1st argument
- takes rework1.ttl, the output of reworkOeoBase.py, as second argument
- queries the OEKG for its relevant triples and places them in the new graph
- corrects several mistakes for special places
- replaces classes and predicated
- outputs graph as rework2.ttl

## labeler.py

- takes path to the latest OEO release .owl file as first argument
- takes rework1.ttl, the output of mainRemodel.py, as second argument
- queries the OEO for labels of any URI in the OEKG
- removes old labels if they exist
- places found labels in the graph
- outputs graph as rework3.ttl

### rework3.ttl is the final version of the reworked oekg

## input files

The latest version of the input files are provided here:

- oeo-full.owl is the OEO release v2.8.0
- oekg_neu.ttl is the OEKG used for the rework (retrieved in april 2025)
- OEKG_Prep.ttl is a file taht gets created by mainRemodel.py as a in-between step
- rework1.ttl, rework2.ttl, rework3.ttl are the latest output of the scripts with the input files provided

## documentation.pdf

- explains all the predicates with definitions, domains and ranges


/////

# shacl folder

## oekg_shacl_old_graph.ttl

- shacl file for the old OEKG

## oekg_shacl_new_graph.ttl

- shacl file for the new OEKG

## New_Graph_ValidationResults(55)

- validation report for the rework3.ttl file (the new OEKG) and the SHALC file oekg_shacl_new_graph.ttl
- contains 55 violations

## Old_Graph_ValidationResults(2695).txt

- validation report for the oekg_neu.ttl file (the old OEKG) and the SHALC file oekg_shacl_old_graph.ttl
- contains 2695 violations


/////

# competency questions folder

## competency questions unanswered.txt

- contains the competency questions with no answers

## answers_old_graph.txt

- contains queries for the competency questions as possible in the old graph (oekg_neu.ttl) with a brief verdict how good these answers are

## answers_new_graph.txt

- contains queries for the competency questions as possible in the new graph (rework3.ttl) with a brief verdict how good these answers are




