import data_extractor

#used in dependency_sentimenter
class Comment:
    def __init__(self, sentence):
        self.sentence = sentence
        parsed = data_extractor.dependency_parse(sentence)
        if parsed['edges'] == []:
            self.connections = []
            self.properties = []
        else:
            edges0 = parsed['edges']
            edges = next((item['edges'][0] for item in edges0 if
                          item['layer'] == 'se.lth.cs.docforia.graph.text.DependencyRelation'))
            self.properties = [item['relation'] for item in edges['properties']]
            size = len(self.properties)
            connections = edges['connections']
            conn_tuples = [None] * size
            for i in range(0, size * 2, 2):
                conn_tuples[int(i / 2)] = (connections[i] - 1, connections[i + 1] - 1)  # -1 because indices start at 1
            self.connections = conn_tuples

        if parsed['nodes'] == []:
            self.tags = []
            self.lemmas = []
            self.pos = []
        else:
            nodes0 = parsed['nodes']
            nodes = next(
                (item['nodes'][0] for item in nodes0 if item['layer'] == 'se.lth.cs.docforia.graph.text.Token'))
            properties = nodes['properties']
            self.tags = [word['cpostag'] for word in properties]
            self.lemmas = [word['lemma'] for word in properties]
            self.pos = [word['pos'] for word in properties]
        self.size = len(self.tags)
