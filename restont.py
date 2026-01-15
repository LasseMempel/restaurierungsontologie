from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD

# Create a new graph
g = Graph()

# Define namespaces
ONTO = Namespace("https://www.w3id.org/archlink/ont/conservationontology#")
CIDOC = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

g.bind("", ONTO)
g.bind("cidoc", CIDOC)
g.bind("owl", OWL)
g.bind("rdfs", RDFS)

# Declare the ontology itself
ontology_uri = URIRef("https://www.w3id.org/archlink/ont/conservationontology")
g.add((ontology_uri, RDF.type, OWL.Ontology))

# Define classes with CIDOC-CRM mappings
class_mappings = {
    "Kollektion": "E78_Curated_Holding",
    "Objekt": "E19_Physical_Object",
    "Objektmaterial": "E57_Material",
    "Zustand": "E3_Condition_State",
    "Schadensphänomen": "E3_Condition_State",
    "Methode": "E7_Activity",
    "Agent": "E39_Actor",
    "Restaurierungsmaterial": "E57_Material",
}

for onto_class, cidoc_class in class_mappings.items():
    g.add((ONTO[onto_class], RDF.type, OWL.Class))
    g.add((ONTO[onto_class], RDFS.subClassOf, CIDOC[cidoc_class]))

# Define Object Properties
properties = {
    "gehört_zu": (ONTO.Objekt, ONTO.Kollektion),
    "besteht_aus": (ONTO.Objekt, ONTO.Objektmaterial),
    "hat_Schaden": (ONTO.Objekt, ONTO.Schadensphänomen),
    "ist_Teil_von": (ONTO.Objekt, ONTO.Objekt),
    "durchgeführt_an": (ONTO.Methode, ONTO.Objekt),
    "durchgeführt_durch": (ONTO.Methode, ONTO.Agent),
    "nutzt_Werkzeug": (ONTO.Methode, ONTO.Objekt),
    "nutzt_Material": (ONTO.Methode, ONTO.Restaurierungsmaterial),
    "ist_Teil_von": (ONTO.Objekt, ONTO.Objekt)
}

for prop_name, (domain, range_) in properties.items():
    prop = ONTO[prop_name]
    g.add((prop, RDF.type, OWL.ObjectProperty))
    g.add((prop, RDFS.domain, domain))
    g.add((prop, RDFS.range, range_))

# Serialize
g.serialize(destination="restorationontology.ttl", format="turtle")

print("Ontology created successfully!")