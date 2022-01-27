import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

class HomeScreen(GObject.GObject):
    def __init__(self):
        super().__init__()

        self.parent = None

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

        transfer_button = Gtk.Button(label="Transfer", name="transfer-button")
        transfer_button.connect("clicked", self.on_transfer_button_clicked)

        logout_button = Gtk.Button(label="Logout", name="logout-button")
        logout_button.connect("clicked", self.on_logout_button_clicked)

        self.vbox.pack_start(transfer_button, True, True, 0)
        self.vbox.pack_start(logout_button, True, True, 0)

    ## Events ##
    
    def on_transfer_button_clicked(self, widget):
        print("Transfer")

    def on_logout_button_clicked(self, widget):
        print("Logout")