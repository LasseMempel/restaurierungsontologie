# Import des Moduls owlready2, welches die Arbeit mit Ontologien in Python ermöglicht
from owlready2 import *
from pylode.profiles.ontpub import OntPub
import rdflib
import json
import pandas as pd
#import pylode
#import types

def downloadThesaurus():
    thesaurus = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQCho2k88nLWrNSXj4Mgj_MwER5GQ9zbZ0OsO3X_QPa9s-3UkoeLLQHuNHoFMKqCFjWMMprKVHMZzOj/pub?gid=0&single=true&output=csv"
    data = pd.read_csv(thesaurus)
    # save data as csv
    data.to_csv("files/thesaurus.csv")

def createOntology(path):
    # Läd die Ontologie und speichert sie als Variable onto. Geladen wird eine leere Ontologie, da der angegebene Pfad leer ist
    onto = get_ontology("http://www.conservationontology.com/conservationontology.owl")
    onto.metadata.comment.append("Konservierungs- und Restaurierungsontologie des LEIZA")
    #onto.metadata.title.append("Konservierungs- und Restaurierungsontologie")
    #onto.metadata.creator.append("Kristina Fella")

    # sämtliche folgenden Anweisungen werden "mit der Ontologie onto" ausgeführt
    with onto:
        # <<<HAUPTKLASSEN>>>

        # Die Klasse RestauratorIn wird erstellt. Diese ist eine Unterklasse von Thing, die Metaklasse aller Klassen der Ontologie
        class RestauratorIn(Thing):
            # pass bedeutet, dass die Definition der Klasse abgeschlossen ist. 
            # Später werden wir hier stattdessen z.B. die Attribute einfügen
            pass

        class Objekt(Thing):
            pass

        class Objektuntersuchung(Thing):
            pass

        class Ergebnis(Thing):
            pass

        class Methode(Thing):
            pass

        class praktischeMaßnahme(Thing):
            pass

        class Material(Thing):
            pass

        class Werkzeug(Thing):
            pass

        class technologischeAuswertung(Thing):
            pass

        class Herstellungstechnik(Thing):
            pass

        class Restaurierungskonzept(Thing):
            pass

        class Zustand(Thing):
            pass

        class Schadensphänomen(Thing):
            pass

        class Schadensursache(Thing):
            pass

        # <<<UNTERKLASSEN>>>

        # Die Klasse Konservierung wird erstellt. Diese ist eine Unterklasse von Konservierungsmaßnahme
        class Materialanalyse(Objektuntersuchung):
            pass

        class manuellesWerkzeug(Werkzeug):
            pass

        class technischesGerät(Werkzeug):
            pass

        # <<<EIGENSCHAFTEN>>>
        class bearbeitet(ObjectProperty):
            domain = [Objekt]
            range = [RestauratorIn]
            #inverse_property = wirdBearbeitetVon

        class wirdBearbeitetVon(ObjectProperty):
            domain = [RestauratorIn]
            range = [Objekt]
            inverse_property = bearbeitet

        class führtDurch(ObjectProperty):
            domain = [RestauratorIn]
            range = [Objektuntersuchung, technologischeAuswertung]
            #inverse_property = wirdDurchgeführtVon

        class wirdDurchgeführtVon(ObjectProperty):
            domain = [Objektuntersuchung, technologischeAuswertung]
            range = [RestauratorIn]
            inverse_property = führtDurch

        class führtZu(ObjectProperty):
            domain = [Objektuntersuchung]
            range = [Ergebnis]
            #inverse_property = entstehtAus

        class entstehtAus(ObjectProperty):
            domain = [Ergebnis]
            range = [Objektuntersuchung]
            inverse_property = führtZu

        class stelltFest(ObjectProperty):
            domain = [Objektuntersuchung]
            range = [Zustand]
            #inverse_property = wirdFestgestelltDurch

        class wirdFestgestelltDurch(ObjectProperty):
            domain = [Zustand]
            range = [Objektuntersuchung]
            inverse_property = stelltFest

        # zulässig?
        class zeigtSichDurch(ObjectProperty):
            domain = [Zustand]
            range = [Schadensphänomen]

        # inverse Properties!

        class zeigenAn(ObjectProperty):
            domain = [Schadensphänomen]
            range = [Zustand]

        class hatUrsache(ObjectProperty):
            domain = [Schadensphänomen]
            range = [Schadensursache]

        class bedingt(ObjectProperty):
            domain = [Zustand]
            range = [Restaurierungskonzept]
            #inverse_property = beziehtSichAuf

        class beziehtSichAuf(ObjectProperty):
            domain = [Restaurierungskonzept]
            range = [Zustand]
            inverse_property = bedingt

        class erstellt(ObjectProperty):
            domain = [RestauratorIn]
            range = [Restaurierungskonzept]
            #inverse_property = wirdErstelltVon

        class wirdErstelltVon(ObjectProperty):
            domain = [Restaurierungskonzept]
            range = [RestauratorIn]
            inverse_property = erstellt

        class bestehtAus(ObjectProperty):
            domain = [Objekt]
            range = [Material]
        
        class wurdeHergestelltDurch(ObjectProperty):
            domain = [Objekt]
            range = [Herstellungstechnik]
            #inverse_property = gibtAuskunftÜber

        class gibtAuskunftÜber(ObjectProperty):
            domain = [Herstellungstechnik]
            range = [Objekt]
            inverse_property = wurdeHergestelltDurch

        class benutzt(ObjectProperty):
            domain = [RestauratorIn]
            range = [Werkzeug]

        class verwendet(ObjectProperty):
            domain = [Materialanalyse]
            range = [Werkzeug]
            #inverse_property = wirdVerwendet

        class wirdVerwendet(ObjectProperty):
            domain = [Werkzeug]
            range = [Materialanalyse]
            inverse_property = verwendet

        class hat(ObjectProperty):
            domain = [Materialanalyse, praktischeMaßnahme]
            range = [Methode]

        class gibtAn(ObjectProperty):
            domain = [Ergebnis]
            range = [Material]

        class gebraucht(ObjectProperty):
            domain = [praktischeMaßnahme]
            range = [Material, Werkzeug]
            #inverse_property = wirdGebrauchtFür

        class wirdGebrauchtFür(ObjectProperty):
            domain = [Material, Werkzeug]
            range = [praktischeMaßnahme]
            inverse_property = gebraucht

    # Speichern der Ontologie als RDF/XML-Datei im Verzeichnis
    onto.save(file = path, format = "rdfxml")
    sync_reasoner() #infer_property_values = True

def appendTitle(title):
    g = rdflib.Graph()
    g.parse("files/ontology.owl")
    # find tripe with type owl:Ontology
    g.update("""INSERT DATA { <http://www.conservationontology.com/conservationontology.owl> rdfs:label 'LEIZA Restaurierungs- und Konservierungsontologie'@de } """)
    g.serialize(destination='files/ontology.owl', format='xml')

def createNodesEdges():
    # load ontology.owl and convert it to json-ld with rdflib
    g = rdflib.Graph()
    g.parse("files/ontology.owl")
    g.serialize(destination='files/ontology.json', format='json-ld')

    # load ontology.json and create a node and a link array for d3.js
    with open('ontology.json') as f:
        data = json.load(f)

    nodes = []
    links = []

    for i in data:
        if i['@type'] == ["http://www.w3.org/2002/07/owl#Class"]:
            nodes.append({'id': i['@id'], 'label': i['@id'].split("#")[-1]})
        elif i['@type'] == ["http://www.w3.org/2002/07/owl#ObjectProperty"]:
            #nodes.append({'id': i['@id'].split("#")[-1], 'label': i['@id'].split("#")[-1]})
            for j in i["http://www.w3.org/2000/01/rdf-schema#domain"]:
                for k in i["http://www.w3.org/2000/01/rdf-schema#range"]:
                    links.append({'from': j['@id'], 'to': k['@id'], 'id': i["@id"],'label': i['@id'].split("#")[-1]})
    with open('files/NodesEdges.json', 'w') as f:
        json.dump({"nodes":nodes,"links":links}, f)

def getSubclasses(parent, data):
    return data[data["parent"] == parent]["prefLabel"].tolist()

def populateInstances():

    # load ontology.owl with owlready2 from file
    onto = get_ontology("files/ontology.owl").load()
    data =pd.read_csv("files/thesaurus.csv")
    # create a list of all values for preflabel for columns with the value "D941BB" in the column parent
    """
    instancePopulationTuples = [("D941BB", onto.manuellesWerkzeug),
                                ("GF9C49", onto.technischesGerät),
                                ("DAC996", onto.Schadensphänomen)
                                ]
    for tuple in instancePopulationTuples:
        instanceList = getSubclasses(tuple[0])
        for entry in instanceList:
            newInstance = tuple[1](entry)
            print(newInstance)
    """
    manuelleWerkzeuge = getSubclasses("D941BB", data)
    technischeGeräte = getSubclasses("GF9C49", data)
    schadensphänomene = getSubclasses("DAC996", data)
    werkstoffe = getSubclasses("B51DAF", data)
    zustände = getSubclasses("GDF8C2", data)
    #technologischeAuswertungen = getSubclasses("G76B7G", data)
    #untersuchungsMethoden = getSubclasses("D4A13D", data)
    materialAnalysen = getSubclasses("G9B788", data)
    maßnahmen = getSubclasses("C79561", data) + getSubclasses("G98FD4", data)
    #untersuchungsErgebnisse = getSubclasses("BC5B57", data)
    untersuchungen = getSubclasses("CA1BC5", data)
    schadensursachen = getSubclasses("F964CG", data)

    for instanz in manuelleWerkzeuge:
        instanz = onto.manuellesWerkzeug(instanz)
    for instanz in technischeGeräte:
        instanz = onto.technischesGerät(instanz)
    for instanz in schadensphänomene:
        instanz = onto.Schadensphänomen(instanz)
    for instanz in werkstoffe:
        instanz = onto.Material(instanz)
    for instanz in zustände:
        instanz = onto.Zustand(instanz)
    #for instanz in technologischeAuswertungen:
    #    instanz = onto.technologischeAuswertung(instanz)
    #for instanz in untersuchungsMethoden:
    #    instanz = onto.Methode(instanz)
    for instanz in materialAnalysen:
        instanz = onto.Materialanalyse(instanz)
    for instanz in maßnahmen:
        instanz = onto.praktischeMaßnahme(instanz)
    #for instanz in untersuchungsErgebnisse:
    #    instanz = onto.Ergebnis(instanz)
    for instanz in untersuchungen:
        instanz = onto.Objektuntersuchung(instanz)
    for instanz in schadensursachen:
        instanz = onto.Schadensursache(instanz)
    

    # Speichern der Ontologie als RDF/XML-Datei im Verzeichnis
    onto.save(file = "files/ontologyWithInstances.owl", format = "rdfxml")
    sync_reasoner() #infer_property_values = True

def checkOntology():
    onto = get_ontology("files/ontologyWithInstances.owl").load()
    with onto:
        sync_reasoner()
        onto.save(file = "files/ontologyWithInstances.owl", format = "rdfxml")

def createInstances():
    onto = get_ontology("files/ontologyWithInstances.owl").load()
    with onto:
        class wirdDurchgeführtAn(ObjectProperty):
            domain = [onto.Eingriff]
            range = [onto.Objekt]
        kristinaFella = onto.RestauratorIn("KristinaFella")
        restaurierungsEingriff = onto.Restaurierung("RestaurierungsEingriff")
        objektInstanz = onto.Objekt("ObjektInstanz")
        kristinaFella.führtDurch.append(restaurierungsEingriff)
        restaurierungsEingriff.wirdDurchgeführtAn.append(objektInstanz)
        #print(kristinaFella.führtDurch[0].wirdDurchgeführtAn)
        #print(onto.Konservierung.wirdDurchgeführtVon.domain)
        onto.save(file = "files/ontologyWithSpecificInstances.owl", format = "rdfxml")

def rdf2jsonld(file, type):
    g = rdflib.Graph()
    g.parse(file)
    g.serialize(destination=file.split(".")[0]+"."+type, format=type)

def OntologyToHTML(ontologyPath):
    # initialise
    od = OntPub(ontology=ontologyPath)
    # produce HTML
    html = od.make_html()
    # or save HTML to a file
    od.make_html(destination=ontologyPath.split(".")[0]+".html")

#downloadThesaurus()
#createOntology("files/ontology.owl")
#appendTitle("Restaurierungs- und Konservierungsontologie")
#createNodesEdges()
#populateInstances()
#checkOntology()
#createInstances()
rdf2jsonld("files/ontology.owl", "json-ld")
#OntologyToHTML("files/ontologyWithInstances.owl")