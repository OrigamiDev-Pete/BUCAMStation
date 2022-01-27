import gi

from HomeScreen import HomeScreen
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class OccupiedScreen(Gtk.Widget):

    __gtype_name__ = "occupiedScreen"

    def __init__(self):
        Gtk.Widget.__init__(self)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

        self.login_button = Gtk.Button(label="Login", name="login-button")
        self.login_button.connect("clicked", self.on_login_button_clicked)

        transfer_button = Gtk.Button(label="Transfer", name="transfer-button")
        transfer_button.connect("clicked", self.on_transfer_button_clicked)

        logout_button = Gtk.Button(label="Logout", name="logout-button")
        logout_button.connect("clicked", self.on_logout_button_clicked)

        self.vbox.pack_start(self.login_button, True, True, 0)
        self.vbox.pack_start(transfer_button, True, True, 0)
        self.vbox.pack_start(logout_button, True, True, 0)


    ## Events ##
    def on_login_button_clicked(self, widget):
        self.parent.change_view(HomeScreen())
    
    def on_transfer_button_clicked(self, widget):
        print("Transfer")

    def on_logout_button_clicked(self, widget):
        print("Logout")
    