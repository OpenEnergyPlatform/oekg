import rdflib
from rdflib import URIRef, Namespace
import sys

def rework(classes, labels, graph, newgraph): #generate output to copy to shacl file
    oeo = Namespace("https://openenergyplatform.org/ontology/oeo/")
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    newgraph.bind("OEO", oeo)
    # inferred energy carriers
    carriers = ["OEO_00010408", "OEO_00010019", "OEO_00010409", "OEO_00010383", "OEO_00000062", "OEO_00000066", "OEO_00010225", "OEO_00000356", "OEO_00010223", "OEO_00000077", "OEO_00010445", "OEO_00000093", "OEO_00000094", "OEO_00000096", "OEO_00000099", "OEO_00000102", "OEO_00320013", "OEO_00320015", "OEO_00320012", "OEO_00320014", "OEO_00000115", "OEO_00010242", "OEO_00010379", "OEO_00140080", "OEO_00020196", "OEO_00000014", "OEO_00000131", "OEO_00010015", "OEO_00010226", "OEO_00000299", "OEO_00010382", "OEO_00010224", "OEO_00000181", "OEO_00010153", "OEO_00010146", "OEO_00010148", "OEO_00010151", "OEO_00010155", "OEO_00010241", "OEO_00000186", "OEO_00000204", "OEO_00000211", "OEO_00000226", "OEO_00000245", "OEO_00010237", "OEO_00320011", "OEO_00000257", "OEO_00000258", "OEO_00010145", "OEO_00010147", "OEO_00010150", "OEO_00010156", "OEO_00110000", "OEO_00000263", "OEO_00010316", "OEO_00010317", "OEO_00000286", "OEO_00000290", "OEO_00000292", "OEO_00000297", "OEO_00010337", "OEO_00010416", "OEO_00000302", "OEO_00010327", "OEO_00140078", "OEO_00000345", "OEO_00010326", "OEO_00010380", "OEO_00020050", "OEO_00000033", "OEO_00140079", "OEO_00010418", "OEO_00000332", "OEO_00010144", "OEO_00000391", "OEO_00010149", "OEO_00010154", "OEO_00010381", "OEO_00000401", "OEO_00010336", "OEO_00010221", "OEO_00010017", "OEO_00010016", "OEO_00010018", "OEO_00000439", "OEO_00010104", "OEO_00010448", "OEO_00010447", "OEO_00000054", "OEO_00010000", "OEO_00000058", "OEO_00000071", "OEO_00010446", "OEO_00000072", "OEO_00000074", "OEO_00000075", "OEO_00010215", "OEO_00000084", "OEO_00000088", "OEO_00020001", "OEO_00000173", "OEO_00000183", "OEO_00140159", "OEO_00000220", "OEO_00000246", "OEO_00000251", "OEO_00000025", "OEO_00010484", "OEO_00010105", "OEO_00000320", "OEO_00230021", "OEO_00140091", "OEO_00010093", "OEO_00020058", "OEO_00110001", "OEO_00140160", "OEO_00140092", "OEO_00000040", "OEO_00000441", "OEO_00000449"]

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

    for c in carriers:
        newgraph.add((URIRef("https://openenergyplatform.org/ontology/oeo/"+c), rdfs.subClassOf, oeo.OEO_00020039))

    newgraph.serialize("rework1.ttl", format='turtle')

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

data = sys.argv[1] #path to the rdf data file

#data = "/home/madeleine/Schreibtisch/oeo-full.owl"
g = rdflib.Graph()
g.parse(data)
reworkG = rdflib.Graph() #new empty graph

rework(classes, labels, g, reworkG)  # print out subclasses and individuals to be copied into shacl (no inferred classes!)








