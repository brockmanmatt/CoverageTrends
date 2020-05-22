"""
builds me a webpage for github.io!
I failed the one asthetic class I took. As such, there is a non-zero chance this design violates multiple
principles of basic design as well as potential obscentity laws, color matching and international treaties.
I apologize for that in advance and to everyon who taught me CSS.
"""

class webpageBuilder:
    """ builds me a webpage """
    """ in hindsight, I could just hard code a webpage instead of this but whatever """
    """ wait, I'm making a python script to just make javascript asdf """

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
        header + '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        header + '<title>{}</title>'.format(self.title)
        header + '<\head>'

        body = badCode()
        body + "<body>"
        body + '<div id="start">'.format(self.content)

        body + '<script src="{}.js"></script>'.format(self.projectName)
        body + "</body>"

        footer = badCode()
        footer + "</html>"

        finalPage = header.content + body.content + footer.content

        with open("{}.html".format(self.projectName), "w") as fh:
            fh.write(finalPage)

        """ builds the javascript; hopefully github.io lets me do this """
        js = badCode()
        js + 'document.getElementById("start").innerHTML = "Did This Work?"\n'

        with open("{}.js".format(self.projectName), "w") as fh:
            fh.write(js.content)


    def addContent(self, content):
        self.content += (content)

class badCode:
    def __init__(self):
        self.content = ""
    def __add__(self, new):
        self.content += new
        self.content += '\n'

        return self.content

    def __repr__(self):
        return self.content
