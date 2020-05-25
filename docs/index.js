const topics = [
'virus_20200525-2100','trump_20200525-2100','pandem_20200525-2100','memori_20200525-2100','honor_20200525-2100','covid_20200525-2100','biden_20200525-2100','american_20200525-2100','weekend_20200525-2030','home_20200525-2000','carolina_20200525-1930','reopen_20200525-1900','year_20200525-1830','penc_20200525-1830','nation_20200525-1730','amid_20200525-1600','case_20200525-1530','know_20200525-1430','make_20200525-1330','black_20200525-1230','death_20200525-1000','florida_20200525-0830','world_20200524-1800','ain_20200524-1010','summer_20200523-2130','time_20200523-1330','beach_20200523-1230','china_20200523-1100'
]
const VARtopics = [
'ain','world','reopen','amid','biden','black','case','coronavirus','covid','memori','pandem','trump','virus','weekend','death','florida','make','know','american','nation','year','home','honor'
]
const SARIMAXtopics = [
'reopen','amid','biden','black','case','coronavirus','covid','memori','pandem','trump','virus','weekend','death','florida','make','know','american','nation','year','home','honor'
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
