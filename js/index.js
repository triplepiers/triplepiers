import data from '../data/data.js';
import configs from '../data/config.js';

import { SideBarHandler } from './menu.js';
import { moveCursors } from './cursor.js';

function initFullPage(config) {
    // init 
    $('#fullpage').fullpage(config);

    // other methods
    // $.fn.fullpage.setAllowScrolling(false); // 禁止滚动（只能方向键 / menu）
}

function initTyped(typedList) {
    typedList.forEach((typedConfig) => {
        new Typed(...typedConfig)
    })
}

function initHomePage(configs, sideBarHandler) {
    $(document).ready(function () {
        // overall
        initFullPage(configs['fullpageOptions']);

        // section1
        initTyped(configs['typedList']);

        // section2
        sideBarHandler.init(); // 生成目录项，并判断侧边目录是否展开
    });

    window.onresize = () => {
        sideBarHandler.isSideBarFold(); // 判断侧边目录是否展开
    }

    window.onmousemove = (e) => {
        moveCursors(e); // 移动 cursor
    }
}

const sideBarHandler = new SideBarHandler(
    '.section2 .basecard.sideBar', 
    '.basecard.sideBar ul.menu', 
    '.section2 .basecard.main .basecard-title',
    data['menu']
);

initHomePage(configs, sideBarHandler);