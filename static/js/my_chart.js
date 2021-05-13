
import {XHttpBackEnd} from "./xhttp_backend.js"

export class MyChart {

    constructor(canvas_id) {
        this.context = document.getElementById(canvas_id).getContext("2d");
        this.chart = null;

        XHttpBackEnd.fetch_chart_5m(2).then(data => this.draw(data));
    }

    draw(item_data) {
    
        if (this.chart != null) {
            this.chart.destroy();
        }
        this.chart = new Chart(this.context, {
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

}
