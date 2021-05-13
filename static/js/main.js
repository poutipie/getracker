import { MyChart } from "./my_chart.js";
import { MyTable } from "./my_table.js";
import { MySearch } from "./my_search.js";

window.onload = function() {

    var _chart = new MyChart("main_chart");
    var _table = new MyTable("main_table");
    var _search = new MySearch("search");

    _table.set_select_item_cb( function(item_id) {
        MyChart.draw(_chart, item_id);
    });

    _search.set_text_enter_handler (function(filter) {
        MyTable.update(_table, filter);
    });
}