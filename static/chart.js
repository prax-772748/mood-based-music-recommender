// Parse the mood history data from the hidden script tag
const moodHistory = JSON.parse(document.getElementById('moodHistoryData').textContent);

// Debugging: Log the mood history data
console.log("Mood History Data:", moodHistory);

// Check if moodHistory is empty
if (!moodHistory || moodHistory.length === 0) {
    console.error("No mood history data available.");
} else {
    // Extract labels (dates) and data (mood lengths)
    const labels = moodHistory.map(entry => entry.date); // Extract dates
    const data = moodHistory.map(entry => entry.mood.length || 0); // Use mood length as a simple score

    // Get the canvas context
    const ctx = document.getElementById('moodChart').getContext('2d');

    // Create the chart
    const moodChart = new Chart(ctx, {
        type: 'line', // You can also use 'bar' for a bar chart
        data: {
            labels: labels,
            datasets: [{
                label: 'Mood Trends',
                data: data,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            }
        }
    });
}