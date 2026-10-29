/**
 * DevOps Quest - Frontend Vanilla JavaScript Client
 * Manages async challenge status updates, UI metrics recalculations,
 * client-side filtering, and system health polling.
 */

document.addEventListener("DOMContentLoaded", () => {
    initChallengeToggles();
    initHideCompletedFilter();
    initHealthCheckPolling();
});

/**
 * Attaches asynchronous event listeners to challenge toggle checkboxes.
 */
function initChallengeToggles() {
    const checkboxes = document.querySelectorAll(".challenge-checkbox");

    checkboxes.forEach((checkbox) => {
        checkbox.addEventListener("change", async (event) => {
            const input = event.target;
            const challengeId = input.dataset.id;
            const isChecked = input.checked;
            const card = document.getElementById(`challenge-card-${challengeId}`);
            const toggleText = document.getElementById(`toggle-text-${challengeId}`);

            // Prevent rapid multi-clicks
            input.disabled = true;

            try {
                const response = await fetch(`/api/challenges/${challengeId}/toggle`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    body: JSON.stringify({ completed: isChecked }),
                });

                if (!response.ok) {
                    throw new Error(`Server returned HTTP ${response.status}`);
                }

                const data = await response.json();

                // Update card visual state
                if (isChecked) {
                    card.classList.add("is-completed");
                    card.dataset.completed = "1";
                    if (toggleText) toggleText.textContent = "Completed";
                } else {
                    card.classList.remove("is-completed");
                    card.dataset.completed = "0";
                    if (toggleText) toggleText.textContent = "Mark as Done";
                }

                // If "Hide Completed" is active and item was marked completed, adjust visibility
                const hideCompletedBox = document.getElementById("filter-hide-completed");
                if (hideCompletedBox && hideCompletedBox.checked && isChecked) {
                    card.style.display = "none";
                }

                // Update metrics & progress bar across the dashboard
                if (data.stats) {
                    updateDashboardStats(data.stats);
                }
            } catch (error) {
                console.error("Failed to update challenge status:", error);
                // Roll back toggle state on failure
                input.checked = !isChecked;
                alert("Failed to update challenge status. Please check your connection.");
            } finally {
                input.disabled = false;
            }
        });
    });
}

/**
 * Updates progress bar and counters in real time.
 */
function updateDashboardStats(stats) {
    const progressBar = document.getElementById("progress-bar-fill");
    const progressText = document.getElementById("progress-percentage-display");
    const summaryText = document.getElementById("progress-summary-text");
    const metricTotal = document.getElementById("metric-total");
    const metricCompleted = document.getElementById("metric-completed");
    const metricPending = document.getElementById("metric-pending");
    const metricRate = document.getElementById("metric-rate");

    const rate = stats.completion_rate;

    if (progressBar) {
        progressBar.style.width = `${rate}%`;
        progressBar.setAttribute("aria-valuenow", rate);
    }
    if (progressText) {
        progressText.textContent = `${rate}%`;
    }
    if (summaryText) {
        summaryText.innerHTML = `<strong>${stats.completed}</strong> of <strong>${stats.total}</strong> Challenges Completed`;
    }
    if (metricTotal) metricTotal.textContent = stats.total;
    if (metricCompleted) metricCompleted.textContent = stats.completed;
    if (metricPending) metricPending.textContent = stats.pending;
    if (metricRate) metricRate.textContent = `${rate}%`;
}

/**
 * Implements client-side "Hide Completed" filtering without page reload.
 */
function initHideCompletedFilter() {
    const hideCompletedBox = document.getElementById("filter-hide-completed");
    if (!hideCompletedBox) return;

    hideCompletedBox.addEventListener("change", (e) => {
        const shouldHide = e.target.checked;
        const cards = document.querySelectorAll(".challenge-card");

        cards.forEach((card) => {
            const isCompleted = card.dataset.completed === "1";
            if (shouldHide && isCompleted) {
                card.style.display = "none";
            } else {
                card.style.display = "";
            }
        });
    });
}

/**
 * Polls the /health endpoint to update the online status indicator pill.
 */
function initHealthCheckPolling() {
    const statusPill = document.getElementById("system-status-indicator");
    if (!statusPill) return;

    const dot = statusPill.querySelector(".status-dot");
    const label = statusPill.querySelector(".status-label");

    async function checkHealth() {
        try {
            const res = await fetch("/health", { cache: "no-store" });
            if (res.ok) {
                const data = await res.json();
                if (data.status === "healthy") {
                    dot.classList.remove("offline");
                    label.textContent = "Online";
                    return;
                }
            }
            dot.classList.add("offline");
            label.textContent = "Degraded";
        } catch {
            dot.classList.add("offline");
            label.textContent = "Offline";
        }
    }

    // Run health check initially and then every 30 seconds
    checkHealth();
    setInterval(checkHealth, 30000);
}
