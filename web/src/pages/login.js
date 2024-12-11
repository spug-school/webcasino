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
  const data = await response.json();

  if (!response.ok) {
    const errorMsg = document.querySelector("#login-error-msg");
    errorMsg.textContent = data?.message || "Virhe kirjautumisessa!";
    return false
  } else {
    localStorage.setItem("token", data.token);
    localStorage.setItem("user_id", data.user_id);
    return true
  }
}

export async function Login(req) {
  const root = document.querySelector("#root");
  root.innerHTML = `
    <div class="form-container">
    <h2>Pelaaja</h2>
    <form action="/login" method="post">
    <label for="username">Pelinimi</label>
    <input type="text" name="username" id="username" placeholder="Pelinimi*" required />
    <label for="password">Salasana</label>
    <input type="password" name="password" id="password" placeholder="Salasana*" required />
    <p id="login-error-msg"></p>
    <button>Sisään!</button>
    </form>
    </div>
    `;
  const form = root.querySelector("form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const username = event.currentTarget.username.value;
    const password = event.currentTarget.password.value;
    
    const loginOk = await loginCasino("http://127.0.0.1:5000/api/login", username, password);

    if (loginOk) return (window.location.href = "/games");
  });
}
