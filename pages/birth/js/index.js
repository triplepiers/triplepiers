import { Paper } from './paper.js';
import { clickEffect } from './clickEffect.js';

window.onload = () => {
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