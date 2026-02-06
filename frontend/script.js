const form = document.getElementById("form");
const result = document.getElementById("result");
const table = document.querySelector("#table tbody");
const preview = document.getElementById("preview");
const imageInput = document.getElementById("imageInput");


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

  let res = await fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    body: formData
  });

  let data = await res.json();

  let color = ["green","orange","red","purple","black"][data.grade];

  result.innerHTML = `Grade: <span style="color:${color}">${data.grade}</span>`;

  loadPatients();
});


// ================= Load History =================
async function loadPatients() {

  let res = await fetch("http://127.0.0.1:5000/patients");
  let data = await res.json();

  table.innerHTML = "";

data.forEach(p => {
  table.innerHTML += `
    <tr>
      <td>${p[0]}</td>  <!-- id -->
      <td>${p[1]}</td>  <!-- name -->
      <td>${p[2]}</td>  <!-- age -->
      <td>${p[3]}</td>  <!-- grade ONLY -->
    </tr>
  `;
});

}

loadPatients();
