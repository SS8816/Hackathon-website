// Function to fetch the leaderboard data and update the table
function fetchLeaderboard() {
    fetch('/leaderboard') // Make a request to the leaderboard route
        .then(response => response.text())
        .then(data => {
            // Update the leaderboard section with new data
            document.getElementById('leaderboard-container').innerHTML = data;
        })
        .catch(error => console.error('Error fetching leaderboard:', error));
}

// Set an interval to refresh the leaderboard every 5 seconds (5000 milliseconds)
setInterval(fetchLeaderboard, 5000);