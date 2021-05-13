

function update_table(items) {
    clear_table();
    add_items(items);
}

function clear_table() {
    var _table = document.getElementById('main_table');
    while(_table.rows.length > 1) {
        _table.deleteRow(1);
    }
}

function add_items(items) {

    let _table = document.getElementById('main_table');

    items.forEach( (item) => {
        var row = _table.insertRow(-1);
        _insert_cells(row, item);

        handler_deco = function(row) {
            return function() {
                let item_id = row.cells[1].innerHTML;
                fetch_chart_5m(item_id).then(item_data => draw_chart(item_data));   
            }
        }

        row.onclick = handler_deco(row);
    });
}


function _insert_cells(row, item) {

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