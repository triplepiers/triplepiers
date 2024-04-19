import { Paper } from './paper.js';
import { clickEffect } from './clickEffect.js';

/*
    根据元素的 delay 属性设置 animationDelay，单位为 (0.1s)
*/
function setAnimationDelay() {
    document.querySelectorAll('[delay]').forEach((ele) => {
        ele.style.animationDelay = ele.getAttribute('delay')*0.1 + 0.5 + 's';
    })
}

/*
    1. 关闭加载动画
    2. 开启彩带动画
    3. 关闭彩带动画、开启点击特效
*/
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

/*
    切换当前显示的 section（通过添加/移除类名 in / out 实现）
    durations: 每个 section 动画持续的时间（ms）
    stay：每个 section 动画播放完毕后保持的时间（ms）
    gap：上下 section 出入场动画错开的时间
    init：初始时延
    forward：最后一个 section 播放完毕后是否消失
*/
function switchSection(durations, stay, gap, init=0, forward=false) {
    let sections = document.querySelectorAll('.main section');
    let timer = init;
    let maxx = forward ? sections.length-1 : sections.length;
    for (let i=0 ; i<maxx; i++) {
        timer += durations[0] + stay;
        setTimeout(() => {
            sections[i].classList.add('out');
            if (i>0) sections[i].classList.remove('in');
        }, timer);
        setTimeout(() => {
            sections[i+1].classList.add('in');
        }, timer+gap);
    }
}

setAnimationDelay();
window.onload = () => {
    document.body.classList.add('loaded');
    setTimeout(() => initAnimation(), 1000);
    switchSection([4000, 2000, 3000], 600, 500, 500, true);
}