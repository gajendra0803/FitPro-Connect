function fetchCounts() {
    fetch('/get_Pushup_counts')
        .then(response => response.json())
        .then(data => {
            document.getElementById("pushup-stage").textContent = data.pushup_stage || "Waiting...";
            // document.getElementById("right-stage").textContent = data.right_squat_stage || "Waiting...";
            document.getElementById("pushup-count").textContent = data.pushup_counter;
            // document.getElementById("right-count").textContent = data.right_squat_counter;
        })
        .catch(error => console.error("Error fetching counts:", error));
}

function toggleCounter() {
    fetch('/toggle_counter', { method: "POST" })
        .then(response => response.json())
        .then(data => {
            alert("Counter " + (data.counter_enabled ? "Started" : "Stopped"));
        });
}

// Auto-refresh data every 0.5 seconds
setInterval(fetchCounts, 500);