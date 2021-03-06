#!/bin/python
from TcpClient import ResponseType, TCPClient
from gpiozero import LED
from pyclbr import Function
import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib


class MyWindow(Gtk.Window):
    def __init__(self) -> None:
        super().__init__(title="Access")

        if len(sys.argv) == 2:
            self.station = sys.argv[1]
        else:
            self.station = "Chapel"

        self.tcp_client = TCPClient("10.0.0.76", 13000, self.station)
        self.card_string = ""
        self.occupied = False
        # True if terminal is in use. Stops cards from being scanned multiple times
        self.active = False
        self.is_fullscreen = False
        self.return_timeout_transfer = None
        self.return_timeout_message = None
        self.pin = LED(4)  # Corresponds to GPIO4 aka pin 7

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(open("/home/pi/dev/BUCAMStation/style.css", "rb").read())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.set_border_width(20)

        self.connect("key_press_event", self.on_key_pressed)
        self.connect("window_state_event", self.on_window_state_changed)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_transition_duration(200)

        ## Home Screen ##

        self.home_screen = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=20)

        heading_label = Gtk.Label(label="Welcome to Blacktown Uniting Church")

        scan_label = Gtk.Label(label="Scan an ID")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

        # Open Office Button #
        if self.station == "Office":
            open_office_button = Gtk.Button(label="Open Door", name="open-office-button")
            open_office_button.set_can_focus(False)
            open_office_button.connect("clicked", self.on_open_office_button_pressed)

        help_button = Gtk.Button(label="Help", name="help-button")
        help_button.set_can_focus(False)
        help_button.connect("clicked", self.on_help_button_pressed)

        box.pack_start(heading_label, True, True, 0)
        box.pack_start(scan_label, True, True, 0)
        if self.station == "Office":
            box.pack_start(open_office_button, True, True, 0)

        help_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, margin=20)
        help_box.pack_end(help_button, False, False, 0)

        self.home_screen.pack_end(help_box, False, False, 0)
        self.home_screen.pack_start(box, True, False, 0)

        self.stack.add_named(self.home_screen, "home")

        ## Occupied Screen ##

        self.occupied_screen = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=20)

        self.current_user_label = Gtk.Label(label="")

        transfer_button = Gtk.Button(label="Transfer", name="transfer-button")
        transfer_button.set_can_focus(False)
        transfer_button.connect("clicked", self.on_transfer_button_clicked)

        logout_button = Gtk.Button(label="Logout", name="logout-button")
        logout_button.set_can_focus(False)
        logout_button.connect("clicked", self.on_logout_button_clicked)

        self.occupied_screen.pack_start(
            self.current_user_label, False, False, 10)
        self.occupied_screen.pack_start(transfer_button, True, True, 0)
        self.occupied_screen.pack_start(logout_button, True, True, 0)

        self.stack.add_named(self.occupied_screen, "occupied")

        ## Message Screen ##

        self.message_screen = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.message_label = Gtk.Label(label="placeholder")

        self.stack.add_named(self.message_screen, "message")

        self.message_screen.pack_start(self.message_label, True, True, 0)

        vbox.pack_start(self.stack, True, True, 0)
        self.add(vbox)

    def return_home(self) -> None:
        self.active = False
        self.card_string = ""
        self.stack.set_visible_child_name("home")
        try:
            GLib.source_remove(self.return_timeout_transfer)
        except:
            pass

    def show_message(self, message: str, delay: int, next: Function) -> None:
        self.message_label.set_label(message)
        self.stack.set_visible_child_name("message")
        self.return_timeout_message = GLib.timeout_add_seconds(delay, self.on_transition_timeout, next)

    def show_transfer_logout_screen(self, data) -> None:
        if data['owner']['CardId'] == self.card_string:
            self.current_user_label.set_label("You own the building")
        else:
            name = data['owner']['FirstName']
            self.current_user_label.set_label(f"{name} owns the building")

        self.stack.set_visible_child_name("occupied")
        self.return_timeout_transfer = GLib.timeout_add_seconds(10, self.on_transition_timeout, self.return_home)

    def open_door(self, timeout) -> None:
        self.pin.on()
        def func(self): return self.pin.off()
        t = GLib.timeout_add_seconds(timeout, func, self)

    ## Events ##

    def on_open_office_button_pressed(self, widget):
        self.open_door(5)

    def on_transition_timeout(self, user_data) -> bool:
        user_data()
        return False

    def on_transfer_button_clicked(self, widget):
        response = self.tcp_client.send_transfer(self.card_string)
        if response.type == ResponseType.OK:
            self.show_message(f"Transfer successful", 3, self.return_home)
        else:
            self.show_message(response.message, 3, self.return_home)

    def on_logout_button_clicked(self, widget):
        response = self.tcp_client.send_logout(self.card_string)
        if response.type == ResponseType.OK:
            self.show_message(f"You have been logged out", 3, self.return_home)
        else:
            self.show_message("Something went wrong", 3, self.return_home)

    def on_help_button_pressed(self, widget):
        dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="For assistance, call Peter on 0458 495 484")
        dialog.format_secondary_text("Please dismiss this dialog when you are finished.")
        dialog.run()
        dialog.destroy()

    def on_key_pressed(self, widget, event):
        if event.keyval == 65307:  # Esc
            if (self.is_fullscreen):
                self.unfullscreen()
            else:
                self.fullscreen()
        if not self.active:
            if event.keyval == 65293:  # Enter
                self.active = True
                response = self.tcp_client.send_access(self.card_string)
                if response.type == ResponseType.OK:
                    self.open_door(5)
                    self.show_transfer_logout_screen(response.data)
                else:
                    self.show_message(response.message, 3, self.return_home)
            else:
                self.card_string += event.string

    def on_window_state_changed(self, widget, event):
        # Checking the Gdk.WindowState flags if the window is fullscreen
        self.is_fullscreen = event.new_window_state & Gdk.WindowState.FULLSCREEN == Gdk.WindowState.FULLSCREEN


if __name__ == "__main__":
    win = MyWindow()
    win.show_all()
    win.connect("destroy", Gtk.main_quit)
    # win.resize(1000, 400)
    win.fullscreen()
    win.set_focus(None)
    Gtk.main()
