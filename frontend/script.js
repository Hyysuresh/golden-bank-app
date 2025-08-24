// Function to handle form submission for both forms
function handleFormSubmission(event) {
    event.preventDefault();

    let username, password, url;
    const message = document.getElementById('message');

    // Check which form was submitted
    if (event.target.id === 'loginForm') {
        username = document.getElementById('username').value;
        password = document.getElementById('password').value;
        url = '/login';
    } else if (event.target.id === 'registerForm') {
        username = document.getElementById('reg-username').value;
        password = document.getElementById('reg-password').value;
        url = '/register';
    } else {
        return;
    }

    // Clear previous message
    message.textContent = '';

    // Send the request to the backend through Nginx
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
    .then(response => response.json().then(data => ({
        status: response.status,
        body: data
    })))
    .then(result => {
        message.textContent = result.body.message;
        if (result.status === 200) {
            if (event.target.id === 'loginForm') {
                window.location.href = 'home.html';
            } else if (event.target.id === 'registerForm') {
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 2000);
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        message.textContent = 'An error occurred. Please try again.';
    });
}

// Add event listeners for both forms
document.getElementById('loginForm')?.addEventListener('submit', handleFormSubmission);
document.getElementById('registerForm')?.addEventListener('submit', handleFormSubmission);

// Add event listener for the logout button
document.getElementById('logout-btn')?.addEventListener('click', () => {
    window.location.href = 'index.html';
});

