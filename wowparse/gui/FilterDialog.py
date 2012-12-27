import wx

from wowparse.filters.FilterConfig import MATCH_TYPES
from wowparse.filters.FilterManifest import FILTER_MANIFEST

ID_FILTER_ADD = wx.NewId()
ID_FILTER_TYPE = wx.NewId()
ID_MATCH_TYPE = wx.NewId()

class FilterDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Filter")

        self.__build_controls()

    def __build_controls(self):
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.__match_type = wx.RadioBox(panel, ID_MATCH_TYPE, "Match Type", choices=MATCH_TYPES)
        self.__match_type.SetSelection(1)
        vbox.Add(self.__match_type, 1, wx.EXPAND | wx.ALL, 10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        sbox = wx.StaticBoxSizer(wx.StaticBox(panel, wx.ID_ANY, "Add Filter"), wx.VERTICAL)

        self.__filter_type = wx.ComboBox(panel, ID_FILTER_TYPE, value="Source Name", choices=FILTER_MANIFEST, style=wx.CB_READONLY)
        self.__filter_type.SetValue(FILTER_MANIFEST[0])
        self.__show_filter_options(FILTER_MANIFEST[0])
        self.__filter_type.Bind(wx.EVT_COMBOBOX, self.OnComboBox, self.__filter_type)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(wx.StaticText(panel, wx.ID_ANY, "Filter Type:"), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER | wx.ALL, 10)
        hbox2.Add(self.__filter_type, 1, wx.ALL, 10)
        sbox.Add(hbox2)

        sbox.AddStretchSpacer()

        button = wx.Button(panel, ID_FILTER_ADD, "Add Filter")
        button.Bind(wx.EVT_BUTTON, self.OnAddFilter, button)
        sbox.Add(button, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        hbox.Add(sbox, 1, wx.EXPAND | wx.ALL, 5)

        sbox = wx.StaticBoxSizer(wx.StaticBox(panel, wx.ID_ANY, "Filters"), wx.VERTICAL)
        self.__filter_list = wx.ListView(panel, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        sbox.Add(self.__filter_list, 1, wx.EXPAND | wx.ALL, 5)
        hbox.Add(sbox, 1, wx.EXPAND | wx.ALL, 5)

        vbox.Add(hbox)

        button = wx.Button(panel, wx.OK, "OK")
        button.Bind(wx.EVT_BUTTON, self.OnOk, button)
        vbox.Add(button, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        panel.SetSizerAndFit(vbox)
        vbox.Fit(self)

    def OnComboBox(self, e):
        print("combobox selected")

    def OnAddFilter(self, e):
        print("Add filter - filter type: %s, match type: %d" % (self.__filter_type.GetValue(), self.__match_type.GetSelection()))

    def OnRemoveFilter(self, e):
        print("Remove filter")

    def OnOk(self, e):
        self.Close()

    def __show_filter_options(self, type):
        if type == "Event Type":
            self.__show_event_type_options()
        elif type == "Source Name":
            self.__show_source_name_options()
        elif type == "Destination Name":
            self.__show_destination_name_options()
        elif type == "Prefix":
            self.__show_prefix_options()
        elif type == "Suffix":
            self.__show_suffix_options()
        else:
            print("Unknown filter type: %s" % type)

    def __show_event_type_options(self):
        pass

    def __show_source_name_options(self):
        pass

    def __show_destination_name_options(self):
        pass

    def __show_prefix_options(self):
        pass

    def __show_suffix_options(self):
        pass
