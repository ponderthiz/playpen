const passing = 75;

function getCurrent() {
    return parseInt(prompt("What is your current grade?"));
}

function getWeight() {
    return parseInt(prompt("What is the weight of the exam?"));
}

function calculate(c, w) {
    // let examGrade = (passing - (c * (1 - w / 100))) / (w / 100);
    let finalScore = ((passing - (1 - (w / 100))*c) / (w / 100));
    let rounded = Math.round(finalScore);
    return `You must get a score of ${rounded} to pass.`;
}

alert(calculate(getCurrent(), getWeight()));