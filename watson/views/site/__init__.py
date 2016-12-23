from flask import request, render_template, redirect, url_for, flash, abort, Blueprint
from os.path import basename
from flask.ext.login import login_required, current_user
from watson.modules.watson import Watson
from watson.modules.annotations import Annotations


site = Blueprint('site', __name__, url_prefix='/site')


@site.route('/')
@site.route('/home')
def v_index():
    pass


@site.route('/artworks')
def v_artworks():
    watson = Watson(
        api_id='',
        api_username='',
        api_password='',
        corpus_name='artworks'
    )
    artworks = []
    for document_id in watson.get_documents()['documents']:
        document_name = basename(document_id)
        document = watson.get_document(document_name)
        artworks.append({
            'name': document_name,
            'label': document['label']
        })
    return render_template('artworks/list.html', artworks=artworks)


@site.route('/artworks/documents', methods=['GET', 'POST'])
def v_submit_document():
    pass


@site.route('/artworks/annotations')
def v_annotations():
    pass


@site.route('/artworks/document/<document_id>/annotations')
def v_document_annotations(document_id):
    watson = Watson(
        api_id='',
        api_username='',
        api_password='',
        corpus_name='artworks'
    )
    document = watson.get_document(document_id)
    annotation_api = Annotations(watson.get_annotations(document_id))
    artwork = {
        'name': document['label'],
        'annotations': annotation_api.filter()
    }
    return render_template('artworks/annotations.html', artwork=artwork)
