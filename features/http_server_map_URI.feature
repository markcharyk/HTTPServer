Feature: Map a URI to a filesystem
    Determine where on the filesystem the URI is pointing and
    if/how it should interact with the files and folders there

    Scenario: The requested resource is not found
        Given a URI /notfound.html
        When I call the function
        Then I have 404 Exception

    Scenario: The requested resource is a folder
        Given a URI /images/
        When I call the function
        Then I have webroot/images/

    Scenario: The requested resource is a file
        Given a URI /a_web_page.html
        When I call the function
        Then I have webroot/a_web_page.html