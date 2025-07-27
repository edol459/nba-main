window.addEventListener("DOMContentLoaded", () => {
  const teamDropdown = document.getElementById("teamSelector");
  const gameDropdown = document.getElementById("gameSelector");

  teamDropdown.addEventListener("change", async () => {
    const team = teamDropdown.value;
    gameDropdown.innerHTML = `<option>Loading games...</option>`;
    gameDropdown.disabled = true;

    if (!team) return;

    const res = await fetch(`/api/games/${team}`);
    const games = await res.json();

    if (games.error) {
      gameDropdown.innerHTML = `<option>Error loading games</option>`;
      return;
    }

    gameDropdown.innerHTML = `<option value="">Select a game</option>`;
    games.forEach(game => {
      const option = document.createElement("option");
      option.value = game.game_id;
      option.textContent = `${team} vs ${game.opponent} (${game.date})`;
      gameDropdown.appendChild(option);
    });

    gameDropdown.disabled = false;
  });

  gameDropdown.addEventListener("change", () => {
    const gameId = gameDropdown.value;
    if (gameId) loadGameOutliers(gameId);
  });
});

function loadGameOutliers(gameId) {
  document.getElementById("output").innerHTML = `<p>Loading game...</p>`;

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
  
  // Generate player headshot URL if player_id exists
  let imgTag = '';
    if (outlier.type === 'player' && outlier.player_id){
      const imgUrl = `https://cdn.nba.com/headshots/nba/latest/1040x760/${outlier.player_id}.png`;
      imgTag = `<img src="${imgUrl}" class="player-headshot" alt="${outlier.name}" />`;
     } else if (outlier.type === 'team' && outlier.team_abbr) {
      const teamLogoUrl = `logos/${outlier.team_abbr}.svg`; 
      imgTag = `<img src="${teamLogoUrl}" class="team-logo-mini" alt="${outlier.name} logo" />`;
    }

    
    const label = `
      ${imgTag}
      <b>${outlier.name}</b><br>
      ${outlier.stat.split(" - ")[1]}<br>
      Actual: ${outlier.actual} ${outlier.stat.split(" - ")[1]}<br>
      Average: ${outlier.avg} ${outlier.stat.split(" - ")[1]}<br>
      Score: ${outlier.score}
    `;


  return `
    <div class="${bar}" style="height:${height}px;">
      <span class="bar-label">${label}</span>
    </div>
  `;
}