import wx

class DetailsDialog(wx.Dialog):
    def __init__(self, parent, event):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Details")

        self.__event = event

        self.__build_controls()

    def __build_controls(self):
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        sbox = wx.StaticBoxSizer(wx.StaticBox(panel, wx.ID_ANY, "Generic Details"), wx.VERTICAL)

        grid = wx.GridSizer(0, 2, 5, 5)

        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Timestamp:"), 0, wx.ALL, 5)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.timestamp), 1, wx.EXPAND | wx.ALL, 5)

        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Type:"), 0, wx.ALL, 5)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.type_name), 1, wx.EXPAND | wx.ALL, 5)

        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Source GUID:"), 0, wx.ALL, 5)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.source_guid), 1, wx.EXPAND | wx.ALL, 5)

        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Source Type:"), 0, wx.ALL, 5)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.source_type), 1, wx.EXPAND | wx.ALL, 5)

        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Source Name:"), 0, wx.ALL, 5)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.source_name), 1, wx.EXPAND | wx.ALL, 5)

        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Source Flags:"), 0, wx.ALL, 5)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.source_flags), 1, wx.EXPAND | wx.ALL, 5)

        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Source Raid Flags:"), 0, wx.ALL, 5)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.source_raid_flags), 1, wx.EXPAND | wx.ALL, 5)

        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Destination GUID:"), 0, wx.ALL, 5)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.dest_guid), 1, wx.EXPAND | wx.ALL, 5)

        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Destination Type:"), 0, wx.ALL, 5)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.dest_type), 1, wx.EXPAND | wx.ALL, 5)

        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Destination Name:"), 0, wx.ALL, 5)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.dest_name), 1, wx.EXPAND | wx.ALL, 5)

        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Destination Flags:"), 0, wx.ALL, 5)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.dest_flags), 1, wx.EXPAND | wx.ALL, 5)

        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Destination Raid Flags:"), 0, wx.ALL, 5)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.dest_raid_flags), 1, wx.EXPAND | wx.ALL, 5)

        sbox.Add(grid, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(sbox, 0, wx.ALL, 5)

        sbox = wx.StaticBoxSizer(wx.StaticBox(panel, wx.ID_ANY, "Arguments"), wx.VERTICAL)

        grid = wx.GridSizer(0, 2, 5, 5)

        if self.__event.has_spell_id:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Spell Id:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.spell_id), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_spell_name:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Spell Name:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.spell_name), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_spell_school:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Spell School:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.spell_school), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_item_id:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Item Id:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.item_id), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_item_name:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Item Name:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.item_name), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_environmental_type:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Environmental Type:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.environmental_type), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_amount:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Amount:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.amount), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_overkill:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Overkill:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.overkill), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_school:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "School:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.school), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_resisted:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Resisted:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.resisted), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_blocked:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Blocked:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.blocked), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_absorbed:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Absorbed:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.absorbed), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_critical:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Critical:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.critical), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_glancing:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Glancing:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.glancing), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_crushing:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Crushing:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.crushing), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_overhealing:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Overhealing:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.overhealing), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_miss_type:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Miss Type:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.miss_type), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_power_type:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Power Type:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.power_type), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_extra_amount:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Extra Amount:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.extra_amount), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_extra_spell_id:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Extra Spell Id:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.extra_spell_id), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_extra_spell_name:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Extra Spell Name:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.extra_spell_name), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_extra_school:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Extra School:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.extra_school), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_aura_type:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Aura Type:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.aura_type), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_remaining:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Remaining:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.remaining), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_unknown1:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Unknown1:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.unknown1), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_unknown2:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Unknown2:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.unknown2), 1, wx.EXPAND | wx.ALL, 5)

        if self.__event.has_failed_type:
            grid.Add(wx.StaticText(panel, wx.ID_ANY, "Failed Type:"), 0, wx.ALL, 5)
            grid.Add(wx.StaticText(panel, wx.ID_ANY, self.__event.failed_type), 1, wx.EXPAND | wx.ALL, 5)

        sbox.Add(grid, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(sbox, 0, wx.ALL, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        button = wx.Button(panel, wx.OK, "OK")
        button.Bind(wx.EVT_BUTTON, self.OnOk, button)
        hbox.Add(button, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        vbox.Add(hbox, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizerAndFit(vbox)
        vbox.Fit(self)

    def OnOk(self, e):
        self.Close()
