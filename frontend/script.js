/* =========================================================
   CAREBLOOM FRONTEND
   Connected to deployed FastAPI backend
========================================================= */

const API_URL = "https://carebloom-2.onrender.com";

let currentUserId = localStorage.getItem("carebloomUserId");
let currentUserName = localStorage.getItem("carebloomUserName");


/* =========================================================
   COMMON HELPERS
========================================================= */

function setMessage(elementId, message, success = true) {
    const element = document.getElementById(elementId);

    if (!element) return;

    element.textContent = message;
    element.style.color = success ? "#2e7d32" : "#d32f2f";
}


async function apiRequest(url, options = {}) {
    const controller = new AbortController();

    // Render free service may take time to wake up
    const timeout = setTimeout(() => {
        controller.abort();
    }, 60000);

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });

        clearTimeout(timeout);

        let data;

        try {
            data = await response.json();
        } catch {
            data = null;
        }

        if (!response.ok) {
            let errorMessage = "Something went wrong.";

            if (data && data.detail) {
                if (typeof data.detail === "string") {
                    errorMessage = data.detail;
                } else {
                    errorMessage = JSON.stringify(data.detail);
                }
            }

            throw new Error(errorMessage);
        }

        return data;

    } catch (error) {
        clearTimeout(timeout);

        if (error.name === "AbortError") {
            throw new Error(
                "Server is taking too long to respond. Please try again."
            );
        }

        throw error;
    }
}


/* =========================================================
   LOGIN / REGISTER TABS
========================================================= */

function showLogin() {
    document.getElementById("loginForm").classList.remove("hidden");
    document.getElementById("registerForm").classList.add("hidden");

    document.getElementById("loginTab").classList.add("active");
    document.getElementById("registerTab").classList.remove("active");
}


function showRegister() {
    document.getElementById("registerForm").classList.remove("hidden");
    document.getElementById("loginForm").classList.add("hidden");

    document.getElementById("registerTab").classList.add("active");
    document.getElementById("loginTab").classList.remove("active");
}


/* =========================================================
   REGISTER
========================================================= */

async function registerUser() {

    const name = document
        .getElementById("registerName")
        .value
        .trim();

    const email = document
        .getElementById("registerEmail")
        .value
        .trim();

    const password = document
        .getElementById("registerPassword")
        .value
        .trim();

    if (!name || !email || !password) {
        setMessage(
            "registerMessage",
            "Please fill all fields.",
            false
        );
        return;
    }

    setMessage(
        "registerMessage",
        "Creating your CareBloom account..."
    );

    try {

        const data = await apiRequest(
            `${API_URL}/api/auth/register`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                })
            }
        );

        setMessage(
            "registerMessage",
            "Account created successfully. Please login."
        );

        document.getElementById("loginEmail").value = email;
        document.getElementById("registerName").value = "";
        document.getElementById("registerEmail").value = "";
        document.getElementById("registerPassword").value = "";

        setTimeout(() => {
            showLogin();
        }, 800);

    } catch (error) {

        setMessage(
            "registerMessage",
            error.message,
            false
        );
    }
}


/* =========================================================
   LOGIN
========================================================= */

async function loginUser() {

    const email = document
        .getElementById("loginEmail")
        .value
        .trim();

    const password = document
        .getElementById("loginPassword")
        .value
        .trim();

    if (!email || !password) {
        setMessage(
            "loginMessage",
            "Please enter email and password.",
            false
        );
        return;
    }

    setMessage(
        "loginMessage",
        "Logging in..."
    );

    try {

        const data = await apiRequest(
            `${API_URL}/api/auth/login`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );

        currentUserId = data.user_id;
        currentUserName = data.name;

        localStorage.setItem(
            "carebloomUserId",
            currentUserId
        );

        localStorage.setItem(
            "carebloomUserName",
            currentUserName
        );

        setMessage(
            "loginMessage",
            "Login successful."
        );

        openApplication();

    } catch (error) {

        setMessage(
            "loginMessage",
            error.message,
            false
        );
    }
}


/* =========================================================
   OPEN APP
========================================================= */

function openApplication() {

    document
        .getElementById("authSection")
        .classList
        .add("hidden");

    document
        .getElementById("appSection")
        .classList
        .remove("hidden");

    document.getElementById(
        "welcomeUser"
    ).textContent =
        `Welcome, ${currentUserName || "CareBloom User"} 🌱`;

    showPage("dashboardPage");
}


/* =========================================================
   LOGOUT
========================================================= */

function logoutUser() {

    localStorage.removeItem("carebloomUserId");
    localStorage.removeItem("carebloomUserName");

    currentUserId = null;
    currentUserName = null;

    document
        .getElementById("appSection")
        .classList
        .add("hidden");

    document
        .getElementById("authSection")
        .classList
        .remove("hidden");

    document.getElementById("loginPassword").value = "";

    showLogin();
}


/* =========================================================
   PAGE NAVIGATION
========================================================= */

function showPage(pageId) {

    const pages =
        document.querySelectorAll(".content-page");

    pages.forEach(page => {
        page.classList.remove("active-page");
    });

    const selectedPage =
        document.getElementById(pageId);

    if (selectedPage) {
        selectedPage.classList.add("active-page");
    }
}


/* =========================================================
   IMAGE PREVIEW
========================================================= */

function previewLeafImage() {

    const input =
        document.getElementById("leafImage");

    const preview =
        document.getElementById("leafPreview");

    if (!input.files || !input.files[0]) {
        preview.style.display = "none";
        return;
    }

    const file = input.files[0];

    const reader = new FileReader();

    reader.onload = function(event) {
        preview.src = event.target.result;
        preview.style.display = "block";
    };

    reader.readAsDataURL(file);
}


/* =========================================================
   AI LEAF ANALYSIS
========================================================= */

async function analyzeLeaf() {

    if (!currentUserId) {
        setMessage(
            "scanStatus",
            "Please login first.",
            false
        );
        return;
    }

    const input =
        document.getElementById("leafImage");

    if (!input.files || input.files.length === 0) {
        setMessage(
            "scanStatus",
            "Please take or select a leaf image.",
            false
        );
        return;
    }

    const file = input.files[0];

    const formData = new FormData();
    formData.append("file", file);

    setMessage(
        "scanStatus",
        "🌿 CareBloom AI is analyzing the leaf..."
    );

    document
        .getElementById("resultCard")
        .classList
        .add("hidden");

    try {

        const data = await apiRequest(
            `${API_URL}/api/disease/predict?user_id=${currentUserId}`,
            {
                method: "POST",
                body: formData
            }
        );

        document.getElementById(
            "resultPlant"
        ).textContent = data.plant || "-";

        document.getElementById(
            "resultDisease"
        ).textContent = data.disease || "-";

        document.getElementById(
            "resultConfidence"
        ).textContent =
            data.confidence !== undefined
                ? `${data.confidence}%`
                : "-";

        document.getElementById(
            "resultHealthScore"
        ).textContent =
            data.health_score !== undefined
                ? `${data.health_score}/100`
                : "-";

        document.getElementById(
            "resultHealthStatus"
        ).textContent =
            data.health_status || "-";

        document.getElementById(
            "resultWeatherRisk"
        ).textContent =
            data.weather_risk || "-";

        document.getElementById(
            "resultTemperature"
        ).textContent =
            data.temperature ?? "-";

        document.getElementById(
            "resultHumidity"
        ).textContent =
            data.humidity ?? "-";

        document.getElementById(
            "resultRainfall"
        ).textContent =
            data.rainfall ?? "-";

        document.getElementById(
            "resultAlertLevel"
        ).textContent =
            data.alert_level || "-";

        document.getElementById(
            "resultAlertMessage"
        ).textContent =
            data.alert_message || "-";

        document.getElementById(
            "resultOrganic"
        ).textContent =
            data.organic_remedy || "-";

        document.getElementById(
            "resultChemical"
        ).textContent =
            data.chemical_treatment || "-";

        document.getElementById(
            "resultPrevention"
        ).textContent =
            data.prevention || "-";

        document.getElementById(
            "resultWaterInterval"
        ).textContent =
            data.watering_interval_days ?? "-";

        document.getElementById(
            "resultNextWater"
        ).textContent =
            data.next_watering_date || "-";

        document.getElementById(
            "resultFertilizerInterval"
        ).textContent =
            data.fertilizer_interval_days ?? "-";

        document.getElementById(
            "resultNextFertilizer"
        ).textContent =
            data.next_fertilizer_date || "-";

        document
            .getElementById("resultCard")
            .classList
            .remove("hidden");

        setMessage(
            "scanStatus",
            "✅ Analysis completed successfully."
        );

        document
            .getElementById("resultCard")
            .scrollIntoView({
                behavior: "smooth"
            });

    } catch (error) {

        setMessage(
            "scanStatus",
            `Analysis failed: ${error.message}`,
            false
        );
    }
}


/* =========================================================
   ADD PLANT
========================================================= */

async function addPlant() {

    const plantName =
        document.getElementById("plantName")
        .value
        .trim();

    const plantingDate =
        document.getElementById("plantingDate")
        .value;

    const location =
        document.getElementById("plantLocation")
        .value
        .trim();

    if (!plantName || !plantingDate || !location) {

        setMessage(
            "plantMessage",
            "Please fill all plant details.",
            false
        );

        return;
    }

    try {

        await apiRequest(
            `${API_URL}/api/plants/add`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    user_id: Number(currentUserId),
                    plant_name: plantName,
                    planting_date: plantingDate,
                    location: location
                })
            }
        );

        setMessage(
            "plantMessage",
            "Plant added successfully."
        );

        document.getElementById("plantName").value = "";
        document.getElementById("plantingDate").value = "";
        document.getElementById("plantLocation").value = "";

        loadPlants();

    } catch (error) {

        setMessage(
            "plantMessage",
            error.message,
            false
        );
    }
}


/* =========================================================
   LOAD USER PLANTS
========================================================= */

async function loadPlants() {

    const container =
        document.getElementById("plantsList");

    container.innerHTML =
        "<p>Loading plants...</p>";

    try {

        const plants = await apiRequest(
            `${API_URL}/api/plants/user/${currentUserId}`
        );

        if (!plants || plants.length === 0) {
            container.innerHTML =
                "<p>No plants added yet.</p>";
            return;
        }

        container.innerHTML = plants.map(
            plant => `
                <div class="list-item">
                    <h4>🌱 ${escapeHTML(plant.plant_name)}</h4>

                    <p>
                        <strong>Plant ID:</strong>
                        ${plant.plant_id}
                    </p>

                    <p>
                        <strong>Planting Date:</strong>
                        ${escapeHTML(plant.planting_date || "-")}
                    </p>

                    <p>
                        <strong>Location:</strong>
                        ${escapeHTML(plant.location || "-")}
                    </p>
                </div>
            `
        ).join("");

    } catch (error) {

        container.innerHTML =
            `<p>Unable to load plants: ${escapeHTML(error.message)}</p>`;
    }
}


/* =========================================================
   DISEASE HISTORY
========================================================= */

async function loadHistory() {

    const container =
        document.getElementById("historyList");

    container.innerHTML =
        "<p>Loading disease history...</p>";

    try {

        const history = await apiRequest(
            `${API_URL}/api/disease/history?user_id=${currentUserId}`
        );

        if (!history || history.length === 0) {
            container.innerHTML =
                "<p>No disease scans found.</p>";
            return;
        }

        container.innerHTML = history.map(
            item => `
                <div class="list-item">

                    <h4>
                        🌿 ${escapeHTML(item.plant)}
                        -
                        ${escapeHTML(item.disease)}
                    </h4>

                    <p>
                        <strong>Confidence:</strong>
                        ${item.confidence}%
                    </p>

                    <p>
                        <strong>Health Score:</strong>
                        ${item.health_score}/100
                    </p>

                    <p>
                        <strong>Status:</strong>
                        ${escapeHTML(item.health_status)}
                    </p>

                    <p>
                        <strong>Scanned:</strong>
                        ${escapeHTML(item.created_at)}
                    </p>

                </div>
            `
        ).join("");

    } catch (error) {

        container.innerHTML =
            `<p>Unable to load history: ${escapeHTML(error.message)}</p>`;
    }
}


/* =========================================================
   ADD REMINDER
========================================================= */

async function addReminder() {

    const plantId =
        Number(
            document.getElementById("reminderPlantId").value
        );

    const reminderType =
        document.getElementById("reminderType").value;

    const reminderDate =
        document.getElementById("reminderDate").value;

    const message =
        document.getElementById("reminderMessage")
        .value
        .trim();

    if (!plantId || !reminderDate || !message) {

        setMessage(
            "reminderStatus",
            "Please fill all reminder details.",
            false
        );

        return;
    }

    try {

        await apiRequest(
            `${API_URL}/api/reminders/add`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    user_id: Number(currentUserId),
                    plant_id: plantId,
                    reminder_type: reminderType,
                    reminder_date: reminderDate,
                    message: message
                })
            }
        );

        setMessage(
            "reminderStatus",
            "Reminder added successfully."
        );

        document.getElementById("reminderPlantId").value = "";
        document.getElementById("reminderDate").value = "";
        document.getElementById("reminderMessage").value = "";

        loadReminders();

    } catch (error) {

        setMessage(
            "reminderStatus",
            error.message,
            false
        );
    }
}


/* =========================================================
   LOAD REMINDERS
========================================================= */

async function loadReminders() {

    const container =
        document.getElementById("reminderList");

    container.innerHTML =
        "<p>Loading reminders...</p>";

    try {

        const reminders = await apiRequest(
            `${API_URL}/api/reminders/user/${currentUserId}`
        );

        if (!reminders || reminders.length === 0) {
            container.innerHTML =
                "<p>No reminders found.</p>";
            return;
        }

        container.innerHTML = reminders.map(
            reminder => `
                <div class="list-item">

                    <h4>
                        🔔 ${escapeHTML(reminder.reminder_type)}
                    </h4>

                    <p>
                        <strong>Plant ID:</strong>
                        ${reminder.plant_id}
                    </p>

                    <p>
                        <strong>Date:</strong>
                        ${escapeHTML(reminder.reminder_date)}
                    </p>

                    <p>
                        <strong>Message:</strong>
                        ${escapeHTML(reminder.message || "-")}
                    </p>

                    <p>
                        <strong>Status:</strong>
                        ${escapeHTML(reminder.status)}
                    </p>

                </div>
            `
        ).join("");

    } catch (error) {

        container.innerHTML =
            `<p>Unable to load reminders: ${escapeHTML(error.message)}</p>`;
    }
}


/* =========================================================
   ADD CONSULTATION
========================================================= */

async function addConsultation() {

    const plantId =
        Number(
            document.getElementById("consultPlantId").value
        );

    const disease =
        document.getElementById("consultDisease")
        .value
        .trim();

    const question =
        document.getElementById("consultQuestion")
        .value
        .trim();

    if (!plantId || !disease || !question) {

        setMessage(
            "consultStatus",
            "Please fill all consultation details.",
            false
        );

        return;
    }

    try {

        await apiRequest(
            `${API_URL}/api/consultation/add`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    user_id: Number(currentUserId),
                    plant_id: plantId,
                    disease: disease,
                    question: question
                })
            }
        );

        setMessage(
            "consultStatus",
            "Consultation request submitted successfully."
        );

        document.getElementById("consultPlantId").value = "";
        document.getElementById("consultDisease").value = "";
        document.getElementById("consultQuestion").value = "";

        loadConsultations();

    } catch (error) {

        setMessage(
            "consultStatus",
            error.message,
            false
        );
    }
}


/* =========================================================
   LOAD CONSULTATIONS
========================================================= */

async function loadConsultations() {

    const container =
        document.getElementById("consultationList");

    container.innerHTML =
        "<p>Loading consultations...</p>";

    try {

        const consultations = await apiRequest(
            `${API_URL}/api/consultation/user/${currentUserId}`
        );

        if (!consultations || consultations.length === 0) {

            container.innerHTML =
                "<p>No consultation requests found.</p>";

            return;
        }

        container.innerHTML = consultations.map(
            consultation => `
                <div class="list-item">

                    <h4>
                        👨‍⚕️ ${escapeHTML(consultation.disease)}
                    </h4>

                    <p>
                        <strong>Plant ID:</strong>
                        ${consultation.plant_id}
                    </p>

                    <p>
                        <strong>Question:</strong>
                        ${escapeHTML(consultation.question)}
                    </p>

                    <p>
                        <strong>Status:</strong>
                        ${escapeHTML(consultation.status)}
                    </p>

                    <p>
                        <strong>Date:</strong>
                        ${escapeHTML(consultation.created_at)}
                    </p>

                </div>
            `
        ).join("");

    } catch (error) {

        container.innerHTML =
            `<p>Unable to load consultations: ${escapeHTML(error.message)}</p>`;
    }
}


/* =========================================================
   BASIC HTML ESCAPING
========================================================= */

function escapeHTML(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


/* =========================================================
   RESTORE LOGIN SESSION
========================================================= */

window.addEventListener("DOMContentLoaded", function() {

    if (currentUserId && currentUserName) {

        openApplication();

    } else {

        document
            .getElementById("authSection")
            .classList
            .remove("hidden");

        document
            .getElementById("appSection")
            .classList
            .add("hidden");

        showLogin();
    }
});