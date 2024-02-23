document.addEventListener('DOMContentLoaded', function() {
    // Connect to the Socket.IO server
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + '/data');

    // Event listener for 'user_update' events
    socket.on('user_update', function(data) {
        // Assuming you have a table with the ID 'usersTable'
        const tableBody = document.getElementById('usersTable').getElementsByTagName('tbody')[0];

        // Check the action type: 'create', 'update', or 'delete'
        if (data.action === 'create') {
            // Create a new row for the new user
            const newRow = tableBody.insertRow();
            newRow.innerHTML = `<td>${data.id}</td><td>${data.name}</td><td>${data.points}</td>`;
            // Add more cells if necessary
        } else if (data.action === 'update') {
            // Find and update the user's row
            // This part requires you to identify rows uniquely, possibly by embedding the user ID within the row's ID attribute when initially creating the table rows
        } else if (data.action === 'delete') {
            // Find and remove the user's row
            // Similar to update, you'll need a way to identify the row to delete
        }
    });
});
