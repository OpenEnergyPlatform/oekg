import sys
import rdflib
from rdflib import URIRef, Namespace, Literal, XSD

def graphFromfile(g, data):  # maybe put an argument in here instead of a path
    newpath = searchAndReplaceURL(data) #fix the url of the old okeg data
    g.parse(newpath)

def searchAndReplaceURL(data):  # creates a new file where "openenergy-platform" is replaced by "openenergyplatform", returns the path of that file
    with open(data, 'r') as file:
        text = file.read()
    renamedText = text.replace('http://openenergy-platform.org', 'https://openenergyplatform.org')
    path = data.rsplit("/", 1)
    if len(path) > 1:
        newpath = path[0] + "/" + "OEKG_Prep.ttl"
    else:
        newpath = "OEKG_Prep.ttl"
    with open(newpath, 'w') as file:
        file.write(renamedText)
    return newpath

def buildQuery(val, qu):  # takes what variables to output and the body of the query for SPARQL
    return '\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\nPREFIX oeo: <https://openenergyplatform.org/ontology/oeo/>\nPREFIX oekg: <https://openenergyplatform.org/ontology/oekg/>\nPREFIX obo: <http://purl.obolibrary.org/obo/>\nPREFIX dc: <http://purl.org/dc/terms/>\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nSELECT DISTINCT ' + val + ' WHERE{\n' + qu + ' .\n}'

def remodelNode(node, graph, newgraph):
# for a node, query all defined relations for it and its scenarios and publications, call functions to place new triples
    bundlePredicates = ["oeo:covers_energy_carrier", "oeo:has_study_keyword", "oekg:doi", "oekg:report_title",
                        "oekg:date_of_publication", "oeo:has_framework", "oekg:has_publication", "oeo:OEO_00000506",
                        "oeo:based_on_sector_division", "oeo:OEO_00000505", "oeo:OEO_00000522", "oeo:OEO_00000508",
                        "oeo:OEO_00000510", "oeo:OEO_00000509", "oekg:has_scenario", "oekg:has_full_name",
                        "oekg:link_to_study", "dc:acronym", "dc:abstract", "oeo:RO_0002234", "oeo:has_model"]
    # 0 oeo:covers_energy_carrier, 1 oeo:has_study_keyword, 2 oekg:doi, 3 oekg:report_title, 4 oekg:date_of_publication, 5 oeo:has_framework, 6 oekg:has_publication, 7 oeo:has author, 8 oeo:based_on_sector_division, 9 oeo:covers sector, 10 oeo:covers, 11 oeo:has contact person, 12 oeo:has organisation, 13 oeo:has funding source, 14 oekg:has_scenario, 15 oekg:has_full_name, 16 oekg:link_to_study, 17 dc:acronym, 18 dc:abstract, 19 obo:has output, 20 oeo:has_model
    bundleQueryResults = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    scenarioPredicates = ["dc:abstract", "oekg:has_full_name", "oeo:covers", "oeo:has_scenario_descriptor",
                          "oeo:covers_interacting_regions", "oeo:OEO_00020222", "oeo:OEO_00020220", "oeo:OEO_00020224",
                          "oekg:scenario_uuid", "rdfs:label", "oeo:RO_0002233", "oeo:RO_0002234"]
    # 0 dc:abstract, 1 oekg:has_full_name, 2 oeo:covers, 3 oeo:has_scenario_descriptor, 4 oeo:covers_interacting_regions, 5 oeo:has interacting region, 6 oeo:has study region, 7 oeo:has scenario year, 8 oekg:scenario_uuid, 9 rdf:label, 10 obo:has input, 11 obo:has output
    scenarioQueryResults = [[], [], [], [], [], [], [], [], [], [], [], []]
    scenarioQueryAllResults = []
    publicationPredicates = ["oekg:link_to_study", "oekg:link_to_study_report", "oekg:publication_uuid", "rdfs:label",
                             "oeo:OEO_00000506", "oekg:date_of_publication", "oekg:doi"]
    # 0 oekg:link_to_study, 1 oekg:link_to_study_report, 2 oekg:publication_uuid, 3 rdf:label, 4 oeo:has author, 5 oekg:date_of_publication, 6 oekg:doi
    publicationQueryResults = [[], [], [], [], [], [], []]
    publicationQueryAllResults = []

    # +++ query all the information for the scneario bundles +++
    constructLists(node, bundlePredicates, bundleQueryResults, graph)

    # 0:covers energy carrier shortcut, 1:has study descriptor tag, 2:has part, 3:based on sector division, 4:covers sector shortcut, 5:covers technology shortcut, 6:has contact person, 7:has organisation, 8:has funding source, 9:label, 10:acronym, 11:abstract, 12: has scenario type, 13: has interacting region, 14: has study region, 15: has scenario year value, 16: has uuid, 17: has information input (shortcut), 18: has information output (shortcut), 19: has reference, 20: has author, 21: has publication date, 22: has doi
    newPredicates = [oeo.OEO_00020432, oeo.OEO_00390071, obo.BFO_0000051, oeo.OEO_00390079, oeo.OEO_00020439,
                     oeo.OEO_00020438, oeo.OEO_00000508, oeo.OEO_00000510, oeo.OEO_00000509, rdfs.label, dc.acronym,
                     dc.abstract, oeo.OEO_00390073, oeo.OEO_00020222, oeo.OEO_00020220, oeo.OEO_00020440,
                     oeo.OEO_00390095, oeo.OEO_00020437, oeo.OEO_00020436, oeo.OEO_00390078, oeo.OEO_00000506,
                     oeo.OEO_00390096, oeo.OEO_00390098]

    createBundleTriples(bundleQueryResults,newPredicates, newgraph)

    # +++ for each scenario of a bundle, query information of the relations +++
    if not len(bundleQueryResults[14]) == 0:
        for s in bundleQueryResults[14]:
            constructLists(s, scenarioPredicates, scenarioQueryResults, graph)
            scenarioQueryAllResults.append(scenarioQueryResults)  # save results for one scenario
            scenarioQueryResults = [[], [], [], [], [], [], [], [], [], [], [], []]  # reset the list after each scenario

    createScenarioTiples(bundleQueryResults, scenarioQueryAllResults, newPredicates, newgraph)

    # +++ for each publication query the graph for relations +++
    if not len(bundleQueryResults[6]) == 0:
        for s in bundleQueryResults[6]:
            constructLists(s, publicationPredicates, publicationQueryResults, graph)
            publicationQueryAllResults.append(publicationQueryResults)  # save results for one publication
            publicationQueryResults = [[], [], [], [], [], [], []]  # reset result list

    createPublicationTriples(bundleQueryResults, publicationQueryAllResults, newPredicates, newgraph)

def createBundleTriples(bundleQueryResults,newPredicates,newgraph):
    # + place the found information for the scenario bundles in the new graph +

    # place energy carrier
    for res in bundleQueryResults[0]:
        newgraph.add((URIRef(node), newPredicates[0], URIRef(res)))  # covers energy carrier

    # place study descriptor tags
    for res in bundleQueryResults[1]:  # these are currently stings and have to be matched to the appropriate oeo classes
        if res == "carbon neutrality":  # special case
            newgraph.add((URIRef(node), newPredicates[1], oeo.OEO_00360014))
            newgraph.add((URIRef(node), newPredicates[1], oeo.OEO_00360011))
        else:
            val = findTagClass(res)  # most matching is done here
            if val != None:
                newgraph.add((URIRef(node), newPredicates[1], URIRef(val)))

    # place frameworks
    for res in bundleQueryResults[5]:
        newgraph.add((URIRef(node), newPredicates[2], URIRef(res)))  # has part
        newgraph.add((URIRef(res), rdf.type, oeo.OEO_00000172))  # framework factsheet

    # place reports
    for res in bundleQueryResults[6]:
        newgraph.add((URIRef(node), newPredicates[2], URIRef(res)))  # has part
        newgraph.add((URIRef(res), rdf.type, oeo.OEO_00020012))  # report

    # place sector divisions
    for res in bundleQueryResults[8]:
        if not res == "http://server/unset-base/Others":  # special bugged cases filtered
            newgraph.add((URIRef(node), newPredicates[3], URIRef(res)))  # based on sector division
    if node == "https://openenergyplatform.org/ontology/oekg/bb7dfe06-b2b1-2b88-652b-7f14e09b8998":
        newgraph.add((URIRef(node), newPredicates[3], URIRef("https://openenergyplatform.org/ontology/oeo/OEO_00000242")))  # add misplaced value for special case

    # place sectors
    for res in bundleQueryResults[9]:
        if not res == "https://openenergyplatform.org/ontology/oeo/OEO_00000242":  # value wrongfully placed here several times
            newgraph.add((URIRef(node), newPredicates[4], URIRef(res)))  # covers sector shortcut

    # place technology
    for res in bundleQueryResults[10]:
        newgraph.add((URIRef(node), newPredicates[5], URIRef(res)))  # covers technology shortcut

    # place contact persons
    for res in bundleQueryResults[11]:
        newgraph.add((URIRef(node), newPredicates[6], URIRef(res)))  # has contact person
        newgraph.add((URIRef(res), rdf.type, oeo.OEO_00000107))  # contact person

    # place organisations
    for res in bundleQueryResults[12]:
        newgraph.add((URIRef(node), newPredicates[7], URIRef(res)))  # has organisation
        newgraph.add((URIRef(res), rdf.type, oeo.OEO_00030022))  # organisation

    # place funders
    if not node == "https://openenergyplatform.org/ontology/oekg/a5127883-aaa9-020e-1e1d-38074dfdb20d":  # remove funders with no label
        for res in bundleQueryResults[13]:
            newgraph.add((URIRef(node), newPredicates[8], URIRef(res)))  # has funding source
            newgraph.add((URIRef(res), rdf.type, oeo.OEO_00090001))  # funding source
    if node == "https://openenergyplatform.org/ontology/oekg/769cff3d-d739-4760-687b-19c3f3675bd9":  # special case
        newgraph.add((URIRef(node), newPredicates[8], URIRef(bundleQueryResults[19][0])))  # funder stuck in output slot
        newgraph.add((URIRef(bundleQueryResults[19][0]), rdf.type, oeo.OEO_00090001))  # funding source

    # place scenarios
    for res in bundleQueryResults[14]:
        newgraph.add((URIRef(node), newPredicates[2], URIRef(res)))  # has part
        newgraph.add((URIRef(res), rdf.type, oeo.OEO_00000365))  # scenario factsheet

    # place labels
    for res in bundleQueryResults[15]:
        newgraph.add((URIRef(node), newPredicates[9], Literal(res, datatype=XSD.string)))  # label

    # place acronyms
    for res in bundleQueryResults[17]:
        newgraph.add((URIRef(node), newPredicates[10], Literal(res, datatype=XSD.string)))  # acronym

    # place abstracts
    for res in bundleQueryResults[18]:
        newgraph.add((URIRef(node), newPredicates[11], Literal(res, datatype=XSD.string)))  # abstract

    # place models
    for res in bundleQueryResults[20]:
        newgraph.add((URIRef(node), newPredicates[2], URIRef(res)))  # has part
        newgraph.add((URIRef(res), rdf.type, oeo.OEO_00000277))  # model factsheet

def createScenarioTiples(bundleQueryResults, scenarioQueryAllResults, newPredicates, newgraph):
        # + place information for the scenarios in the new graph +
        j = 0
        for r in scenarioQueryAllResults:
            #place abstracts
            for res in r[0]:
                newgraph.add((URIRef(bundleQueryResults[14][j]), newPredicates[11], Literal(res, datatype=XSD.string)))  # abstract

            #place labels
            for res in r[1]:
                newgraph.add((URIRef(bundleQueryResults[14][j]), newPredicates[9], Literal(res, datatype=XSD.string)))  # label

            #place syenario types
            for res in r[3]:
                newgraph.add((URIRef(bundleQueryResults[14][j]), newPredicates[12], URIRef(res)))  # scenario type

            #place interacting regions
            for res in r[5]:
                if not bundleQueryResults[14][j] == "https://openenergyplatform.org/ontology/oekg/scenario/ef7c8632-9048-be78-a46e-a128c3abc57d": #this one has study regions stuck here
                    newgraph.add((URIRef(bundleQueryResults[14][j]), newPredicates[13], URIRef(res)))  # interacting regions
                    newgraph.add((URIRef(res), rdf.type, oeo.OEO_00020036))  # interacting region

            #place study regions
            if bundleQueryResults[14][j] == "https://openenergyplatform.org/ontology/oekg/scenario/ef7c8632-9048-be78-a46e-a128c3abc57d":
                for res in r[5]: #study regions for this study were saved as interacting regions
                    country = str(res).rsplit("/", 1) #they also have faulty URIs
                    newgraph.add((URIRef(bundleQueryResults[14][j]), newPredicates[14], URIRef("https://openenergyplatform.org/ontology/oekg/region/" + country[1])))  # study regions
                    newgraph.add((URIRef("https://openenergyplatform.org/ontology/oekg/region/" + country[1]), rdf.type, oeo.OEO_00020032))  # study region

            for res in r[6]:
                    newgraph.add((URIRef(bundleQueryResults[14][j]), newPredicates[14], URIRef(res)))  # study regions
                    newgraph.add((URIRef(res), rdf.type, oeo.OEO_00020032))  # study region

            #place scenario years
            for res in r[7]:
                if not res == "None":
                    newgraph.add((URIRef(bundleQueryResults[14][j]), newPredicates[15], Literal(str(res) + "-01-01", datatype=XSD.dateTime)))  # scenario year value

            #place uuids
            for res in r[8]:
                newgraph.add((URIRef(bundleQueryResults[14][j]), newPredicates[16], Literal(res, datatype=XSD.string)))  # uuid

            #place acronyms
            for res in r[9]:
                newgraph.add((URIRef(bundleQueryResults[14][j]), newPredicates[10], Literal(res, datatype=XSD.string)))  # acronym

            #place inputs
            if bundleQueryResults[14][j] == "https://openenergyplatform.org/ontology/oekg/scenario/b7c25295-ee96-2af2-bca7-2af14ea78853":
            # repair where the same input got different URIs
                specialInputs = [
                    "https://openenergyplatform.org/ontology/oekg/input_datasets/05e8a737-6921-73a8-36a0-df187732bc41",
                    "https://openenergyplatform.org/ontology/oekg/input_datasets/41f1cc20-33e0-cf10-806e-90f92a6d9782",
                    "https://openenergyplatform.org/ontology/oekg/input_datasets/6d38086e-4b28-769a-905f-a6b03b9c8438",
                    "https://openenergyplatform.org/ontology/oekg/input_datasets/6e57cfc5-28aa-3170-8c61-89ceaad83505",
                    "https://openenergyplatform.org/ontology/oekg/input_datasets/96c1ee74-59ae-707f-8044-cca33639694f",
                    "https://openenergyplatform.org/ontology/oekg/input_datasets/aef3e7a0-9276-5b89-d75a-ba4ae729f6bb",
                    "https://openenergyplatform.org/ontology/oekg/input_datasets/fc405d84-e545-ae5a-de69-2ae4b2dbced4"]
                placeSpecialCases(specialInputs, bundleQueryResults[14][j], newPredicates[17], newgraph, oeo.OEO_00030029)  # input, exogenopus data
            elif bundleQueryResults[14][j] == "https://openenergyplatform.org/ontology/oekg/scenario/e9da6e0a-5592-3ca9-47e0-c8c011f834e3":
                specialInputs = [
                    "https://openenergyplatform.org/ontology/oekg/input_datasets/aef3e7a0-9276-5b89-d75a-ba4ae729f6bb",
                    "https://openenergyplatform.org/ontology/oekg/input_datasets/41f1cc20-33e0-cf10-806e-90f92a6d9782",
                    "https://openenergyplatform.org/ontology/oekg/input_datasets/96c1ee74-59ae-707f-8044-cca33639694f",
                    "https://openenergyplatform.org/ontology/oekg/input_datasets/05e8a737-6921-73a8-36a0-df187732bc41",
                    "https://openenergyplatform.org/ontology/oekg/input_datasets/6d38086e-4b28-769a-905f-a6b03b9c8438",
                    "https://openenergyplatform.org/ontology/oekg/input_datasets/6e57cfc5-28aa-3170-8c61-89ceaad83505",
                    "https://openenergyplatform.org/ontology/oekg/input_datasets/fc405d84-e545-ae5a-de69-2ae4b2dbced4"]
                placeSpecialCases(specialInputs, bundleQueryResults[14][j], newPredicates[17], newgraph, oeo.OEO_00030029)  # input, exogenopus data
            elif bundleQueryResults[14][j] == "https://openenergyplatform.org/ontology/oekg/scenario/2e4abb2b-43f0-935c-babd-1976ae5a128e":
                specialInputs = ["https://openenergyplatform.org/ontology/oekg/input_datasets/eafdff4a-a638-5a99-1019-afae867e88d7"]
                placeSpecialCases(specialInputs, bundleQueryResults[14][j], newPredicates[17], newgraph, oeo.OEO_00030029)  # input, exogenopus data
            elif bundleQueryResults[14][j] == "https://openenergyplatform.org/ontology/oekg/scenario/ff9765f6-b2ea-fb3c-1d77-b043b856e956":
                specialInputs = ["https://openenergyplatform.org/ontology/oekg/input_datasets/eafdff4a-a638-5a99-1019-afae867e88d7"]
                placeSpecialCases(specialInputs, bundleQueryResults[14][j], newPredicates[17], newgraph, oeo.OEO_00030029)  # input, exogenopus data
            elif bundleQueryResults[14][j] == "https://openenergyplatform.org/ontology/oekg/scenario/ea32122d-d5b2-b201-41ed-7369118a3a26":
                specialInputs = ["https://openenergyplatform.org/ontology/oekg/input_datasets/1c9e6b50-a6c3-5bfd-c273-a190cbb7db6b"]
                placeSpecialCases(specialInputs, bundleQueryResults[14][j], newPredicates[17], newgraph, oeo.OEO_00030029)  # input, exogenopus data
            else:
                for res in r[10]:
                    newgraph.add((URIRef(bundleQueryResults[14][j]), newPredicates[17], URIRef(res)))  # input
                    newgraph.add((URIRef(res), rdf.type, oeo.OEO_00030029))  # exogenous data

            #place outputs
            if bundleQueryResults[14][j] == "https://openenergyplatform.org/ontology/oekg/scenario/b7c25295-ee96-2af2-bca7-2af14ea78853":
                # repair where the same output got different URIs
                specialInputs = [
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/8c0dbcf9-800f-acf3-9fb0-dd6d7bec82fd",
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/c2c08004-b4f2-85a9-3f47-925f478a483d",
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/c66cf7d3-fbe7-ef6e-a4af-ff6b7c1a0130",
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/ce6c1e5a-05b2-9a83-e549-8d7431d47a9b",
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/426aa600-5b85-5c42-0cd9-b214674c3063",
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/ef2ce1e0-2690-a644-012e-135d78ec3cb5",
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/db346762-a144-6e3c-7295-39f79387c32f",
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/ffd2426f-7eb6-957d-e00a-260d7b3cb15f"]
                placeSpecialCases(specialInputs, bundleQueryResults[14][j], newPredicates[18], newgraph, oeo.OEO_00030030)  # output, endogenous data
            elif bundleQueryResults[14][j] == "https://openenergyplatform.org/ontology/oekg/scenario/e9da6e0a-5592-3ca9-47e0-c8c011f834e3":
                specialInputs = [
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/40dd5112-51ec-97f0-74fd-df48543248c6",
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/c2c08004-b4f2-85a9-3f47-925f478a483d",
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/ce6c1e5a-05b2-9a83-e549-8d7431d47a9b",
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/8c0dbcf9-800f-acf3-9fb0-dd6d7bec82fd",
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/db346762-a144-6e3c-7295-39f79387c32f",
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/ef2ce1e0-2690-a644-012e-135d78ec3cb5",
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/c66cf7d3-fbe7-ef6e-a4af-ff6b7c1a0130",
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/426aa600-5b85-5c42-0cd9-b214674c3063"]
                placeSpecialCases(specialInputs, bundleQueryResults[14][j], newPredicates[18], newgraph, oeo.OEO_00030030)  # output, endogenous data
            elif bundleQueryResults[14][j] == "https://openenergyplatform.org/ontology/oekg/scenario/444fca1a-8e8f-1e56-9773-6852691621b0":
                specialInputs = [
                    "https://openenergyplatform.org/ontology/oekg/output_datasets/3f0b2467-49f4-011a-83b5-3acdf04cab51"]
                placeSpecialCases(specialInputs, bundleQueryResults[14][j], newPredicates[18], newgraph, oeo.OEO_00030030)  # output, endogenous data
            else:
                for res in r[11]:
                    newgraph.add((URIRef(bundleQueryResults[14][j]), newPredicates[18], URIRef(res)))  # output
                    newgraph.add((URIRef(res), rdf.type, oeo.OEO_00030030))  # endogenous data

            j += 1

def createPublicationTriples(bundleQueryResults,publicationQueryAllResults,newPredicates,newgraph):
    # + place information for the publications in the new graph +
    j = 0
    for r in publicationQueryAllResults:
        # place references (links)
        # if the same link is both in [0] and [1] rdflib will only add it once
        for res in r[0]:
            if not bundleQueryResults[6][j] == "https://openenergyplatform.org/ontology/oekg/publication/1ae6110b-24fc-4f17-91da-bed92715c443":  # a wrong link is placed here
                newgraph.add((URIRef(bundleQueryResults[6][j]), newPredicates[19], URIRef(res)))  # has reference
                newgraph.add((URIRef(res), rdf.type, oeo.OEO_00000353))  # reference
        if bundleQueryResults[6][j] == "https://openenergyplatform.org/ontology/oekg/publication/1ae6110b-24fc-4f17-91da-bed92715c443":  # chose the right link for this scenario
            newgraph.add((URIRef(bundleQueryResults[6][j]), newPredicates[19], URIRef(r[1][1])))  # has reference
            newgraph.add((URIRef(r[1][1]), rdf.type, oeo.OEO_00000353))  # reference
        else:
            if not bundleQueryResults[6][j] == "https://openenergyplatform.org/ontology/oekg/publication/e8a4722c-83f2-1b2d-f316-ddc20b52bd29":  # remove a wrong value
                for res in r[1]:
                    newgraph.add((URIRef(bundleQueryResults[6][j]), newPredicates[19], URIRef(res)))  # has reference
                    newgraph.add((URIRef(res), rdf.type, oeo.OEO_00000353))  # reference

        # place uuids
        for res in r[2]:
            newgraph.add((URIRef(bundleQueryResults[6][j]), newPredicates[16], Literal(res, datatype=XSD.string)))  # uuid

        # place labels
        if bundleQueryResults[6][j] == "https://openenergyplatform.org/ontology/oekg/publication/03bb96e4-aee2-aef7-25ac-7db3826adfbf":
            newgraph.add((URIRef(bundleQueryResults[6][j]), newPredicates[9],
                          Literal("Climate neutrality, Energy security and Sustainability: A pathway to bridge the gap through Sufficiency, Efficiency and Renewables", datatype=XSD.string)))  # add missing label taken from study link
        if len(r[3]) > 1:  # chose correct label is several are present
            if bundleQueryResults[6][j] == "https://openenergyplatform.org/ontology/oekg/publication/1ae6110b-24fc-4f17-91da-bed92715c443":
                newgraph.add((URIRef(bundleQueryResults[6][j]), newPredicates[9], Literal(r[3][0], datatype=XSD.string)))  # label
            elif bundleQueryResults[6][j] == "https://openenergyplatform.org/ontology/oekg/publication/9076287c-a58c-e8dd-1e9b-e2ca53eb411c":
                newgraph.add((URIRef(bundleQueryResults[6][j]), newPredicates[9], Literal(r[3][2], datatype=XSD.string)))  # label
            else:
                newgraph.add((URIRef(bundleQueryResults[6][j]), newPredicates[9], Literal(r[3][1], datatype=XSD.string)))  # label
        else:
            for res in r[3]:
                newgraph.add((URIRef(bundleQueryResults[6][j]), newPredicates[9], Literal(res, datatype=XSD.string)))  # label

        # place authors
        for res in r[4]:
            if not res.count("http") > 1:  # remove broken author uris
                newgraph.add((URIRef(bundleQueryResults[6][j]), newPredicates[20], URIRef(res)))  # has author
                newgraph.add((URIRef(res), rdf.type, oeo.OEO_00000064))  # author

        # place publication dates
        for res in r[5]:  # the date was saved in 3 different formats
            date = None
            if not res == "None":
                if "/" in res:
                    d = res.split("/")
                    if len(d[1]) < 2:
                        d[1] = "0" + d[1]
                    if len(d[2]) < 2:
                        d[2] = "0" + d[2]
                    date = d[0] + "-" + d[1] + "-" + d[2]
                elif "-" in res:
                    date = res
                elif len(res) == 4:
                    date = res + "-01-01"
            if date != None:
                newgraph.add((URIRef(bundleQueryResults[6][j]), newPredicates[21], Literal(date, datatype=XSD.dateTime)))  # publication date
        if not bundleQueryResults[6][j] == "https://openenergyplatform.org/ontology/oekg/publication/e8a4722c-83f2-1b2d-f316-ddc20b52bd29":
            for res in r[6]:
                newgraph.add((URIRef(bundleQueryResults[6][j]), newPredicates[22], Literal(res, datatype=XSD.string)))  # doi
        j += 1

def constructLists(subject, predicates, resultList, graph):  # for given subject and predicate and a graph, fill a list with the objects
    i = 0
    for pred in predicates:
        query = buildQuery("?o", "<" + subject + "> " + pred + " ?o")
        qres = graph.query(query)
        for row in qres:
            resultList[i].append(str(row.o.toPython()))
        i += 1

def findTagClass(tag):  # for a given string return the appropriate annotated oeo class
    dict = {"(changes in) demand": "https://openenergyplatform.org/ontology/oeo/OEO_00140040",
            "demand": "https://openenergyplatform.org/ontology/oeo/OEO_00140040",
            "100% renewables": "https://openenergyplatform.org/ontology/oeo/OEO_00140133",
            "renewable energy share": "https://openenergyplatform.org/ontology/oeo/OEO_00140133",
            "acceptance": "https://openenergyplatform.org/ontology/oeo/OEO_00360000",
            "CO2 emissions": "https://openenergyplatform.org/ontology/oeo/OEO_00260007",
            "CO2 emission": "https://openenergyplatform.org/ontology/oeo/OEO_00260007",
            "decarbonization pathways": "https://openenergyplatform.org/ontology/oeo/OEO_00010212",
            "decarbonisation pathway": "https://openenergyplatform.org/ontology/oeo/OEO_00010212",
            "degree of electrifiaction": "https://openenergyplatform.org/ontology/oeo/OEO_00020254",
            "electrical energy share": "https://openenergyplatform.org/ontology/oeo/OEO_00020254",
            "Efficiency": "https://openenergyplatform.org/ontology/oeo/OEO_00140050",
            "efficiency value": "https://openenergyplatform.org/ontology/oeo/OEO_00140050",
            "electricity grid": "https://openenergyplatform.org/ontology/oeo/OEO_00000143",
            "final energy demand": "https://openenergyplatform.org/ontology/oeo/OEO_00050016",
            "final energy consumption value": "https://openenergyplatform.org/ontology/oeo/OEO_00050016",
            "Flexibility": "https://openenergyplatform.org/ontology/oeo/OEO_00360007",
            "flexibility": "https://openenergyplatform.org/ontology/oeo/OEO_00360007",
            "gas grid": "https://openenergyplatform.org/ontology/oeo/OEO_00020004",
            "Greenhouse gas emissions": "https://openenergyplatform.org/ontology/oeo/OEO_00000199",
            "greenhouse gas emission": "https://openenergyplatform.org/ontology/oeo/OEO_00000199",
            "heating grid": "https://openenergyplatform.org/ontology/oeo/OEO_00020005",
            "model intercomparison study": "https://openenergyplatform.org/ontology/oeo/OEO_00360002",
            "negative emissions": "https://openenergyplatform.org/ontology/oeo/OEO_00000293",
            "policies and measures": "https://openenergyplatform.org/ontology/oeo/OEO_00140151",
            "policy instrument": "https://openenergyplatform.org/ontology/oeo/OEO_00140151",
            "primary energy demand": "https://openenergyplatform.org/ontology/oeo/OEO_00050018",
            "primary energy consumption value": "https://openenergyplatform.org/ontology/oeo/OEO_00050018",
            "regionalisation": "https://openenergyplatform.org/ontology/oeo/OEO_00340006",
            "resilience": "https://openenergyplatform.org/ontology/oeo/OEO_00360015",
            "study report due to legal obligation": "https://openenergyplatform.org/ontology/oeo/OEO_00020373",
            "sufficiency": "https://openenergyplatform.org/ontology/oeo/OEO_00010444",
            "total gross electricity generation": "https://openenergyplatform.org/ontology/oeo/OEO_00240012",
            "gross electricity generation": "https://openenergyplatform.org/ontology/oeo/OEO_00240012",
            "total net electricity generation": "https://openenergyplatform.org/ontology/oeo/OEO_00240013",
            "net electricity generation": "https://openenergyplatform.org/ontology/oeo/OEO_00240013",
            "model coupling": "https://openenergyplatform.org/ontology/oeo/OEO_00020406",
            "sector coupling": "https://openenergyplatform.org/ontology/oeo/OEO_00020408",
            "energy conversion efficiency": "https://openenergyplatform.org/ontology/oeo/OEO_00140049",
            "energy demand": "https://openenergyplatform.org/ontology/oeo/OEO_00140146",
            "scenario projection comparison": "https://openenergyplatform.org/ontology/oeo/OEO_00360003",
            "climate neutrality criterion": "https://openenergyplatform.org/ontology/oeo/OEO_00360010",
            "process climate neutrality": "https://openenergyplatform.org/ontology/oeo/OEO_00360011",
            "material climate neutrality": "https://openenergyplatform.org/ontology/oeo/OEO_00360014",
            "life cycle assessment": "https://openenergyplatform.org/ontology/oeo/OEO_00330023"}

    return dict.get(tag)

def placeSpecialCases(specialInputs, subject, predicate, newgraph, type):  # for a list of input subject, place them with their subject, predicate and class in the new graph
    for inp in specialInputs:
        newgraph.add((URIRef(subject), predicate, URIRef(inp)))  # input
        newgraph.add((URIRef(inp), rdf.type, type))

def finishDataset(oldgraph, newgraph): #for input and output data, add their labels, iris, ids and uuids
    datasets = []
    gatherNodes(datasets, newgraph, buildQuery("?o", "?s oeo:OEO_00020437 ?o"))
    gatherNodes(datasets, newgraph, buildQuery("?o", "?s oeo:OEO_00020436 ?o"))
    # 0: label, 1: has iri, 2: oekg:has_id, 3: has uuid
    oldpreds = ["http://www.w3.org/2000/01/rdf-schema#label",
                "https://openenergyplatform.org/ontology/oeo/has_iri",
                "https://openenergyplatform.org/ontology/oeo/has_id",
                "https://openenergyplatform.org/ontology/oeo/has_key"]
    newpreds = ["http://www.w3.org/2000/01/rdf-schema#label",
                "https://openenergyplatform.org/ontology/oeo/OEO_00390094",
                "https://openenergyplatform.org/ontology/oekg/has_id",
                "https://openenergyplatform.org/ontology/oeo/OEO_00390095"]

    addExtraStrings(datasets, oldgraph, newgraph, newpreds[0], oldpreds[0])
    addExtraStrings(datasets, oldgraph, newgraph, newpreds[1], oldpreds[1])
    addExtraInts(datasets, oldgraph, newgraph, newpreds[2], oldpreds[2])
    addExtraStrings(datasets, oldgraph, newgraph, newpreds[3], oldpreds[3])

def finishModelFrame(oldgraph, newgraph): #for models and frameworks, add their labels and iris
    datasets = []
    gatherNodes(datasets, newgraph, buildQuery("?o", "?s obo:BFO_0000051 ?o. ?o a oeo:OEO_00000172"))
    gatherNodes(datasets, newgraph, buildQuery("?o", "?s obo:BFO_0000051 ?o. ?o a oeo:OEO_00000277"))
    # 0: label, 1: has iri
    oldpreds = ["http://www.w3.org/2000/01/rdf-schema#label", "https://openenergyplatform.org/ontology/oeo/has_iri"]
    newpreds = ["http://www.w3.org/2000/01/rdf-schema#label", "https://openenergyplatform.org/ontology/oeo/OEO_00390094"]

    addExtraStrings(datasets, oldgraph, newgraph, newpreds[0], oldpreds[0])
    addExtraStrings(datasets, oldgraph, newgraph, newpreds[1], oldpreds[1])

def finishRegions(oldgraph, newgraph): # for study regions and interacting regions, add their regions and fix their references
    datasets = []
    gatherNodes(datasets, newgraph, buildQuery("?o", "?s oeo:OEO_00020220 ?o"))
    gatherNodes(datasets, newgraph, buildQuery("?o", "?s oeo:OEO_00020222 ?o"))
    # 0: label, 1: has reference
    oldpreds = ["http://www.w3.org/2000/01/rdf-schema#label", "https://openenergyplatform.org/ontology/oekg/reference"]
    newpreds = ["http://www.w3.org/2000/01/rdf-schema#label", "https://openenergyplatform.org/ontology/oeo/OEO_00390078"]
    addExtraStrings(datasets, oldgraph, newgraph, newpreds[0], oldpreds[0])
    for dset in datasets:
        ref = dset.rsplit("/", 1)
        ref = "https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/" + str(ref[1])
        newgraph.add((URIRef(dset), URIRef(newpreds[1]), URIRef(ref)))
        newgraph.add((URIRef(ref), rdf.type, oeo.OEO_00000353))

def finishLabels(oldgraph, newgraph):  # looks for oekg specific labels that cannot be extracted from the oeo
    datasets = []
    gatherNodes(datasets, newgraph, buildQuery("?o", "?s oeo:OEO_00000506 ?o"))  # authors
    gatherNodes(datasets, newgraph, buildQuery("?o", "?s oeo:OEO_00000508 ?o"))  # contact person
    gatherNodes(datasets, newgraph, buildQuery("?o", "?s oeo:OEO_00000510 ?o"))  # organisation
    gatherNodes(datasets, newgraph, buildQuery("?o", "?s oeo:OEO_00000509 ?o"))  # organisation

    addExtraStrings(datasets, oldgraph, newgraph, "http://www.w3.org/2000/01/rdf-schema#label","http://www.w3.org/2000/01/rdf-schema#label")

def gatherNodes(datasets, newgraph, query): #add the results for ?o in a given query to a list
    qres = newgraph.query(query)
    for row in qres:
        datasets.append(row.o.toPython())

def addExtraStrings(datasets, oldgraph, newgraph, pred, oldpred):#for a list of subjects, and one predicate, add the objects as string to the graph
    allResults = []
    queryHelper(datasets, oldpred, oldgraph, allResults)
    i = 0
    for dset in datasets:
        if len(allResults[i]) > 0:
            newgraph.add((URIRef(dset), URIRef(pred), Literal(allResults[i][0], datatype=XSD.string)))
        i += 1

def addExtraInts(datasets, oldgraph, newgraph, pred, oldpred): #for a list of subjects, and one predicate, add the objects as integer to the graph
    allResults = []
    queryHelper(datasets, oldpred, oldgraph, allResults)
    i = 0
    for dset in datasets:
        if len(allResults[i]) > 0:
            newgraph.add((URIRef(dset), URIRef(pred), Literal(int(allResults[i][0]), datatype=XSD.integer)))
        i += 1

def queryHelper(datasets, predicate, graph, resultList):  # for a list of subjects and one predicate, construct a list of the result lists for the objects
    for dset in datasets:
        result = []
        query = buildQuery("?o", "<" + dset + "> <" + predicate + "> ?o")
        qres = graph.query(query)
        for row in qres:
            if not str(row.o.toPython()) == "None":  # filter out unwanted results
                result.append(row.o.toPython())
        resultList.append(result)


Oekgdata = sys.argv[1] #path to the oekg data file
data = sys.argv[2] # path to the File with the output of reworkOEOBase
#Oekgdata = "/home/madeleine/Schreibtisch/Bachelorarbeit/oekg_Material/oekg_neu.ttl"
#data = "/home/madeleine/PycharmProjects/pythonProject/bachelorPyFiles/output_rework_oekg_step1.ttl"

# this is not in a main() because the graphs do not like to be loaded from inside a function
g = rdflib.Graph()
reworkG = rdflib.Graph()
graphFromfile(g, Oekgdata)  # change this to load a rdflib graph from sometwhere else
reworkG.parse(data)

oeo = Namespace("https://openenergyplatform.org/ontology/oeo/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
dc = Namespace("http://purl.org/dc/terms/")
oekg = Namespace("https://openenergyplatform.org/ontology/oekg/")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
obo = Namespace("http://purl.obolibrary.org/obo/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
reworkG.bind("RDFS", rdfs)
reworkG.bind("DC", dc)
reworkG.bind("OEKG", oekg)
reworkG.bind("XSD", xsd)
reworkG.bind("OBO", obo)

nodes = []
qres = g.query(buildQuery("?s", "?s a oeo:OEO_00010252")) #find all the bundles
for row in qres:
    nodes.append(row.s.toPython())

for n in nodes: #add bundles to the new graph
    reworkG.add((URIRef(n), rdf.type, oeo.OEO_00020227))

for node in nodes: #remodel every bundle with scenarios and publications
    remodelNode(node, g, reworkG)

# for all nodes that are not bundle specific, ass their relations
# if any values in here are duplicates rdflib will only add them once
finishDataset(g, reworkG)
finishModelFrame(g, reworkG)
finishRegions(g, reworkG)
finishLabels(g, reworkG)

#save the new graph in a file
reworkG.serialize("output_rework_oekg_step2.ttl", format='turtle')
