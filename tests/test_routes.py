import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()


TEXT = 'Cats are great pets. They sleep a lot. Dogs need more walks. Fish are quiet. Birds sing every morning.'


def test_pages_load(client):
    for url in ['/', '/how-it-works', '/about']:
        assert client.get(url).status_code == 200


def test_404_page(client):
    response = client.get('/this-does-not-exist')
    assert response.status_code == 404
    assert b'does not exist' in response.data


def test_home_form_shows_summary(client):
    response = client.post('/', data={'text': TEXT, 'length': 'short'})
    assert response.status_code == 200
    assert b'Cats are great pets.' in response.data


def test_home_form_empty_text(client):
    response = client.post('/', data={'text': '   '})
    assert b'Please enter some text' in response.data


def test_api_summarize(client):
    response = client.post('/api/summarize', json={'text': TEXT, 'length': 'long'})
    data = response.get_json()
    assert response.status_code == 200
    assert data['summary_count'] <= data['original_count']


def test_api_bad_length(client):
    response = client.post('/api/summarize', json={'text': TEXT, 'length': 'huge'})
    assert response.status_code == 400


def test_api_text_too_long(client):
    response = client.post('/api/summarize', json={'text': 'a ' * 20000})
    assert response.status_code == 400


def test_old_endpoint_still_works(client):
    response = client.post('/post_summary', json={'textString': TEXT})
    assert 'summary' in response.get_json()


def test_html_is_escaped(client):
    response = client.post('/', data={'text': '<script>alert(1)</script> is here. One. Two. Three.'})
    assert b'<script>alert(1)</script>' not in response.data
