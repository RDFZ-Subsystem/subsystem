let cnt = Array(en.length).fill(2), firstime = Array(en.length).fill(true);
let idx = 0, flag = false;

function deleteWord(id) {
    en.splice(id, 1);
    zh.splice(id, 1);
    cnt.splice(id, 1);
    firstime.splice(id, 1);
    if (sm) sen.splice(id, 1)
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

function showWord() {
    flag = false;
    idx = getRandomInt(0, en.length);
    document.getElementById('word').innerText = en[idx];
    document.getElementById('sen').innerText = '';
    document.getElementById('tip').innerText = '';
    if (firstime[idx]) document.getElementById('first').innerText = 'first time';
    else document.getElementById('first').innerText = '';
    document.getElementById('remain').innerText = en.length;
    document.getElementById('wordcnt').innerText = cnt[idx];
    document.getElementById('guide').innerText = 'Please recall the meaning of the word.';
    document.getElementById('know').style.display = 'none';
    document.getElementById('donotknow').style.display = 'none';
    document.getElementById('next').style.text-align = 'center';
}

function showTip() {
    flag = true;
    document.getElementById('tip').innerText = zh[idx];
    if (sm) document.getElementById('sen').innerText = sen[idx];
    document.getElementById('guide').innerText = '';
    document.getElementById('know').style.text-align = 'center';
    document.getElementById('donotknow').style.text-align = 'center';
    document.getElementById('next').style.display = 'none';
}


function checkKnow() {
    cnt[idx]--;
    if (firstime[idx] || cnt[idx] === 0) {
        deleteWord(idx);
    }
    if (en.length === 0) {
        document.getElementById('know').disabled = true;
        document.getElementById('donotknow').disabled = true;
        document.getElementById('next').disabled = true;
        document.getElementById('finish').innerText = 'Finished';
    } else {
        showWord();
    }
}

function checkDonotknow() {
    firstime[idx] = false;
    cnt[idx] = 2;
    showWord();
}

document.onkeydown = function(event) {
    if (event.keyCode == 40 || event.keyCode == 83) {
        showTip();
    }
};

document.onkeydown = function(event) {
    if ((event.keyCode == 37 || event.keyCode == 65) && flag) {
        checkKnow();
    }
    if ((event.keyCode == 39 || event.keyCode == 68) && flag) {
        checkDonotknow();
    }
};

window.onload = showWord;