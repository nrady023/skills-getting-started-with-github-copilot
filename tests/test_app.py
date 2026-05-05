def test_get_activities(client):
    """Test GET /activities returns all activities with expected structure."""
    # Arrange
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Soccer Team",
        "Basketball Club", "Art Studio", "Drama Workshop", "Debate Team", "Science Club"
    ]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert set(data.keys()) == set(expected_activities)
    for activity_name, activity_data in data.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_signup_for_activity_success(client):
    """Test POST /activities/{activity_name}/signup successfully adds a participant."""
    # Arrange
    activity_name = "Soccer Team"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": f"Signed up {email} for {activity_name}"}
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_for_activity_duplicate(client):
    """Test POST /activities/{activity_name}/signup returns 400 for duplicate signup."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data == {"detail": "Student already signed up for this activity"}


def test_signup_for_activity_not_found(client):
    """Test POST /activities/{activity_name}/signup returns 404 for nonexistent activity."""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "Activity not found"}


def test_delete_participant_success(client):
    """Test DELETE /activities/{activity_name}/participants/{email} removes a participant."""
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"  # Already signed up
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": f"Removed {email} from {activity_name}"}
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_delete_participant_not_found(client):
    """Test DELETE /activities/{activity_name}/participants/{email} returns 404 for missing participant."""
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "Participant not found"}


def test_delete_participant_activity_not_found(client):
    """Test DELETE /activities/{activity_name}/participants/{email} returns 404 for nonexistent activity."""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "Activity not found"}