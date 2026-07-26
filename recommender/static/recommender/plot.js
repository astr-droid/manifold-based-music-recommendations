const xs = points.map(p => p.x);
const ys = points.map(p => p.y);
const labels = points.map(p => `${p.name} — ${p.artist}`);
const colors = points.map(() => "#636EFA");

const trace = {
  x: xs,
  y: ys,
  text: labels,
  mode: "markers",
  type: "scatter",
  marker: { size: 6, color: colors },
  hoverinfo: "text",
};

Plotly.newPlot("plot", [trace], {
  title: "UMAP Embedding of Songs",
  hovermode: "closest",
});

document.getElementById("plot").on("plotly_click", function (data) {
  const point = data.points[0];
  const idx = point.pointIndex;
  const clicked = points[idx];

  document.getElementById("selected-info").innerHTML =
    `<p>Selected: <strong>${clicked.name}</strong> by ${clicked.artist}. ` +
    `<a href="/recommend/${clicked.id}/">Get recommendations</a></p>`;

  const newColors = points.map((p) => (p.id === clicked.id ? "#EF553B" : "#636EFA"));
  Plotly.restyle("plot", { "marker.color": [newColors] });
});