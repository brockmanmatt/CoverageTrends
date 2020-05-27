const topics = [
'vote_20200527-1840','hong_20200527-1840','twitter_20200527-1830','trump_20200527-1830','pandem_20200527-1830','mask_20200527-1830','death_20200527-1830','covid_20200527-1830','coronavirus_20200527-1830','case_20200527-1830','polic_20200527-0920','plan_20200527-0920','nurs_20200527-0920','mail_20200527-0920','biden_20200527-0920','home_20200527-0900','american_20200527-0050','reopen_20200526-2110','presid_20200526-2110','test_20200526-1100','reopen_20200526-1100','memori_20200526-1100','american_20200526-1100','reopen_20200526-1040','memori_20200526-1040','american_20200526-1040','home_20200526-0610','summer_20200526-0530','face_20200526-0430','year_20200526-0330','virus_20200525-2230','live_20200525-2230','honor_20200525-2100','weekend_20200525-2030','carolina_20200525-1930','penc_20200525-1830','nation_20200525-1730','amid_20200525-1600','know_20200525-1430','make_20200525-1330','black_20200525-1230','florida_20200525-0830','world_20200524-1800','ain_20200524-1010','time_20200523-1330','beach_20200523-1230','china_20200523-1100'
]
const VARtopics = [
'world','summer','amid','american','reopen','make','case','year','home','pandem','know','hong_and_kong','face','black','virus','polic','test','vote_and_mail','coronavirus','biden','nation','weekend','twitter','covid','home_and_nurs','nurs_and_home','honor','mail_and_vote','death','plan','mask','trump','florida','live','memori','ain'
]
const SARIMAXtopics = [
'summer','amid','american','reopen','make','case','year','home','pandem','know','hong_and_kong','face','black','virus','polic','test','vote_and_mail','coronavirus','biden','nation','weekend','twitter','covid','home_and_nurs','nurs_and_home','honor','mail_and_vote','death','plan','mask','trump','florida','live','memori'
]
const CORRELATIONtopics = [
'mail_and_vote','memori','trump','mask','plan','death','coronavirus','biden','vote_and_mail','test','nurs_and_home','home_and_nurs','twitter','covid','year','polic','face','home','hong_and_kong','pandem','american','summer','case','reopen'
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
function setupCORRELATIONImageBox(){
    var myToken=document.getElementById("CORRELATIONButton").value;
    var myIssue = myToken
    issue = myIssue
    var newHTML = '<canvas id="line-chart" width="200" height="200"></canvas>'
    newHTML += '<div id="selectBox"></div>'
    document.getElementById("imgBox").innerHTML = newHTML;
    genGraph(issue)
};
function setupDropdownBox(){
    newHTML = '<table id="SelectTable">'
    newHTML += '<caption><i>Select a Series</i></caption>'
    newHTML += '<tr>'
    newHTML += '<th>Issue (last updated)</th><'
    newHTML += '<th>VAR</th>'
    newHTML += '<th>SARIMAX</th>'
    newHTML += '<th>Lagged Corr</th>'
    newHTML += '</tr>'
    newHTML += '<td><select id="issueButton" onchange="setupImgBox()">';
    topics.forEach(topic => newHTML+= '<option value='+topic+'>'+topic+'</option>');
    newHTML += '</select></td>'
    newHTML += '<td><select id="VARButton" onchange="setupVARImgBox()">';
    VARtopics.forEach(topic => newHTML+= '<option value='+topic+'>'+topic+'</option>');
    newHTML += '</select></td>'
    newHTML += '<td><select id="SARIMAXButton" onchange="setupSARIMAXImageBox()">';
    SARIMAXtopics.forEach(topic => newHTML+= '<option value='+topic+'>'+topic+'</option>');
    newHTML += '</select></td>'
    newHTML += '<td><select id="CORRELATIONButton" onchange="setupCORRELATIONImageBox()">';
    CORRELATIONtopics.forEach(topic => newHTML+= '<option value='+topic+'>'+topic+'</option>');
    newHTML += '</select></td>'
    newHTML += '</tr></table>';
    document.getElementById("dropdowns").innerHTML = newHTML;
};
