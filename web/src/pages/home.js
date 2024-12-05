async function getData(url) {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

export async function Home(req) {
  const root = document.querySelector("#root");
  root.innerHTML = `
    <div class="render">
      <canvas></canvas>
    </div>
    <div class="messages">
      <h3>Messages</h3>
    </div>
    <div class="control">
      <div class="inner-control">
          <h3>Control</h3>
      </div>
    </div>
      `;
  try {
    const data = await getData("http://127.0.0.1:5000/api/");
    const p = document.createElement("p");
    p.innerHTML = data.path;
    root.append(p);
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}
