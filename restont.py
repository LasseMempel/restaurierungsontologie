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

# Define classes with superclasses: CIDOC-CRM mappings here but can be internal too...
class_mappings = {
    #"Kollektion": "E78_Curated_Holding",
    "Konservierungs_und_Restaurierungsobjekt": "E19_Physical_Object",
    "Objektmaterial": "E57_Material",
    "Physischer_Objektzustand": "E3_Condition_State",
    "Schadensphänomen": "E3_Condition_State",
    "Behandlungsmethode": "E7_Activity",
    #"Agent": "E39_Actor",
    "Konservierungs_und_Restaurierungsmaterial": "E57_Material",
    "Konservierungs_und_Restaurierungswerkzeug": "E19_Physical_Object"
}

for onto_class, cidoc_class in class_mappings.items():
    g.add((ONTO[onto_class], RDF.type, OWL.Class))
    g.add((ONTO[onto_class], RDFS.label, Literal(onto_class.replace("_", " "), lang="de")))
    g.add((ONTO[onto_class], RDFS.subClassOf, CIDOC[cidoc_class]))

# Define Object Properties
properties = {
    #"gehört_zu": (ONTO.Konservierungs_und_Restaurierungsobjekt, ONTO.Kollektion),
    "besteht_aus": (ONTO.Konservierungs_und_Restaurierungsobjekt, ONTO.Objektmaterial),
    "hat_Schaden": (ONTO.Konservierungs_und_Restaurierungsobjekt, ONTO.Schadensphänomen),
    "hat_Zustand": (ONTO.Konservierungs_und_Restaurierungsobjekt, ONTO.Physischer_Objektzustand),
    "ist_Teil_von": (ONTO.Konservierungs_und_Restaurierungsobjekt, ONTO.Konservierungs_und_Restaurierungsobjekt),
    "durchgeführt_an": (ONTO.Behandlungsmethode, ONTO.Konservierungs_und_Restaurierungsobjekt),
    #"durchgeführt_durch": (ONTO.Behandlungsmethode, ONTO.Agent),
    "nutzt_Werkzeug": (ONTO.Behandlungsmethode, ONTO.Konservierungs_und_Restaurierungswerkzeug),
    "nutzt_Material": (ONTO.Behandlungsmethode, ONTO.Konservierungs_und_Restaurierungsmaterial)
}

for prop_name, (domain, range_) in properties.items():
    prop = ONTO[prop_name]
    g.add((prop, RDF.type, OWL.ObjectProperty))
    g.add((prop, RDFS.domain, domain))
    g.add((prop, RDFS.range, range_))

# Serialize
g.serialize(destination="restorationontology.ttl", format="turtle")

print("Ontology created successfully!")