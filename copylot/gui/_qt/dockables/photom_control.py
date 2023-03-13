from qtpy.QtWidgets import (
    QWidget,
    QApplication,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QGridLayout,
    QSlider,
    QTabWidget,
)
from qtpy.QtCore import Qt, Signal, Slot
import time

from copylot.gui._qt.job_runners.worker import Worker

# from widgets.utils.affinetransform import AffineTransform


class PhotomControlDockWidget(QWidget):
    # TODO: Need to define the threads needed
    # thread_launching = Signal()

    def __init__(self, parent, threadpool):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.threadpool = threadpool
        self.state_tracker = False
        self.tabmanager = TabManager(self)
        # Set the main Layout
        self.main_layout = QGridLayout()

        # Photom overlay window
        self.window1 = None
        # Buttons
        self.sl_opacity = QSlider(Qt.Horizontal)
        self.sl_opacity.setRange(0, 100)
        # self.sl_opacity.setValue(int(self.window1.opacity * 100))
        self.opacity_indicator = QLabel(f'Opacity {0.0 * 100} %')

        # Set the Widget Layout
        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.sl_opacity, 0, 0)
        self.layout.addWidget(self.opacity_indicator, 0, 1)

        # Tab Manager
        self.layout.addWidget(self.tabmanager, 3, 0, 1, 3)
        # def handle_photom_launch(self):
        #     self.state_tracker = not self.state_tracker
        #     if self.state_tracker:
        #         self.setStyleSheet("background-color: red;")
        #     else:
        #         scshot_box = QGroupBox('Screen shot')
        #         scshot_box.setStyleSheet('font-size: 14pt')
        #         scshot_box.layout = QGridLayout()
        #         scshot_box.layout.addWidget(self.le_scshot, 0, 0)
        #         scshot_box.layout.addWidget(self.pb_scshot, 0, 1)
        #         scshot_box.setLayout(scshot_box.layout)
        self.setLayout(self.layout)

        @property
        def parameters(self):
            raise NotImplementedError("parameters not yet implemented")

class TabManager(QTabWidget):
    """
    A TabManager that manages multiple tabs.

    """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        # self.buttonSize = (200, 100)

        # Add contents for each tab
        self.laser_cali = LaserPositionCalibration(self)
        self.pattern_ctrl = PatternControl(self)
        self.multi_pattern = MultiPatternControl(self)

        # Add tabs
        self.addTab(self.laser_cali, 'Calibration')
        self.addTab(self.pattern_ctrl, 'Single Scan')
        self.addTab(self.multi_pattern, 'Multi Scans')

    def update_current_laser(self, laser_idx):
        """
        To update current laser selection in the laser selection boxes.
        Since the laser selection box on each tab is an independent widget, laser selection update has to be controlled
        uniquely from tab manager.
        :param laser_idx: index of laser
        """
        self.parent.current_laser = laser_idx
        for i in range(self.count()):
            if hasattr(self.widget(i), 'laser_selection_box'):
                self.widget(i).laser_selection_box.laser_selection.buttons()[self.parent.current_laser].setChecked(True)

    def update_calibration_status(self):
        """
        To update calibration status in the laser selection boxes.
        Since the laser selection box on each tab is an independent widget, laser calibration status update has to be
        controlled uniquely from tab manager.
        """
        for i in range(self.count()):
            if hasattr(self.widget(i), 'laser_selection_box'):
                boxgrid = self.widget(i).laser_selection_box.laser_box_grid
                for laser_num in range(2):
                    if self.parent.transform_list[laser_num].affmatrix is None:
                        boxgrid.itemAtPosition(laser_num, 1).widget().setText('Not calibrated')
                        boxgrid.itemAtPosition(laser_num, 1).widget().setStyleSheet('color: gray')
                    else:
                        boxgrid.itemAtPosition(laser_num, 1).widget().setText('Calibration Done!')
                        boxgrid.itemAtPosition(laser_num, 1).widget().setStyleSheet('color: green')

    def update_scan_shape(self, ind):
        self.parent.current_scan_shape = ind
        self.pattern_ctrl.bg_pattern_selection.buttons()[ind].setChecked(True)
        self.multi_pattern.bg_indiv.bg_shape.buttons()[ind].setChecked(True)

    def update_scan_pattern(self, ind):
        self.parent.current_scan_pattern = ind
        unit = self.pattern_ctrl.get_pattern_unit()
        unit.bg_scan.buttons()[ind].setChecked(True)
        self.multi_pattern.bg_indiv.bg_scan.buttons()[ind].setChecked(True)





