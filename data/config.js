export default {
    fullpageOptions: {
        continuousVertical: true,  // 循环展示
        // navigation: true,         // 显示 section 目录
        // slidesNavigation: true,   // 显示 slide   目录
        controlArrows: false,     // 隐藏 slide 横向滑箭头
        scrollOverflow: false,    // 不然 section2 会寄
    },
    typedList: [
        [
            '#typed',
            {
                strings: ['施工中...', '摸鱼中...'],
                typeSpeed: 200,   // 打字速度
                backSpeed: 100,    // 退格速度
                backDelay: 1000,  // 退格前延时
                // 循环
                loop: true,
                loopCount: Infinity,
                // 显示 cursor
                showCorsor: true,
                cursorChar: '|',
                autoInsertCss: true,
            }
        ]
    ],
};