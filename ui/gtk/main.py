# vim:set et sts=4 sw=4:
#
# ibus - The Input Bus
#
# Copyright(c) 2007-2008 Huang Peng <shawn.p.huang@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or(at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

import os
import sys
import getopt
import ibus
import gtk
import locale
import panel

class PanelApplication:
    def __init__ (self):
        self.__bus = ibus.Bus()
        self.__bus.connect("destroy", self.__bus_destroy_cb)

        self.__panel = panel.Panel(self.__bus)

    def run(self):
        gtk.main()

    def __bus_destroy_cb(self, _ibus):
        gtk.main_quit()


def launch_panel():
    # gtk.settings_get_default().props.gtk_theme_name = "/home/phuang/.themes/aud-Default/gtk-2.0/gtkrc"
    # gtk.rc_parse("./themes/default/gtkrc")
    PanelApplication().run()

def print_help(out, v = 0):
    print >> out, "-h, --help             show this message."
    print >> out, "-d, --daemonize        daemonize ibus"
    sys.exit(v)

def main():
    daemonize = False
    shortopt = "hd"
    longopt = ["help", "daemonize"]
    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopt, longopt)
    except getopt.GetoptError, err:
        print_help(sys.stderr, 1)

    for o, a in opts:
        if o in("-h", "--help"):
            print_help(sys.stdout)
        elif o in("-d", "--daemonize"):
            daemonize = True
        else:
            print >> sys.stderr, "Unknown argument: %s" % o
            print_help(sys.stderr, 1)

    if daemonize:
        if os.fork():
            sys.exit()

    launch_panel()

if __name__ == "__main__":
    locale.bind_textdomain_codeset("ibus", "UTF-8")
    main()