from owlready2 import *
import rdflib
from rdflib import URIRef, Namespace
import sys


def reasoning(data):
    path = data.rsplit("/", 1)
    if len(path) > 1:
        newpath = path[0] + "/" + "OEO_Prep.owl"
    else:
        newpath = "OEO_Prep.owl"

    onto = get_ontology(data).load()

    with onto:
        sync_reasoner()

    onto.save(newpath)

    return newpath

def rework(classes, labels, graph, newgraph): #generate output to copy to shacl file
    oeo = Namespace("https://openenergyplatform.org/ontology/oeo/")
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    newgraph.bind("OEO", oeo)

    i = 0
    for cl in classes:
        print("\n" + labels[i] + "\n")
        i += 1
        #these are for the results
        parents = []
        children = []
        # this is needed for the recursion
        subjects = []
        subjects.append(cl)

        exploreSubClass(subjects, parents, children, graph) #get a list of all classes and subclasses recursively

        indivs = []
        indParents = []

        for c in children:
            exploreIndivs(c, indParents, indivs, graph) #get a list of classes and their individuals

        exploreIndivs(cl, indParents, indivs, graph) #add the highest hierachy parent and their individuals

        shaclOutput(cl, children, indivs) #print in a convenient way to copy to shacl

        j = 0
        for p in parents:
            newgraph.add((URIRef(children[j]), rdfs.subClassOf, URIRef(p)))
            j += 1

        j = 0

        for ind in indivs:
            newgraph.add((URIRef(ind), rdf.type, URIRef(indParents[j])))
            j += 1

    print("\ndescripor tags\n") # descriptor tags a queried differently but are also printed
    annotationQuery(graph)

    newgraph.serialize("output_rework_oekg_step1.ttl", format='turtle')

def exploreSubClass(subjects, parents, children, graph): #recursively look through the subclasses, make arrays for parents and children
    if len(subjects)==0:
        return
    else:
        for s in subjects:
            current = []
            knows_query = subClassQuery("<" + s + ">")
            qres = graph.query(knows_query)

            for row in qres:
                r = str(row.s.toPython())
                parents.append(s)
                children.append(r)
                current.append(r)
            exploreSubClass(current, parents, children, graph)

def subClassQuery(c):
    return '\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\nPREFIX oeo: <https://openenergyplatform.org/ontology/oeo/>\nPREFIX oekg: <https://openenergyplatform.org/ontology/oekg/>\nPREFIX obo: <http://purl.obolibrary.org/obo/>\nPREFIX dc: <http://purl.org/dc/terms/>\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nSELECT DISTINCT ?s WHERE{\n?s rdfs:subClassOf ' + c + ' \n}'

def exploreIndivs(subject, indParents, indivs, graph): #for the given subject, append the individuals with their parents as list each
    knows_query = individualQuery("<" + subject + ">")
    qres = graph.query(knows_query)

    for row in qres:
        r = str(row.s.toPython())
        indParents.append(subject)
        indivs.append(r)

def individualQuery(c):
    return '\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\nPREFIX oeo: <https://openenergyplatform.org/ontology/oeo/>\nPREFIX oekg: <https://openenergyplatform.org/ontology/oekg/>\nPREFIX obo: <http://purl.obolibrary.org/obo/>\nPREFIX dc: <http://purl.org/dc/terms/>\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nSELECT DISTINCT ?s WHERE{\n?s a <http://www.w3.org/2002/07/owl#NamedIndividual>.\n?s a '  + c + ' \n}'

def shaclOutput (subject, children, indivs): #output a string that can be used in the shacls section it is needed in
    results = []
    results.append(subject.replace('https://openenergyplatform.org/ontology/oeo/','oeo:'))
    for child in children:
        results.append(child.replace('https://openenergyplatform.org/ontology/oeo/','oeo:'))
    for ind in indivs:
        results.append(ind.replace('https://openenergyplatform.org/ontology/oeo/', 'oeo:'))
    result = " "
    results = list(set(results)) #remove duplicates
    for r in results:
        result = result + r + " "
    print(result)

def annotationQuery(graph): #query for things with the "oekg" annotation for the keywords/tags
    knows_query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dc: <http://purl.org/dc/terms/> 
        PREFIX obo: <http://purl.obolibrary.org/obo/> 
        PREFIX oekg: <https://openenergyplatform.org/ontology/oekg/> 
        PREFIX oeo: <https://openenergyplatform.org/ontology/oeo/> 
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT DISTINCT ?s WHERE{
    ?s <https://openenergyplatform.org/ontology/oeo/OEO_00020425> ?o.
            }"""
    qres = graph.query(knows_query)

    results = []
    results2 = [] #this is only needed because there is this one different URI
    for row in qres:
        results.append(str(row.s.toPython()))
    for r in results:
        results2.append(r.replace('https://openenergyplatform.org/ontology/oeo/', 'oeo:'))
    results = []
    for r in results2:
        results.append(r.replace('http://www.openenergyplatform.org/ontology/oeo/', 'oeo:')) #strangely one of the URIs has a different structure
    result = " "
    for r in results:
        result = result + r + " "
    print(result)

#this is not in a main() because the graph do not like to be loaded inside a function
# for the following subjects their subclasses and individuals are to be found and added to a new graph
classes = ["https://openenergyplatform.org/ontology/oeo/OEO_00000367",
            "https://openenergyplatform.org/ontology/oeo/OEO_00000368",
            "https://openenergyplatform.org/ontology/oeo/OEO_00000407",
            "https://openenergyplatform.org/ontology/oeo/OEO_00020039",
            "https://openenergyplatform.org/ontology/oeo/OEO_00000364"]
labels = ["sector", "sector division", "technology", "energy carrier", "scenario"]

#data = sys.argv[1] #path to the rdf data file

data = "/home/madeleine/Schreibtisch/oeo-full.owl"
g = rdflib.Graph()
g.parse(reasoning(data))
reworkG = rdflib.Graph() #new empty graph

rework(classes, labels, g, reworkG)  # print out subclasses and individuals to be copied into shacl (no inferred classes!)








