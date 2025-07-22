// Fetch game list and populate dropdown when page loads
window.addEventListener("DOMContentLoaded", () => {
  fetch('/api/games')
    .then(res => res.json())
    .then(games => {
      const dropdown = document.getElementById("gameDropdown");
      dropdown.innerHTML = ""; // Clear loading option
      games.forEach(game => {
        const option = document.createElement("option");
        option.value = game.game_id;
        option.textContent = `${game.matchup} (${game.date})`;
        dropdown.appendChild(option);
      });
    })
    .catch(err => {
      console.error("Error loading games:", err);
      document.getElementById("output").innerHTML = `<p style="color:red;">Error loading game list.</p>`;
    });
});

// Load outliers for selected game when button is clicked
document.getElementById("loadBtn").addEventListener("click", () => {
  const gameId = document.getElementById("gameDropdown").value;
  if (!gameId) return;
  loadGameOutliers(gameId);
});

function loadGameOutliers(gameId) {
  document.getElementById("output").innerHTML = `<p>Loading data for game ${gameId}...</p>`;

  fetch(`/api/outliers/${gameId}`)
    .then((response) => {
      if (!response.ok) throw new Error("Game not found or error from server.");
      return response.json();
    })
    .then((data) => {
      renderOutliers(data);
    })
    .catch((err) => {
      console.error("Error:", err);
      document.getElementById("output").innerHTML =
        `<p style="color:red;">❌ Error: ${err.message}</p>`;
    });
}

function renderOutliers(data) {
  const outliers = data.outliers[0]; // assumes one payload per game
  const teamA = data.teams[0];
  const teamB = data.teams[1];

  const headerHTML = `
    <h2 class="team-header">
      <img class="team-logo" src="logos/${teamA}.svg" alt="${teamA} logo">
      ${teamA} vs ${teamB}
      <img class="team-logo" src="logos/${teamB}.svg" alt="${teamB} logo">
    </h2>
  `;

  const posBars = outliers.positive.map((out, i) => makeBar(out, false, i)).join('');
  const negBars = outliers.negative.map((out, i) => makeBar(out, true, i)).join('');

  document.getElementById("output").innerHTML = `
    ${headerHTML}
    <div class="timeline-container">
      <div class="outlier-column negative">${negBars}</div>
      <div class="timeline-center"></div>
      <div class="outlier-column positive">${posBars}</div>
    </div>
  `;
}

function makeBar(outlier, isNegative, index) {
  const height = 500 - index * 100; // top bar tallest
  const bar = isNegative ? 'bar negative' : 'bar positive';
  const label = `<b>${outlier.name}</b><br> ${outlier.stat.split(" - ")[1]} <br>Actual: ${outlier.actual} ${outlier.stat.split(" - ")[1]} <br> Average: ${outlier.avg} ${outlier.stat.split(" - ")[1]}`;

  return `
    <div class="${bar}" style="height:${height}px;">
      <span class="bar-label">${label}</span>
    </div>
  `;
}