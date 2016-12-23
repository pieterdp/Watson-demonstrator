

class Annotations:

    def __init__(self, annotations):
        self.annotations = annotations
        self.threshold = 0.5

    def filter(self):
        """
        Remove double annotations and everything lower than self.threshold
        :return:
        """
        filtered = {}
        for annotation in self.annotations[0]:
            annotation_id = annotation['concept']['id']
            if annotation['score'] <= self.threshold:
                continue
            if annotation_id in filtered:
                filtered[annotation_id]['text_index'] = filtered[annotation_id]['text_index'] + annotation['text_index']
            else:
                filtered[annotation_id] = {
                    'id': annotation_id,
                    'label': annotation['concept']['label'],
                    'score': annotation['score'],
                    'text_index': annotation['text_index']
                }
        list_filtered = []
        for key, annotation in filtered.items():
            list_filtered.append(annotation)
        return sorted(list_filtered, key=lambda ann: ann['score'], reverse=True)
