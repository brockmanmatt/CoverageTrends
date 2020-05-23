import os

"""
builds me a webpage for github.io!
I failed the one asthetic class I took. As such, there is a non-zero chance this design violates multiple
principles of basic design as well as potential obscentity laws, color matching and international treaties.
I apologize for that in advance and to everyone who taught me CSS and should visit them in the asylum to let them know im using it.
"""

class webpageBuilder:
    """ builds me a webpage """
    """ in hindsight, I could just hard code a webpage instead of this but whatever """
    """ wait, I'm making a python script to just make javascript asdf """
    """ I'm fairly certain I don't actually want to automatically generate this thing """

    def __init__(self, projectName="index", title="PLACEHOLDER"):
        """ builds a website with some javascript at projectName.html, projectNAme.js and PLACEHOLDER title """
        self.content = ""
        self.projectName = projectName
        self.title = title

    def buildWebpage(self):
        """ builds the actual webpage """
        header = badCode()
        header + '<html lang="en">'
        header + '<head>'
        header + '<meta charset="UTF-8">'
        #header + '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        header + '<title>{}</title>'.format(self.title)

        header + '<style>'
        header + 'img {'
        header + '  width: 70%;'
        header + '}'
        header + '</style>'


        header + '</head>'

        body = badCode()
        body + "<body>"
        body + "  <div class=\"item\" id=\"example-graphs\">"
        body + "  <div id=\"dropdowns\"></div>"
        body + "  <div id=\"imgBox\"></div>"
        body + "</div>"
        body + '<script src="{}.js"></script>'.format(self.projectName)

        body + '<script>'
        body + 'setupDropdownBox()'
        body + 'setupImgBox()'
        body + '</script>'


        body + "</body>"

        footer = badCode()
        footer + "</html>"

        finalPage = header.content + body.content + footer.content

        with open("docs/{}.html".format(self.projectName), "w") as fh:
            fh.write(finalPage)

        """ builds the javascript; hopefully github.io lets me do this """
        js = badCode()

        actual_files = os.listdir("docs/img")

        actual_files = os.listdir("docs/img")
        actual_options = [x[:-4].split("_") for x in actual_files if x.endswith(".jpg")]
        actual_options = sorted(actual_options, reverse=True)
        formated_options = ["{}_{}".format(x[1], x[0]) for x in actual_options]

        js + "const topics = ["
        js + ",".join(["'{}'".format(x) for x in formated_options])
        js + "]"


        """ setupImageBox sets up the actual graph"""

        js +   "function setupImgBox(){"
        js +   "    var myToken=document.getElementById(\"issueButton\").value;"

        js +   "    var myIssue = myToken.split('_')"
        js +   "    console.log(myIssue)"
        js +   "    issue = myIssue[1] + '_' + myIssue[0]"

        js +   "    img_name = issue + \".jpg\";"

        js +   "    var newHTML = '<img src = \"./img/';"
        js +   "    newHTML += img_name;"
        js +   "    newHTML += '\" width=90%>';"

        js +   "    document.getElementById(\"imgBox\").innerHTML = newHTML;"
        js +   "};"

        """ setupDropDownBox sets up the time and issue select buttons """
        """ time should give the option of aggregating everything from wihin the last 24 hours"""
        """Then maaybe one for last week, last month"""

        """ the problem is, each of those dropdown will have more and more content"""
        """can skin that cat later"""

        js +   "function setupDropdownBox(){"
        js +   "    newHTML = '<table id=\"SelectTable\">'"
        js +   "    newHTML += '<caption><i>Select a Series</i></caption>'"

        js +   "    newHTML += '<tr><th>Issue (last updated)</th></tr>'"

        js +   "    newHTML += '<td><select id=\"issueButton\" onchange=\"setupImgBox()\">';"
        js +   "    topics.forEach(topic => newHTML+= '<option value='+topic+'>'+topic+'</option>');"
        js +   "    newHTML += '</select></td></tr></table>';"

        js +   "    document.getElementById(\"dropdowns\").innerHTML = newHTML;"

        js +   "};"

        with open("docs/{}.js".format(self.projectName), "w") as fh:
            fh.write(js.content)


class badCode:
    """ bad way of adding new lines to html im generating; there's probably a library I should use somewhere """
    def __init__(self):
        """ has a blank string """
        self.content = ""
    def __add__(self, new):
        """ adding new content to it sticks a new line at the end """
        self.content += new
        self.content += '\n'

        return self.content

    def __repr__(self): #I need to override something else, just gonna call content
        """ This doesn't do what I think it does so I don't use it"""
        return self.content
