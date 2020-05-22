"""
builds me a webpage for github.io!
I failed the one asthetic class I took. As such, there is a non-zero chance this design violates multiple
principles of basic design as well as potential obscentity laws, color matching and international treaties.
I apologize for that in advance and to everyon who taught me CSS.
"""

class webpageBuilder:
    """ builds me a webpage """

    def __init__(self):
        self.content = ""

    def buildWebpage(self, outputURL):
        """ builds the actual webpage """
        scripts = ""
        header = "<html><head>{}</head>".format(scripts) #I think some other stuff goes up there,

        body = "{}".format(self.content)

        footer = "</html>"

        finalPage = header + body + footer

        with open(outputURL, "w") as fh:
            fh.write(finalPage)

    def addContent(self, content):
        self.content += (content)
