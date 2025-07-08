// emotional_support_app/static/script.js
async function submitEntry() {
  const entry = document.getElementById("entry").value;
  const responseDiv = document.getElementById("response");
  const res = await fetch("/journal", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ entry })
  });
  const data = await res.json();
  responseDiv.innerHTML = `
    <p><strong>Sentiment:</strong> ${data.sentiment.label}</p>
    <p><strong>Affirmation:</strong> ${data.affirmation}</p>
  `;
}
