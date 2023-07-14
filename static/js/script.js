// 网站被隐藏后title动效
//  var OriginTitle = document.title;
//  var titleTime;
//  document.addEventListener('visibilitychange', function () {
//      if (document.hidden) {
//          document.title = OriginTitle + '崩溃了ヽ(●-`Д´-)ノ';
//          clearTimeout(titleTime);
//      }
//      else {
//          document.title = OriginTitle+'恢复啦ヾ(Ő∀Ő)ノ' ;
//          titleTime = setTimeout(function () {
//              document.title = OriginTitle;
//          }, 500);
//      }
//  });


// 签到显示
function showSigninResult(title, message) {
    $('#signinResult').text(`${title}: ${message}`);
    $('#signinModal').modal('show');
}

// 输入框随机显示
// 在输入框处于输入状态时不触发过渡效果
function rotatePlaceholder() {
    var products = [
        '苹果键盘', '平底锅', '华为手机', '画笔', '英语教科书', '衣服', '文件夹', '戴尔电脑', '刀具套装', '三星手机',
        '美术颜料', '数学教科书', '鞋子', '笔记本', '惠普打印机', '煎锅', '小米手机', '油画画布', '物理教科书', '外套',
        '文件柜', '联想笔记本', '炒锅', 'OPPO手机', '水彩颜料', '化学教科书', '森马短裤', '书包', '戴尔显示器',
        '炖锅', '荣耀手机', '画架', '生物教科书', 'T恤', '文件夹套装', '惠普台式机', '汤锅', '一加手机', '铅笔',
        '历史教科书', '裙子', '电脑包', 'MacBook Pro', '炒菜锅', 'vivo手机', '彩色铅笔', '地理教科书', '衬衫', '信封',
        'MacBook Air', '煮锅', '草稿本', '英语词典', '内裤', '文件夹夹', '戴尔笔记本', '高压锅', '调色板',
        '化妆品教程书', '袜子', '信纸', '联想台式机', '平底炒锅', '三星Galaxy手机', '素描铅笔', '音乐教科书', '外套衣架', '打孔器',
        '惠普笔记本', '焖锅', 'OPPO Reno手机', '水彩画刷', '体育教科书', '裤子夹', '文件夹标签', '戴尔游戏笔记本', '汤煲', '红米手机',
        '钢笔', '计算机科学教科书', '外套挂钩', '订书机', '苹果iMac', '炒面锅', '荣耀Magic手机', '油画棒', '经济学教科书', '衬衫夹',
        '胶带', '联想游戏笔记本', '压力锅', 'vivo X手机', '彩色铅笔套装', '艺术史教科书', '内衣', '文件夹索引', '戴尔工作站', '奶锅',
        '华为Mate手机', '素描纸', '心理学教科书', '连衣裙', '回形针', 'Mac Pro', '蒸锅', '荣耀Play手机', '水粉颜料', '化妆品化学书', '短袜',
        '订书钉', '惠普工作站', '炖煮锅', 'OPPO Find手机', '水彩画本', '哲学教科书', '外套钩', '胶水', '联想工作站', '炒菜铲',
        '三星Note手机', '素描画纸', '政治学教科书', '毛衣', '回形针盒'
    ];

    var searchInput = $('#KeyWordSearch');
    var timer;

    //当输入框获取焦点时，使用clearInterval停止切换placeholder的定时器
    searchInput.on('focus', function () {
        clearInterval(timer);
    });
    //当输入框失去焦点时，调用startTimer函数重新启动切换placeholder的定时器
    //这样就可以在输入框处于输入状态时阻止过渡效果的触发。
    searchInput.on('blur', function () {
        startTimer();
    });

    function startTimer() {
        timer = setInterval(function () {
            var randomNumber = Math.floor(Math.random() * 56) + 1; // 随机生成 1-56
            var currentProductIndex = Math.floor(Math.random() * products.length); // 随机生成 0 - products.length

            var placeholderText = '当前有' + randomNumber + '%的人在搜索[' + products[currentProductIndex] + ']';
            searchInput.fadeOut(400, function () {
                $(this).attr('placeholder', placeholderText).fadeIn(400);
            });
        }, 3000);
    }

    startTimer();


}

$(document).ready(function () {
    rotatePlaceholder();
});



