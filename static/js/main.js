import { MyChart } from "./my_chart.js";
import { MyTable } from "./my_table.js";

window.onload = function() {

    var _chart = new MyChart("main_chart");
    var _table = new MyTable("main_table");

    MyChart.draw(_chart, 2);
    _table.set_select_item_cb( function(item_id) {
        MyChart.draw(_chart, item_id);
    });
}