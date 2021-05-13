
import {XHttpBackEnd} from "./xhttp_backend.js"

export class MyChart {

    constructor(canvas_id) {
        this.context = document.getElementById(canvas_id).getContext("2d");
        this.chart = null;

        //XHttpBackEnd.fetch_chart_5m(2).then(data => this._draw(data));
    }

    /**
     * 
     * @param {MyChart} self 
     * @param {int} item_id 
     */
    static draw(self, item_id) {
        XHttpBackEnd.fetch_chart_5m(item_id)
        .then(dat => self._backend_draw(dat));
    }

    _backend_draw(graph_data) {

        if (this.chart != null) {
            this.chart.destroy();
        }
        this.chart = new Chart(this.context, {
            type: "line",
            data: {
                labels: graph_data.timestamps,
                datasets: [
                    {
                        label: graph_data.item_name + " - sell",
                        data: graph_data.high_prices,
                        borderColor: "rgb(214, 176, 111)",
                        lineTension: 0.1,
                    },
                    {
                        label: graph_data.item_name + " - buy",
                        data: graph_data.low_prices,
                        borderColor: "rgb(111, 127, 214)",
                        lineTension: 0.1,
                    }
                ]
            },
            options: {
            responsive: true,
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
