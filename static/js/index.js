$(document).ready(function () {
    // 公告板时间刷新
    function updateDateTime() {
        var currentDate = new Date();
        var formattedDate = currentDate.toLocaleString();
        $('#current-datetime').text(formattedDate);
    }

    // Call the updateDateTime function initially
    updateDateTime();
    // Update the datetime every second
    setInterval(updateDateTime, 1000);


    // 每日金句
    var apiUrl = 'https://api.xygeng.cn/one';
    var content = $('#daily-golden-sentence-content');
    var source = $('#daily-golden-sentence-source');

    function requestAndDisplaySentence() {
    $.ajax({
        url: apiUrl,
        method: 'GET',
        dataType: 'json',
        success: function (response) {
            if (response.data.content.length > 45) {
                setTimeout(function() {
                    requestAndDisplaySentence(); // 递归调用函数，直到长度小于等于45个字为止
                }, 1000); // 等待1秒
            } else {
                content.text(response.data.content);
                source.text("——" + response.data.name + "·" + response.data.origin);
            }
        },
        error: function () {
            content.text('Failed to fetch the daily sentence.');
        }
        });
    }
    // requestAndDisplaySentence();
    $(window).on('load', requestAndDisplaySentence);

});
