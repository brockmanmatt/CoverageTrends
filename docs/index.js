const topics = [
'virus_20200525-0900','trump_20200525-0900','memori_20200525-0900','death_20200525-0900','covid_20200525-0900','case_20200525-0900','black_20200525-0900','biden_20200525-0900','amid_20200525-0900','florida_20200525-0830','weekend_20200525-0800','pandem_20200525-0800','world_20200524-1800','ain_20200524-1010','summer_20200523-2130','time_20200523-1330','beach_20200523-1230','china_20200523-1100'
]
const VARtopics = [
'ain','world','reopen','amid','biden','black','case','coronavirus','covid','memori','pandem','trump','virus','weekend','death','florida'
]
const SARIMAXtopics = [
'reopen','amid','biden','black','case','coronavirus','covid','memori','pandem','trump','virus','weekend','death','florida'
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
function setupVARImgBox(){
    var myToken=document.getElementById("VARButton").value;
    var myIssue = myToken
    issue = myIssue
    img_name = issue + ".jpg";
    var newHTML = '<img src = "./models/VAR/';
    newHTML += img_name;
    newHTML += '" width=90%>';
    document.getElementById("imgBox").innerHTML = newHTML;
};
function setupSARIMAXImageBox(){
    var myToken=document.getElementById("SARIMAXButton").value;
    var myIssue = myToken
    issue = myIssue
    img_name = issue + ".jpg";
    var newHTML = '<img src = "./models/SARIMAX/';
    newHTML += img_name;
    newHTML += '" width=90%>';
    document.getElementById("imgBox").innerHTML = newHTML;
};
function setupDropdownBox(){
    newHTML = '<table id="SelectTable">'
    newHTML += '<caption><i>Select a Series</i></caption>'
    newHTML += '<tr><th>Issue (last updated)</th><th>VAR Model</th></th><th>SARIMAX Model</th></tr>'
    newHTML += '<td><select id="issueButton" onchange="setupImgBox()">';
    topics.forEach(topic => newHTML+= '<option value='+topic+'>'+topic+'</option>');
    newHTML += '</select></td>'
    newHTML += '<td><select id="VARButton" onchange="setupVARImgBox()">';
    VARtopics.forEach(topic => newHTML+= '<option value='+topic+'>'+topic+'</option>');
    newHTML += '</select></td>'
    newHTML += '<td><select id="SARIMAXButton" onchange="setupSARIMAXImageBox()">';
    SARIMAXtopics.forEach(topic => newHTML+= '<option value='+topic+'>'+topic+'</option>');
    newHTML += '</select></td>'
    newHTML += '</tr></table>';
    document.getElementById("dropdowns").innerHTML = newHTML;
};
