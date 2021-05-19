
import {XHttpBackEnd} from "./xhttp_backend.js";

export class MyTable {

    constructor(table_id) {

        this.table = document.getElementById(table_id);
        this.tbody = this.table.getElementsByTagName('tbody')[0];
        this.select_item_cb = function(item_id) {};
        MyTable.update(this);
    }

    set_select_item_cb(cb) {
        this.select_item_cb = cb;
    }

    static update(self, filter = '') {
        XHttpBackEnd.fetch_items(filter)
        .then(items => self._backend_update(items));
    }

    _backend_update(items) {
        this.clear_table();
        this.add_items(items);

        if (this.tbody.rows.length > 0) {
            let item_id = this.tbody.rows[0].cells[1].innerHTML;
            this.select_item_cb(item_id);
        }
    }

    clear_table() {
        while(this.tbody.rows.length > 0) {
            this.tbody.deleteRow(0);
        }
    }
    
    add_items(items) {
        
        items.forEach( (item) => {
            var row = this.tbody.insertRow(-1);
            this._insert_cells(row, item);
    
            
            var handler_deco = function(self, row) {
                return function() {
                    let item_id = row.cells[1].innerHTML;
                    self.select_item_cb(item_id);
                }
            }
            row.onclick = handler_deco(this, row);
        });
    }

    _insert_cells(row, item) {

        var profit = item.price_high - item.price_low;
        var roi = (profit / item.price_high) * 100;

        var cell = row.insertCell(0);
        cell.innerHTML = item.name;
    
        var cell = row.insertCell(1);
        cell.innerHTML = item.id;
    
        var cell = row.insertCell(2);
        cell.innerHTML = item.value;
    
        var cell = row.insertCell(3);
        cell.innerHTML = item.price_high;

        var cell = row.insertCell(4);
        cell.innerHTML = item.price_low;

        var cell = row.insertCell(5);
        cell.innerHTML = profit;

        var cell = row.insertCell(6);
        cell.innerHTML = Number.parseFloat(roi).toPrecision(2) + "%";

        var cell = row.insertCell(7);
        cell.innerHTML = item.volume;

        var cell = row.insertCell(8);
        cell.innerHTML = item.ge_limit;
    
        var cell = row.insertCell(9);
        cell.innerHTML = item.members;
    
        var cell = row.insertCell(10);
        cell.innerHTML = item.low_alch;
    
        var cell = row.insertCell(11);
        cell.innerHTML = item.high_alch;
    }
}
