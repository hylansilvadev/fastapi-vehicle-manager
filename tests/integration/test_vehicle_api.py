from fastapi.testclient import TestClient


def test_create_vehicle(client: TestClient):
    response = client.post(
        '/vehicles/',
        json={
            'marca': 'Toyota',
            'modelo': 'Corolla',
            'placa': 'ABC-1234',
            'ano': '2022',
            'cor': 'Prata',
            'preco': '120000.0',
            'proprietario': 'Joao Silva',
            'km': '15000',
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data['marca'] == 'Toyota'
    assert data['placa'] == 'ABC-1234'
    assert 'id' in data


def test_create_vehicle_duplicate_placa(client: TestClient):
    payload = {
        'marca': 'Honda',
        'modelo': 'Civic',
        'placa': 'XYZ-9876',
        'ano': '2021',
        'cor': 'Preto',
        'preco': '110000.0',
        'proprietario': 'Maria Souza',
        'km': '30000',
    }
    # Cria o primeiro
    response1 = client.post('/vehicles/', json=payload)
    assert response1.status_code == 201

    # Tenta criar o segundo com a mesma placa
    response2 = client.post('/vehicles/', json=payload)
    # Deve retornar conflito (409)
    assert response2.status_code == 409


def test_get_vehicles(client: TestClient):
    # Cria alguns veículos
    client.post(
        '/vehicles/',
        json={
            'marca': 'Fiat',
            'modelo': 'Uno',
            'placa': 'AAA-1111',
            'ano': '2010',
            'cor': 'Branco',
            'preco': '20000.0',
            'proprietario': 'José',
            'km': '100000',
        },
    )
    client.post(
        '/vehicles/',
        json={
            'marca': 'Ford',
            'modelo': 'Ka',
            'placa': 'BBB-2222',
            'ano': '2015',
            'cor': 'Vermelho',
            'preco': '30000.0',
            'proprietario': 'Ana',
            'km': '80000',
        },
    )

    response = client.get('/vehicles/')
    assert response.status_code == 200
    data = response.json()

    if isinstance(data, dict) and 'items' in data:
        assert len(data['items']) >= 2
    else:
        assert len(data) >= 2


def test_get_vehicle_by_id(client: TestClient):
    # Cria um veículo
    create_response = client.post(
        '/vehicles/',
        json={
            'marca': 'Chevrolet',
            'modelo': 'Onix',
            'placa': 'CCC-3333',
            'ano': '2020',
            'cor': 'Azul',
            'preco': '60000.0',
            'proprietario': 'Carlos',
            'km': '50000',
        },
    )
    vehicle_id = create_response.json()['id']

    # Busca por ID
    get_response = client.get(f'/vehicles/{vehicle_id}')
    assert get_response.status_code == 200
    assert get_response.json()['id'] == vehicle_id


def test_get_vehicle_not_found(client: TestClient):
    import uuid

    fake_id = str(uuid.uuid4())
    response = client.get(f'/vehicles/{fake_id}')
    assert response.status_code == 404


def test_update_vehicle(client: TestClient):
    # Cria um veículo
    create_response = client.post(
        '/vehicles/',
        json={
            'marca': 'Jeep',
            'modelo': 'Compass',
            'placa': 'DDD-4444',
            'ano': '2023',
            'cor': 'Cinza',
            'preco': '150000.0',
            'proprietario': 'Luiz',
            'km': '5000',
        },
    )
    vehicle_id = create_response.json()['id']

    # Atualiza parcialmente (PATCH)
    update_response = client.patch(
        f'/vehicles/{vehicle_id}', json={'cor': 'Preto', 'preco': '145000.0'}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data['cor'] == 'Preto'
    assert data['preco'] == '145000.0'


def test_delete_vehicle(client: TestClient):
    # Cria um veículo
    create_response = client.post(
        '/vehicles/',
        json={
            'marca': 'Hyundai',
            'modelo': 'HB20',
            'placa': 'EEE-5555',
            'ano': '2019',
            'cor': 'Branco',
            'preco': '50000.0',
            'proprietario': 'Pedro',
            'km': '60000',
        },
    )
    vehicle_id = create_response.json()['id']

    # Deleta
    delete_response = client.delete(f'/vehicles/{vehicle_id}')
    assert delete_response.status_code == 204

    # Verifica se foi deletado mesmo
    get_response = client.get(f'/vehicles/{vehicle_id}')
    assert get_response.status_code == 404


def test_get_vehicles_with_filters(client: TestClient):
    response = client.get('/vehicles/?marca=Fiat&ano=2010&order_dir=asc')
    assert response.status_code == 200
