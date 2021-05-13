
import {XHttpBackEnd} from "./xhttp_backend.js";

export class MyTable {

    constructor(table_id) {
        this.table = document.getElementById(table_id);
        XHttpBackEnd.fetch_items().then(items => this.update_table(items));
    }

    update_table(items) {
        this.clear_table();
        this.add_items(items);
    }

    clear_table() {
        while(this.table.rows.length > 1) {
            this.table.deleteRow(1);
        }
    }
    
    add_items(items) {
        
        items.forEach( (item) => {
            var row = this.table.insertRow(-1);
            this._insert_cells(row, item);
    
            //var handler_deco = function(row) {
            //    return function() {
            //        let item_id = row.cells[1].innerHTML;
            //        fetch_chart_5m(item_id).then(item_data => draw_chart(item_data));   
            //    }
            //}
    
            //row.onclick = handler_deco(row);
        });
    }

    _insert_cells(row, item) {

        var cell = row.insertCell(0);
        cell.innerHTML = item.name;
    
        var cell = row.insertCell(1);
        cell.innerHTML = item.id;
    
        var cell = row.insertCell(2);
        cell.innerHTML = item.value;
    
        var cell = row.insertCell(3);
        cell.innerHTML = item.ge_limit;
    
        var cell = row.insertCell(4);
        cell.innerHTML = item.members;
    
        var cell = row.insertCell(5);
        cell.innerHTML = item.low_alch;
    
        var cell = row.insertCell(6);
        cell.innerHTML = item.high_alch;
    }

}
