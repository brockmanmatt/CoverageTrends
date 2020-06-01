const topics = [
'white_20200601-0610','twitter+trump_20200601-0610','trump_20200601-0610','rioter_20200601-0610','riot_20200601-0610','protest_20200601-0610','polic_20200601-0610','mayor_20200601-0610','georg_20200601-0610','floyd_20200601-0610','death_20200601-0610','covid_20200601-0610','citi_20200601-0610','antifa_20200601-0610','america_20200601-0610','watch_20200601-0430','hong+kong_20200601-0430','store_20200531-2230','offic_20200531-2230','coronavirus_20200531-2230','black_20200531-2230','pandem_20200531-0930','kong+hong_20200531-0930','live_20200530-2150','biden+trump+twitter_20200530-2150','twitter_20200530-0720','reopen_20200530-0720','minneapoli_20200530-0720','coronavirus+trump+biden_20200530-0720','china_20200530-0720','nurs+home_20200529-1650','tweet_20200529-1640','check_20200529-1640','vote+mail_20200528-2350','social_20200528-2350','home_20200528-2350','biden_20200528-2350','test_20200528-1710','order_20200528-1710','mail+vote_20200528-0830','fact_20200528-0830','lost_20200527-2250','hous_20200527-2250','mask_20200527-1830','case_20200527-1830','plan_20200527-0920','american_20200527-0050','presid_20200526-2110','memori_20200526-1100','american_20200526-1100','memori_20200526-1040','american_20200526-1040','summer_20200526-0530','face_20200526-0430','year_20200526-0330','virus_20200525-2230','honor_20200525-2100','weekend_20200525-2030','carolina_20200525-1930','penc_20200525-1830','nation_20200525-1730','amid_20200525-1600','know_20200525-1430','make_20200525-1330','florida_20200525-0830','world_20200524-1800','ain_20200524-1010','time_20200523-1330','beach_20200523-1230'
]
const VARtopics = [
'world','watch','china','check','summer','offic','floyd+death+georg','amid','american','reopen','make','rioter','store','case','order','hong+kong','tweet','nurs+home','floyd','hous','fact','year','lost','home','pandem','know','citi','face','black','protest','virus','polic','floyd+georg+death','mail+vote','test','riot','coronavirus','biden','nation','weekend','vote+mail','twitter','covid','antifa','america','death+floyd+georg','georg+floyd+death','honor','death','georg','kong+hong','plan','mask','white','coronavirus+trump+biden','trump','twitter+trump','florida','live','social','memori','ain','mayor'
]
const SARIMAXtopics = [
'watch','china','check','summer','offic','amid','american','reopen','make','rioter','store','case','order','hong+kong','tweet','nurs+home','floyd','hous','fact','year','lost','home','pandem','know','citi','face','black','protest','virus','polic','floyd+georg+death','mail+vote','test','riot','coronavirus','biden','nation','weekend','vote+mail','twitter','covid','antifa','america','death+floyd+georg','georg+floyd+death','honor','death','georg','kong+hong','plan','mask','white','coronavirus+trump+biden','trump','twitter+trump','florida','live','social','memori','mayor'
]
const CORRELATIONtopics = [
'georg+floyd+death','death+floyd+georg','social','memori','live','mayor','twitter+trump','trump','mask','kong+hong','plan','coronavirus+trump+biden','white','death','georg','riot','coronavirus','biden','test','mail+vote','floyd+georg+death','antifa','america','twitter','covid','vote+mail','lost','year','floyd','fact','hous','polic','protest','black','face','citi','home','pandem','american','offic','floyd+death+georg','summer','check','china','watch','nurs+home','hong+kong','tweet','store','case','order','rioter','reopen'
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
