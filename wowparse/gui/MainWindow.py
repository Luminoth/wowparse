import logging
import os
import threading
import time
import wx
import wx.lib.mixins.listctrl
import wx.lib.newevent

from DetailsDialog import DetailsDialog
from EventListCtrl import EventListCtrl
from FilterDialog import FilterDialog
from wowparse.CombatLogParser import CombatLogParser

ID_DETAILS = wx.NewId()
ID_FILTER = wx.NewId()

ParseProgressEvent, EVT_PARSE_PROGRESS = wx.lib.newevent.NewEvent()
ParseFinishedEvent, EVT_PARSE_FINISHED = wx.lib.newevent.NewEvent()

class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "WoW Combat Log Parser", size=(800, 600))

        self.__logger = logging.getLogger("wowparse.MainWindow")
        self.__parser_thread = None
        self.__timer_start = 0

        self.CreateStatusBar()
        self.__build_menu()

        self.__build_controls()

        self.Bind(EVT_PARSE_PROGRESS, self.OnParseProgress)
        self.Bind(EVT_PARSE_FINISHED, self.OnParseFinished)

        self.Centre()

    def __build_menu(self):
        menubar = wx.MenuBar()
        self.__build_file_menu(menubar)
        self.__build_event_menu(menubar)
        self.__build_filter_menu(menubar)
        self.__build_help_menu(menubar)
        self.SetMenuBar(menubar)

    def __build_file_menu(self, menubar):
        filemenu = wx.Menu()

        menu = filemenu.Append(wx.ID_OPEN, "&Open...", "Open a file to parse")
        self.Bind(wx.EVT_MENU, self.OnOpen, menu)

        filemenu.AppendSeparator()

        menu = filemenu.Append(wx.ID_EXIT, "E&xit", "Exit WoW Combat Log Parser")
        self.Bind(wx.EVT_MENU, self.OnExit, menu)

        menubar.Append(filemenu, "&File")

    def __build_event_menu(self, menubar):
        eventmenu = wx.Menu()

        self.__details_menu = eventmenu.Append(ID_DETAILS, "Details...", "View event details...")
        self.Bind(wx.EVT_MENU, self.OnDetails, self.__details_menu)
        self.__enable_details(False)

        menubar.Append(eventmenu, "Event")

    def __build_filter_menu(self, menubar):
        filtermenu = wx.Menu()

        menu = filtermenu.Append(ID_FILTER, "Filter...", "Filter log messages")
        self.Bind(wx.EVT_MENU, self.OnFilter, menu)

        menubar.Append(filtermenu, "Filter")

    def __build_help_menu(self, menubar):
        helpmenu = wx.Menu()

        menu = helpmenu.Append(wx.ID_ABOUT, "&About...", "About WoW Combat Log Parser")
        self.Bind(wx.EVT_MENU, self.OnAbout, menu)

        menubar.Append(helpmenu, "&Help")

    def __build_controls(self):
        panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.__event_list = EventListCtrl(panel, self)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.__event_list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.__event_list)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnItemRightClick, self.__event_list)
        hbox.Add(self.__event_list, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(hbox)

    def __enable_details(self, enable):
        self.__details_menu.Enable(enable)

    def OnParseProgress(self, e):
        self.SetStatusText("Parsing log file %s: %s%%" % (e.filename, e.progress))

    def OnParseFinished(self, e):
        self.__parser_thread.join()
        self.__parser_thread = None

        self.SetStatusText("Rebuilding event list (this may take a while)...")
        filtered = self.__event_list.rebuild(e.events)
        self.SetStatusText("Processed %d events in %.2f seconds (%d filtered)" % (len(e.events), time.time() - self.__timer_start, filtered))

    def OnItemSelected(self, e):
        self.__enable_details(self.__event_list.GetSelectedItemCount() > 0)

    def OnItemDeselected(self, e):
        self.__enable_details(self.__event_list.GetSelectedItemCount() > 0)

    def OnItemRightClick(self, e):
        if e.GetIndex() < 0:
            return

        popup = wx.Menu()
        menu = popup.Append(ID_DETAILS, "Details...", "View event details...")
        self.Bind(wx.EVT_MENU, self.OnDetails, menu)

        self.__event_list.PopupMenu(popup)

    def OnOpen(self, e):
        dlg = wx.FileDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            filename = os.path.join(dlg.GetDirectory(), dlg.GetFilename())
            self.SetStatusText("Parsing log file %s: 0%%..." % filename)

            self.__timer_start = time.time()
            self.__parser_thread = ParserThread(self, filename)
            self.__parser_thread.start()
        dlg.Destroy()

    def OnExit(self, e):
        self.Close(True)

    def OnDetails(self, e):
        event = self.__event_list.selected_event
        if event:
            dlg = DetailsDialog(self, event)
            dlg.ShowModal()
            dlg.Destroy()

    def OnFilter(self, e):
        dlg = FilterDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "WoW Combat Log Parser", "About WoW Combat Log Parser", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

class ParserThread(threading.Thread):
    def __init__(self, window, filename):
        threading.Thread.__init__(self)

        self.__window = window
        self.__filename = filename

    def run(self):
        parser = CombatLogParser()
        events = parser.parse(self.__filename, self.progress_callback)

        wx.PostEvent(self.__window, ParseFinishedEvent(events=events))

    def progress_callback(self, progress):
        wx.PostEvent(self.__window, ParseProgressEvent(filename=self.__filename, progress=progress))
