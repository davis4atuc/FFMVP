def test_hello_world(client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Enter Username' in response.data

# def test_echo_input(client, mocker):
#     # Mock the Sleeper API functions
#     mocker.patch('sleeper_api.get_user', return_value={'user_id': '12345'})
#     mocker.patch('sleeper_api.get_user_leagues', return_value=[{'league_id': '67890'}])
#     mocker.patch('sleeper_api.get_roster_ids', return_value=[{'roster_id': 1, 'owner_id': '12345'}])
#     mocker.patch('sleeper_api.get_user_roster_id', return_value=1)

#     # Send a POST request to the /echo_user_input route
#     response = client.post('/echo_user_input', data={'user_input': 'test_user'})

#     # Assert the response
#     assert response.status_code == 200
#     assert b"username Roster id: 1" in response.data