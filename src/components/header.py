
class NavBar:

    def __init__(self) -> None:
        self.style = "header.css"

        self.links = {
            "Budgeting":"/",
            "Ledgers":"/ledgers"
        }


    def render(self):

        html = "<ul class=\"header\">"

        for i in self.links:
            html = html + f"<a href=\"{self.links[i]}\">{i}</a>\n"

        html = html + "</ul>"

        return html
