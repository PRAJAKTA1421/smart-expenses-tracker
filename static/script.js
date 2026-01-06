// Check if there is data
if (categoryData.labels.length > 0) {

    const ctx = document.getElementById("expenseChart").getContext("2d");

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: categoryData.labels,
            datasets: [{
                data: categoryData.values,
                backgroundColor: [
                    "#22c55e",
                    "#38bdf8",
                    "#facc15",
                    "#fb7185",
                    "#a78bfa"
                ],
                borderWidth: 1
            }]
        },
        options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: "bottom",
            labels: {
                color: "#e5e7eb"
            }
        }
    }
}

    });
    // MONTHLY BAR CHART
if (monthlyData.labels.length > 0) {

    const ctx2 = document.getElementById("monthlyChart").getContext("2d");

    new Chart(ctx2, {
        type: "bar",
        data: {
            labels: monthlyData.labels,
            datasets: [{
                label: "Monthly Expense (₹)",
                data: monthlyData.values,
                backgroundColor: "#38bdf8"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    ticks: { color: "#e5e7eb" }
                },
                y: {
                    ticks: { color: "#e5e7eb" }
                }
            },
            plugins: {
                legend: {
                    labels: { color: "#e5e7eb" }
                }
            }
        }
    });
}


} else {
    document.getElementById("expenseChart").parentElement.innerHTML =
        "<p style='text-align:center;color:#94a3b8'>No expense data available</p>";
}
