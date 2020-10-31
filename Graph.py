
import wx
from math import log, tan, sin, cos, pi
from numpy import arange
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import (
    A6, A5, A4, A3, A2, A1, A0, letter,
    legal, elevenSeventeen, landscape)
from reportlab.lib.colors import (
    black, darkgrey, lightgrey, white,
    blue, midnightblue, lightblue, yellow,
    lightpink, red, darkgreen, green, lightgreen)
from reportlab.lib.units import mm, inch


class BldGrf(wx.Frame):
    '''Routine to build form and populate grid'''
    def __init__(self):

        super(BldGrf, self).__init__(None, wx.ID_ANY, title='Graph Paper Plotter',
                          size=(550, 700), style=wx.DEFAULT_FRAME_STYLE &
                          ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX |
                            wx.MINIMIZE_BOX | wx.CLOSE_BOX))

        self.x_mult = ['1']
        self.y_mult = ['1']

        PaperSz = ['A6', 'A5', 'A4', 'A3', 'A2', 'A1', 'A0',
                   'Letter', 'Legal', '11 x 17']

        self.pgsizes = {'A6': A6, 'A5': A5, 'A4': A4, 'A3': A3, 'A2': A2,
                        'A1': A1, 'A0': A0, 'Letter': letter, 'Legal': legal,
                        '11 x 17': elevenSeventeen}

        GraphType = ['Quad', 'Dot', 'Lined Paper', 'Python Coding',
                     'Isometric', 'Polar Cordinate',
                     'Log Log', 'Semi Log']

        Colors = ['black', 'dark grey', 'light grey', 'white',
                  'blue', 'midnight blue', 'light blue',
                  'red', 'light red', 'yellow',
                  'dark green', 'green', 'light green']

        Width = ['.1', '.2', '.5', '1', '1.5', '2', '2.5']
        '''
        wx.Frame.__init__(self, parent, id, title='Graph Paper Plotter',
                          size=(550, 700), style=wx.DEFAULT_FRAME_STYLE &
                          ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX |
                            wx.MINIMIZE_BOX | wx.CLOSE_BOX))'''

        font1 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD)

        # set the Sizer property (same as SetSizer)
        self.Sizer = wx.BoxSizer(wx.VERTICAL)

        self.specsizer = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        text1 = wx.StaticText(self,
                              label='Select Criteria for Graph Paper',
                              style=wx.TE_CENTER)
        text1.SetForegroundColour((255, 0, 0))
        text1.SetFont(font1)
        self.specsizer.Add(text1, 0, wx.ALL, 10)

        self.cmbsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        note1 = wx.StaticText(self, label='Graph Type',
                              style=wx.ALIGN_LEFT)
        note1.SetForegroundColour((255, 0, 0))

        note2 = wx.StaticText(self, label='Paper Size',
                              style=wx.ALIGN_CENTER_VERTICAL)
        note2.SetForegroundColour((255, 0, 0))

        self.GrphTyp = wx.ComboBox(self, id=1, pos=(10, 10), size=(160, -1),
                                   choices=GraphType, style=wx.CB_READONLY)
        self.GrphTyp.Bind(wx.EVT_COMBOBOX, self.OnCmb)
        self.GrphTyp.SetHint('Graph Type')

        self.PgSize = wx.ComboBox(self, id=1, pos=(10, 10), size=(150, -1),
                                  choices=PaperSz, style=wx.CB_READONLY)
        self.PgSize.SetHint('Paper Size')

        self.cmbsizer1.Add(note1, 0, wx.RIGHT | wx.TOP, border=8)
        self.cmbsizer1.Add(self.GrphTyp, 0, wx.ALIGN_LEFT, 5)
        self.cmbsizer1.Add((30, 10))
        self.cmbsizer1.Add(note2, 0, wx.RIGHT | wx.TOP, border=8)
        self.cmbsizer1.Add(self.PgSize, 0, wx.ALIGN_LEFT, 5)

        self.designsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.radiosizer = wx.BoxSizer(wx.VERTICAL)

        lblList = ['Portrait', 'Landscape']
        self.orientbox = wx.RadioBox(self, label='Select Orientation',
                                     pos=(80, 10), choices=lblList,
                                     majorDimension=1,
                                     style=wx.RA_SPECIFY_ROWS)

        lblList1 = ['mm', 'inch']
        self.unitsbox = wx.RadioBox(self, label='Select Units',
                                    pos=(80, 10), choices=lblList1,
                                    majorDimension=1,
                                    style=wx.RA_SPECIFY_ROWS)
        self.unitsbox.Bind(wx.EVT_RADIOBOX, self.OnRadio)

        lblList2 = ['solid', 'dashed']
        self.stylebox = wx.RadioBox(self, label='Select Line Style',
                                    pos=(80, 10), choices=lblList2,
                                    majorDimension=1,
                                    style=wx.RA_SPECIFY_ROWS)

        self.radiosizer.Add(self.orientbox, 0, wx.ALIGN_LEFT |
                            wx.TOP | wx.RIGHT, 20)
        self.radiosizer.Add(self.unitsbox, 0, wx.ALIGN_LEFT | wx.TOP, 20)
        self.radiosizer.Add(self.stylebox, 0, wx.ALIGN_LEFT | wx.TOP, 20)

        self.mrgsizer = wx.BoxSizer(wx.VERTICAL)
        mrg = wx.StaticText(self,
                            label='''Minimum Page Boarder
        (actual to be set by graph grid)''',
                            style=wx.ALIGN_CENTER)

        self.mrgsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        leftmrg = wx.StaticText(self, label='Left',
                                style=wx.ALIGN_CENTER_VERTICAL)
        self.lefttxt = wx.TextCtrl(self, size=(50, -1),
                                   value='',
                                   style=wx.TE_LEFT)
        topmrg = wx.StaticText(self, label='Top',
                               style=wx.ALIGN_CENTER_VERTICAL)
        self.toptxt = wx.TextCtrl(self, size=(50, -1),
                                  value='',
                                  style=wx.TE_LEFT)
        self.mrgsizer2.Add(leftmrg, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        self.mrgsizer2.Add(self.lefttxt, 0)
        self.mrgsizer2.Add((55, 10))
        self.mrgsizer2.Add(topmrg, 0, wx.ALIGN_CENTER | wx.RIGHT | wx.LEFT, 5)
        self.mrgsizer2.Add(self.toptxt, 0)

        self.mrgsizer3 = wx.BoxSizer(wx.HORIZONTAL)

        rightmrg = wx.StaticText(self, label='Right',
                                 style=wx.ALIGN_CENTER_VERTICAL)
        self.righttxt = wx.TextCtrl(self, size=(50, -1),
                                    value='',
                                    style=wx.TE_LEFT)
        btmmrg = wx.StaticText(self, label='Bottom',
                               style=wx.ALIGN_CENTER_VERTICAL)
        self.btmtxt = wx.TextCtrl(self, size=(50, -1),
                                  value='',
                                  style=wx.TE_LEFT)
        self.mrgsizer3.Add(rightmrg, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        self.mrgsizer3.Add(self.righttxt, 0)
        self.mrgsizer3.Add((25, 10))
        self.mrgsizer3.Add(btmmrg, 0, wx.ALIGN_CENTER | wx.RIGHT | wx.LEFT, 5)
        self.mrgsizer3.Add(self.btmtxt, 0)

        self.mrgsizer.Add(mrg, 0, wx.ALIGN_LEFT | wx.RIGHT | wx.TOP, 30)
        self.mrgsizer.Add((15, 10))
        self.mrgsizer.Add(self.mrgsizer2, 0, wx.ALIGN_LEFT | wx.RIGHT, 20)
        self.mrgsizer.Add((10, 10))
        self.mrgsizer.Add(self.mrgsizer3, 0, wx.ALIGN_LEFT | wx.RIGHT, 20)

        self.designsizer1.Add(self.mrgsizer, 0)
        self.designsizer1.Add((30, 10))
        self.designsizer1.Add(self.radiosizer, 0)
        self.designsizer1.Add((60, 10))

        self.notesizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.note3 = wx.StaticText(self, label='MAJOR LINES',
                                   style=wx.ALIGN_LEFT)
        self.note3.SetForegroundColour((0, 0, 255))

        self.note4 = wx.StaticText(self, label='MINOR LINES',
                                   style=wx.ALIGN_LEFT)
        self.note4.SetForegroundColour((0, 0, 255))
        self.notesizer1.Add(self.note3, 0, wx.LEFT |
                            wx.ALIGN_CENTER, border=40)
        self.notesizer1.Add(self.note4, 0, wx.LEFT |
                            wx.ALIGN_CENTER, border=85)

        self.cmbsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.note5 = wx.StaticText(self, label='Line Color',
                                   style=wx.ALIGN_LEFT)
        self.note5.SetForegroundColour((255, 0, 0))

        self.MajColor = wx.ComboBox(self, id=1, pos=(10, 10), size=(150, -1),
                                    choices=Colors, style=wx.CB_READONLY)
        self.MajColor.SetHint('Color')

        self.MinColor = wx.ComboBox(self, id=1, pos=(10, 10), size=(150, -1),
                                    choices=Colors, style=wx.CB_READONLY)
        self.MinColor.SetHint('Color')

        self.cmbsizer2.Add((15, 10))
        self.cmbsizer2.Add(self.note5, 0, wx.RIGHT | wx.TOP, border=8)
        self.cmbsizer2.Add(self.MajColor, 0, wx.ALIGN_LEFT, 5)
        self.cmbsizer2.Add((30, 10))
        self.cmbsizer2.Add(self.MinColor, 0, wx.ALIGN_LEFT, 5)

        self.cmbsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.note6 = wx.StaticText(self, label='Line Weight',
                                   style=wx.ALIGN_LEFT)
        self.note6.SetForegroundColour('red')

        self.MajWt = wx.ComboBox(self, id=1, pos=(10, 10), size=(150, -1),
                                 choices=Width, style=wx.CB_READONLY)
        self.MajWt.SetHint('weight')

        self.MinWt = wx.ComboBox(self, id=1, pos=(10, 10), size=(150, -1),
                                 choices=Width, style=wx.CB_READONLY)
        self.MinWt.SetHint('weight')

        self.cmbsizer3.Add(self.note6, 0, wx.ALIGN_CENTER)
        self.cmbsizer3.Add((10, 10))
        self.cmbsizer3.Add(self.MajWt, 0, wx.ALIGN_LEFT)
        self.cmbsizer3.Add((30, 10))
        self.cmbsizer3.Add(self.MinWt, 0, wx.ALIGN_LEFT)

        self.chkmjr = wx.CheckBox(self,
                                  label="Show Major Lines",
                                  size=(180, 30))

        self.spcsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text2 = wx.StaticText(self, label='Line\nSpacing', size=(60, 50),
                                   style=wx.ALIGN_CENTER_VERTICAL)
        self.text2.SetForegroundColour('red')
        self.text2.SetFont(font)

        self.text3 = wx.StaticText(self, label='Line\nSpacing', size=(60, 50),
                                   style=wx.ALIGN_CENTER_VERTICAL)
        self.text3.SetForegroundColour('red')
        self.text3.SetFont(font)

        self.note7 = wx.StaticText(self,
                                   label=('X-Axis\n(' + self.unitsbox.GetString
                                          (self.unitsbox.GetSelection())
                                          + ')'),
                                   style=wx.ALIGN_LEFT)
        self.note7.SetForegroundColour('blue')

        self.note8 = wx.StaticText(self,
                                   label=('Y-Axis\n(' + self.unitsbox.GetString
                                          (self.unitsbox.GetSelection())
                                          + ')'),
                                   style=wx.ALIGN_LEFT | wx.ALIGN_TOP)
        self.note8.SetForegroundColour('blue')

        self.x_axis = wx.TextCtrl(self, id=1, size=(50, -1), value='')

        self.y_axis = wx.TextCtrl(self, id=1, size=(50, -1), value='')

        self.spcsizer.Add(self.text2, 0, wx.RIGHT | wx.LEFT, 15)
        self.spcsizer.Add(self.note7, 0, wx.ALIGN_LEFT | wx.RIGHT | wx.LEFT, 8)
        self.spcsizer.Add(self.x_axis, 0, wx.ALIGN_LEFT, 5)
        self.spcsizer.Add((30, 10))
        self.spcsizer.Add(self.text3, 0,  wx.RIGHT, 15)
        self.spcsizer.Add(self.note8, 0, wx.RIGHT, 8)
        self.spcsizer.Add((10, 10))
        self.spcsizer.Add(self.y_axis, 0, wx.ALIGN_LEFT)

        self.mjrsizer = wx.BoxSizer(wx.HORIZONTAL)
        intrvnote = wx.StaticText(self, label='Specify Major\nLine Intervals',
                                  style=wx.ALIGN_LEFT)
        intrvnote.SetForegroundColour('red')

        self.x_interval = wx.TextCtrl(self, size=(50, -1),
                                      value='',
                                      style=wx.TE_LEFT)

        self.intrvnote1 = wx.StaticText(self, label='',
                                        style=wx.ALIGN_LEFT,
                                        size=(100, 30))
        self.intrvnote1.SetForegroundColour('red')

        self.y_interval = wx.TextCtrl(self, size=(50, -1),
                                      value='',
                                      style=wx.TE_LEFT)

        self.mjrsizer.Add(intrvnote, 0, wx.RIGHT, 25)
        self.mjrsizer.Add(self.x_interval, 0, wx.RIGHT, 35)
        self.mjrsizer.Add(self.intrvnote1, 0, wx.RIGHT, 10)
        self.mjrsizer.Add(self.y_interval, 0)

        # Add buttons for grid modifications
        self.b1 = wx.Button(self, label="Print\nPreview")
        self.Bind(wx.EVT_BUTTON, self.PrintFile, self.b1)

        self.b2 = wx.Button(self, label="Reset\nBoxes")
        self.Bind(wx.EVT_BUTTON, self.OnReset, self.b2)

        self.b3 = wx.Button(self, label="Save Page\nas PDF")
        self.Bind(wx.EVT_BUTTON, self.SaveFile, self.b3)

        self.b4 = wx.Button(self, label="Exit")
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.b4)

        # add a button box and place the buttons
        self.btnbox = wx.BoxSizer(wx.HORIZONTAL)
        self.btnbox.Add(self.b2, 0, wx.ALL, 5)
        self.btnbox.Add(self.b3, 0, wx.ALL, 5)
        self.btnbox.Add(self.b1, 0, wx.ALL, 5)
        self.btnbox.Add((30, 10))
        self.btnbox.Add(self.b4, 0, wx.ALL, 5)

        self.Sizer.Add(self.specsizer, 0, wx.ALL | wx.ALIGN_CENTER)
        self.Sizer.Add(self.cmbsizer1, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        self.Sizer.Add(self.designsizer1, 0, wx.LEFT, 50)
        self.Sizer.Add((10, 15))
        self.Sizer.Add(self.notesizer1, 0, wx.TOP | wx.BOTTOM |
                       wx.ALIGN_CENTER, 10)
        self.Sizer.Add(self.cmbsizer2, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        self.Sizer.Add(self.cmbsizer3, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        self.Sizer.Add(self.chkmjr, 0, wx.LEFT, 140)
        self.Sizer.Add((10, 30))
        self.Sizer.Add(self.spcsizer, 0, wx.LEFT | wx.ALIGN_LEFT, 80)
        # self.Sizer.Add((10, 10))
        self.Sizer.Add(self.mjrsizer, 0, wx.ALIGN_LEFT | wx.LEFT, 60)
        self.Sizer.Add(self.btnbox, 0, wx.ALIGN_CENTER | wx.TOP, 25)

        self.SetSizer(self.Sizer)
        self.b4.SetFocus()

        self.Show()
        self.Center()

    def SaveFile(self, evt):
        # get a pdf file name
        filename = self.PDF_File()
        # proced to the page building
        if self.GrphTyp.GetValue() in ('Quad', 'Python Coding', 'Dot'):
            self.GrdCanvas(filename)
        elif self.GrphTyp.GetValue() in ('Log Log', 'Semi Log'):
            self.LogCanvas(filename)
        elif self.GrphTyp.GetValue() == 'Isometric':
            self.IsoCanvas(filename)
        elif self.GrphTyp.GetValue() == 'Polar Cordinate':
            self.PolarCanvas(filename)
        elif self.GrphTyp.GetValue() == 'Lined Paper':
            self.LinesCanvas(filename)

    def PDF_File(self):
        saveDialog = wx.FileDialog(self, message='Save Report as PDF.',
                                   wildcard='PDF (*.pdf)|*.pdf',
                                   style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if saveDialog.ShowModal() == wx.ID_CANCEL:
            filename = ''

        filename = saveDialog.GetPath()
        if filename.find(".pdf") == -1:
            filename = filename + '.pdf'

        saveDialog.Destroy()

        return filename

    def GrdCanvas(self, filename):
        self.filename = filename    # no need to assign a file extention
        self.footer = "Copyright © 2020 KPH Projects"

        # validate that all the data is present before procedding
        parms = self.ValData()
        if parms is False:
            return

        c = canvas.Canvas(filename, parms[1])

        width, height = parms[1]

        # zero out the grid line cordinates
        xlist = []
        ylist = []

        # specify the line locations for the x_axis
        xlist = self.grdlst(parms[2], xlist, width, parms[3],
                            parms[10], parms[11], 1, parms[7], parms[14])
        # specify the line locations for the y_axis
        ylist = self.grdlst(parms[2], ylist, height, parms[4],
                            parms[13], parms[12], 1, parms[7], parms[15])

        if self.GrphTyp.GetValue() in ('Quad', 'Python Coding'):
            c.setStrokeColor(parms[5])
            c.setLineWidth(parms[6])
            if self.stylebox.GetStringSelection() == 'Dashed':
                c.setDash(1, 2)
            else:
                c.setDash(1, 0)
            c.grid(xlist, ylist)
        elif self.GrphTyp.GetValue() == 'Dot':
            c.setLineWidth(.1)
            c.setStrokeColor(parms[5])
            c.setFillColor(parms[5])
            dot_dia = parms[6] * parms[2]
            for y in ylist:
                for x in xlist:
                    c.circle(x, y, dot_dia, fill=1)

        # if major axis is to be plotted the list is
        # just the sub list of the minor lines
        if parms[7] is True:
            xlist = xlist[0::parms[14]]
            ylist = ylist[0::parms[15]]

            c.setStrokeColor(parms[8])
            c.setLineWidth(parms[9])
            if self.stylebox.GetStringSelection() == 'Dashed':
                c.setDash(1, 2)
            else:
                c.setDash(1, 0)
            c.grid(xlist, ylist)

        c.showPage()
        c.save()

    def grdlst(self, units, lst, cnv_dim, gap, mrg1, mrg2,
               firstrun, majln, intrvl):

        # available area to plot graph on page
        grph_dim = cnv_dim - (mrg1 + mrg2) * units   # in pixels
        origin = mrg1 * units
        # if major lines are to plotted then use those
        # dimensions to set graph size and determine
        # maximum number of blocks will fit space
        if majln is True:
            maxlns = int(grph_dim // (intrvl * gap * units)) * intrvl
        else:
            maxlns = int(grph_dim // (gap * units))
        # set the list for x and y axis
        for i in range(0, maxlns+1):
            lst.append(origin + gap * i * units)

        return lst

    def LogCanvas(self, filename):
        self.filename = filename    # no need to assign a file extention
        self.footer = "Copyright © 2020 KPH Projects"

        ylist = []

        # validate that all the data is present before procedding
        parms = self.ValData()
        if parms is False:
            return

        c = canvas.Canvas(filename, parms[1])

        width, height = parms[1]

        x_min, x_max = self.loglst(parms[2], width, parms[10],
                                   parms[11], parms[3])

        if self.GrphTyp.GetValue() == 'Semi Log':
            # specify the line locations for the y_axis based on a square grid
            y_min = self.grdlst(parms[2], ylist, height, parms[4],
                                parms[13], parms[12], 1, parms[7], parms[15])

            # if major axis is to be plotted the list is
            # just the sub list of the minor lines
            if parms[7] is True:
                y_max = ylist[0::parms[15]]

                c.setStrokeColor(parms[8])
                c.setLineWidth(parms[9])
                if self.stylebox.GetStringSelection() == 'Dashed':
                    c.setDash(1, 2)
                else:
                    c.setDash(1, 0)
                c.grid(x_max, y_max)

                c.setStrokeColor(parms[5])
                c.setLineWidth(parms[6])
                if self.stylebox.GetStringSelection() == 'Dashed':
                    c.setDash(1, 2)
                else:
                    c.setDash(1, 0)
                c.grid(x_min, y_min)
            else:
                # problem with colors if major lines is not checked
                # then colors are not brought back fron ValData
                c.setStrokeColor(parms[8])
                c.setLineWidth(parms[9])
                if self.stylebox.GetStringSelection() == 'Dashed':
                    c.setDash(1, 2)
                else:
                    c.setDash(1, 0)

                y_max = [min(y_min), max(y_min)]
                c.grid(x_max, y_max)

                c.setStrokeColor(parms[5])
                c.setLineWidth(parms[6])
                if self.stylebox.GetStringSelection() == 'Dashed':
                    c.setDash(1, 2)
                else:
                    c.setDash(1, 0)
                c.grid(x_min, y_min)

        elif self.GrphTyp.GetValue() == 'Log Log':
            y_min, y_max = self.loglst(parms[2], height, parms[13],
                                       parms[12], parms[4])

            c.setStrokeColor(parms[5])
            c.setLineWidth(parms[6])
            if self.stylebox.GetStringSelection() == 'Dashed':
                c.setDash(1, 2)
            else:
                c.setDash(1, 0)
            c.grid(x_min, y_min)

            c.setStrokeColor(parms[8])
            c.setLineWidth(parms[9])
            if self.stylebox.GetStringSelection() == 'Dashed':
                c.setDash(1, 2)
            else:
                c.setDash(1, 0)
            c.grid(x_max, y_max)

        c.showPage()
        c.save()

    def loglst(self, units, cnv_dim, mrg1, mrg2, cyls):
        # zero out the grid line cordinates
        lnlist = []
        ln_list = []
        lst_min = []
        lst_max = []
        lst_tmp = []

        # specify the line locations for the ***Major x_axis
        # the last value or the first log cycle
        last_ln = (((cnv_dim - (mrg1 + mrg2) * units)
                   / cyls))
        # the location of each line is a relationship of the log(10) line
        for i in range(1, 10):
            ln = last_ln * log(i, 10)
            ln_list.append(ln)
        # add the last line location to the list
        ln_list.append(last_ln)

        # set the first cycle of lines over to the left margine
        for j in range(0, len(ln_list)):
            lnlist.append(ln_list[j] + mrg1 * units)
        # generate the remaining log cycles the number depending on parms[3]
        # x_list[9] * k being the last line plotted in the previous cycle
        for k in range(0, cyls):
            for i in range(0, 10):
                lst_max.append(lnlist[i] + (k * ln_list[9]))
        # make this set of lines the major lines for the log scale

        # Now Generate the *** Minor x_axis
        lst_tmp = [0]
        lnlist = []
        for i in range(1, 10):
            if (abs(lst_max[i-1] - lst_max[i])) >= 15:
                for j in [n * .1 for n in range(0, 10)]:
                    ln = last_ln * log(i+j, 10)
                    lst_tmp.append(ln)
            elif (abs(lst_max[i-1] - lst_max[i])) < 15 \
                    and (abs(lst_max[i-1] - lst_max[i])) >= 7:
                for j in [n * .25 for n in range(0, 4)]:
                    ln = last_ln * log(i+j, 10)
                    lst_tmp.append(ln)
            else:
                ln = last_ln * log(i+.5, 10)
                lst_tmp.append(ln)
        lst_tmp.append(last_ln)

        for j in range(0, len(lst_tmp)):
            lnlist.append(lst_tmp[j] + mrg1 * units)

        # generate the remaining log cycles the number depending on parms[3]
        # x_list[9] * k being the last line plotted in the previous cycle
        for k in range(0, cyls):
            for i in range(1, len(lnlist)):
                lst_min.append(lnlist[i] + (k * ln_list[9]))

        return lst_min, lst_max

    def IsoCanvas(self, filename):

        parms = self.ValData()
        if parms is False:
            return

        c = canvas.Canvas(filename, parms[1])
        width, height = parms[1]

        # specify the line locations for the x_axis
        xlist = []
        xlist = self.grdlst(parms[2], xlist, width, parms[3],
                            parms[10], parms[11], 1, parms[7], parms[14])

        ylist = [parms[13] * parms[2], height - parms[12] * parms[2]]

        c.setStrokeColor(parms[8])
        c.setLineWidth(parms[9])
        c.grid(xlist, ylist)

        xm = max(xlist)

        linelst = self.isolst(parms[2], width, height, parms[3], parms[10],
                              parms[11], parms[13], parms[12], xm)
        c.setStrokeColor(parms[5])
        c.setLineWidth(parms[6])
        for i in linelst:
            c.line(i[0], i[1], i[2], i[3])

        c.showPage()
        c.save()

    def isolst(self, units, width, height, gap, mrg1x, mrg2x,
               mrg1y, mrg2y, xm):

        lst = []

        m = tan(30 * pi / 180)
        x_incrm = gap * 2 * units
        y_incrm = m * x_incrm
        xo = mrg1x * units
        yo = mrg1y * units
        ym = height - mrg2y * units

        # this section provides the lines from the bottom left
        # corner and across the bottom x_axis
        for n in arange(0, xm - xo, x_incrm):
            xs = xo + n
            b = yo - m * xs
            xn = xm
            yn = b + m * xm
            if n == 0:
                y1st = yn
            if yn > ym:
                yn = ym
                xn = (yn - b) / m
            ln = (xs, yo, xn, yn)
            lst.append(ln)

        # this section provides the lines from the bottom left
        # corner and up the left y_axis
        ys = (m * 2 * gap + mrg1y) * units
        for n in arange(ys, ym, y_incrm):
            b = n - m * xo
            if y1st > ym:
                yn = n
                xn = (yn - b) / m
                ln = (xo, ys, xn, yn)
                lst.append(ln)
            else:
                xn = xm
                yn = b + m * xn
                if yn > ym:
                    yn = ym
                    xn = (yn - b) / m
                ln = (xo, n, xn, yn)
                lst.append(ln)

        # this section provides the lines from the bottom left
        # corner and across the top x_axis
        m = -m
        ys = 2 * gap * units * tan(30 * pi / 180) + yo
        for n in arange(ys, ym, y_incrm):
            xs = xo
            ys = n
            b = n - xs * m
            xn = xm
            yn = m * xn + b
            if yn < yo:
                yn = yo
                xn = (yn - b) / m
            ln = (xs, ys, xn, yn)
            lst.append(ln)

        # this section provides the lines from the top left
        # corner and across the top x_axis

        # the maximum value for y from the previous list is
        # highest point on y axis from previous plot
        max_y = lst[-1][1]
        max_x = lst[-1][0]
        # find what would have been the next y_axis value to be
        # plotted then move it to the corresponding point on the x_axis
        next_y = max_y - (m * 2 * gap * units)
        next_x = max_x
        b_next = next_y - m * next_x
        ystart = ym
        xstart = (ystart - b_next) / m

        for n in arange(xstart, xm, x_incrm):
            xs = n
            ys = ym
            b = ys - m * xs
            xn = xm
            yn = xn * m + b
            if yn > ym:
                yn = ym
                xn = (yn - b) / m
            ln = (xs, ys, xn, yn)
            lst.append(ln)

        return lst

    def PolarCanvas(self, filename):
        self.filename = filename    # no need to assign a file extention
        self.footer = "Copyright © 2020 KPH Projects"

        # validate that all the data is present before procedding
        parms = self.ValData()
        if parms is False:
            return

        c = canvas.Canvas(filename, parms[1])

        width, height = parms[1]
        mrg1x = parms[10]
        mrg2x = parms[11]
        mrg1y = parms[13]
        mrg2y = parms[12]
        units = parms[2]

        fx = ((width - (mrg1x + mrg2x) * units) / 2) + mrg1x * units
        fy = ((height - (mrg1y + mrg2y) * units) / 2) + mrg1y * units

        center = [fx, fy]
        radius = min(center) - 100
        circ_spc = (parms[3] * units)

        for rad in arange(circ_spc, radius, circ_spc):
            c.setStrokeColor(parms[5])
            c.setLineWidth(parms[6])
            c.circle(center[0], center[1], rad, fill=0)

        c.circle(center[0], center[1], 1, fill=1)

        for theta in arange(0, 360, 15):
            radians_x = sin(theta * pi / 180)
            radians_y = cos(theta * pi / 180)
            x1 = radians_x * circ_spc + center[0]
            y1 = radians_y * circ_spc + center[1]
            x2 = radians_x * radius + center[0]
            y2 = radians_y * radius + center[1]
            c.setStrokeColor(parms[8])
            if theta % 90 == 0:
                c.setLineWidth(2*parms[9])
            else:
                c.setLineWidth(1.5 * parms[9])
            c.line(x1, y1, x2, y2)

        for theta in arange(0, 360, 45):
            radians_x = sin(theta * pi / 180)
            radians_y = cos(theta * pi / 180)
            if 180 >= theta >= 0:
                n = 10
            else:
                n = 25
            x1 = radians_x * radius + center[0] + radians_x * n
            y1 = radians_y * radius + center[1] + radians_y * n
            c.setFont("Courier", 10)
            c.drawString(x1, y1, str(theta))

        for theta in arange(0, 360, 5):
            radians_x = sin(theta * pi / 180)
            radians_y = cos(theta * pi / 180)
            x1 = radians_x * (radius - .8 * radius) + center[0]
            y1 = radians_y * (radius - .8 * radius) + center[1]
            x2 = radians_x * radius + center[0]
            y2 = radians_y * radius + center[1]
            c.setStrokeColor(parms[8])
            c.setLineWidth(parms[9])
            c.line(x1, y1, x2, y2)

        for theta in arange(0, 360, 1):
            radians_x = sin(theta * pi / 180)
            radians_y = cos(theta * pi / 180)
            x1 = radians_x * (radius - .05 * radius) + center[0]
            y1 = radians_y * (radius - .05 * radius) + center[1]
            x2 = radians_x * radius + center[0]
            y2 = radians_y * radius + center[1]
            c.setStrokeColor(parms[8])
            c.setLineWidth(.5 * parms[9])
            c.line(x1, y1, x2, y2)

        c.setStrokeColor(black)
        c.setLineWidth(1)
        c.rect(mrg1x * units, mrg1y * units,
               (width - (mrg1x + mrg2x) * units),
               (height - (mrg1y + mrg2y) * units))

        c.showPage()
        c.save()

    def LinesCanvas(self, filename):
        self.filename = filename    # no need to assign a file extention
        self.footer = "Copyright © 2020 KPH Projects"

        # validate that all the data is present before procedding
        parms = self.ValData()
        if parms is False:
            return

        c = canvas.Canvas(filename, parms[1])

        width, height = parms[1]
        mrg1x = parms[10]
        mrg2x = parms[11]
        mrg1y = parms[13]
        mrg2y = parms[12]
        units = parms[2]

        fx = (width - (mrg1x + mrg2x) * units)
        fy = (height - (mrg1y + mrg2y) * units)
        steps = parms[3] * units / 2
        x1 = mrg1x * units
        x2 = fx + mrg1x * units

        n = 1
        for i in arange(mrg1y * units + 20, fy, steps):
            c.setStrokeColor(parms[8])
            c.setLineWidth(parms[9])
            y = i
            if n % 2 == 0:
                c.setDash(1, 2)
            else:
                c.setDash(1, 0)
            c.line(x1, y, x2, y)
            n += 1

        c.setDash(1, 0)
        c.setStrokeColor(black)
        c.setLineWidth(1)
        c.rect(mrg1x * units, mrg1y * units, fx, fy)

        if parms[15] != 0:
            y1 = mrg1y * units
            y2 = mrg1y * units + fy
            x = (mrg1x + parms[4]) * units
            c.setDash(1, 0)
            c.setStrokeColor(lightpink)
            c.setLineWidth(.5)
            c.line(x, y1, x, y2)

        c.showPage()
        c.save()

    def ValData(self):

        colrs = {'dark green': darkgreen, 'green': green,
                 'light green': lightgreen, 'light blue': lightblue,
                 'blue': blue, 'midnight blue': midnightblue, 'red': red,
                 'light red': lightpink, 'yellow': yellow, 'black': black,
                 'dark grey': darkgrey, 'light grey': lightgrey,
                 'white': white}

        if self.GrphTyp.GetValue() == '':
            wx.MessageBox('Please select graph type.', 'Missing Data',
                          wx.OK | wx.ICON_INFORMATION)
            return False
        else:
            self.graphtyp = self.GrphTyp.GetValue()

        if self.PgSize.GetValue() == '':
            wx.MessageBox('Please select page size.', 'Missing Data',
                          wx.OK | wx.ICON_INFORMATION)
            return False
        else:
            if self.orientbox.GetStringSelection() == 'Landscape':
                self.size = landscape(self.pgsizes[self.PgSize.GetValue()])
            else:
                self.size = self.pgsizes[self.PgSize.GetValue()]
        if self.unitsbox.GetStringSelection() == 'mm':
            self.unit = mm
        else:
            self.unit = inch

        # set page margines
        if self.lefttxt.GetValue() == '':
            self.leftmrg = 0
        else:
            self.leftmrg = eval(self.lefttxt.GetValue())

        if self.righttxt.GetValue() == '':
            self.rightmrg = 0
        else:
            self.rightmrg = eval(self.righttxt.GetValue())

        if self.toptxt.GetValue() == '':
            self.topmrg = 0
        else:
            self.topmrg = eval(self.toptxt.GetValue())

        if self.btmtxt.GetValue() == '':
            self.btmmrg = 0
        else:
            self.btmmrg = eval(self.btmtxt.GetValue())

        if self.x_interval.GetValue() == '':
            self.x_mjrintrvl = 1
        else:
            self.x_mjrintrvl = eval(self.x_interval.GetValue())

        if self.y_interval.GetValue() == '':
            self.y_mjrintrvl = 1
        else:
            self.y_mjrintrvl = eval(self.y_interval.GetValue())

        # set line spacing for x and y axis
        if self.x_axis.GetValue() == '' or self.y_axis.GetValue() == '':
            wx.MessageBox('Grid spacing is need for both x & Y axis',
                          'Missing Data',
                          wx.OK | wx.ICON_INFORMATION)
            return False
        else:
            self.xgap = eval(self.x_axis.GetValue())
            self.ygap = eval(self.y_axis.GetValue())

        # set properties for minor lines
        if self.MinColor.GetValue() == '' or self.MinWt.GetValue() == '':
            wx.MessageBox('Information is needed for the minor grid lines.',
                          'Missing Data',
                          wx.OK | wx.ICON_INFORMATION)
            return False
        else:
            self.colorMinor = colrs[self.MinColor.GetValue()]
            self.lineWidthMinor = eval(self.MinWt.GetValue())

        # set properties for major lines and confirm major lines
        self.majorLine = self.chkmjr.GetValue()
        if self.majorLine is True:
            if self.MajColor.GetValue() == '' or self.MajWt.GetValue() == '':

                return False
            else:
                self.colorMajor = colrs[self.MajColor.GetValue()]
                self.lineWidthMajor = eval(self.MajWt.GetValue())

        else:
            if self.MajColor.GetValue() == '' or self.MajWt.GetValue() == '':
                self.colorMajor = black
                self.lineWidthMajor = 1
            else:
                self.colorMajor = colrs[self.MajColor.GetValue()]
                self.lineWidthMajor = eval(self.MajWt.GetValue())

        if self.size[0] - (self.leftmrg + self.rightmrg
                           + self.xgap) * self.unit < 1 \
           or self.size[1] - (self.topmrg + self.btmmrg
                              + self.ygap) * self.unit < 1:

            wx.MessageBox(
                ('Page size and margines\ndo not work\
 check selected\nunits and specified sizes.'),
                'Wrong Units',
                wx.OK | wx.ICON_INFORMATION)

            return False

        return [self.graphtyp, self.size, self.unit, self.xgap, self.ygap,
                self.colorMinor, self.lineWidthMinor, self.majorLine,
                self.colorMajor, self.lineWidthMajor, self.leftmrg,
                self.rightmrg, self.topmrg, self.btmmrg, self.x_mjrintrvl,
                self.y_mjrintrvl]

    def PrintFile(self, evt):
        PDFFrm(self)

    def OnCmb(self, evt):
        obj = evt.GetEventObject()
        self.chkmjr.Enable()
        self.chkmjr.SetValue(False)
        self.orientbox.SetSelection(0)
        self.MinWt.Enable()
        self.x_interval.Enable()
        self.y_interval.Enable()
        self.y_axis.Enable()
        self.MajColor.Enable()
        self.MajWt.Enable()
        self.text2.SetLabel('Line\nSpacing')
        self.note6.SetLabel('Line Weight')
        self.note7.SetLabel('X-Axis\n(' + self.unitsbox.GetString
                            (self.unitsbox.GetSelection()) + ')')
        self.text3.SetLabel('Line\nSpacing')
        self.note8.SetLabel('Y-Axis\n(' + self.unitsbox.GetString
                            (self.unitsbox.GetSelection()) + ')')
        self.note3.SetLabel('MAJOR LINES')
        self.note4.SetLabel('MINOR LINES')

        if obj.GetValue() == 'Python Coding':
            self.PgSize.ChangeValue('Legal')
            self.lefttxt.ChangeValue('20')
            self.righttxt.ChangeValue('6')
            self.toptxt.ChangeValue('5')
            self.btmtxt.ChangeValue('10')
            self.chkmjr.SetValue(True)
            self.unitsbox.SetSelection(0)
            self.orientbox.SetSelection(1)
            self.x_axis.ChangeValue('4')
            self.y_axis.ChangeValue('6')
            self.x_interval.ChangeValue('4')
            self.y_interval.ChangeValue('8')
            self.MajColor.ChangeValue('dark grey')
            self.MajWt.ChangeValue('1.5')
            self.MinColor.ChangeValue('light red')
            self.MinWt.ChangeValue('.5')
        elif obj.GetValue() == 'Dot':
            self.note4.SetLabel('DOTS')
            self.note6.SetLabel('Dot Size')
            self.x_interval.ChangeValue('1')
            self.y_interval.ChangeValue('1')
            self.x_interval.Enable(False)
            self.y_interval.Enable(False)
            self.chkmjr.SetValue(False)
            self.chkmjr.Enable(False)
            self.MajColor.Disable()
            self.MajWt.Disable()
        elif obj.GetValue() == 'Semi Log':
            self.text2.SetLabel('Number of\nLog Cycles')
            self.note7.SetLabel('X-Axis')
            self.x_interval.Enable(False)
        elif obj.GetValue() == 'Log Log':
            self.text2.SetLabel('Number of\nLog Cycles')
            self.note7.SetLabel('X-Axis')
            self.text3.SetLabel('Number of\nLog Cycles')
            self.note8.SetLabel('Y-Axis')
            self.x_interval.Enable(False)
            self.y_interval.Enable(False)
            self.chkmjr.SetValue(True)
            self.chkmjr.Enable(False)
        elif obj.GetValue() == 'Isometric':
            self.note3.SetLabel('VERTICAL LINES')
            self.note4.SetLabel('DIAGONAL LINES')
            self.chkmjr.SetValue(True)
            self.chkmjr.Enable(False)
            self.y_interval.ChangeValue('0')
            self.x_interval.ChangeValue('1')
            self.y_axis.ChangeValue('0')
            self.x_interval.Disable()
            self.y_interval.Disable()
            self.y_axis.Disable()
        elif obj.GetValue() == 'Polar Cordinate':
            self.note3.SetLabel('CONCENTRIC CIRCLES')
            self.note4.SetLabel('RADIAL LINES')
            self.text2.SetLabel('Circle\nSpacing')
            self.note7.SetLabel('Spacing\n(' + self.unitsbox.GetString
                                (self.unitsbox.GetSelection()) + ')')
            self.chkmjr.SetValue(False)
            self.chkmjr.Enable(False)
            self.y_interval.ChangeValue('0')
            self.x_interval.ChangeValue('1')
            self.y_axis.ChangeValue('0')
            self.x_interval.Disable()
            self.y_interval.Disable()
            self.y_axis.Disable()
        elif obj.GetValue() == 'Lined Paper':
            self.note3.SetLabel('PRIMARY LINES')
            self.note4.SetLabel('SECONDARY LINES')
            self.text2.SetLabel('Primary\nSpacing')
            self.note7.SetLabel('(' + self.unitsbox.GetString
                                (self.unitsbox.GetSelection()) + ')')
            self.text3.SetLabel('Margine\nLocation')
            self.note8.SetLabel('(' + self.unitsbox.GetString
                                (self.unitsbox.GetSelection()) + ')')
            self.chkmjr.SetLabel('Show Secondary Lines')
            self.intrvnote1.SetLabel('0 for\nNo Margine')
            self.x_interval.ChangeValue('1')
            self.x_interval.Disable()

    def OnRadio(self, evt):
        self.note7.SetLabel('X-Axis\n(' + self.unitsbox.GetString
                            (self.unitsbox.GetSelection()) + ')')
        self.note8.SetLabel('Y-Axis\n(' + self.unitsbox.GetString
                            (self.unitsbox.GetSelection()) + ')')

    def OnClose(self, evt):
        self.Destroy()

    def OnReset(self, evt):
        self.chkmjr.Enable()
        self.MinWt.Enable()
        self.x_interval.Enable()
        self.y_interval.Enable()
        self.y_axis.Enable()
        self.MajColor.Enable()
        self.MajWt.Enable()
        self.text2.SetLabel('Line\nSpacing')
        self.note7.SetLabel('X-Axis\n(' + self.unitsbox.GetString
                            (self.unitsbox.GetSelection()) + ')')
        self.text3.SetLabel('Line\nSpacing')
        self.note8.SetLabel('Y-Axis\n(' + self.unitsbox.GetString
                            (self.unitsbox.GetSelection()) + ')')
        self.note3.SetLabel('MAJOR LINES')
        self.note4.SetLabel('MINOR LINES')
        self.GrphTyp.ChangeValue('')
        self.PgSize.ChangeValue('')
        self.lefttxt.ChangeValue('')
        self.righttxt.ChangeValue('')
        self.toptxt.ChangeValue('')
        self.btmtxt.ChangeValue('')
        self.chkmjr.SetValue(False)
        self.unitsbox.SetSelection(0)
        self.orientbox.SetSelection(0)
        self.x_axis.ChangeValue('')
        self.y_axis.ChangeValue('')
        self.x_interval.ChangeValue('')
        self.y_interval.ChangeValue('')
        self.MajColor.ChangeValue('')
        self.MajWt.ChangeValue('')
        self.MinColor.ChangeValue('')
        self.MinWt.ChangeValue('')


class PDFFrm(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel
        self.Maximize(True)

        self.parent = parent
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrm)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonpanel = pdfButtonPanel(self, wx.NewId(),
                                          wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        vsizer.Add(self.buttonpanel, 0,
                   wx.GROW | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.viewer = pdfViewer(self, wx.NewId(), wx.DefaultPosition,
                                wx.DefaultSize, wx.HSCROLL |
                                wx.VSCROLL | wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW | wx.LEFT | wx.RIGHT |
                   wx.BOTTOM, 5)
        loadbutton = wx.Button(self, wx.NewId(), "Load PDF file",
                               wx.DefaultPosition, wx.DefaultSize, 0)
        loadbutton.SetForegroundColour((255, 0, 0))
        vsizer.Add(loadbutton, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        hsizer.Add(vsizer, 1, wx.GROW | wx.ALL, 5)
        self.SetSizer(hsizer)
        self.SetAutoLayout(True)

        # introduce buttonpanel and viewer to each other
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel

        self.Bind(wx.EVT_BUTTON, self.OnLoadButton, loadbutton)

        self.CenterOnParent()
        self.GetParent().Enable(False)
        self.Show(True)
        self.__eventLoop = wx.GUIEventLoop()
        self.__eventLoop.Run()

    def OnLoadButton(self, event):
        dlg = wx.FileDialog(self, wildcard="*.pdf")
        if dlg.ShowModal() == wx.ID_OK:
            wx.BeginBusyCursor()
            self.viewer.LoadFile(dlg.GetPath())
            wx.EndBusyCursor()
        dlg.Destroy()

    def OnCloseFrm(self, evt):
        self.GetParent().Enable(True)
        self.__eventLoop.Exit()
        self.Destroy()


if __name__ == '__main__':

    app = wx.App(False)
    frm = BldGrf()
    app.MainLoop()
