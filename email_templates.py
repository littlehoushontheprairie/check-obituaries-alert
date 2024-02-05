class EmailTemplates:
    def __init__(self):
        file = open("templates/index.html", "r")
        self.basic_template: str = file.read()

        file = open("templates/error.html", "r")
        self.error_template: str = file.read()

    def generate_basic_template(self, entries: dict) -> str:
        return self.basic_template.format(to_name=entries["to_name"], obituaries=entries["obituaries"])

    def generate_error_template(self, entries: dict) -> str:
        return self.error_template.format(to_name=entries["to_name"], status_code=entries["status_code"])

    def generate_obituaries_body(self, obituaries: list) -> str:
        html = ""

        for obituary in obituaries:
            html = html + "<div>"
            html = html + "<h4>" + obituary["full_name"] + "</h4>"
            html = html + "<p>" + obituary["obituary_snippet"] + "</p>"
            html = html + "<p><a href='" + obituary["link"] + "'>" + \
                obituary["published_on"] + "</a></p>"
            html = html + "</div><br>"

        return html
