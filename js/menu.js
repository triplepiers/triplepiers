export class SideBarHandler {
    constructor(sidebarTag, menuTag, mainTitleTag, menuList) {
        this.sidebar = document.querySelector(sidebarTag);
        this.menu = document.querySelector(menuTag);
        this.mainTitle = document.querySelector(mainTitleTag);
        this.menuList = menuList;

        this.menuEleList = null;
        this.activeIdx = 0;        // 默认选择第一版
    }

    init() {
        this.genMenu();
        this.isSideBarFold();
    }

    // 生成侧边的一级目录
    genMenu() {
        if (this.menu) {
            this.menuList.forEach((menuItem, idx) => {
                let item = document.createElement("li");
                item.innerHTML = `<div class="hover"></div><div class="text">${menuItem[0]}<span>${menuItem[1]}</span></div>`;

                item.style.setProperty('--i', idx); // 用来做延时
                item.addEventListener('click', () => {
                    this.handleClick(idx)
                })

                this.menu.appendChild(item);
            });

            // 稍作延迟，表示我写了动画
            setTimeout(() => {
                this.menu.classList.add('unfold');
            }, 300);

            // 更新一下 EleList
            this.menuEleList = this.menu.querySelectorAll("li");
            // 默认激活第一项
            this.activate(this.activeIdx);
        } else {
            console.log("Error: there is NO menu element");
        }
    }

    // 判断侧边目录是否展开
    isSideBarFold() {
        // 监听 main 宽度，决定是否折叠目录
        if (document.body.clientWidth <= 945) {
            this.menu.classList.remove('unfold');
            this.sidebar.setAttribute("fold", "true");
        } else {
            this.sidebar.removeAttribute("fold");
            setTimeout(() => {
                this.menu.classList.add('unfold');
            }, 300);
        }
    }

    // 激活一级菜单
    activate(idx) {
        // 修改侧边栏
        this.menuEleList[idx].setAttribute('active', true);
        // 修改主栏
        this.mainTitle.innerHTML = `${this.menuList[idx][0]}<span>${this.menuList[idx][1]}</span>`;
        // loadData
        this.loadData(idx);
    }

    // 处理点击事件
    handleClick(idx) {
        // if change
        if (idx != this.activeIdx) {
            // deactivate
            this.menuEleList[this.activeIdx].removeAttribute('active');
            // activate
            this.activate(idx);
            this.activeIdx = idx;
        }
    }

    // 更新主栏内容
    loadData(idx) {
        console.log("TODO: loading data for section ", idx, "...")
    }
}