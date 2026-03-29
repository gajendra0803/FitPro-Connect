function bicepPopup() {
    document.getElementById("bicep").style.display = "flex";
}

function bicepclosePopup() {
    document.getElementById("bicep").style.display = "none";
}

function squatPopup() {
    document.getElementById("squat").style.display = "flex";
}

function pushUp_popup(){
    document.getElementById("Pushup").style.display="flex";
}

function Crunches_popup(){
    document.getElementById("Crunches").style.display="flex";
}
function Crunchesclose_popup(){
    document.getElementById("Crunches").style.display="none";
}

function PushupclosePopup(){
    document.getElementById("Pushup").style.display="none";
}

function squatclosePopup() {
    document.getElementById("squat").style.display = "none";
}

function start_bicep_curl() {
    window.open("/start-bicep_curl", "_blank");  // Ab Flask ka index.html naye tab me open hoga
}

function start_squat() {
    window.open("/start-squat", "_blank");  // Ab Flask ka index.html naye tab me open hoga
}

function start_pushup() {
    window.open("/start-pushup", "_blank");  // Ab Flask ka index.html naye tab me open hoga
}

function start_crunches() {
    window.open("/start-crunches", "_blank");  // Ab Flask ka index.html naye tab me open hoga
}



