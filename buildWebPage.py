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
        self.content = ""
        self.projectName = projectName
        self.title = title

    def generate(self):
        self.buildWebpage()
        self.buildJavaScript()

    def buildWebpage(self):
        """ builds the actual webpage """
        header = badCode()
        header + '<html lang="en">'
        header + '<head>'
        header + '<meta charset="UTF-8">'
        #header + '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        header + '<title>{}</title>'.format(self.title)
        header + '</head>'

        body = badCode()
        body + "<body>"
        body + '<div id="start"></div>'.format(self.content)

        body + '<script src="{}.js"></script>'.format(self.projectName)
        body + "</body>"

        footer = badCode()
        footer + "</html>"

        finalPage = header.content + body.content + footer.content

        with open("{}.html".format(self.projectName), "w") as fh:
            fh.write(finalPage)

        """ builds the javascript; hopefully github.io lets me do this """
        js = badCode()
        js + 'document.getElementById("start").innerHTML = "<img src=img/test.jpg>"\n'

        js + "const publishers = ["
        js + ",".join(["'{}'".format(x) for x in os.listdir("archived_links")])
        js + "]"

        js + 'function addCharts(){'
        js + ""
        js + '}'

        js + "addCharts()"

        with open("{}.js".format(self.projectName), "w") as fh:
            fh.write(js.content)


    def addContent(self, content):
        self.content += (content)

class badCode:
    """ bad way of adding new lines to html im generating; there's probably a library I should use somewhere """
    def __init__(self):
        self.content = ""
    def __add__(self, new):
        self.content += new
        self.content += '\n'

        return self.content

    def __repr__(self): #I need to override something else, just gonna call content
        return self.content
