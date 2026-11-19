const $quest1 = document.querySelector("#question1")
const $buttons1 = $quest1.getElementsByTagName("button")

function selectButton(){
    this.classList.toggle("selected")
}

for (const button of $buttons1){
    button.addEventListener("click", selectButton)
}