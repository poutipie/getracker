
export class MySearch {

    constructor(input_id) {
        this.input = document.getElementById(input_id);
        this.on_enter_cb = function(text) {};
    
        this.input.addEventListener("keyup", MySearch.text_enter_handler(this));
    }

    set_text_enter_handler(cb) {
        this.on_enter_cb = cb;
    }

    static text_enter_handler(self) {
        return function(event) {
            if (event.code === "Enter") {
                event.preventDefault();
                self.on_enter_cb(self.input.value);
            }
        }
    }
}