const sidebar = document.querySelector('.basecard.sideBar');
const menu = document.querySelector('.basecard.sideBar ul.menu');

function genMenu(menuList) {
    if (menu) {
        menuList.forEach((menuItem, idx) => {
            let item = document.createElement("li");
            item.innerHTML = `<div class="hover"></div><div class="text">${menuItem[0]}<span>${menuItem[1]}</span></div>`;
            item.style.setProperty('--i', idx); // 用来做延时
            menu.appendChild(item);
        });
        // 稍作延迟，表示我写了动画
        setTimeout(() => {
            menu.classList.add('unfold');
        }, 300);
    } else {
        console.log("Error: there is NO menu element");
    }
}

function isSideBarFold() {
    // 监听 main 宽度，决定是否折叠目录
    if (document.body.clientWidth <= 945) {
        menu.classList.remove('unfold');
        sidebar.setAttribute("fold", "true");
    } else {
        sidebar.removeAttribute("fold");
        setTimeout(() => {
            menu.classList.add('unfold');
        }, 300);
    }
}

export {
    genMenu,
    isSideBarFold
}