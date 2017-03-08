from flask_nav import Nav
from flask_nav.elements import *

nav = Nav()

nav.register_element("top", Navbar(
    "PyQdbS",
    View("Hello", 'frontend.hello'),
    View("Add a Quote", 'frontend.add_quote'),
    View("Show Quotes", 'frontend.show_quotes', page=1),

    Subgroup("Other Stuff",
        Link("GitHub", "https://github.com/miniCruzer/PyQdbS"),
        Link("AlphaChat", "https://www.alphachat.net/"),
        Link("Shitposted", "https://shitposted.com/"),
    )
))