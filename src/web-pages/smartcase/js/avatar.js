const avatar_object = {
    name: '',
    robe_color: '',
    power: [],
    getName() {
        console.log(this.name)
    }
}

function updateName() {
    let $avatar = document.querySelector("#char_name")
    avatar_object.name = $avatar.value
}

const $submit = document.querySelector("#submit")
$submit.addEventListener("click", updateName)