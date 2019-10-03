var apiBox = document.getElementById("api-key");
var generateButton = document.getElementById("generate-api");
var clearButton = document.getElementById("clear-api");

function generateAPI(){
    var api = Math.random()*10000;
    apiBox.setAttribute("placeholder", api);
}

function clearAPI(){
    apiBox.removeAttribute("placeholder");
}