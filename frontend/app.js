
const $ = (id) => document.getElementById(id);

const api = (path, options = {}) => fetch(`/api${path}`, {
  credentials: "same-origin",
  ...options,
  headers: {
    ...(options.body ? { "Content-Type": "application/json" } : {}),
    ...options.headers
  }
});

function duration(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  return `${h}u ${m}m`;
}

function date(value) {
  return new Date(value).toLocaleDateString("nl-BE", {
    day: "2-digit",
    month: "short",
    year: "numeric"
  });
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, c => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }[c]));
}

function showLogin() {
  $("dashboard").hidden = true;
  $("login-screen").hidden = false;
}

function showDashboard(user) {
  $("login-screen").hidden = true;
  $("dashboard").hidden = false;
  $("welcome").textContent = `Ingelogd als ${user.email}`;
}

async function loadDashboard() {
  try {
    const [statsRes, activitiesRes] = await Promise.all([
      api("/stats"),
      api("/activities?limit=30")
    ]);

    if (!statsRes.ok || !activitiesRes.ok) {
      throw new Error("Gegevens konden niet worden geladen.");
    }

    const stats = await statsRes.json();
    const activities = await activitiesRes.json();

    $("count").textContent = stats.activity_count;
    $("duration").textContent = duration(stats.total_seconds);
    $("distance").textContent =
      `${(stats.total_distance_meters / 1000).toFixed(1)} km`;

    $("activities").innerHTML = activities.length
      ? activities.map(a => `
        <tr>
          <td>${escapeHtml(a.sport)}</td>
          <td>${date(a.started_at)}</td>
          <td>${duration(a.duration_seconds)}</td>
          <td>${a.distance_meters == null
            ? "—"
            : (a.distance_meters / 1000).toFixed(2) + " km"}</td>
          <td>${escapeHtml(a.source)}</td>
        </tr>
      `).join("")
      : '<tr><td colspan="5" class="empty">Nog geen activiteiten.</td></tr>';

  } catch (error) {
    $("connection").textContent = "Fout bij laden";
    $("activities").innerHTML =
      '<tr><td colspan="5" class="empty">Kan gegevens niet laden.</td></tr>';
  }
}

// ACCOUNTINSTELLINGEN

function initAccount() {
  const accountButton = $("account-settings");
  const accountPanel = $("account-panel");
  const closeButton = $("close-account");
  const accountForm = $("account-form");

  if (!accountButton || !accountPanel || !closeButton || !accountForm) {
    console.error("Accountinitialisatie mislukt: HTML-element ontbreekt.");
    return;
  }

  accountButton.addEventListener("click", () => {
    accountPanel.hidden = false;
    accountPanel.scrollIntoView({
      behavior: "smooth",
      block: "start"
    });
  });

  closeButton.addEventListener("click", () => {
    accountPanel.hidden = true;
  });

  accountForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const error = $("account-error");
    const success = $("account-success");
    const button = $("save-account");

    error.hidden = true;
    success.hidden = true;

    const newPassword = $("new-password").value;
    const confirmPassword = $("confirm-password").value;

    if (newPassword !== confirmPassword) {
      error.textContent = "De nieuwe wachtwoorden komen niet overeen.";
      error.hidden = false;
      return;
    }

    if (!newPassword && !$("new-email").value.trim()) {
      error.textContent = "Vul minstens één nieuw gegeven in.";
      error.hidden = false;
      return;
    }

    button.disabled = true;
    button.textContent = "Opslaan...";

    try {
      const response = await api("/auth/account", {
        method: "PUT",
        body: JSON.stringify({
          current_password: $("current-password").value,
          new_email: $("new-email").value.trim() || null,
          new_password: newPassword || null
        })
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.detail || "Wijzigingen konden niet worden opgeslagen."
        );
      }

      $("welcome").textContent = `Ingelogd als ${result.email}`;
      accountForm.reset();

      success.textContent = "Je accountgegevens zijn succesvol gewijzigd.";
      success.hidden = false;

    } catch (err) {
      error.textContent = err.message;
      error.hidden = false;
    } finally {
      button.disabled = false;
      button.textContent = "Wijzigingen opslaan";
    }
  });
}

// AUTHENTICATIE

async function checkSession() {
  try {
    const response = await api("/auth/me");

    if (!response.ok) {
      showLogin();
      return;
    }

    const user = await response.json();

    showDashboard(user);
    await loadDashboard();

  } catch {
    $("login-error").textContent =
      "Kan geen verbinding maken met de server.";
    showLogin();
  }
}

function initLogin() {
  $("login-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const button = $("login-button");
    const error = $("login-error");

    button.disabled = true;
    button.textContent = "Aanmelden...";
    error.hidden = true;

    try {
      const response = await api("/auth/login", {
        method: "POST",
        body: JSON.stringify({
          email: $("email").value,
          password: $("password").value
        })
      });

      if (!response.ok) {
        throw new Error("E-mailadres of wachtwoord is onjuist.");
      }

      const userResponse = await api("/auth/me");

      if (!userResponse.ok) {
        throw new Error("Sessie kon niet worden gestart.");
      }

      const user = await userResponse.json();

      showDashboard(user);
      await loadDashboard();

    } catch (err) {
      error.textContent = err.message;
      error.hidden = false;
    } finally {
      button.disabled = false;
      button.textContent = "Aanmelden";
    }
  });
}

function initDashboard() {
  $("logout").addEventListener("click", async () => {
    await api("/auth/logout", { method: "POST" });
    showLogin();
  });

  $("refresh").addEventListener("click", loadDashboard);
}

// INITIALISATIE

function initApp() {
  initAccount();
  initLogin();
  initDashboard();
  checkSession();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initApp, { once: true });
} else {
  initApp();
}
