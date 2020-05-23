var allowedFromDates = {}
allowedFromDates['20200523-0130'] = ['china', 'reopen', 'biden', 'pandem', 'black']
var allowedFromTopic = {}
allowedFromTopic['china'] = ['20200523-0000', '20200523-0030', '20200523-0110', '20200523-0130']
allowedFromTopic['reopen'] = ['20200523-0000', '20200523-0030', '20200523-0110', '20200523-0130']
allowedFromTopic['black'] = ['20200523-0000', '20200523-0030', '20200523-0110', '20200523-0130']
allowedFromTopic['biden'] = ['20200522-2100', '20200522-2140', '20200522-2200', '20200522-2230', '20200522-2300', '20200523-0000', '20200523-0030', '20200523-0110', '20200523-0130']
allowedFromTopic['pandem'] = ['20200523-0000', '20200523-0030', '20200523-0110', '20200523-0130']
const dates = [
'20200523-0130'
]
const topics = [
'china','reopen','black','biden','pandem'
]
function setupImgBox(){
    var time = document.getElementById("timeButton").value;
    var issue=document.getElementById("issueButton").value;
    img_name = time + "_" + issue + ".jpg";
    var newHTML = '<img src = "./img/';
    newHTML += img_name;
    newHTML += '" width=90%>';
    document.getElementById("imgBox").innerHTML = newHTML;
};
function setupDropdownBox(){
    newHTML = '<table id="SelectTable">'
    newHTML += '<caption><i>Select a Series</i></caption>'
    newHTML += '<tr><th>Datetime</th><th>Issue</th><th></tr></tr>'
    newHTML += '<tr><td><select id="timeButton" onchange="setupImgBox()">';
    dates.forEach(time => newHTML+= '<option value='+time+'>'+time+'</option>');
    newHTML+= '</select></td>';
    newHTML += '<td><select id="issueButton" onchange="setupImgBox()">';
    topics.forEach(topic => newHTML+= '<option value='+topic+'>'+topic+'</option>');
    newHTML += '</select></td></tr></table>';
    document.getElementById("dropdowns").innerHTML = newHTML;
};
