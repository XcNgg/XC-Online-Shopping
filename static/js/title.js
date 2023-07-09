// 网站被隐藏后title动效
 var OriginTitle = document.title;
 var titleTime;
 document.addEventListener('visibilitychange', function () {
     if (document.hidden) {
         document.title = '崩溃了ヽ(●-`Д´-)ノ';
         clearTimeout(titleTime);
     }
     else {
         document.title = '恢复啦ヾ(Ő∀Ő)ノ' + OriginTitle;
         titleTime = setTimeout(function () {
             document.title = OriginTitle;
         }, 500);
     }
 });
