import requests
from urllib.parse import urljoin
import time


class Watson:
    def __init__(self, api_username, api_password, api_id, corpus_name):
        self.url = \
            'https://gateway.watsonplatform.net/concept-insights/api/v2/corpora/{api_id}/{corpus_name}/documents/' \
                .format(api_id=api_id, corpus_name=corpus_name)
        self.api_username = api_username
        self.api_password = api_password

    def submit_document(self, name, label, part_content_type, part_name, part_data):
        document = {
            'label': label,
            'parts': [
                {
                    'name': part_name,
                    'data': part_data,
                    'content-type': part_content_type
                }
            ]
        }
        response = requests.post(urljoin(self.url, name), data=document, auth=(self.api_username, self.api_password))
        return response.json()

    def get_annotations(self, document_name):
        url = urljoin(self.url, document_name) + '/processing_state'
        response = requests.get(url, auth=(self.api_username, self.api_password))
        parsed = response.json()
        status = parsed['status']
        while status == 'processing':
            response = requests.get(url, auth=(self.api_username, self.api_password))
            parsed = response.json()
            if parsed['status'] == 'ready':
                status = 'ready'
            elif parsed['status'] == 'error':
                raise Exception(parsed['error'])
            time.sleep(10)
        annotation_response = requests.get(urljoin(self.url, document_name) + '/annotations',
                                           auth=(self.api_username, self.api_password))
        annotation_parsed = annotation_response.json()
        return annotation_parsed['annotations']

    def get_documents(self):
        response = requests.get(self.url, auth=(self.api_username, self.api_password))
        return response.json()

    def get_document(self, document_name):
        response = requests.get(urljoin(self.url, document_name), auth=(self.api_username, self.api_password))
        return response.json()
