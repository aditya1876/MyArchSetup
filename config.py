# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from typing import List  # noqa: F401

mod = "mod4"
myTerm = "alacritty"                             # My terminal of choice
myConfig = "/home/adi02/.config/qtile/config.py"    # The Qtile config file location


keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down(), desc="Move focus down in stack pane"),
    Key([mod], "j", lazy.layout.up(), desc="Move focus up in stack pane"),
    # Move windows up or down in current stack
    Key([mod, "shift"], "k", lazy.layout.shuffle_down(), desc="Move window down in current stack "),
    Key([mod, "shift"], "j", lazy.layout.shuffle_up(), desc="Move window up in current stack "),
    # Switch window focus to other pane(s) of stack
    Key([mod], "Tab", lazy.layout.next(), desc="Switch window focus to other pane(s) of stack"),
    # Swap panes of split stack
    Key([mod, "shift"], "Tab", lazy.layout.rotate(), desc="Swap panes of split stack"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "n", lazy.layout.normalize(), desc='normalize window size ratios'),
    #Key([mod], "m", lazy.layout.maximize(), desc='toggle window between minimum and maximum sizes'),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc='toggle floating'),
    Key([mod, "shift"], "m", lazy.window.toggle_fullscreen(), desc='toggle fullscreen'), 
    #My applications
    Key([mod, "mod1"], "t", lazy.spawn(myTerm), desc="Launch alacritty terminal"),
    Key([mod, "mod1"], "c", lazy.spawn("speedcrunch"), desc="Launch speedcrunch calculator"),
    Key([mod, "mod1"], "z", lazy.spawn("chromium"), desc="Launch chromium browser"),
    Key([mod, "mod1"], "m", lazy.spawn("elisa"), desc="Launch elisa player"),
    Key([mod, "mod1"], "s", lazy.spawn("dmenu_run"), desc = "Launch Dmenu"),
    #Key([mod, "mod1"], "c", lazy.spawn("speedcrunch"), desc="Launch speedcrunch calculator"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

#Layouts
layout_theme = {"border_width": 2,"margin": 6,"border_focus": "e1acff","border_normal": "1D2330"}

layouts = [
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.MonadTall(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.TreeTab(font = "Ubuntu",fontsize = 10,sections = ["FIRST", "SECOND"],section_fontsize = 11,bg_color = "141414",active_bg = "90C435",active_fg = "000000",
		inactive_bg = "384323",inactive_fg = "a0a0a0",padding_y = 5,section_top = 10,panel_width = 50),
    layout.Floating(**layout_theme)
]
colors = [["#292e3e", "#292e3e"], # panel background
          ["#434758", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#8d62a9", "#8d62a9"], # border line color for other tab and odd widgets
          ["#668bd7", "#668bd7"], # color for the even widgets
          ["#e1acff", "#e1acff"]] # window name

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize = 12,
    padding = 2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
				widget.Image(filename = "~/.config/qtile/icons/python.png",mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn('dmenu_run')}),
				widget.GroupBox(font = "Ubuntu Bold",fontsize = 13,margin_y = 3,margin_x = 0,padding_y = 5,padding_x = 3,borderwidth = 3,active = colors[2],
				inactive = colors[2],rounded = False,highlight_color = colors[1],highlight_method = "line",this_current_screen_border = colors[3],
				this_screen_border = colors [4],other_current_screen_border = colors[0],other_screen_border = colors[0],foreground = colors[2],background = colors[0]),
				#widget.Prompt(prompt = prompt,font = "Ubuntu Mono",padding = 10,foreground = colors[3],background = colors[1]),
				widget.Sep(linewidth = 0,padding = 20,foreground = colors[2],background = colors[0]),
				widget.WindowName(foreground = colors[6],background = colors[0],padding = 0),
				#widget.TextBox(text = '',background = colors[0],foreground = colors[4],padding = 0,fontsize = 37),
				#widget.TextBox(text = " ₿",padding = 0,foreground = colors[2],background = colors[4],fontsize = 12),
				#widget.BitcoinTicker(foreground = colors[2],background = colors[4],padding = 5),
				#widget.TextBox(text = '',background = colors[4],foreground = colors[5],padding = 0,fontsize = 37),
				#widget.TextBox(text = " 🌡",padding = 2,foreground = colors[2],background = colors[5],fontsize = 11),
				widget.ThermalSensor(foreground = colors[2],background = colors[5],threshold = 90,padding = 5),
				#widget.TextBox(text='',background = colors[5],foreground = colors[4],padding = 0,fontsize = 37),
				#widget.TextBox(text = " ⟳",padding = 2,foreground = colors[2],background = colors[4],fontsize = 14),
				widget.CheckUpdates(update_interval = 1800,distro = 'Arch',foreground = colors[2],
				mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},background = colors[4]),
				#widget.TextBox(text = "Updates",padding = 5,mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
				#foreground = colors[2],background = colors[4]),
				#widget.TextBox(text = '',background = colors[4],foreground = colors[5],padding = 0,fontsize = 37),
				#widget.TextBox(text = " 🖬",foreground = colors[2],background = colors[5],padding = 0,fontsize = 14),
				#widget.Memory(foreground = colors[2],background = colors[5],mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e htop')},
				#padding = 5),
				#widget.TextBox(text='',background = colors[5],foreground = colors[4],padding = 0,fontsize = 37),
				#widget.Net(interface = "enp6s0",format = '{down} ↓↑ {up}',foreground = colors[2],background = colors[4],padding = 5),
				#widget.TextBox(text = '',background = colors[4],foreground = colors[5],padding = 0,fontsize = 37),
				widget.TextBox(text = " Vol:",foreground = colors[2],background = colors[5],padding = 0),
				widget.Volume(foreground = colors[2],background = colors[5],padding = 5),
				#widget.TextBox(text = '',background = colors[5],foreground = colors[4],padding = 0,fontsize = 37),
				#widget.CurrentLayoutIcon(custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],foreground = colors[0],background = colors[4],padding = 0,
				#scale = 0.7),
				#widget.CurrentLayout(foreground = colors[2],background = colors[4],padding = 5),
				#widget.TextBox(text = '',background = colors[4],foreground = colors[5],padding = 0,fontsize = 37),
				widget.Clock(foreground = colors[2],background = colors[4],format = "%Y-%m-%d %A, %B [ %H:%M ]"),
				#widget.Sep(linewidth = 0,padding = 10,foreground = colors[0],background = colors[5]),
				#widget.Systray(background = colors[0],padding = 5),
                #widget.CurrentLayout(),
                #widget.GroupBox(),
                #widget.Prompt(),
                #widget.WindowName(),
                #widget.Chord(
                #    chords_colors={
                #        'launch': ("#ff0000", "#ffffff"),
                #    },
                #    name_transform=lambda name: name.upper(),
                #),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                #widget.Systray(),
                #widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
                #widget.QuickExit(),
            ],
			opacity=0.7,
			size=24,
        ),
    ),
]
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
