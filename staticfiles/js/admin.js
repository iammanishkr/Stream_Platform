const ctx = document.getElementById('myBarChart').getContext('2d');
const myBarChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Artists', 'Songs', 'Users'],
        datasets: [{
            label: 'Count',
            data: [{{ artists_count }}, {{ songs_count }}, {{ users_count }}],
            backgroundColor: [
                'rgba(29, 185, 84, 0.6)',
                'rgba(29, 185, 84, 0.6)',
                'rgba(29, 185, 84, 0.6)'
            ],
            borderColor: [
                'rgba(29, 185, 84, 1)',
                'rgba(29, 185, 84, 1)',
                'rgba(29, 185, 84, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    color: '#bbb' // Change y-axis label color
                }
            },
            x: {
                ticks: {
                    color: '#bbb' // Change x-axis label color
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    color: '#bbb' // Change legend label color
                }
            }
        }
    }
});