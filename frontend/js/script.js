const form = document.getElementById("form");
const result = document.getElementById("result");
const confidenceEl = document.getElementById("confidence");
const explanationEl = document.getElementById("explanation");
const heatmapImg = document.getElementById("heatmap");

const table = document.querySelector("#table tbody");
const preview = document.getElementById("preview");
const imageInput = document.getElementById("imageInput");

let chart; // for chart.js


// ================= Image Preview =================
imageInput.onchange = () => {
  preview.src = URL.createObjectURL(imageInput.files[0]);
  preview.style.display = "block";
};


// ================= Predict =================
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  let formData = new FormData(form);

  result.innerText = "Predicting...";
  confidenceEl.innerText = "";
  explanationEl.innerText = "";
  heatmapImg.style.display = "none";

  let res = await fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    body: formData
  });

  let data = await res.json();

  let colorMap = {
    "Normal": "green",
    "Doubtful": "orange",
    "Mild": "gold",
    "Moderate": "purple",
    "Severe": "red"
  };

  let color = colorMap[data.grade] || "black";

  result.innerHTML = `Grade: <span style="color:${color}">${data.grade}</span>`;
  confidenceEl.innerText = `Confidence: ${data.confidence}%`;
  explanationEl.innerText = data.explanation;

  heatmapImg.src = "http://127.0.0.1:5000/" + data.heatmap;
  heatmapImg.style.display = "block";

  loadPatients();
});


// ================= Load History + Chart =================
async function loadPatients() {

  let res = await fetch("http://127.0.0.1:5000/patients");
  let data = await res.json();

  table.innerHTML = "";

  // 🔥 FIX: map numbers → labels
const gradeMap = {
  "0": "Normal",
  "1": "Doubtful",
  "2": "Mild",
  "3": "Moderate",
  "4": "Severe"
};

let counts = {
  "Normal": 0,
  "Doubtful": 0,
  "Mild": 0,
  "Moderate": 0,
  "Severe": 0
};

data.forEach(p => {

  let grade = String(p[3]); // 🔥 IMPORTANT FIX

  if (gradeMap[grade]) {
    grade = gradeMap[grade];
  }

  table.innerHTML += `
    <tr>
      <td>${p[0]}</td>
      <td>${p[1]}</td>
      <td>${p[2]}</td>
      <td>${grade}</td>
    </tr>
  `;

  counts[grade]++;
});

  // 🔥 DRAW CHART
  if (chart) chart.destroy();

  chart = new Chart(document.getElementById("chart"), {
    type: "bar",
    data: {
      labels: Object.keys(counts),
      datasets: [{
        label: "Patients",
        data: Object.values(counts),
        backgroundColor: "#2563eb"
      }]
    }
  });
}

loadPatients();