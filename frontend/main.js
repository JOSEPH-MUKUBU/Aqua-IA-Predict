const API_URL = "http://127.0.0.1:8000";

// DOM Elements
const alertBadge = document.getElementById("alert-badge");
const alertText = document.getElementById("alert-text");
const alertDot = document.querySelector(".dot");

const riskNumber = document.getElementById("risk-number");
const riskCircle = document.getElementById("risk-circle");
const probableCause = document.getElementById("probable-cause");

const valPh = document.getElementById("val-ph");
const valTurb = document.getElementById("val-turb");
const valCond = document.getElementById("val-cond");
const valChlor = document.getElementById("val-chlor");
const valTemp = document.getElementById("val-temp");
const valPress = document.getElementById("val-press");
const valFlow = document.getElementById("val-flow");

// Chart Setup
const ctx = document.getElementById('mainChart').getContext('2d');

const chartData = {
    labels: [],
    datasets: [
        {
            label: 'pH',
            borderColor: '#58a6ff',
            backgroundColor: 'transparent',
            data: [],
            yAxisID: 'y',
            tension: 0.4
        },
        {
            label: 'Turbidite (NTU)',
            borderColor: '#d29922',
            backgroundColor: 'transparent',
            data: [],
            yAxisID: 'y1',
            tension: 0.4
        }
    ]
};

const mainChart = new Chart(ctx, {
    type: 'line',
    data: chartData,
    options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index',
            intersect: false,
        },
        plugins: {
            legend: {
                labels: { color: '#c9d1d9' }
            }
        },
        scales: {
            x: {
                ticks: { color: '#8b949e' },
                grid: { color: 'rgba(255,255,255,0.05)' }
            },
            y: {
                type: 'linear',
                display: true,
                position: 'left',
                ticks: { color: '#58a6ff' },
                grid: { color: 'rgba(255,255,255,0.05)' }
            },
            y1: {
                type: 'linear',
                display: true,
                position: 'right',
                ticks: { color: '#d29922' },
                grid: { drawOnChartArea: false }
            },
        }
    }
});

let timeIndex = 0;

// Fetch pipeline
async function fetchAndPredict() {
    try {
        // 1. Get simulated data
        const simRes = await fetch(`${API_URL}/simulate`);
        if (!simRes.ok) throw new Error("Simulation failed");
        const sensorData = await simRes.json();

        // 2. Predict using POST
        const predRes = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(sensorData)
        });
        if (!predRes.ok) throw new Error("Prediction failed");
        const predData = await predRes.json();

        updateDashboard(sensorData, predData);

    } catch (error) {
        console.error("Erreur de connexion a l'API:", error);
        setAlertState("Hors Ligne", "#8b949e", "rgba(255,255,255,0.05)");
    }
}

function updateDashboard(sensors, prediction) {
    // Update Sensors
    valPh.textContent = sensors.ph.toFixed(2);
    valTurb.textContent = sensors.turbidity.toFixed(2);
    valCond.textContent = sensors.conductivity.toFixed(0);
    valChlor.textContent = sensors.chlorine.toFixed(2);
    valTemp.textContent = sensors.temperature.toFixed(1);
    valPress.textContent = sensors.pressure.toFixed(2);
    valFlow.textContent = sensors.flow.toFixed(0);

    // Update Prediction
    const risk = prediction.Risk_Index;
    riskNumber.textContent = Math.round(risk);

    // Update SVG Circle (circumference is 100)
    riskCircle.setAttribute("stroke-dasharray", `${risk}, 100`);

    // Update Cause
    probableCause.textContent = prediction.Probable_Cause;

    // Update Alert Badge & Colors
    let color = "#3fb950"; // Vert
    let bg = "rgba(63, 185, 80, 0.1)";
    let badgeText = "Normal";

    if (prediction.Alert_Level === "Rouge") {
        color = "#f85149"; // Rouge
        bg = "rgba(248, 81, 73, 0.1)";
        badgeText = "Alerte Critique";
    } else if (prediction.Alert_Level === "Jaune") {
        color = "#d29922"; // Jaune
        bg = "rgba(210, 153, 34, 0.1)";
        badgeText = "Alerte Mineure";
    }

    setAlertState(badgeText, color, bg);
    riskCircle.setAttribute("stroke", color);

    // Update Chart
    const now = new Date();
    const timeLabel = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;

    chartData.labels.push(timeLabel);
    chartData.datasets[0].data.push(sensors.ph);
    chartData.datasets[1].data.push(sensors.turbidity);

    // Keep max 20 points
    if (chartData.labels.length > 20) {
        chartData.labels.shift();
        chartData.datasets[0].data.shift();
        chartData.datasets[1].data.shift();
    }

    mainChart.update();
}

function setAlertState(text, dotColor, bgColor) {
    alertText.textContent = text;
    alertText.style.color = dotColor;
    alertDot.style.backgroundColor = dotColor;
    alertBadge.style.background = bgColor;
    alertBadge.style.borderColor = dotColor;
}

// Start loop
setInterval(fetchAndPredict, 1500);
fetchAndPredict();
