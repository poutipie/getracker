export { XHttpBackEnd };

class XHttpBackEnd {

    static async fetch_items(filter= '') {

        let xhttp = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: `{"filter": "${filter}"}`
        }
    
        return fetch("item_data", xhttp).then( (response) => response.json())
    }
    
    static async fetch_chart_5m(item_id) {
    
        let xhttp = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: `{"item_id": "${item_id}"}`
        }
    
        return fetch("chart_5m", xhttp).then( (response) => response.json())
    }

}
