import threading
from pathlib import Path

import wx

from autosheet.app import operations
from autosheet.utils import paths, strings


class Window(wx.Frame):
    """
    Main window of the application.
    """

    def __init__(self, title: str, size: tuple[int, int]) -> None:
        """
        Initialize the window.
        """
        super(Window, self).__init__(
            None,
            title=title,
            size=size,
            style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX),
        )

        # Class variable
        self.pdf_path: str | None = None

        # Set icon
        icon = wx.Icon(str(paths.get_path(paths.RESOURCES_FOLDER / "icon.ico")), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Create panel
        self.panel = wx.Panel(self)

        # Create vertical box sizer
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Create logo
        image = wx.Image(
            str(paths.get_path(paths.RESOURCES_FOLDER / "logo.png")), wx.BITMAP_TYPE_ANY
        )
        image = image.Scale(100, 100, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self.panel, bitmap=wx.Bitmap(image))
        vbox.Add(bitmap, flag=wx.ALIGN_CENTER | wx.TOP, border=15)

        # Create title label
        title_label = wx.StaticText(self.panel, label=title)
        font = title_label.GetFont()
        font.PointSize += 10
        font = font.Bold()
        title_label.SetFont(font)
        vbox.Add(title_label, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        # Create description label
        description_label = wx.StaticText(self.panel, label=strings.DESCRIPTION_LABEL)
        vbox.Add(description_label, flag=wx.ALIGN_CENTER | wx.TOP, border=5)

        # Create version label
        version_label = wx.StaticText(self.panel, label=strings.VERSION_LABEL)
        font = version_label.GetFont()
        font.PointSize -= 2
        version_label.SetFont(font)
        vbox.Add(version_label, flag=wx.ALIGN_CENTER | wx.TOP, border=5)

        # Add stretch spacer
        vbox.AddStretchSpacer()

        # Create steps label
        self.steps_label = wx.StaticText(self.panel)
        self.steps_label.Hide()
        vbox.Add(self.steps_label, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=0)

        # Create a progress bar
        self.gauge = wx.Gauge(self.panel, range=100, size=(200, 25))
        self.gauge.Hide()
        vbox.Add(self.gauge, flag=wx.ALIGN_CENTER | wx.BOTTOM)

        # Add stretch spacer
        vbox.AddStretchSpacer()

        # Create result label
        self.result_label = wx.StaticText(self.panel)
        vbox.Add(self.result_label, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        # Create a horizontal sizer for the buttons.
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)

        # Add the "Select Image" button.
        self.select_image_btn = wx.Button(self.panel, label=strings.SELECT_IMAGE_BTN_LABEL)
        self.select_image_btn.Bind(wx.EVT_BUTTON, self.on_select_image_btn_clicked)
        hbox_buttons.Add(self.select_image_btn, flag=wx.RIGHT, border=5)

        # Add the "Open Datasheet" button
        self.open_datasheet_btn = wx.Button(self.panel, label=strings.OPEN_DATASHEET_BTN_LABEL)
        self.open_datasheet_btn.Bind(wx.EVT_BUTTON, self.on_open_datasheet_btn_clicked)
        self.open_datasheet_btn.SetDefault()
        self.open_datasheet_btn.Disable()
        hbox_buttons.Add(self.open_datasheet_btn, flag=wx.LEFT, border=5)

        # Add the horizontal sizer to the vertical sizer.
        vbox.Add(hbox_buttons, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=15)

        # Add trademark label
        trademark_label = wx.StaticText(self.panel, label=strings.TRADEMARK_LABEL)
        font = trademark_label.GetFont()
        font.PointSize -= 2
        trademark_label.SetFont(font)
        vbox.Add(trademark_label, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        # Set initial state
        self.set_initial_state()

        # Set sizer
        self.panel.SetSizer(vbox)

    def set_initial_state(self) -> None:
        """
        Set the initial state of the window.
        """
        self.pdf_path = None

        self.steps_label.Hide()
        self.steps_label.SetLabel(strings.STEPS_LABEL_1_LOADING)
        self.gauge.Hide()
        self.gauge.SetValue(0)

        self.result_label.SetLabel(strings.RESULT_LABEL_INITIAL)
        self.open_datasheet_btn.Disable()

        wx.CallAfter(self.panel.Layout)

    def on_select_image_btn_clicked(self, _: wx.Event) -> None:
        """
        Open the file dialog when the "Select Image" button is clicked.
        """

        # Disable the button
        self.select_image_btn.Disable()
        self.panel.Layout()

        # Define file types: only common image formats
        wildcard = "Image files (*.png;*.jpg;*.jpeg;*.bmp)|*.png;*.jpg;*.jpeg;*.bmp"

        # Open file dialog
        with wx.FileDialog(
            self,
            strings.FILE_DIALOG_TITLE,
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_OK:
                try:
                    wx.BeginBusyCursor()
                    image_path = Path(file_dialog.GetPath())
                    threading.Thread(
                        target=self.do_operations, args=(image_path,), daemon=True
                    ).start()
                except Exception as e:
                    wx.MessageBox(str(e), "Error", wx.ICON_ERROR | wx.OK)
                finally:
                    wx.EndBusyCursor()
                    self.set_initial_state()

        # Enable the button
        self.select_image_btn.Enable()
        self.panel.Layout()

    def do_operations(self, image_path: Path) -> None:
        """
        Perform the operations in a separate thread.
        """
        # Show the steps label and the gauge
        wx.CallAfter(self.steps_label.Show)
        wx.CallAfter(self.gauge.Show)
        wx.CallAfter(self.result_label.SetLabel, strings.RESULT_LAVEL_ANALYZING)
        wx.CallAfter(self.panel.Layout)

        # Step 1: Load the image
        wx.CallAfter(self.steps_label.SetLabel, strings.STEPS_LABEL_1_LOADING)
        raw_image = operations.load_image(image_path)
        wx.CallAfter(self.gauge.SetValue, 25)
        wx.CallAfter(self.panel.Layout)

        # Step 2: Process the image
        wx.CallAfter(self.steps_label.SetLabel, strings.STEPS_LABEL_2_PROCESSING)
        processed_image = operations.process_image(image_path.stem, raw_image)
        wx.CallAfter(self.gauge.SetValue, 50)
        wx.CallAfter(self.panel.Layout)

        # Step 3: Recognize text
        wx.CallAfter(self.steps_label.SetLabel, strings.STEPS_LABEL_3_RECOGNIZING)
        raw_image_text, processed_image_text = operations.recognize_text(raw_image, processed_image)
        wx.CallAfter(self.gauge.SetValue, 75)
        wx.CallAfter(self.panel.Layout)

        # Step 4: Find datasheet
        wx.CallAfter(self.steps_label.SetLabel, strings.STEPS_LABEL_4_FINDING)
        self.pdf_path = operations.find_datasheet(raw_image_text, processed_image_text)
        wx.CallAfter(self.gauge.SetValue, 100)
        wx.CallAfter(self.panel.Layout)

        # Done
        wx.CallAfter(self.steps_label.SetLabel, strings.STEPS_LABEL_5_DONE)
        wx.CallAfter(self.result_label.SetLabel, f"{strings.RESULT_LABEL_DONE}{self.pdf_path.stem}")
        wx.CallAfter(self.open_datasheet_btn.Enable)
        wx.CallAfter(self.panel.Layout)

    def on_open_datasheet_btn_clicked(self, _: wx.Event) -> None:
        """
        Open the datasheet when the "Open Datasheet" button is clicked.
        """
        if self.pdf_path is not None:
            operations.open_datasheet(self.pdf_path)
