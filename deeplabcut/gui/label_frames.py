"""
DeepLabCut2.0 Toolbox (deeplabcut.org)
© A. & M. Mathis Labs
https://github.com/AlexEMG/DeepLabCut
Please see AUTHORS for contributors.

https://github.com/AlexEMG/DeepLabCut/blob/master/AUTHORS
Licensed under GNU Lesser General Public License v3.0

"""

import os
import pydoc
import sys

import wx

import deeplabcut
from deeplabcut.utils import auxiliaryfunctions, skeleton

media_path = os.path.join(deeplabcut.__path__[0], "gui", "media")
logo = os.path.join(media_path, "logo.png")


class Label_frames(wx.Panel):
    """
    """

    def __init__(self, parent, gui_size, cfg):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        # variable initilization
        self.method = "automatic"
        self.config = cfg
        # design the panel
        sizer = wx.GridBagSizer(5, 5)

        text = wx.StaticText(self, label="DeepLabCut - Step 3. Label Frames")
        sizer.Add(text, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=15)
        # Add logo of DLC
        icon = wx.StaticBitmap(self, bitmap=wx.Bitmap(logo))
        sizer.Add(icon, pos=(0, 4), flag=wx.TOP | wx.RIGHT | wx.ALIGN_RIGHT, border=5)

        line1 = wx.StaticLine(self)
        sizer.Add(line1, pos=(1, 0), span=(1, 5), flag=wx.EXPAND | wx.BOTTOM, border=10)

        self.cfg_text = wx.StaticText(self, label="Select the config file")
        sizer.Add(self.cfg_text, pos=(2, 0), flag=wx.TOP | wx.LEFT, border=5)

        if sys.platform == "darwin":
            self.sel_config = wx.FilePickerCtrl(
                self,
                path="",
                style=wx.FLP_USE_TEXTCTRL,
                message="Choose the config.yaml file",
                wildcard="*.yaml",
            )
        else:
            self.sel_config = wx.FilePickerCtrl(
                self,
                path="",
                style=wx.FLP_USE_TEXTCTRL,
                message="Choose the config.yaml file",
                wildcard="config.yaml",
            )
        sizer.Add(
            self.sel_config, pos=(2, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND, border=5
        )
        self.sel_config.SetPath(self.config)
        self.sel_config.Bind(wx.EVT_BUTTON, self.select_config)

        self.cfg3d_text = wx.StaticText(self, label="Select the config3d file")
        sizer.Add(
            self.cfg3d_text,
            pos=(3, 0),
            flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT,
            border=5,
        )

        if sys.platform == "darwin":
            self.sel_config3d = wx.FilePickerCtrl(
                self,
                path="",
                style=wx.FLP_USE_TEXTCTRL,
                message="Optional: select the 3D config.yaml",
                wildcard="*.yaml",
            )
        else:
            self.sel_config3d = wx.FilePickerCtrl(
                self,
                path="",
                style=wx.FLP_USE_TEXTCTRL,
                message="Optional: select the 3D config.yaml",
                wildcard="*.yaml",
            )
        sizer.Add(
            self.sel_config3d,
            pos=(3, 1),
            span=(1, 3),
            flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
            border=5,
        )
        self.sel_config3d.SetPath("")
        self.config3d = None
        self.sel_config3d.Bind(wx.EVT_FILEPICKER_CHANGED, self.select_config3d)

        self.help_button = wx.Button(self, label="Help")
        sizer.Add(self.help_button, pos=(5, 0), flag=wx.LEFT, border=10)
        self.help_button.Bind(wx.EVT_BUTTON, self.help_function)

        self.check = wx.Button(self, label="Check Labels!")
        sizer.Add(self.check, pos=(6, 4), flag=wx.BOTTOM | wx.RIGHT, border=10)
        self.check.Bind(wx.EVT_BUTTON, self.check_labelF)
        self.check.Enable(True)

        self.build = wx.Button(self, label="Build skeleton")
        sizer.Add(self.build, pos=(5, 3), flag=wx.BOTTOM | wx.RIGHT, border=10)
        self.build.Bind(wx.EVT_BUTTON, self.build_skeleton)
        self.build.Enable(True)

        self.cfg = auxiliaryfunctions.read_config(self.config)
        if self.cfg.get("multianimalproject", False):

            self.check = wx.Button(self, label="Check Labels Individuals")
            sizer.Add(self.check, pos=(6, 3), flag=wx.BOTTOM | wx.RIGHT, border=10)
            self.check.Bind(wx.EVT_BUTTON, self.check_labelInd)
            self.check.Enable(True)

        self.ok = wx.Button(self, label="Label Frames")
        sizer.Add(self.ok, pos=(5, 4))
        self.ok.Bind(wx.EVT_BUTTON, self.label_frames)

        self.reset = wx.Button(self, label="Reset")
        sizer.Add(
            self.reset, pos=(5, 1), span=(1, 1), flag=wx.BOTTOM | wx.RIGHT, border=10
        )
        self.reset.Bind(wx.EVT_BUTTON, self.reset_label_frames)

        sizer.AddGrowableCol(2)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def help_function(self, event):

        filepath = "help.txt"
        f = open(filepath, "w")
        sys.stdout = f
        fnc_name = "deeplabcut.label_frames"
        pydoc.help(fnc_name)
        f.close()
        sys.stdout = sys.__stdout__
        help_file = open("help.txt", "r+")
        help_text = help_file.read()
        wx.MessageBox(help_text, "Help", wx.OK | wx.ICON_INFORMATION)
        help_file.close()
        os.remove("help.txt")

    def check_labelF(self, event):
        dlg = wx.MessageDialog(
            None,
            "This will now plot the labeled frames afer you have finished labeling!",
        )
        result = dlg.ShowModal()
        deeplabcut.check_labels(self.config, visualizeindividuals=False)

    def check_labelInd(self, event):
        dlg = wx.MessageDialog(
            None,
            "This will now plot the labeled frames afer you have finished labeling!",
        )
        result = dlg.ShowModal()
        deeplabcut.check_labels(self.config, visualizeindividuals=True)

    def build_skeleton(self, event):
        skeleton.SkeletonBuilder(self.config)

    def select_config(self, event):
        """
        """
        self.config = self.sel_config.GetPath()

    def select_config3d(self, event):
        """
        """
        self.config3d = self.sel_config3d.GetPath()

    def label_frames(self, event):
        if self.config3d == "":
            self.config3d = None
        deeplabcut.label_frames(self.config, config3d=self.config3d, sourceCam=None)

    def reset_label_frames(self, event):
        """
        Reset to default
        """
        self.config = []
        self.sel_config.SetPath("")
        self.sel_config3d.SetPath("")
