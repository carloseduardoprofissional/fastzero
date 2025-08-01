import json
from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_read_html_deve_retornar_ok_e_html(client):
    response = client.get('/text')

    assert response.status_code == HTTPStatus.OK
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert '<h1>Olá, FastAPI!</h1>' in response.text


def test_create_user_deve_retornar_created_e_usuario(client):
    user_data = {
        'name': 'Carlos Eduardo',
        'email': 'carlos@email.com',
        'password': 'string',
    }

    response = client.post('/users/', json=user_data)
    response_dict = json.loads(response.text)
    assert response.status_code == HTTPStatus.CREATED
    assert response_dict['id'] > 0
    assert response.json()['name'] == user_data['name']
    assert response_dict['email'] == user_data['email']
    assert 'password' not in response_dict  # Ensure password is not returned
    assert response.headers['content-type'] == 'application/json'


def test_read_users_deve_retornar_lista_de_usuarios(client):
    response = client.get('users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['users'] == [
        {'id': 1, 'name': 'Carlos Eduardo', 'email': 'carlos@email.com'}
    ]


def test_crget_user_deve_retornar_usuario_by_idtask(client):
    user_data = {'id': 1, 'name': 'Carlos Eduardo', 'email': 'carlos@email.com'}

    response = client.get('users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_data


def test_get_user_deve_retornar_usuario_not_found_quando_usuario_nao_existir(client):
    response = client.get('users/-1')
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_user_deve_retornar_usuario_atualizado(client):
    user_data = {
        'name': 'Carlos Eduardo',
        'email': 'carlos@email.com',
        'password': 'string',
    }

    response = client.put('users/1', json=user_data)
    user_data['id'] = 1
    del user_data['password']  # Ensure password is not returned
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_data


def test_update_user_deve_retornar_usuario_not_found_quando_usuario_nao_existir(client):
    user_data = {
        'name': 'Carlos Eduardo',
        'email': 'carlos@email.com',
        'password': 'string',
    }
    response = client.put('users/222', json=user_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_user_deve_retornar_ok(client):
    response = client.delete('users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User successfully deleted'}


def test_delete_user_deve_retornar_usuario_not_found_quando_usuario_nao_existir(client):
    response = client.delete('users/-1')
    assert response.status_code == HTTPStatus.BAD_REQUEST
