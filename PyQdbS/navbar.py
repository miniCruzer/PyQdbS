from flask_nav import Nav
from flask_nav.elements import Navbar, Link, Subgroup, View

nav = Nav()

nav.register_element("top", Navbar(
    "PyQdbS",
    View("Hello", 'frontend.hello'),
    View("Add a Quote", 'frontend.add_quote'),
    View("Show Quotes", 'frontend.show_quotes', page=1),
    View("Random Quote", 'frontend.show_quote_random'),
    View("Search", "frontend.search_quotes"),
    View("Admin", "admin.index"),

    Subgroup("Other Stuff",
        Link("GitHub", "https://github.com/miniCruzer/PyQdbS"),
        Link("AlphaChat", "https://www.alphachat.net/")
    )
))
