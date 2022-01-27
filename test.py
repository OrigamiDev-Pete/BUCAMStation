import gi

from OccupiedScreen import OccupiedScreen
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from HomeScreen import HomeScreen

class MyWindow(Gtk.Window):
    def __init__(self) -> None:
        super().__init__(title="Access")

        self.card_string = ""
        self.occupied = False
        self.is_fullscreen = False
        self.current_view = None

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(open("style.css", "rb").read())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.set_border_width(20)

        self.connect("key_press_event", self.on_key_pressed)
        self.connect("window_state_event", self.on_window_state_changed)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_transition_duration(200)

        ## UnoccupiedScreen ##

        self.UnoccupiedScreen = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

        self.login_button = Gtk.Button(label="Login", name="login-button")
        self.login_button.connect("clicked", self.on_login_button_clicked)

        self.UnoccupiedScreen.pack_start(self.login_button, True, True, 0)

        self.stack.add_named(self.UnoccupiedScreen, "unoccupied")

        ## OccupiedScreen ##

        self.OccupiedScreen = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

        transfer_button = Gtk.Button(label="Transfer", name="transfer-button")
        transfer_button.connect("clicked", self.on_transfer_button_clicked)

        logout_button = Gtk.Button(label="Logout", name="logout-button")
        logout_button.connect("clicked", self.on_logout_button_clicked)

        self.OccupiedScreen.pack_start(transfer_button, True, True, 0)
        self.OccupiedScreen.pack_start(logout_button, True, True, 0)

        self.stack.add_named(self.OccupiedScreen, "occupied")

        self.add(self.stack)


    ## Events ##
    def on_login_button_clicked(self, widget):
        self.stack.set_visible_child_name("occupied")
    
    def on_transfer_button_clicked(self, widget):
        print("Transfer")

    def on_logout_button_clicked(self, widget):
        print("Logout")

    def on_key_pressed(self, widget, event):
        if event.keyval == 65307: # Esc
            if (self.is_fullscreen):
                self.unfullscreen()
            else:
                self.fullscreen()

        if event.keyval == 65293: # Enter
            #TODO send card_string
            print(self.card_string)
            self.card_string = ""
        else:
            self.card_string += event.string
    
    def on_window_state_changed(self, widget, event):
        self.is_fullscreen = event.new_window_state & Gdk.WindowState.FULLSCREEN == Gdk.WindowState.FULLSCREEN # Checking the Gdk.WindowState flags if the window is fullscreen



if __name__ == "__main__":
    win = MyWindow()
    win.show_all()
    win.connect("destroy", Gtk.main_quit)
    win.resize(1000, 400)
    win.set_focus(None)
    Gtk.main()