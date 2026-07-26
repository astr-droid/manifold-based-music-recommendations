const xs = points.map(p => p.x);
const ys = points.map(p => p.y);
const labels = points.map(p => `${p.name} — ${p.artist}`);
const colors = points.map(() => "#a78bfa");

const trace = {
  x: xs,
  y: ys,
  text: labels,
  mode: "markers",
  type: "scatter",
  marker: { size: 6, color: colors, line: { width: 0 } },
  hoverinfo: "text",
};

Plotly.newPlot("plot", [trace], {
  title: { text: "UMAP Embedding of Songs", font: { color: "#ece7f5", family: "Space Grotesk" } },
  paper_bgcolor: "#171220",
  plot_bgcolor: "#171220",
  font: { color: "#8f84a3", family: "IBM Plex Mono" },
  xaxis: { gridcolor: "#2f2640", zerolinecolor: "#2f2640" },
  yaxis: { gridcolor: "#2f2640", zerolinecolor: "#2f2640" },
  hovermode: "closest",
});

document.getElementById("plot").on("plotly_click", function (data) {
  const point = data.points[0];
  const idx = point.pointIndex;
  const clicked = points[idx];

  document.getElementById("selected-info").innerHTML =
    `<p>Selected: <strong>${clicked.name}</strong> by ${clicked.artist}. ` +
    `<a class="cta" href="/recommend/${clicked.id}/">Get recommendations</a></p>`;

  const newColors = points.map((p) => (p.id === clicked.id ? "#f0abfc" : "#a78bfa"));
  Plotly.restyle("plot", { "marker.color": [newColors] });
});