function loadGame() {
  const gameId = document.getElementById("gameIdInput").value;
  fetch(`../backend/output/${gameId}.json`)
    .then(res => res.json())
    .then(data => renderOutliers(data))
    .catch(err => {
      document.getElementById("output").innerHTML = `<p>Error: ${err}</p>`;
    });
}

function renderOutliers(data) {
  const outliers = data.outliers[0];
  const posBars = outliers.positive.map((out, i) => makeBar(out, false, i)).join('');
  const negBars = outliers.negative.map((out, i) => makeBar(out, true, i)).join('');

  document.getElementById("output").innerHTML = `
    <h2>Outliers for ${data.teams[0]} vs. ${data.teams[1]}</h2>
    <div class="timeline-container">
      <div class="outlier-column negative">${negBars}</div>
      <div class="timeline-center"></div>
      <div class="outlier-column positive">${posBars}</div>
    </div>
  `;
}


function makeBar(out, isNegative, rank) {
  const heights=[500,400,300,200,100]
  const height = heights[rank] || 100

  return `
    <div class="bar-wrapper">
      <div class="bar ${isNegative ? 'negative' : 'positive'}" style="height: ${height}px"></div>
      <div class="bar-label">
        ${out.stat}<br>
        actual: ${out.actual}, avg: ${out.avg}
      </div>
    </div>
  `;
}
