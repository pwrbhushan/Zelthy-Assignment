var submitBtn = document.getElementById('submit');
submitBtn[i].addEventListener('click', function () {
    console.log('updateChart');
    updateChart(this.value)
});

function updateChart(date) {
    let url = "/chart/";
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'start_date': date,
        })
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log(data)
            location.reload()
        })
}