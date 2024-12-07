async function getData(url) {
  const response = await fetch(url, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

export async function Profile(req) {
  const root = document.querySelector("#root");
  const data = await getData("http://127.0.0.1:5000/api/profile");
  root.innerHTML = `
    <div id="title">
    <h1>My profile</h1>
    </div>
    <div>
    </div>
    </div>
    `;
  // <p>ID: ${data.id}</p>
  // <p>Username: ${data.username}</p>
  console.log(data);
}
