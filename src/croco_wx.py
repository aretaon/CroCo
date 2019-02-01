#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
The CroCo Cross-Link Converter GUI

Graphical interface to convert results from data analysis of chemical cross-linking /
mass-spectrometry experiments.

This script creates the GUI in wxPython (https://wxpython.org/pages/overview/)
"""
import os, sys

import wx
import wx.adv
import pandas as pd

import croco
#from pandas import read_csv



class CroCoMainFrame(wx.Frame):
    """ The wx window class for the croco cross-link converter GUI

    Attributes:
        availReads (dict): Dictionary with writing operation to list: [function to call (func), options for displaying a related widget (list)].
                           Structure of options list:
                           (Label for the widget (str)),
                           type of the widget (can be 'file'/'dir'/'input'/'check'),
                           Help text (str),
                           Optional multi-purpose field: e.g. default value for input fields)
        availWrites (dict):  Dictionary with writing operation to list. For
                             structure see availReads.
        currentPath (str): set starting path for folder selection GUI
        col_order (list of str): defines the column headers required for xtable output
        inputOptionsToUserInput (dict): mapping the label names to the user-provided input
        outputOptionsToUserInput (dict): mapping the label names to the user-provided input

    """

    def __init__(self):
        """
        Initialises parameters for the MainFrame
        """
        # ensure the parent's __init__ is called
        wx.Frame.__init__(self,
                          None,
                          wx.ID_ANY,
                          style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,
                          title='The CroCo cross-link converter')

        self.panel = wx.Panel(self)

        ## setting the icon for the frame
        # in case of calling croco from the source folder structure...
        file_dir, file_name = os.path.split(__file__)
        if os.path.exists(os.path.join(file_dir,
                                       './croco/data/croco_logo.ico')):
            iconFile = os.path.abspath(os.path.join(file_dir,
                                                      './croco/data/croco_logo.ico'))
        # ... or calling from a exe-file in a folder-setup with the data folder at top-level
        elif os.path.exists('./croco/data/croco_logo.ico'):
            iconFile = os.path.abspath('./croco/data/croco_logo.ico')
        # ... or calling from within a single bundled exe-file
        else:
            try:
                # PyInstaller creates a temp folder and stores its path in _MEIPASS
                base_path = sys._MEIPASS
                iconFile =  os.path.abspath(\
                    os.path.join(base_path, './data/croco_logo.ico'))
            # ... or something went wrong
            except:
                raise Exception('croco_logo.ico not found')
        ## end setting the icon

        icon = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.currentPath = os.getcwd()

        # define the croco read and write options and link to the modules
        # each value of a dict is a list of [ functionToCall, options]
        self.availReads = {'pLink1': [croco.pLink1.Read, []],
                           'pLink2': [croco.pLink2.Read, []],
                           'Kojak': [croco.Kojak.Read, [('Kojak rawfile',
                                                         'input',
                                                         'Please provide the name of the rawfile for the data')]],
                           'Kojak+Percolator': [croco.KojakPercolator.Read, []],
                           'StavroX': [croco.StavroX.Read, [('SSF file',
                                                             'file',
                                                             'Please provide an SSF file as returned by StavroX')]],
                           'Xi': [croco.Xi.Read, []],
                           'Xi+XiFDR': [croco.XiSearchFDR.Read,[('Xi search file',
                                                                   'file',
                                                                   'Please provide Xi output file')]],
                           'xQuest': [croco.xQuest.Read, []],
                           'xTable': [croco.xTable.Read, []]}

        self.availWrites =  {'xTable': [croco.xTable.Write, []],
                             'xVis': [croco.xVis.Write, []],
                             'xiNet': [croco.xiNET.Write, []],
                             'DynamXL': [croco.DynamXL.Write, []],
                             'xWalk': [croco.xWalk.Write, [('PDB to map xlinks to',
                                                            'file',
                                                            'Please provide a PDB file you want to map the xlinks to.\n'+\
                                                            'No special format is required as only the filename is used'),
                                                           ('Offset',
                                                            'input',
                                                            'Difference between the index in the PDB file and the xTable ' +\
                                                            '(e.g. 1 for 12 in the xTable and 13 in the PDB)'),
                                                           ('Chains',
                                                            'input',
                                                            'Map chains to protein names (e.g. Protein1:AB, Protein2:C). '+\
                                                            'Use exactly the same naming scheme as the xTable file'),
                                                           ('PDB Atom code',
                                                            'input',
                                                            'Provide an PDB atom code (e.g. CB) for distance calculation')]],
                             'pLabel': [croco.pLabel.Write, [('Dir containing mgf files',
                                                              'dir',
                                                              'Provide path to a folder containing mgf-files corresponding to the'+\
                                                              'rawfile names in the input file'),
                                                             ('Xlinker as referenced by pLabel',
                                                              'input',
                                                              'Provide a cross-linker name (e.g. BS3) that is used by pLabel'+\
                                                              'to calculate the potentially linked amino acids',
                                                              'BS3'),
                                                             ('Merge mgf files',
                                                              'check',
                                                              'Tick to merge mgf files into one file containign' +
                                                              'only the spectra  mentioned in the (merged) pLabel')]],
                              'customTable': [croco.customTable.Write, [('Custom Template',
                                                                         'file',
                                                                         'Provide tample file for parsing')]]}

        self.col_order = ['rawfile', 'scanno', 'prec_ch',
                          'pepseq1', 'xlink1',
                          'pepseq2', 'xlink2', 'xtype',
                          'modmass1', 'modpos1', 'mod1',
                          'modmass2', 'modpos2', 'mod2',
                          'prot1', 'xpos1', 'prot2',
                          'xpos2', 'type', 'score', 'ID', 'pos1', 'pos2', 'decoy']

        #: bool: True if the read format is set
        self.readSet = False
        #: bool: True if the write format is set
        self.writeSet = False

        # create a menu bar
        self.makeMenuBar()

        # load widgets
        # ALWAYS AFTER LOADING MENU AND STATUS BAR!!!!
        self.createWidgets()

        # Dicts mapping the label names to the user-provided input
        self.inputOptionsToUserInput = {}
        self.outputOptionsToUserInput = {}

    def createWidgets(self):
        """
        Create the widgets for the croco MainFrame

        Attributes:

            compactTableCheck (wx.CheckBox): whether to compact the table before passing to output function
            mergeTableCheck (wx.CheckBox): Whether to merge multiple files (pass paths in loop)
            multipleSettingsCheck (wx.CheckBox): whether to apply the same settings to all files or call separately
            writeFormat (str): the format to write data to (from availWrites)
            readFormat (str): the format to read data from (from availReads)
        """

        ## define the widgets
        # define the contents of the first sizer

        input_lbl = wx.StaticText(self.panel,wx.ID_ANY, label='Input', style=wx.ALIGN_CENTER )
        self.inputButton = wx.Button(self.panel, label='Load file(s)')
        self.inputButton.Enable(False)
        self.readFormat = wx.Choice(self.panel, choices=sorted(list(self.availReads.keys())))

        output_lbl = wx.StaticText(self.panel,wx.ID_ANY, label='Output', style=wx.ALIGN_CENTER )
        self.outputButton = wx.Button(self.panel, label='Write to')
        self.outputButton.Enable(False)
        self.writeFormat = wx.Choice(self.panel, choices=sorted(list(self.availWrites.keys())))

        self.compactTableCheck = wx.CheckBox(self.panel, label='Compact xTable')
        self.mergeTableCheck = wx.CheckBox(self.panel, label='Merge files')
        self.multipleSettingsCheck = wx.CheckBox(self.panel, label='Same settings for all files')

        self.controlStart = wx.Button(self.panel, label='Start')
        self.controlStart.Enable(False)
        controlQuit = wx.Button(self.panel, label='Quit')

        helpButton = wx.ContextHelpButton(self.panel)

        ## create Connects

        self.readFormat.Bind(wx.EVT_CHOICE, self.OnReadFormat)
        self.readFormat.Bind(wx.EVT_HELP,
                             lambda evt: self.Info('Select data-format for input', caption='Help'))
        self.writeFormat.Bind(wx.EVT_CHOICE, self.OnWriteFormat)
        self.writeFormat.Bind(wx.EVT_HELP,
                              lambda evt: self.Info('Select data-format for output', caption='Help'))

        self.inputButton.Bind(wx.EVT_BUTTON, self.OnOpenSwitch)
        self.inputButton.Bind(wx.EVT_HELP,
                              lambda evt: self.Info('Opens a dialog to select file for input', caption='Help'))
        self.outputButton.Bind(wx.EVT_BUTTON, self.onOutputDir)
        self.outputButton.Bind(wx.EVT_HELP,
                              lambda evt: self.Info('Opens a dialog to select output dir', caption='Help'))

        controlQuit.Bind(wx.EVT_BUTTON, self.onExit)
        self.controlStart.Bind(wx.EVT_BUTTON, self.onStart)
        self.controlStart.Bind(wx.EVT_HELP,
                               lambda evt: self.Info('Start the conversion', caption='Help'))

        self.compactTableCheck.Bind(wx.EVT_HELP,
                               lambda evt: self.Info('Only add minimal columns to xTable', caption='Help'))
        self.mergeTableCheck.Bind(wx.EVT_HELP,
                               lambda evt: self.Info('Merge the data from multiple input files into one. Does not work for pLink or xi+xiFDR.', caption='Help'))
        self.multipleSettingsCheck.Bind(wx.EVT_HELP,
                               lambda evt: self.Info('Use the same settings for all processed files.', caption='Help'))


        ## define the layout
        # define the sizers (main widget layouts) used in the app
        topSizer = wx.BoxSizer(wx.VERTICAL)
        loadSizer = wx.FlexGridSizer(rows=2, cols=3, vgap=10, hgap=10)
        loadSizerContainer = wx.BoxSizer(wx.HORIZONTAL)
        controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        checkSizer = wx.BoxSizer(wx.HORIZONTAL)

        # assign the widgets to the sizers
        loadSizer.AddMany([input_lbl,
                          (self.readFormat, 1, wx.EXPAND),
                          self.inputButton,
                          output_lbl,
                          (self.writeFormat, 1, wx.EXPAND),
                          self.outputButton])

        # allow to resize the second row
        loadSizer.AddGrowableCol(1, 1)
        # contain the grid in a BoxSizer to set borders individually
        loadSizerContainer.Add(loadSizer, proportion=1, flag=wx.ALL|wx.EXPAND)

        # Set checkboxes
        checkSizer.Add(self.compactTableCheck, 1, wx.ALL|wx.EXPAND, 5)
        checkSizer.Add(self.mergeTableCheck, 1, wx.ALL|wx.EXPAND, 5)
        checkSizer.Add(self.multipleSettingsCheck, 1, wx.ALL|wx.EXPAND, 5)

        # Set start and quit buttons
        controlSizer.Add(self.controlStart, 1, wx.RIGHT, 5)
        controlSizer.Add(controlQuit, 0, wx.LEFT | wx.ALIGN_RIGHT, 5)
        controlSizer.Add(helpButton, 0, wx.LEFT | wx.ALL | wx.EXPAND, 5)

        # assign lower sizers to the top-level sizer
        topSizer.Add(loadSizerContainer, 0, wx.ALL|wx.EXPAND, 5)
        # topSizer.Add(reviewSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(checkSizer, 0, wx.EXPAND|wx.RIGHT, 5)
        topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(controlSizer, 0, wx.EXPAND|wx.RIGHT, 5)
        # topSizer.Add(gauge, 0,wx.ALL|wx.EXPAND, 5)

        # assign the top sizer to the panel i.e. main layout instance
        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)

    def makeMenuBar(self):
        """
        Create the top menu for the CroCo MainFrame
        """

        # Make a file menu
        fileMenu = wx.Menu()

        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        # menu_load = fileMenu.Append(-1, "&Load file\tCtrl-O",
        #         "Load a new file")
        # fileMenu.AppendSeparator()

        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "File")
        menuBar.Append(helpMenu, "Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        # self.Bind(wx.EVT_MENU, self.OnLoad, menu_load)
        self.Bind(wx.EVT_MENU, self.onExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.onAbout, aboutItem)

    ## GUI Functions

    def OnReadFormat(self, event):
        """
        function to enable the file input button only after an input format was chosen

        Args:
            event (wx.Event)
        """
        self.theReadFormat = self.readFormat.GetString(self.readFormat.GetSelection())
        print('[onReadFormat] Reading {} format'.\
            format(self.theReadFormat))
        self.inputButton.Enable(True)

    def OnWriteFormat(self, event):
        """
        function to enable the file output button only after an input format was chosen

        Args:
            event (wx.Event)
        """
        self.theWriteFormat = self.writeFormat.GetString(self.writeFormat.GetSelection())
        print('[onWriteFormat] Writing {} format'.\
            format(self.theWriteFormat))
        self.outputButton.Enable(True)

    def OnOpenSwitch(self, event):
        """
        Open a dir-opening dialog if pLink was selected, else file-opening

        Args:
            event (wx.Event)
        """
        if 'pLink' in self.theReadFormat:
            self.onInputDir()
        else:
            self.onInputFile()

    def onInputFile(self):
        """
        Open a file dialaog and set the paths

        Attributes:
            theInput (list of str): selected input paths

        """
        dlg = wx.FileDialog(self,
                            message="Choose one or multiple files for input",
                            defaultDir=self.currentPath,
                            defaultFile="",
                            wildcard="*.*",
                            style=wx.FD_MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.theInput = dlg.GetPaths()
            self.currentPath = os.path.dirname(self.theInput[0])
            print('[onInputFile] Loaded {}'.format(', '.join(self.theInput)))
        dlg.Destroy()

        self.readSet = True
        if self.writeSet:
            self.controlStart.Enable(True)

    def onInputDir(self):
        """
        Open a dir dialaog and set the paths
        """
        dlg = wx.DirDialog(self,
                           message="Choose one or multiple directories for Input:",
                           defaultPath=self.currentPath,
                           style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

        if dlg.ShowModal() == wx.ID_OK:
            # self.theInput is always a list of paths
            self.theInput = [dlg.GetPath()]
            self.currentPath = dlg.GetPath()
            print('[onInputDir] Loaded {}'.format(self.currentPath))

        dlg.Destroy()

        self.readSet = True
        if self.writeSet:
            self.controlStart.Enable(True)

    def onOutputDir(self, event):
        """
        Open a dialog to select an output dir

        Attributes:
            theOutput (str): Path to write output
        """
        dlg = wx.DirDialog(self,
                           message="Choose a directory:",
                           defaultPath=self.currentPath,
                           style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            self.currentPath = self.theOutput = dlg.GetPath()
            print('[onOutputDir] Loaded {}'.format(self.currentPath))

        dlg.Destroy()

        self.writeSet = True
        if self.readSet:
            self.controlStart.Enable(True)

    def onExit(self, event):
        """Close the frame, terminating the application."""
        dlg = wx.MessageDialog(self,
            "Do you really want to close this application?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def onCancel(self, event):
        self.closeProgram()

    def onAbout(self, event):
        """Show the about dialog"""

        aboutInfo = wx.adv.AboutDialogInfo()
        aboutInfo.SetName("The CroCo cross-link converter")
        aboutInfo.SetVersion('0.5.12')
        aboutInfo.SetDescription("Graphical interface to convert results from "+\
                                 "data analysis of chemical cross-linking "+\
                                 "mass-spectrometry experiments.")
        aboutInfo.SetCopyright("(C) 2018")
        aboutInfo.SetWebSite("www.halomem.de")
        aboutInfo.AddDeveloper("Julian Bender (jub@halomem.de)")

        wx.adv.AboutBox(aboutInfo)

    def Warning(self, message, caption = 'Warning!'):
        """
        Issue a warning on the console and as a wx window

        Args:
            message (str): Message to send
            caption (str): Title for the wx-window
        """
        print('[WARN] {}'.format(message))
        dlg = wx.MessageDialog(self, message, caption, wx.OK | wx.ICON_WARNING)
        del self.wait
        dlg.ShowModal()
        dlg.Destroy()

    def Info(self, message, caption = 'CroCo'):
        """
        Generate a message dialog

        Args:
            message (str): Message to send
            caption (str): Title for the wx-window
        """
        dlg = wx.MessageDialog(self, message, caption, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    ## Procedural Functions

    def onStart(self, event):
        """
        Show dialog if additional user input is required.
        Otherwise start the conversion
        """
        # Check if there are options to ask for
        if len(self.availReads[self.theReadFormat][1]) > 0 or\
            len(self.availWrites[self.theWriteFormat][1]) > 0:

            # init the OptionsWindow as child
            OptionsFrame = CroCoOptionsFrame(self)

            # set the variables in the child window
            OptionsFrame.InputOptionsToAsk = self.availReads[self.theReadFormat][1]
            OptionsFrame.OutputOptionsToAsk = self.availWrites[self.theWriteFormat][1]

            # update the controls according to the variables
            OptionsFrame.updateOptions()
            # show the window
            OptionsFrame.Show()

        else:
            # reset args dicts
            self.inputOptionsToUserInput = dict()
            self.outputOptionsToUserInput = dict()

            self.onRun(event)

    def onRun(self, event):
        """
        Collect all necessary information from self and start the
        conversion by calling the actual conversion script

        Args:
            event (wx.Event)
        """

        print('[onRun] Going to convert {} from {} '.format(', '.join(self.theInput),
                                                   self.theReadFormat) +
               'format to {} format'.format(self.theWriteFormat))

        # Displays a busy cursor during the run of the programme
        self.wait = wx.BusyCursor()

        def runCroCo(f):
            """
            Function to wrap up the CroCo call to simplify maintenance.

            Relies on many variables in self

            Args:
                f (list): list of filepaths to call CroCo on
            Returns:
                outpath (str): path where the files are written
            """
            try:
                if len(self.inputOptionsToUserInput) > 0 :
                    if self.multipleSettingsCheck.GetValue() is False:

                        # init a list of xtables because every single call to
                        # croco with a different set of options will
                        # generate another table
                        allData = list()
                        for file in f:
                            fname = os.path.basename(file)
                            print(fname)
                            # Collect the input options for this file by concatenating
                            # the options label with the file name
                            args = list()
                            for option in self.availReads[self.theReadFormat][1]:
                                label = fname + ' - ' + option[0]
                                args.append(self.inputOptionsToUserInput[label])
                            print('[onRun] Found input args for file {}: "{}"'.format(fname, args))
                            s = self.availReads[self.theReadFormat][0](f, *args, col_order=self.col_order)
                            allData.append(s)

                        xtable = pd.concat(allData)

                    else:
                        args = list(self.inputOptionsToUserInput.values())
                        print('[onRun] Found input args for file {}: "{}"'.format(f, args))
                        xtable = self.availReads[self.theReadFormat][0](f, *args, col_order=self.col_order)
                else:
                    print('[onRun] No extra input arguments required.')
                    xtable = self.availReads[self.theReadFormat][0](f, col_order=self.col_order)
                print('[onRun] Table(s) successfully read: {}'.format(', '.join(f)))
            except Exception as e:
                self.Warning('Error while reading Input-file: ' + str(e))

            print('[onRun] xTable read from input: {}'.format(', '.join(xtable.columns)))

            # Compact the xTable if checkbox is checked
            xtable = croco.HelperFunctions.applyColOrder(xtable,
                                                         col_order=self.col_order,
                                                         compact=self.compactTableCheck.GetValue())

            # if no user-defined output dir use current
            if self.theOutput == '':
                self.theOutput = os.path.dirname(f)

            # set filename for output file
            fileString = '_'.join([os.path.splitext(os.path.basename(x))[0] for x in f])
            fileString = croco.HelperFunctions.alphanum_string(fileString)
            fname = fileString + '_' + self.theReadFormat +\
                    '_to_' + self.theWriteFormat

            # generate output path w/o extension
            outpath = os.path.join(self.theOutput, fname)

            try:
                print('[onRun] Writing table in {} format to {}'.format(self.theWriteFormat, outpath))
                if len(self.outputOptionsToUserInput) > 0:
                    args = list(self.outputOptionsToUserInput.values())
                    print('[onRun] Found output args: "{}"'.format(args))
                    self.availWrites[self.theWriteFormat][0](xtable, outpath, *args)
                else:
                    print('[onRun] No extra output arguments required.')
                    self.availWrites[self.theWriteFormat][0](xtable, outpath)
                print('[onRun] Table successfully written!')
            except Exception as e:
                self.Warning('[onRun] Conversion of {} was '.format(f) +
                                   'not successfull:{}'.format(str(e)))

            return outpath

        if self.mergeTableCheck.GetValue() == True:
            outpath = runCroCo(self.theInput)
        else:
            for f in self.theInput:
                outpath = runCroCo([f])

        # ends busy cursor
        del self.wait
        self.Info('File(s) successfully written ' +
                 'to {}!'.format(outpath),
                 caption='Success!')

class CroCoOptionsFrame(wx.Frame):
    """
    Child Frame to CroCoMainWindow asking the user for input
    regarding the possible options of a submodule

    Attributes:
        parent (wx.Frame): parent frame
        currentPath (str): current working directory
        InputOptionsToAsk (list): Input options from CroCoMainWindow
        InputOptionsToAsk (list): Output options from CroCoMainWindow
    """

    def __init__(self, parent):
        """
        Initialise the wxFrame

        Args:
            parent: parent object
        """
        wx.Frame.__init__(self,
                          wx.GetApp().TopWindow,
                          wx.ID_ANY,
                          style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,
                          title='Options')

        self.panel = wx.Panel(self)

        ## setting the icon for the frame
        # in case of calling croco from the source folder structure...
        file_dir, file_name = os.path.split(__file__)
        if os.path.exists(os.path.join(file_dir,
                                       './croco/data/croco_logo.ico')):
            iconFile = os.path.abspath(os.path.join(file_dir,
                                                      './croco/data/croco_logo.ico'))
        # ... or calling from a exe-file in a folder-setup with the data folder at top-level
        elif os.path.exists('./croco/data/croco_logo.ico'):
            iconFile = os.path.abspath('./croco/data/croco_logo.ico')
        # ... or calling from within a single bundled exe-file
        else:
            try:
                # PyInstaller creates a temp folder and stores its path in _MEIPASS
                base_path = sys._MEIPASS
                iconFile =  os.path.abspath(\
                    os.path.join(base_path, './data/croco_logo.ico'))
            # ... or something went wrong
            except:
                raise Exception('croco_logo.ico not found')
        ## end setting the icon

        icon = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # generate a variable containing the parent to allow pushing back
        # the user-provided input
        self.parent = parent

        # set starting path for folder selection GUI
        self.currentPath = os.getcwd()

        # in these variables the options from CroCoMainWindow will be written
        self.InputOptionsToAsk = []
        self.OutputOptionsToAsk = []

    def updateOptions(self):
        """
        Collect the variables that determine the layout of the options window and
        compute the window layout

        Attributes:
            textCtrls (dict): mapping text labels to input text fields.
                              all inputs done by extra dialog widgets (file and paths) are
                              stored upon closing the dialogs. Text and checkbox inputs have to be evaaluated
                              when the okay-Button has been pressed
        """

        def CreateOptionsContainer(self, option, listofOptions, filename=None):
            """
            Creates and options widget comprising a label and an input field
            (either a button for a file or dir dialog or a free text input)

            Args:
                option (tuple): (label, type of input)
                listOfOptions (list): a list object to append to user-input to
                filename (str): if the same options are processed for multiple
                                files, add the filename to the options label
            Returns:
                optionContainer: wx.BoxSizer object
            """

            if filename:
                # append space to filename to simplify code
                filename = filename+' - '
            else:
                # set the filename to an empty string
                filename = ''

            # when using separate options for multiple files, the filename
            # is added to the option to ask for and the combined label
            # serves as key for later retrieving the inputs
            label = filename + option[0]

            optionLabel = wx.StaticText(self.panel,
                                        wx.ID_ANY,
                                        # name for the label preceding the buttons
                                        label=label,
                                        style=wx.ALIGN_CENTER)
            optionLabel.Bind(wx.EVT_HELP,
                             lambda evt: self.Info(option[2], caption='Help'))

            if option[1] == 'file':
                optionButton = wx.Button(self.panel, label='Load file', name=label)
                # Bind using a lambda function to be able to pass multiple args
                # to the called function
                # see: https://wiki.wxpython.org/Passing%20Arguments%20to%20Callbacks
                optionButton.Bind(wx.EVT_BUTTON,
                                  lambda evt, appendTo=listofOptions, label=label: self.onOpenFile(evt, appendTo, label))
                optionButton.Bind(wx.EVT_HELP,
                                  lambda evt: self.Info(option[2], caption='Help'))

            elif option[1] == 'dir':
                optionButton = wx.Button(self.panel, label='Open directory', name=label)
                optionButton.Bind(wx.EVT_BUTTON,
                                  lambda evt, appendTo=listofOptions, label=label: self.onOpenDir(evt, appendTo, label))
                optionButton.Bind(wx.EVT_HELP,
                                  lambda evt: self.Info(option[2], caption='Help'))
            elif option[1] == 'input':
                # The 4th (optional) element of the options tuple is the multi
                # purpose field that may contain the default value for the
                # input field
                if len(option) > 3:
                    defValue = option[3]
                else:
                    defValue = ''
                optionButton = wx.TextCtrl(self.panel, value=defValue, name=label)
                self.textCtrls[label] = optionButton
                optionButton.Bind(wx.EVT_HELP,
                                  lambda evt: self.Info(option[2], caption='Help'))
            elif option[1] == 'check':
                optionButton = wx.CheckBox(self.panel, name=label)
                self.textCtrls[label] = optionButton
                optionButton.Bind(wx.EVT_HELP,
                                  lambda evt: self.Info(option[2], caption='Help'))
            else:
                raise Exception('[createOptionsContainer] Wrong options format for option: {}'\
                                    .format(label))

            optionContainer = wx.BoxSizer(wx.HORIZONTAL)
            optionContainer.Add(optionLabel, 0, wx.ALL|wx.EXPAND, 5)
            optionContainer.Add(optionButton, 0, wx.ALL|wx.EXPAND, 5)

            return optionContainer

        # dict mapping text labels to input text fields
        self.textCtrls = {}

        # lists containign the label, button sizers for passing to higher
        # level sizer
        InputOptionContainers = []
        OutputOptionContainers = []

        def GenerateOutputOptionContainers(file=None):
            """
            Wrapper for routine to generate label/input containers for either
            a set of filename/options combinations or for a single
            """
            for option in self.InputOptionsToAsk:
                optionContainer = CreateOptionsContainer(self,
                                                         option,
                                                         self.parent.inputOptionsToUserInput,
                                                         filename=file)
                InputOptionContainers.append((optionContainer, 0, wx.ALL|wx.EXPAND, 5))

            for option in self.OutputOptionsToAsk:
                optionContainer = CreateOptionsContainer(self,
                                                         option,
                                                         self.parent.outputOptionsToUserInput,
                                                         filename=file)
                OutputOptionContainers.append((optionContainer, 0, wx.ALL|wx.EXPAND, 5))

        if self.parent.multipleSettingsCheck.GetValue() is False:
            for file in self.parent.theInput:
                file = os.path.basename(file)
                GenerateOutputOptionContainers(file)
        else:
            GenerateOutputOptionContainers()

        ### createWidgets

        inputSizer = wx.BoxSizer(wx.VERTICAL)
        inputSizer.AddMany(InputOptionContainers)

        outputSizer = wx.BoxSizer(wx.VERTICAL)
        outputSizer.AddMany(OutputOptionContainers)

        optionSizer = wx.BoxSizer(wx.HORIZONTAL)
        optionSizer.Add(inputSizer, 0, wx.ALL|wx.EXPAND, 5)
        optionSizer.Add(outputSizer, 0, wx.ALL|wx.EXPAND, 5)

        ## Controls
        okayButton = wx.Button(self.panel, label='Okay')
        closeButton = wx.Button(self.panel, label='Close')
        helpButton = wx.ContextHelpButton(self.panel)

        controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        controlSizer.Add(okayButton, 0, wx.EXPAND|wx.LEFT, 5)
        controlSizer.Add(closeButton, 0, wx.EXPAND|wx.RIGHT, 5)
        controlSizer.Add(helpButton, 0, wx.LEFT | wx.ALL | wx.EXPAND, 5)

        ## topSizer
        topSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer.Add(optionSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(controlSizer, 0, wx.ALL|wx.EXPAND, 5)

        # assign the top sizer to the panel i.e. main layout instance
        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)

        closeButton.Bind(wx.EVT_BUTTON, self.onCancel)
        okayButton.Bind(wx.EVT_BUTTON, self.onOkay)

    def onCancel(self, event):
        print('[onCancel] Closing options window')
        self.Close()

    def onOkay(self, event):
        """
        If the user clicks okay, all inputs will be evaluated, returned to
        the parent classe and the onRun method of the parent class will
        be called
        """

        def CollectUserOptionsInput(file=None):
            """
            Wrapper for collecting the user input stored as attributes of
            CroCoOptionsWindow and return it to the parent class
            """
            # label, type, help, optional
            for option in self.OutputOptionsToAsk:

                if file == None:
                    label = option[0]
                else:                
                    label = file + ' - ' + option[0]
                # all inputs done by extra dialog widgets (file and paths) are
                # stored upon closing
                # the dialogs. Text and checkbox inputs have to be evaaluated
                # when the okay-Button has been pressed
                if (option[1] == 'input') or (option[1] == 'check'):
                    userInput = self.textCtrls[label].GetValue()
                    self.parent.outputOptionsToUserInput[label] = userInput

            for option in self.InputOptionsToAsk:
                if file == None:
                    label = option[0]
                else:                
                    label = file + ' - ' + option[0]
                    
                if (option[1] == 'input') or (option[1] == 'check'):
                    userInput = self.textCtrls[label].GetValue()
                    self.parent.inputOptionsToUserInput[label] = userInput

        if self.parent.multipleSettingsCheck.GetValue() is False:
            for file in self.parent.theInput:
                file = os.path.basename(file)
                CollectUserOptionsInput(file)
        else:
            CollectUserOptionsInput()

        print('[onOkay] Options for Input')
        for key in self.parent.inputOptionsToUserInput:
            print('\t{}: {}'.format(key, self.parent.inputOptionsToUserInput[key]))

        print('[onOkay] Options for Output')
        for key in self.parent.outputOptionsToUserInput:
            print('\t{}: {}'.format(key, self.parent.outputOptionsToUserInput[key]))


        self.parent.onRun(event)

        # Closing options window after passing options to main window
        self.Close()

    def onOpenFile(self, event, dictToAppend, label):
        """File opening method of CroCoOptionsWindow"""
        dlg = wx.FileDialog(self,
                            message="Choose a file for input",
                            defaultDir=self.currentPath,
                            defaultFile="",
                            wildcard="*.*",
                            style=wx.FD_MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK:
             self.currentPath = dictToAppend[label] = dlg.GetPath()
             print('[onOpenFile] Loaded {}'.format(self.currentPath))
        dlg.Destroy()

    def onOpenDir(self, event, dictToAppend, label):
        """Dir opening method of CroCoOptionsWindow"""
        dlg = wx.DirDialog(self,
                           message="Choose one directory for Input:",
                           defaultPath=self.currentPath,
                           style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

        if dlg.ShowModal() == wx.ID_OK:
            self.currentPath = dictToAppend[label] = dlg.GetPath()
            print('[onOpenDir] Loaded {}'.format(self.currentPath))
        dlg.Destroy()

    def Info(self, message, caption = 'CroCo'):
        """Info dialog method of CroCoOptionsWindow"""
        dlg = wx.MessageDialog(self, message, caption, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = CroCoMainFrame().Show()
    app.MainLoop()