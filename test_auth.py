import pytest

# Test the home page
def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Login' in response.data

# Test user registration
def test_register_user(client):
    """Test that a new user can be registered."""
    response = client.post('/register', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'registration Successful!! Please Login' in response.data

def test_register_existing_user(client):
    """Test that registering an existing user fails."""
    client.post('/register', data={'username': 'testuser', 'password': 'password'})
    response = client.post('/register', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
    assert b'Username already taken.' in response.data

# Test user login
def test_login_success(client):
    """Test successful login."""
    client.post('/register', data={'username': 'testuser', 'password': 'password'})
    response = client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'User Logged in Successfully' in response.data

def test_login_invalid_password(client):
    """Test login with incorrect password."""
    client.post('/register', data={'username': 'testuser', 'password': 'password'})
    response = client.post('/login', data={'username': 'testuser', 'password': 'wrong-password'}, follow_redirects=True)
    assert b'Invalid Credentials' in response.data

# Test authenticated routes
def test_tasks_list_requires_login(client):
    """Test that the tasks page redirects to login if not authenticated."""
    response = client.get('/tasks')
    assert response.status_code == 302 # Redirect status code
    assert '/login' in response.headers['Location']

def test_tasks_list_shows_for_logged_in_user(client):
    """Test that tasks are shown for a logged-in user."""
    client.post('/register', data={'username': 'testuser', 'password': 'password'})
    client.post('/login', data={'username': 'testuser', 'password': 'password'})
    response = client.get('/tasks')
    assert response.status_code == 200
    assert b'User Logged in Successfully' in response.data

# Test adding a task
def test_add_task(client):
    """Test adding a task for a logged-in user."""
    client.post('/register', data={'username': 'testuser', 'password': 'password'})
    client.post('/login', data={'username': 'testuser', 'password': 'password'})
    response = client.post('/tasks/add', data={'description': 'Test task 1'}, follow_redirects=True)
    assert b'Task Added Successfully' in response.data

# Test deleting a task
def test_delete_task(client):
    """Test that a user can delete their own task."""
    client.post('/register', data={'username': 'testuser', 'password': 'password'})
    client.post('/login', data={'username': 'testuser', 'password': 'password'})
    client.post('/tasks/add', data={'description': 'Task to be deleted'})
    
    # Get the task ID from the app's in-memory data
    from AUTH.Authentication import users, tasks
    user_id = next(iter(users.keys()))
    task_id = tasks[user_id][0]['id']
    
    response = client.post(f'/tasks/delete/{task_id}', follow_redirects=True)
    assert b'Task Deleted Successfully!!' in response.data

    
# # Test authorization failure (deleting a task that doesn't exist or is not owned)
def test_delete_non_existent_task(client):
    """Test that attempting to delete a non-existent task fails gracefully."""
    client.post('/register', data={'username': 'testuser', 'password': 'password'})
    client.post('/login', data={'username': 'testuser', 'password': 'password'})
    response = client.post('/tasks/delete/non-existent-id', follow_redirects=True)
    assert b'Task Not found or you dont have permission to delete this task' in response.data