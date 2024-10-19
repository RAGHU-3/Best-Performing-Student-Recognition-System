$(document).ready(function () {
    // Handle form submission to add student
    $('#studentForm').on('submit', function (e) {
        e.preventDefault(); // Prevent page reload on form submission

        // Collect student data from the form
        const student = {
            name: $('#name').val(),
            gpa: parseFloat($('#gpa').val()),
            attendance: parseFloat($('#attendance').val()),
            hackathons: parseInt($('#hackathons').val()),
            papers: parseInt($('#papers').val()),
            mentoring: parseInt($('#mentoring').val())
        };

        // Send student data to backend using AJAX POST request
        $.ajax({
            url: '/add_student',  // API endpoint to add student
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(student),
            success: function () {
                alert('Student added successfully!');
                $('#studentForm')[0].reset(); // Clear the form
                loadLeaderboard(); // Reload the leaderboard
            },
            error: function (xhr, status, error) {
                console.error('Error adding student:', error);
                alert('Failed to add student. Please try again.');
            }
        });
    });

    // Function to load the leaderboard from backend
    function loadLeaderboard() {
        $.ajax({
            url: '/rank',  // API endpoint to get ranked students
            type: 'GET',
            success: function (students) {
                $('#leaderboard').empty(); // Clear the leaderboard

                // Iterate over the student data and add rows to the table
                students.forEach(function (student) {
                    $('#leaderboard').append(`
                        <tr>
                            <td>${student[0]}</td>  <!-- Name -->
                            <td>${student[1]}</td>  <!-- GPA -->
                            <td>${student[2]}</td>  <!-- Attendance -->
                            <td>${student[3]}</td>  <!-- Hackathons -->
                            <td>${student[4]}</td>  <!-- Papers -->
                            <td>${student[5]}</td>  <!-- Mentoring -->
                            <td>${student[6]}</td>  <!-- Score -->
                        </tr>
                    `);
                });
            },
            error: function (xhr, status, error) {
                console.error('Error loading leaderboard:', error);
                alert('Failed to load leaderboard. Please try again.');
            }
        });
    }

    // Load the leaderboard on page load
    loadLeaderboard();
});
