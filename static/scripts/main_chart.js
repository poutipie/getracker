
main_chart = null;

function draw_chart(item_data) {

    var main_context = document.getElementById("main_chart").getContext("2d");

    if (main_chart != null) {
        main_chart.destroy();
    };

    main_chart = new Chart(main_context, {
        type: "line",
        data: {
            labels: item_data.high_timestamps,
            datasets: [
                {
                label: item_data.item_name,
                data: item_data.high_prices,
                borderColor: "rgb(75, 192, 192)",
                lineTension: 0.1,
                }
            ]
        },
        options: {
        responsive: false,
        scales: {
            xAxes: [{
            type: 'time',
            time: {
                parser: 'YYYY/MM/DD HH:mm:ss',
                displayFormats: {
                day: 'YY MMM DD'
                },
            },
            }]
        }
        }
    });
}