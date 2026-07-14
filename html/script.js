let data = [];
let patterns = {};

let pass = 0;
let review = 0;
let fail = 0;

let topAuth = "";
let topApi = "";

async function loadDashboard() {

    const response = await fetch("../outputs/verification.json");
    const patternResponse = await fetch("../outputs/patterns.json");

    data = await response.json();
    patterns = await patternResponse.json();

    pass = 0;
    review = 0;
    fail = 0;

    data.forEach(app => {

        if (app.status === "PASS") {
            pass++;
        }

        else if (app.status === "REVIEW") {
            review++;
        }

        else if (app.status === "FAIL") {
            fail++;
        }

    });

    document.getElementById("totalApps").textContent = data.length;

    document.getElementById("passCount").textContent = pass;

    document.getElementById("reviewCount").textContent = review;

    document.getElementById("failCount").textContent = fail;

    document.getElementById("buildableCount").textContent =
    patterns.Buildability.Yes;

    new Chart(document.getElementById("verificationChart"), {

    type: "bar",

    data: {

        labels: ["PASS", "REVIEW", "FAIL"],

        datasets: [{

    label: "Verification Results",

    data: [pass, review, fail],

    backgroundColor: [
        "#22c55e",
        "#facc15",
        "#ef4444"
    ],

    borderColor: [
        "#16a34a",
        "#eab308",
        "#dc2626"
    ],

    borderWidth: 2

    

}]

    },

    options: {

        responsive: true,

        plugins: {

            legend: {

                display: false

            }

        }

    }

});

new Chart(document.getElementById("authChart"), {

    type: "pie",

    data: {

        labels: Object.keys(patterns["Authentication Methods"]),

        datasets: [{

    data: Object.values(patterns["Authentication Methods"]),

    backgroundColor: [
        "#2563eb",
        "#22c55e",
        "#a855f7",
        "#f97316",
        "#ef4444",
        "#14b8a6",
        "#ec4899"
    ],

    borderWidth: 1

}]

    },

        options: {

        responsive: true,

        plugins: {

            legend: {

                position: "bottom"

            }

        }

    }

});

    

new Chart(document.getElementById("apiChart"), {

    type: "doughnut",

    data: {

        labels: Object.keys(patterns["API Types"]),

        datasets: [{

    data: Object.values(patterns["API Types"]),

    backgroundColor: [
        "#06b6d4",
        "#3b82f6",
        "#8b5cf6",
        "#f59e0b",
        "#10b981",
        "#ef4444"
    ],

    borderWidth: 1

}]

    },

    options: {

    responsive: true,

    plugins: {

        legend: {

            position: "bottom"

        }

    }

}

});

new Chart(document.getElementById("serveChart"), {

    type: "pie",

    data: {

        labels: Object.keys(patterns["Self Serve vs Gated"]),

        datasets: [{

    data: Object.values(patterns["Self Serve vs Gated"]),

    backgroundColor: [
        "#6b7280",
        "#22c55e",
        "#2563eb",
        "#f97316"
    ],

    borderWidth: 1

}]

    },
    options: {

    responsive: true,

    plugins: {

        legend: {

            position: "bottom"

        }

    }

}

});

const tableBody = document.getElementById("tableBody");

data.forEach(app => {

    const row = document.createElement("tr");

    let badgeClass = "";

if(app.status === "PASS"){

    badgeClass = "pass";

}
else if(app.status === "REVIEW"){

    badgeClass = "review";

}
else{

    badgeClass = "fail";

}

row.innerHTML = `
    <td>${app.app_name}</td>

    <td>
        <span class="badge ${badgeClass}">
            ${app.status}
        </span>
    </td>

    <td>${app.confidence}</td>

    <td>${app.notes}</td>
`;

    tableBody.appendChild(row);

});

const insights = document.getElementById("insights");

const totalApps = data.length;

const authMethods = patterns["Authentication Methods"];
const apiTypes = patterns["API Types"];
const buildable = patterns["Buildability"]["Yes"];

    topAuth = Object.keys(authMethods).reduce((a, b) =>
    authMethods[a] > authMethods[b] ? a : b
);

    topApi = Object.keys(apiTypes).reduce((a, b) =>
    apiTypes[a] > apiTypes[b] ? a : b
);

insights.innerHTML = `

<div class="insight">
✔ <strong>Total Applications:</strong> ${totalApps}
</div>

<div class="insight">
✔ <strong>PASS:</strong> ${pass}
</div>

<div class="insight">
✔ <strong>REVIEW:</strong> ${review}
</div>

<div class="insight">
✔ <strong>FAIL:</strong> ${fail}
</div>

<div class="insight">
✔ <strong>Buildable APIs:</strong> ${buildable}
</div>

<div class="insight">
✔ <strong>Most Common Authentication:</strong> ${topAuth}
</div>

<div class="insight">
✔ <strong>Most Common API Type:</strong> ${topApi}
</div>

<div class="recommendation">

💡 <strong>Recommendation</strong>

<br><br>

Review applications with <strong>Unknown</strong> onboarding and
<strong>REVIEW</strong> status first. These integrations likely need
additional documentation or manual verification.

</div>

`;

}

loadDashboard();

const searchInput = document.getElementById("searchInput");
let selectedStatus = "ALL";

function filterTable() {

    const searchText = searchInput.value.toLowerCase();

    const rows = document.querySelectorAll("#tableBody tr");

    rows.forEach(row => {

        const appName = row.cells[0].textContent.toLowerCase();

        const rowStatus = row.cells[1].textContent.trim();

        const matchesSearch = appName.includes(searchText);

        const matchesStatus =
            selectedStatus === "ALL" ||
            rowStatus === selectedStatus;

        if (matchesSearch && matchesStatus) {

            row.style.display = "";

        } else {

            row.style.display = "none";

        }

    });

}

searchInput.addEventListener("keyup", filterTable);

const filterButtons = document.querySelectorAll(".filter-btn");

filterButtons.forEach(button => {

    button.addEventListener("click", function () {

        filterButtons.forEach(btn => btn.classList.remove("active"));

        this.classList.add("active");

        selectedStatus = this.dataset.status;

        filterTable();

    });

});

const themeToggle = document.getElementById("themeToggle");

themeToggle.addEventListener("click", () => {

    document.body.classList.toggle("dark");

    if(document.body.classList.contains("dark")){

        themeToggle.textContent="☀️ Light Mode";

    }

    else{

        themeToggle.textContent="🌙 Dark Mode";

    }

});

const exportBtn = document.getElementById("exportCSV");

exportBtn.addEventListener("click", exportCSV);

function exportCSV(){

    let csv = "Application,Status,Confidence,Notes\n";

    const rows = document.querySelectorAll("#tableBody tr");

    rows.forEach(row=>{

        if(row.style.display==="none") return;

        const cols = row.querySelectorAll("td");

        const rowData = [];

        cols.forEach((col,index)=>{

            if(index===1){

                rowData.push(col.innerText.trim());

            }

            else{

                rowData.push('"' + col.innerText.replace(/\n/g," ") + '"');

            }

        });

        csv += rowData.join(",") + "\n";

    });

    const blob = new Blob([csv],{type:"text/csv"});

    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href=url;

    a.download="verification_export.csv";

    a.click();

    window.URL.revokeObjectURL(url);

}

const pdfBtn = document.getElementById("exportPDF");

pdfBtn.addEventListener("click", exportPDF);

function exportPDF(){

    const { jsPDF } = window.jspdf;

    const doc = new jsPDF();

    let y = 20;

    doc.setFontSize(20);
    doc.text("COMPOSIO API RESEARCH REPORT",20,y);

    y += 15;

    doc.setFontSize(12);

    doc.text("Generated By: Lokesh Barkale",20,y);

    y += 8;

    doc.text("Generated On: " + new Date().toLocaleString(),20,y);

    y += 15;

    doc.setFontSize(16);

    doc.text("SUMMARY",20,y);

    y += 10;

    doc.setFontSize(12);

    doc.text(`Total Applications : ${data.length}`,20,y);

    y+=8;

    doc.text(`PASS : ${pass}`,20,y);

    y+=8;

    doc.text(`REVIEW : ${review}`,20,y);

    y+=8;

    doc.text(`FAIL : ${fail}`,20,y);

    y+=8;

    doc.text(`Buildable APIs : ${patterns.Buildability.Yes}`,20,y);

    y+=15;

    doc.setFontSize(16);

    doc.text("INSIGHTS",20,y);

    y+=10;

    doc.setFontSize(12);

    doc.text(`Most Common Authentication : ${topAuth}`,20,y);

    y+=8;

    doc.text(`Most Common API : ${topApi}`,20,y);

    y+=8;

    doc.text("Recommendation:",20,y);

    y+=8;

    doc.text("Review Unknown onboarding APIs first.",25,y);

    y+=15;

    doc.setFontSize(16);

    doc.text("APPLICATIONS",20,y);

    y+=10;

    doc.setFontSize(10);

    const rows=document.querySelectorAll("#tableBody tr");

    rows.forEach(row=>{

        if(row.style.display==="none") return;

        if(y>275){

            doc.addPage();

            y=20;

        }

        const cols=row.querySelectorAll("td");

        doc.text(
            `${cols[0].innerText} | ${cols[1].innerText} | ${cols[2].innerText}`,
            20,
            y
        );

        y+=7;

    });

    doc.save("Composio_API_Research_Report.pdf");

}

// Sidebar Active Menu

const navLinks = document.querySelectorAll(".sidebar nav a");

navLinks.forEach(link => {

    link.addEventListener("click", function () {

        navLinks.forEach(item => item.classList.remove("active"));

        this.classList.add("active");

    });

});