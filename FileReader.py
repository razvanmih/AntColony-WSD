import untangle as tr


class SemEvalParser:
    path = 'eng-coarse-all-words.xml'
    tree = tr.Element('None', ['none'])

    text_ids = []
    instances = []

    def __init__(self):
        self.tree = tr.parse(self.path)
        self.index = 0
        self.text_ids = self.get_text_ids()
        self.instances = self.get_all_instances()

    def get_text_ids(self):
        ids = []
        for text in self.tree.corpus.text:
            ids.append(text['id'])
        return ids

    def get_text_by(self, id):
        for text in self.tree.corpus.text:
            if text['id'] == id:
                return text

    def get_all_sentences_from(self, text_id):
        return self.get_text_by(text_id).sentence

    def get_all_instances_from(self, text_id):
        all_instances = []
        sentences = [sentence for sentence in self.get_all_sentences_from(text_id)]
        for sentence in sentences:
            instances = sentence.children
            for instance in instances:
                id = instance['id']
                lemma = instance['lemma']
                all_instances.append((id, lemma))
        return all_instances

    def get_all_instances(self):
        all_instances = []
        for text_id in self.get_text_ids():
            for instance in self.get_all_instances_from(text_id):
                all_instances.append(instance)
        return all_instances

    def next_instance(self):
        all_instances = self.instances
        if len(all_instances) > self.index:
            instance = all_instances[self.index]
            self.index += 1
            return instance

    def reset_index(self):
        self.index = 0

    def get_instance_for(self, index):
        all_instances = self.instances
        if len(all_instances) > index:
            return all_instances[index]

    def get_instances_by(self, text=None, sentence=None, instance=None):
        id = ""
        if text != None:
            id = text
        if sentence != None:
            id = sentence
        if instance != None:
            id = instance
        return [instance for instance in self.instances if id in instance[0]]

    def get_sentences_ids_by(self, text_id):
        sentences = self.get_all_sentences_from(text_id)
        return [sentence['id'] for sentence in sentences]
