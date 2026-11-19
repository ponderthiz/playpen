// const $h2 = document.querySelector('h2');
// $h2.textContent = "Ken's To Do List";

const $list = document.querySelector("#my-list");
let $items = $list.getElementsByTagName("li");

const $span = document.querySelector("span");


function addItem(text) {
    let $newItem = document.createElement("li");
    $newItem.textContent = text;
    $list.append($newItem);
    update();
}

function removeItem(index) {
    $items[index].remove();
    update();
}

function strikeItem(index) {
    $items[index].setAttribute("class", "strike");
    update();
}

function update() {
    const count = $list.getElementsByTagName("li").length;
    $span.textContent = ` ${count} items left`;
    if (count === 0) {
        alert("All done!");
    }
}

update();
addItem("Eat");
removeItem(2);