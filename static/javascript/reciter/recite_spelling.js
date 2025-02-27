let cnt = Array(en.length).fill(2), firstime = Array(en.length).fill(true);
let idx = 0, flag = false, input;

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

    idx = getRandomInt(0, en.length);
    document.getElementById('word').innerText = zh[idx];
    if (firstime[idx]) document.getElementById('first').innerText = 'first time';
    else document.getElementById('first').innerText = '';
    document.getElementById('remain').innerText = en.length;
    document.getElementById('wordcnt').innerText = cnt[idx];
    document.getElementById('user_ans').innerText = '';
}

function showTip() {

    flag = true;
    document.getElementById('tip').innerText = en[idx];
    document.getElementById('wordcnt').innerText = cnt[idx];
    document.getElementById('user_ans').innerText = input;
    if (sm) document.getElementById('sen').innerText = sen[idx];
}

function checkInput() {
    input = document.getElementById('input').value;
    if (flag) {
        document.getElementById('tip').innerText = '';
        document.getElementById('sen').innerText = '';
        document.getElementById('input').value = '';
        showWord();
        flag = false;
    } else {
        if (input === en[idx]) {
            cnt[idx]--;
            if (firstime[idx] || cnt[idx] === 0) {
                deleteWord(idx);
            }
            if (en.length === 0) {
                document.getElementById('input').disabled = true;
                document.getElementById('submit').disabled = true;
                document.getElementById('finish').innerText = 'Finished';
            } else {
                document.getElementById('input').value = '';
                showWord();
            }
        } else {
            firstime[idx] = false;
            cnt[idx] = 2;
            document.getElementById('input').value = '';
            showTip();
        }
    }
}


window.onload = showWord;
