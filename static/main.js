function display() {
    var refresh = 1000;
    myTime = setTimeout('display_time()',refresh);
}
       
function display_time() {
    const d = new Date();
    let text = d.toLocaleTimeString('en-US', {hour12: false});
    document.getElementById("time").innerHTML = text;
    display();
}


var start = document.getElementById('control');
var reset = document.getElementById('reset');

var h = document.getElementById("hour");
var m = document.getElementById("minute");
var s = document.getElementById("sec");

var h_b = document.getElementById("hour_b");
var m_b = document.getElementById("minute_b");
var s_b = document.getElementById("sec_b");
var trig = document.getElementById("triggerAudio");

//store a reference to the startTimer variable
var startTimer = null;
var statusTimer = false;
start.addEventListener('click', function(){
    //initialize the variable
    if (statusTimer === false) {
        startTime();
    } else {
        stopTime();
    }
})

reset.addEventListener('click', function(){
    h.value = 0;
    m.value = 0;
    s.value = 0;

    h_b.value = 0;
    m_b.value = 0;
    s_b.value = 0;
    //stop the timer after pressing "reset"
    stopTime()
})

function timer(){
    if(h.value == 0 && m.value == 0 && s.value == 0){
        h.value = 0;
        m.value = 0;
        s.value = 0;
    } else if(h.value == 0 && m.value == 0 && s.value == 1){
        s.value--;
        trig.click();
    } else if(s.value != 0){
        s.value--;
    } else if(m.value != 0 && s.value == 0){
        s.value = 59;
        m.value--;
    } else if(h.value != 0 && m.value == 0){
        m.value = 60;
        h.value--;
    }
    
    //Stop Timer if user didn't fill Break input
    if (h.value == 0 && m.value == 0 && s.value == 0 && h_b.value == 0 && m_b.value == 0 && s_b.value == 0) {
        stopTime();
    }

     //Break Timer Countdown
    if (h.value == 0 && m.value == 0 && s.value == 0){
        if(h_b.value == 0 && m_b.value == 0 && s_b.value == 0){
            h_b.value = 0;
            m_b.value = 0;
            s_b.value = 0;
        } else if(h_b.value == 0 && m_b.value == 0 && s_b.value == 1){
            s_b.value--;
            trig.click();
            stopTime();
        } else if(s_b.value != 0){
            s_b.value--;
        } else if(m_b.value != 0 && s_b.value == 0){
            s_b.value = 59;
            m_b.value--;
        } else if(h_b.value != 0 && m_b.value == 0){
            m_b.value = 60;
            h_b.value--;
        }
    } 
}

trig.addEventListener('click', function(){
    play();
})


function startTime(){
    control.innerHTML = '<span>Pause</span>'
    control.classList.add("timer__btn--stop")
    control.classList.remove("timer__btn--start")
    statusTimer = true 
    startTimer = setInterval(function() {
        timer();
    }, 1000);
}

//stop the function after pressing the reset button, 
//so the time wont go down when selecting a new time after pressing reset
function stopTime() {
    control.innerHTML = '<span>Start</span>'
    control.classList.add("timer__btn--start")
    control.classList.remove("timer__btn--stop")
    statusTimer = false
    clearInterval(startTimer);
}

function play() {
    var audio = document.getElementById("audio");
    audio.play();
  }

