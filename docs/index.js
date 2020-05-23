const topics = [
'trump_20200523-1800','memori_20200523-1800','coronavirus_20200523-1800','black_20200523-1800','biden_20200523-1800','ain_20200523-1800','weekend_20200523-1700','pandem_20200523-1500','covid_20200523-1400','time_20200523-1330','beach_20200523-1230','reopen_20200523-1200','china_20200523-1100','open_20200523-0330','open_20200523-0300','open_20200523-0230','case_20200523-0000'
]
function setupImgBox(){
    var myToken=document.getElementById("issueButton").value;
    var myIssue = myToken.split('_')
    console.log(myIssue)
    issue = myIssue[1] + '_' + myIssue[0]
    img_name = issue + ".jpg";
    var newHTML = '<img src = "./img/';
    newHTML += img_name;
    newHTML += '" width=90%>';
    document.getElementById("imgBox").innerHTML = newHTML;
};
function setupDropdownBox(){
    newHTML = '<table id="SelectTable">'
    newHTML += '<caption><i>Select a Series</i></caption>'
    newHTML += '<tr><th>Issue (last updated)</th></tr>'
    newHTML += '<td><select id="issueButton" onchange="setupImgBox()">';
    topics.forEach(topic => newHTML+= '<option value='+topic+'>'+topic+'</option>');
    newHTML += '</select></td></tr></table>';
    document.getElementById("dropdowns").innerHTML = newHTML;
};
