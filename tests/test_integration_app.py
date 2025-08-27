def test_hello_world(client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Echo User Input' in response.data

def test_echo_input(client):
        # Send a POST request to the /echo_user_input route
        response = client.post('/echo_user_input', data={'user_input': 'test_user'})

        # Assert the response
        assert response.status_code == 200
        assert b"test_user" in response.data

def test_get_roster(client, mocker):
        # Mock the Sleeper API functions
        mocker.patch('app.get_user', return_value={'user_id': '12345'})
        mocker.patch('app.get_user_leagues', return_value=[{'league_id': '67890'}])
        mocker.patch('app.get_roster_ids', return_value=[{'roster_id': 1, 'owner_id': '12345'}])
        mocker.patch('app.get_roster_by_id', return_value={'players': ['player1', 'player2']})

        # Send a POST request to the /get_roster route
        response = client.post('/get_roster', data={'sleeper_username': 'test_user'})
        print(response.data)    

        # Assert the response
        assert response.status_code == 200
        assert b"roster" in response.data