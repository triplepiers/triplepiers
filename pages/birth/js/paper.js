"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * by muji@2dfire.com
 * 设计思路：2个主要方法，Paper(),Process();
 * Paper()方法主要用于
 * 1.创建canvas实例，build();
 * 2.渲染canvas实例，render();
 * 
 * Process()方法主要是用于:计算进程,控制动画的状态。 
 */

var Paper = function () {
    function Paper(_ref) {
        var params = _ref.params;

        _classCallCheck(this, Paper);

        this.CONST = {
            SPRITE_WIDTH: 20,
            SPRITE_HEIGHT: 20,
            PAPER_LENGTH: 500, //纸片数量
            DURATION: 8000,
            TRANSLATE_RATE: 50,
            COLORS: ["#EF5350", "#EC407A", "#AB47BC", "#7E57C2", "#5C6BC0", "#42A5F5", "#29B6F6", "#26C6DA", "#26A69A", "#66BB6A", "#9CCC65", "#D4E157", "#FFEE58", "#FFCA28", "#FFA726", "#FF7043", "#8D6E63", "#BDBDBD", "#78909C"]
            //定义父元素，最基础canvas宽高，纸片数量，定位时y的范围，间隔时常,旋转角度，旋转速度
        };var elm = params.elm,
            width = params.width,
            height = params.height,
            length = params.length,
            yRange = params.yRange,
            duration = params.duration,
            rotationRange = params.rotationRange,
            speedRange = params.speedRange,
            isLoop = params.isLoop;
        /**确定父元素，默认父元素body */
        //删除已有的canvas

        this.parent = document.getElementById(elm) || document.body;
        if (document.getElementsByTagName("canvas").length > 0) {
            this.canvas = null;
            this.parent.removeChild(this.parent.childNodes[0]);
        }
        this.canvas = document.createElement("canvas");
        this.canvas.id = 'paper';
        this.ctx = this.canvas.getContext("2d");
        this.width = width || this.parent.offsetWidth;
        this.height = height || this.parent.offsetHeight;
        this.length = length || this.CONST.PAPER_LENGTH;
        this.yRange = yRange || this.height * 2;
        this.progress = new Progress({
            duration: duration || this.CONST.DURATION,
            isLoop: isLoop
        });
        this.rotationRange = typeof rotationRange === "number" ? rotationRange : 10;
        this.speedRange = typeof speedRange === "number" ? speedRange : 10;
        //纸片canvas集合
        this.sprites = [];
        this.canvas.style.cssText = ["display: block", "position: absolute", "top: 0", "left: 0", "pointer-events: none"].join(";");
        this.render = this.render.bind(this);
        this.build();
        this.parent.append(this.canvas);
        this.progress.start(performance.now());
        requestAnimationFrame(this.render);
    }

    _createClass(Paper, [{
        key: "build",
        value: function build() {
            for (var i = 0; i < this.length; ++i) {
                var canvas = document.createElement("canvas"),
                    ctx = canvas.getContext("2d");

                canvas.width = this.CONST.SPRITE_WIDTH; //定义的常量纸片的宽
                canvas.height = this.CONST.SPRITE_HEIGHT; //定义的常量纸片的高

                canvas.position = {
                    initX: Math.random() * this.width,
                    initY: -canvas.height - Math.random() * this.yRange
                };

                canvas.rotation = this.rotationRange / 2 - Math.random() * this.rotationRange;
                canvas.speed = this.speedRange / 2 + Math.random() * (this.speedRange / 2);

                ctx.save();
                ctx.fillStyle = this.CONST.COLORS[Math.random() * this.CONST.COLORS.length | 0]; //随机的填充颜色
                var random = Math.random() * 3;
                if (random < 1) {
                    ctx.arc(10, 10, 10, 0, Math.PI * 2); //圆形坐标x，圆心坐标y，r半径，开始角度，结束角度
                } else if (random < 2) {
                    ctx.fillRect(0, 0, canvas.width, canvas.height); //绘制四边形
                } else {
                    //绘制三角形
                    ctx.moveTo(0, 0);
                    ctx.lineTo(0, 20);
                    ctx.lineTo(20, 20);
                    ctx.closePath();
                }
                ctx.fill();
                ctx.restore();
                this.sprites.push(canvas);
            }
        }
    }, {
        key: "render",
        value: function render(now) {
            var progress = this.progress.tick(now);

            this.canvas.width = this.width;
            this.canvas.height = this.height;

            for (var i = 0; i < this.length; ++i) {
                this.ctx.save();
                /**
                 * 纸片的初始位置x + 纸片旋转 * 常量平移*进程
                 */

                this.ctx.translate(this.sprites[i].position.initX + this.sprites[i].rotation * this.CONST.TRANSLATE_RATE * progress, //添加到水平坐标（x）上的值
                this.sprites[i].position.initY + progress * (this.height + this.yRange)); //添加到垂直坐标（y）上的值。
                this.ctx.rotate(this.sprites[i].rotation); //方法旋转当前的绘图。
                this.ctx.drawImage(this.sprites[i], //图像，画布或视频
                -this.CONST.SPRITE_WIDTH * Math.abs(Math.sin(progress * Math.PI * 2 * this.sprites[i].speed)) / 2, //在画布上放置图像的 x 坐标位置。
                //雪碧图的width * 
                -this.CONST.SPRITE_HEIGHT / 2, //在画布上放置图像的 y 坐标位置。
                this.CONST.SPRITE_WIDTH * Math.abs(Math.sin(progress * Math.PI * 2 * this.sprites[i].speed)), //可选。要使用的图像的宽度（伸展或缩小图像）
                this.CONST.SPRITE_HEIGHT); //可选。要使用的图像的高度（伸展或缩小图像）。
                this.ctx.restore();
            }
            requestAnimationFrame(this.render);
        }
    }]);

    return Paper;
}();

var Progress = function () {
    function Progress(params) {
        _classCallCheck(this, Progress);

        //默认时常，是否重复
        var duration = params.duration,
            isLoop = params.isLoop;

        this.timestamp = null;
        this.duration = duration || 1000;
        this.progress = 0;
        this.delta = 0;
        this.progress = 0;
        this.isLoop = !!isLoop;
        this.reset();
    }

    _createClass(Progress, [{
        key: "reset",
        value: function reset() {
            this.timestamp = null;
        }
    }, {
        key: "start",
        value: function start(now) {
            this.timestamp = now;
        }
    }, {
        key: "tick",
        value: function tick(now) {
            if (this.timestamp) {
                this.delta = now - this.timestamp;
                this.progress = Math.min(this.delta / this.duration, 1);

                if (this.progress >= 1 && this.isLoop) {
                    this.start(now);
                }
                return this.progress;
            } else {
                return 0;
            }
        }
    }]);

    return Progress;
}();

export {
    Paper
}