const apiUrl = 'http://localhost:5000';

    // Registration
    document.getElementById('registerForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = document.getElementById('registerUsername').value;
      const password = document.getElementById('registerPassword').value;
      try {
        const response = await fetch(`${apiUrl}/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password }),
        });
        const result = await response.json();
        alert(result.message);
      } catch (err) {
        alert('Registration failed.');
      }
    });

    // Login
  document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const username = document.getElementById('loginUsername').value;
  const password = document.getElementById('loginPassword').value;

  try {
    const response = await fetch(`${apiUrl}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      const result = await response.json();
      alert(result.error || 'Something went wrong.');
      return;
    }

    const result = await response.json();
    console.log('Token:', result.token);

    // Redirect to another page or perform further actions
    alert('Login successful!');
  } catch (err) {
    console.error('Error:', err);
    alert('Network error. Please try again later.');
  }
});
