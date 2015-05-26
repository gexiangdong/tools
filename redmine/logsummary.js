document.write('<div id="logsummary"></div>');

function showCommitLogReport(index){
    var html = '';
    var data;
    if(index == 0){
        data = logSummary7;
    }else if(index == 1){
        data = logSummary30;
    }else{
        data = logSummaryAll;
    }
    html += "<ul>";
    html += '<li class="' + (index == 0 ? 'current' : '') + '"><a href="javascript:showCommitLogReport(0);">最近一周</a></li>';
    html += '<li class="' + (index == 1 ? 'current' : '') + '"><a href="javascript:showCommitLogReport(1);">最近30天</a></li>';
    html += '<li class="' + (index == 2 ? 'current' : '') + '"><a href="javascript:showCommitLogReport(2);">所有提交日志</a></li>';
    html += "</ul>";
    
    html += "<table><thead><tr><th>用户</th><th>提交次数</th><th>关联redmine次数</th><th>关联比例</th></tr></thead>";
    html += "<tbody>";
    for(i=0; i<data.length; i++){
        var rate = data[i][2] * 100.0 / data[i][1];
        rate = Math.round(rate);
        styleClass = "score" + Math.floor(rate / 10);
        html += '<tr class="' + styleClass + '">';
        html += '<td class="name">' + data[i][0] + '</td>';
        html += '<td class="count">' + data[i][1] + '</td>';
        html += '<td class="passcount">' + data[i][2] + '</td>';
        html += '<td class="passrate">' + rate + '%</td>';
        html += '</tr>';
    }
    html += "</tbody>";
    html += "</table>";
    
    document.getElementById("logsummary").innerHTML = html;
}

window.setTimeout("showCommitLogReport(0)", 1000);
