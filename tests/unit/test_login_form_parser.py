from pyrilo.api.auth.LoginFormParser import LoginFormParser

def test_parser_extracts_action_and_inputs():
    html = """
    <html>
        <body>
            <form action="/login-action" method="post">
                <input type="text" name="username" />
                <input type="password" name="password" />
                <input type="hidden" name="execution" value="e1s1" />
                <input type="hidden" name="tab_id" value="X99" />
            </form>
        </body>
    </html>
    """
    parser = LoginFormParser()
    parser.feed(html)

    assert parser.action == "/login-action"
    assert parser.hidden_inputs["execution"] == "e1s1"
    assert parser.hidden_inputs["tab_id"] == "X99"
    # Ensure normal inputs are NOT captured as hidden
    assert "username" not in parser.hidden_inputs

def test_parser_handles_no_form():
    html = "<html><body><h1>Welcome</h1></body></html>"
    parser = LoginFormParser()
    parser.feed(html)

    assert parser.action is None
    assert parser.hidden_inputs == {}

def test_parser_finds_first_form_only():
    """Ensure if there are multiple forms, we only care about the login one (first one)."""
    html = """
    <form action="/login-action"><input type="hidden" name="id" value="1"/></form>
    <form action="/search"><input type="hidden" name="q" value="test"/></form>
    """
    parser = LoginFormParser()
    parser.feed(html)

    assert parser.action == "/login-action"
    assert parser.hidden_inputs["id"] == "1"
    assert "q" not in parser.hidden_inputs