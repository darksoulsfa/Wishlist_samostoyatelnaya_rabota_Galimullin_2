def test_index(client):
    assert client.get('/').status_code == 200

def test_add(client):
    client.post('/add', data={'name':'Тест','price':'100'})
    assert 'Тест' in client.get('/').data.decode()

def test_search(client):
    client.post('/add', data={'name':'Книга','price':'500'})
    rv = client.get('/search?q=Книга')
    assert rv.status_code == 200

def test_404(client):
    assert client.get('/wish/99999').status_code == 404

def test_validation(client):
    rv = client.post('/add', data={'name':'','price':'abc'})
    assert rv.status_code == 200
