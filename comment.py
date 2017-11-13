import data_extractor

class Comment:
    def __init__(self,sentence):
        self.sentence = sentence
        parsed = data_extractor.dependency_parse(sentence)
        if parsed['edges'] == []:
            self.connections = []
            self.properties = []
        else:
            edges0 = parsed['edges']
            edges = next((item['edges'][0] for item in edges0 if item['layer'] == 'se.lth.cs.docforia.graph.text.DependencyRelation'))
            self.connections = edges['connections']
            self.properties = [item['relation'] for item in edges['properties']]

        if parsed['nodes'] == []:
            self.tags = []
            self.lemmas = []
            self.pos = []
        else:
            nodes0 = parsed['nodes']
            nodes = next((item['nodes'][0] for item in nodes0 if item['layer'] == 'se.lth.cs.docforia.graph.text.Token'))
            properties = nodes['properties']
            self.tags = [word['cpostag'] for word in properties]
            self.lemmas = [word['lemma'] for word in properties]
            self.pos = [word['pos'] for word in properties]