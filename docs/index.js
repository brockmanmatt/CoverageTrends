const topics = [
'vote+mail_20200528-1710','trump_20200528-1710','test_20200528-1710','reopen_20200528-1710','order_20200528-1710','minneapoli_20200528-1710','kong+hong_20200528-1710','georg_20200528-1710','floyd_20200528-1710','death_20200528-1710','covid_20200528-1710','coronavirus_20200528-1710','twitter_20200528-0830','mail+vote_20200528-0830','fact_20200528-0830','check_20200528-0830','lost_20200527-2250','hous_20200527-2250','pandem_20200527-1830','mask_20200527-1830','case_20200527-1830','polic_20200527-0920','plan_20200527-0920','biden_20200527-0920','american_20200527-0050','presid_20200526-2110','memori_20200526-1100','american_20200526-1100','memori_20200526-1040','american_20200526-1040','home_20200526-0610','summer_20200526-0530','face_20200526-0430','year_20200526-0330','virus_20200525-2230','live_20200525-2230','honor_20200525-2100','weekend_20200525-2030','carolina_20200525-1930','penc_20200525-1830','nation_20200525-1730','amid_20200525-1600','know_20200525-1430','make_20200525-1330','black_20200525-1230','florida_20200525-0830','world_20200524-1800','ain_20200524-1010','time_20200523-1330','beach_20200523-1230','china_20200523-1100'
]
const VARtopics = [
'world','check','summer','amid','american','reopen','make','case','order','floyd','hous','fact','year','lost','home','pandem','know','face','black','protest','virus','polic','mail+vote','test','coronavirus','biden','nation','weekend','vote+mail','twitter','covid','honor','death','georg','kong+hong','plan','mask','trump','florida','live','memori','ain'
]
const SARIMAXtopics = [
'check','summer','amid','american','reopen','make','case','order','floyd','hous','fact','year','lost','home','pandem','know','face','black','protest','virus','polic','mail+vote','test','coronavirus','biden','nation','weekend','vote+mail','twitter','covid','honor','death','georg','kong+hong','plan','mask','trump','florida','live','memori'
]
const CORRELATIONtopics = [
'memori','trump','mask','kong+hong','plan','death','georg','coronavirus','biden','test','mail+vote','twitter','covid','vote+mail','lost','year','floyd','fact','hous','polic','protest','face','home','pandem','american','summer','check','case','order','reopen'
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
