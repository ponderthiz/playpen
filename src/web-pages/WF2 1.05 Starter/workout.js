const $list = document.querySelector("#my-list")

const $span = document.querySelector("span")

let $items = $list.getElementsByTagName("li")

let num = $items.length

const $buttons = $list.getElementsByTagName("button")
for (const button of $buttons){
    button.addEventListener("click", removeItem)
}

const $addBtn = document.querySelector("#addBtn");
$addBtn.addEventListener("click", addItem);



update()

function update(){
    let $strikes = document.querySelectorAll(".strike")
    let remaining = num - $strikes.length
    $span.textContent = `(${remaining} left!)`
    if(remaining == 0){
        setTimeout( alert, 500, "Way to go Ken!")
    }
}

function addItem(){
    let $item = document.createElement("li")
    let $input = document.querySelector("#myInput")
    $item.textContent = $input.value
    $item.addEventListener("click", strikeItem);
    $input.value = ""
    addButton($item)

    $list.append($item)
    num += 1
    update()
}

function removeItem(){
    this.parentElement.remove()
    num -= 1
    update()
}

function strikeItem(){
    this.classList.toggle("strike")
    update()
}

for (const item of $items){
    item.addEventListener("click", strikeItem)
}

function addButton($item){
    let $button = document.createElement("button")
    $button.textContent = "X"
    $button.addEventListener("click", removeItem)
    $item.append($button)
}