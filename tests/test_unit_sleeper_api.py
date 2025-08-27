def test_get_user_not_found(client, mocker):
        # Mock the get_user function to return None
        # mocker.patch('app.get_user', return_value=None)

        # Send a POST request to the /get_roster route
        response = client.post('/get_roster', data={'sleeper_username': 'nonexistent_user'})

        # Assert the response
        assert response.status_code == 200
        assert b"User not found" in response.data

def test_get_user_found(client, mocker):
        # Mock the get_user function to return a valid user
        mocker.patch('app.get_user', return_value={'user_id': '12345'})
        mocker.patch('app.get_user_leagues', return_value=[{'league_id': '67890'}])
        mocker.patch('app.get_roster_ids', return_value=[{'roster_id': 1, 'owner_id': '12345'}])
        mocker.patch('app.get_roster_by_id', return_value={'players': ['player1', 'player2']})

        # Send a POST request to the /get_roster route
        response = client.post('/get_roster', data={'sleeper_username': 'existent_user'})

        # Assert the response
        assert response.status_code == 200
        assert b"roster" in response.data
        assert b"player1" in response.data
        assert b"player2" in response.data
