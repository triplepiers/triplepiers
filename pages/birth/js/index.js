import { Paper } from './paper.js';
import { clickEffect } from './clickEffect.js';

function setAnimationDelay() {
    document.querySelectorAll('[delay]').forEach((ele) => {
        ele.style.animationDelay = ele.getAttribute('delay')*0.1 + 0.5 + 's';
    })
}

function initAnimation() {
    document.getElementById("loader").style.display = 'none';
    document.getElementById("main").classList.add('show');
    var paper = new Paper({
        params: {
            width: window.innerWidth,     //背景图的宽
            height: window.innerHeight + 30, //背景图的高,
            duration: 5000,
            isLoop: false
        }
    })
    setTimeout(() => {
        paper = null;  // 停止彩带飘落
        document.getElementById('paper').style.opacity = '0'; // 移除彩带画布
        clickEffect(); // 开始点击特效
    }, 5000)
}

function switchSection() {
    let sections = document.querySelectorAll('.main section');
    setTimeout(() => {
        sections[0].classList.add('out');
        sections[1].classList.add('in');
    }, 4500);
    setTimeout(() => {
        sections[1].classList.remove('in');
        sections[1].classList.add('out');
        sections[2].classList.add('in');
    }, 7000);
}

setAnimationDelay();
window.onload = () => {
    document.body.classList.add('loaded');
    setTimeout(() => initAnimation(), 1000);
    switchSection();
}