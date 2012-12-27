import wx
import wx.lib.mixins.listctrl
import wx.lib.newevent

from wowparse.filters.FilterConfig import FilterConfig

#class EventListCtrl(wx.ListView, wx.lib.mixins.listctrl.ColumnSorterMixin):
class EventListCtrl(wx.ListView, wx.lib.mixins.listctrl.ColumnSorterMixin, wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin):
#class EventListCtrl(wx.ListView, wx.lib.mixins.listctrl.ColumnSorterMixin, wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin, wx.lib.mixins.listctrl.ListRowHighlighter):
    def __init__(self, parent, main_window):
        wx.ListView.__init__(self, parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.LC_VRULES)
        wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin.__init__(self)
        #wx.lib.mixins.listctrl.ListRowHighlighter.__init__(self)

        self.__main_window = main_window

        self.InsertColumn(0, "Id")
        self.InsertColumn(1, "Timestamp")
        self.InsertColumn(2, "Event")
        self.InsertColumn(3, "Source")
        self.InsertColumn(4, "Destination")
        self.__reset_column_widths()

        self.itemDataMap = {}
        wx.lib.mixins.listctrl.ColumnSorterMixin.__init__(self, 5)

    @property
    def selected_event(self):
        idx = self.GetFirstSelected()
        if idx < 0:
            return None

        data = self.GetItemData(idx)
        if data not in self.itemDataMap:
            return None
        return self.itemDataMap[data]

    def GetListCtrl(self):
        return self

    def rebuild(self, events):
        self.DeleteAllItems()
        self.__reset_column_widths()
        wx.SafeYield()

        count = len(events)
        self.itemDataMap = events

        filters = FilterConfig()

        filtered = 0
        counter = 0
        last_id = 0
        for id, event in events.items():
            percent = int((float(id) / float(count)) * 100.0)
            self.__main_window.SetStatusText("Processing event %d/%d (%d%%), this may take a while..." % (id, count, percent))
            if filters.filter(event):
                self.InsertStringItem(counter, "%d" % (event.id + 1))
                self.SetStringItem(counter, 1, event.timestamp)
                self.SetStringItem(counter, 2, event.type_name)
                self.SetStringItem(counter, 3, event.source_name)
                self.SetStringItem(counter, 4, event.dest_name)
                self.SetItemData(counter, id)
                #wx.SafeYield()

                last_id = event.id
                counter += 1
            else:
                filtered += 1

        self.SetColumnWidth(0, 24 if last_id == 0 else 12 * len("%d" % last_id))
        self.SortListItems(0, -1)
        return filtered

    def __reset_column_widths(self):
        self.SetColumnWidth(0, 24)
        self.SetColumnWidth(1, 130)
        self.SetColumnWidth(2, 175)
        self.SetColumnWidth(3, 175)
        #self.SetColumnWidth(4, 175)
