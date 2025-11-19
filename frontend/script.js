const API_URL = "http://localhost:8000/api/videos"; // FastAPI endpoint

const svg = d3.select("#chart");
const width = window.innerWidth - 100;
const height = 500;
svg.attr("width", width).attr("height", height);

async function fetchData() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();

    if (!Array.isArray(data)) {
      console.error("Invalid data format:", data);
      return;
    }

    // Parse and prepare data
    const processed = data
      .map(d => ({
        title: d.title?.substring(0, 40) || "Untitled",
        time: new Date(d.publishedAt)
      }))
      .sort((a, b) => b.time - a.time)
      .slice(0, 10); // show latest 10

    renderChart(processed);
  } catch (err) {
    console.error("Fetch error:", err);
  }
}

function renderChart(data) {
  svg.selectAll("*").remove();

  const x = d3
    .scaleBand()
    .domain(data.map(d => d.title))
    .range([60, width - 60])
    .padding(0.2);

  const y = d3
    .scaleLinear()
    .domain([0, data.length])
    .range([height - 60, 60]);

  // Bars
  svg
    .selectAll(".bar")
    .data(data)
    .enter()
    .append("rect")
    .attr("class", "bar")
    .attr("x", d => x(d.title))
    .attr("width", x.bandwidth())
    .attr("y", (d, i) => y(i))
    .attr("height", 40)
    .attr("rx", 10)
    .attr("ry", 10);

  // Labels
  svg
    .selectAll(".label")
    .data(data)
    .enter()
    .append("text")
    .attr("x", d => x(d.title) + x.bandwidth() / 2)
    .attr("y", (d, i) => y(i) + 25)
    .attr("fill", "#fff")
    .attr("text-anchor", "middle")
    .attr("font-size", "12px")
    .text(d => d.title);

  // Title
  svg
    .append("text")
    .attr("x", width / 2)
    .attr("y", 40)
    .attr("text-anchor", "middle")
    .attr("fill", "#0ff")
    .attr("font-size", "16px")
    .text("Latest YouTube Videos (Live)");
}

// Fetch new data every 10 seconds
fetchData();
setInterval(fetchData, 10000);
