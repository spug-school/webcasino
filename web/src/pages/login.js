async function loginCasino(url, username, password) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  } else {
    const data = await response.json();
    localStorage.setItem("token", data.token);
  }
}

export async function Login(req) {
  const root = document.querySelector("#root");
  console.log(req);
  root.innerHTML = `
    <div class="form-container">
    <form action="/login" method="post">
    <label for="username">Username</label>
    <input type="text" name="username" id="username" required />
    <label for="password">Password</label>
    <input type="password" name="password" id="password" required />
    <button>Log In</button>
    </form>
    </div>
    `;
  const form = root.querySelector("form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const username = event.currentTarget.username.value;
    const password = event.currentTarget.password.value;
    await loginCasino("http://127.0.0.1:5000/api/login", username, password);
    console.log("yo");
    return (window.location.href = "/");
  });
}
