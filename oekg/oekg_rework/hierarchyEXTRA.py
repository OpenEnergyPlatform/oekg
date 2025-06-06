from owlready2 import *
import rdflib
from rdflib import URIRef, Namespace
import sys


def reasoning(data):
    path = data.rsplit("/", 1)
    if len(path) > 1:
        newpath = path[0] + "/" + "Prep.owl"
    else:
        newpath = "Prep.owl"

    onto = get_ontology(data).load()

    with onto:
        sync_reasoner()

    onto.save(newpath)

    return newpath

def prepareParis(parentclass, graph): #generate output to copy to shacl file

    #these are for the results
    parents = []
    children = []
    # this is needed for the recursion
    subjects = []
    subjects.append(parentclass)

    exploreSubClass(subjects, parents, children, graph) #get a list of all classes and subclasses recursively

    indivs = []
    indParents = []

    for c in children:
        exploreIndivs(c, indParents, indivs, graph) #get a list of classes and their individuals

    exploreIndivs(parentclass, indParents, indivs, graph) #add the highest hierachy parent and their individuals

    return parents, children, indivs, indParents

def placeTriples(parents, children, indivs, indParents, graph):
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    j = 0
    for p in parents:
        graph.add((URIRef(children[j]), rdfs.subClassOf, URIRef(p)))
        j += 1

    j = 0
    for ind in indivs:
        graph.add((URIRef(ind), rdf.type, URIRef(indParents[j])))
        j += 1

def removetriples (parents, children, indivs, indParents, graph):
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    j = 0
    for p in parents:
        graph.remove((URIRef(children[j]), rdfs.subClassOf, URIRef(p)))
        j += 1

    j = 0
    for ind in indivs:
        graph.remove((URIRef(ind), rdf.type, URIRef(indParents[j])))
        j += 1

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
    return '\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\nPREFIX oeo: <https://openenergyplatform.org/ontology/oeo/>\nPREFIX oekg: <https://openenergyplatform.org/ontology/oekg/>\nPREFIX obo: <http://purl.obolibrary.org/obo/>\nPREFIX dc: <http://purl.org/dc/terms/>\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nSELECT DISTINCT ?s WHERE{\n?s a '  + c + ' \n}'


#this is not in a main() because the graph do not like to be loaded inside a function

graph = sys.argv[1] #path to the rdf data file
parentclass = sys.argv[2]
mode = sys.argv[3] # 0: place hierachy with reasoning, 1: place hierachy without reasoning, 2: remove hierachy

data = sys.argv[4] #path to the ontology

#data = "/home/madeleine/Schreibtisch/oeo-full.owl"
#graph = "/home/madeleine/PycharmProjects/pythonProject/bachelorPyFiles/rework1.ttl"
#parentclass = "https://openenergyplatform.org/ontology/oeo/OEO_00000367"
#mode = 2


h = rdflib.Graph() #the knowledge graph
h. parse(graph)


if mode < 2:
    g = rdflib.Graph() #the ontology
    if mode == 0:
        data = reasoning(data)
    g.parse(data)
    parents, children, indivs, indParents = prepareParis(parentclass, g)
    placeTriples(parents, children, indivs, indParents, h)
elif mode == 2:
    parents, children, indivs, indParents = prepareParis(parentclass, h)
    removetriples(parents, children, indivs, indParents, h)


h.serialize("result.ttl", format='turtle')













