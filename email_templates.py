class EmailTemplates:
    def __init__(self):
        file = open("templates/index.html", "r")
        self.basic_template = file.read()

        file = open("templates/error.html", "r")
        self.error_template = file.read()

    def generate_basic_template(self, entries):
        return self.basic_template.format(email_greeting=entries["email_greeting"], obituaries=entries["obituaries"])

    def generate_error_template(self, entries):
        return self.error_template.format(email_greeting=entries["email_greeting"], status_code=entries["status_code"])

    def generate_obituaries_body(self, obituaries):
        html = ""

        for obituary in obituaries:
            html = html + "<div>"
            html = html + "<h4>" + obituary["full_name"] + "</h4>"
            html = html + "<p>" + obituary["obituary_snippet"] + "</p>"
            html = html + "<p><a href='" + obituary["link"] + "'>" + \
                obituary["published_on"] + "</a></p>"
            html = html + "</div><br>"

        return html
