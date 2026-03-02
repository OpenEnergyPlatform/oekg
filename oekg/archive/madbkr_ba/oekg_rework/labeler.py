import sys
import rdflib
from rdflib import URIRef, Namespace, Literal, XSD

def buildQuery(val,qu):
    return '\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\nPREFIX oeo: <https://openenergyplatform.org/ontology/oeo/>\nPREFIX oekg: <https://openenergyplatform.org/ontology/oekg/>\nPREFIX obo: <http://purl.obolibrary.org/obo/>\nPREFIX dc: <http://purl.org/dc/terms/>\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nSELECT DISTINCT '+val+' WHERE{\n'+qu+' .\n}'

dataoeo = sys.argv[1] #path for the oeo
dataoekg = sys.argv[2] #parth for the output file of mainRemodel
#dataoeo = "/home/madeleine/Schreibtisch/oeo-full.owl"
#dataoekg = "/home/madeleine/PycharmProjects/pythonProject/bachelorPyFiles/output_rework_oekg_step2.ttl"


f = rdflib.Graph()
g = rdflib.Graph()
f.parse(dataoeo)
g.parse(dataoekg)
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
uris = []


qres = g.query(buildQuery("?s ?p ?o","?s ?p ?o")) #query the oekg for all the relevant URIs

for row in qres:
    uris.append(row.s.toPython())
    uris.append(row.p.toPython())
    if type(row.o) == rdflib.term.URIRef:
        uris.append(row.o.toPython())

uris = list(set(uris)) #remove duplicates
redUris = [] #save only the URIS that can be labeled by the oeo
labels = []
i = 0

for u in uris: #query the oeo for all the labels of the identified URIs
    qres = f.query(buildQuery("?label","<"+str(u)+"> rdfs:label ?label"))
    if not len(qres)== 0:
        redUris.append(u)
    for row in qres:
        labels.append(row.label.toPython())

for u in redUris:
    g.remove((URIRef(u),rdfs.label,None)) #remove the current labels for anything found
    g.add((URIRef(u), rdfs.label, Literal(labels[i], datatype=XSD.string))) #add the new labels
    i = i+1

g.serialize("output_rework_oekg_final.ttl", format='turtle')



