import sys
import os
import time
import webbrowser
from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio import __version__, REPO_DIR, MachineState
from nupic_studio.simulation import Simulation
from nupic_studio.htm import MAX_PREVIOUS_STEPS, MAX_PREVIOUS_STEPS_WITH_INFERENCE
from nupic_studio.ui import ICON, Global, State, DEFAULT_CONFIGURATION
from nupic_studio.ui.architecture_window import ArchitectureWindow
from nupic_studio.ui.node_information_window import NodeInformationWindow
from nupic_studio.ui.simulation_window import SimulationWindow
from nupic_studio.ui.output_window import OutputWindow
from nupic_studio.ui.project_properties_window import ProjectPropertiesWindow


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        """
        Initializes a new instance of this class.
        """
        QtWidgets.QMainWindow.__init__(self)
        self.state = State.NO_STARTED
        self.paused = False
        self.simulation = None
        self.pending_project_changes = False
        self.num_steps_pending = 0
        self.loadConfig()
        self.initUI()

    def initUI(self):

        # update_timer
        self.update_timer = QtCore.QTimer(self)
        self.update_timer.timeout.connect(self.update)

        # menu_file_new
        self.menu_file_new = QtWidgets.QAction(self)
        self.menu_file_new.setText("&New Project")
        self.menu_file_new.setShortcut('Ctrl+N')
        self.menu_file_new.triggered.connect(self.newProject)

        # menu_file_open
        self.menu_file_open = QtWidgets.QAction(self)
        self.menu_file_open.setText("&Open Project")
        self.menu_file_open.setShortcut('Ctrl+O')
        self.menu_file_open.triggered.connect(self.openProject)

        # menu_file_save
        self.menu_file_save = QtWidgets.QAction(self)
        self.menu_file_save.setText("&Save Project")
        self.menu_file_save.setShortcut('Ctrl+S')
        self.menu_file_save.triggered.connect(self.saveProject)

        # menu_file_exit
        self.menu_file_exit = QtWidgets.QAction(self)
        self.menu_file_exit.setText("&Exit")
        self.menu_file_exit.setShortcut('Ctrl+Q')
        self.menu_file_exit.triggered.connect(self.menuFileExit_click)

        # menu_file
        self.menu_file = QtWidgets.QMenu()
        self.menu_file.addAction(self.menu_file_new)
        self.menu_file.addAction(self.menu_file_open)
        self.menu_file.addAction(self.menu_file_save)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.menu_file_exit)
        self.menu_file.setTitle("&File")

        # menu_view_architecture
        self.menu_view_architecture = QtWidgets.QAction(self)
        self.menu_view_architecture.setText("&Network Architecture")
        self.menu_view_architecture.triggered.connect(self.menuViewArchitecture_click)

        # menu_view_simulation
        self.menu_view_simulation = QtWidgets.QAction(self)
        self.menu_view_simulation.setText("&Simulation")
        self.menu_view_simulation.triggered.connect(self.menuViewSimulation_click)

        # menu_view_node_information
        self.menu_view_node_information = QtWidgets.QAction(self)
        self.menu_view_node_information.setText("Node &Information")
        self.menu_view_node_information.triggered.connect(self.menuViewNodeInformation_click)

        # menu_view_output
        self.menu_view_output = QtWidgets.QAction(self)
        self.menu_view_output.setText("&Output")
        self.menu_view_output.triggered.connect(self.menuViewOutput_click)

        # menu_view_tool_windows
        self.menu_view_tool_windows = QtWidgets.QMenu()
        self.menu_view_tool_windows.addAction(self.menu_view_architecture)
        self.menu_view_tool_windows.addAction(self.menu_view_node_information)
        self.menu_view_tool_windows.addAction(self.menu_view_simulation)
        self.menu_view_tool_windows.addAction(self.menu_view_output)
        self.menu_view_tool_windows.setTitle("Tool &Windows")

        # menu_view
        self.menu_view = QtWidgets.QMenu()
        self.menu_view.addMenu(self.menu_view_tool_windows)
        self.menu_view.setTitle("&View")

        # menu_edit
        self.menu_edit = QtWidgets.QMenu()
        self.menu_edit.setTitle("&Edit")

        # menu_project_properties
        self.menu_project_properties = QtWidgets.QAction(self)
        self.menu_project_properties.setText("Properties...")
        self.menu_project_properties.triggered.connect(self.menuProjectProperties_click)

        # menu_project
        self.menu_project = QtWidgets.QMenu()
        self.menu_project.addAction(self.menu_project_properties)
        self.menu_project.setTitle("&Project")

        # menu_tools
        self.menu_tools = QtWidgets.QMenu()
        self.menu_tools.setTitle("&Tools")

        # menu_user_wiki
        self.menu_user_wiki = QtWidgets.QAction(self)
        self.menu_user_wiki.setText("User Wiki")
        self.menu_user_wiki.triggered.connect(self.menuUserWiki_click)

        # menu_go_to_website
        self.menu_go_to_website = QtWidgets.QAction(self)
        self.menu_go_to_website.setText("Project Website")
        self.menu_go_to_website.triggered.connect(self.menuGoToWebsite_click)

        # menu_about
        self.menu_about = QtWidgets.QAction(self)
        self.menu_about.setText("About")
        self.menu_about.triggered.connect(self.menuAbout_click)

        # menu_help
        self.menu_help = QtWidgets.QMenu()
        self.menu_help.addAction(self.menu_user_wiki)
        self.menu_help.addAction(self.menu_go_to_website)
        self.menu_help.addAction(self.menu_about)
        self.menu_help.setTitle("&Help")

        # menu_main
        self.menu_main = self.menuBar()
        self.menu_main.addMenu(self.menu_file)
        self.menu_main.addMenu(self.menu_view)
        self.menu_main.addMenu(self.menu_project)
        self.menu_main.addMenu(self.menu_help)

        # button_init
        self.button_init = QtWidgets.QAction(self)
        self.button_init.setEnabled(False)
        self.button_init.setIcon(QtGui.QIcon(os.path.join(REPO_DIR, 'images', 'button_initialize.png')))
        self.button_init.setToolTip("Initialize simulation")
        self.button_init.triggered.connect(self.buttonInit_click)

        # button_step
        self.button_step = QtWidgets.QAction(self)
        self.button_step.setEnabled(False)
        self.button_step.setIcon(QtGui.QIcon(os.path.join(REPO_DIR, 'images', 'button_step.png')))
        self.button_step.setToolTip("Forward one time step")
        self.button_step.triggered.connect(self.buttonStep_click)

        # button_multiple_steps
        self.button_multiple_steps = QtWidgets.QAction(self)
        self.button_multiple_steps.setEnabled(False)
        self.button_multiple_steps.setIcon(QtGui.QIcon(os.path.join(REPO_DIR, 'images', 'button_multiple_steps.png')))
        self.button_multiple_steps.setToolTip("Forward a specific number of time steps")
        self.button_multiple_steps.triggered.connect(self.buttonMultipleSteps_click)

        # button_stop
        self.button_stop = QtWidgets.QAction(self)
        self.button_stop.setEnabled(False)
        self.button_stop.setIcon(QtGui.QIcon(os.path.join(REPO_DIR, 'images', 'button_stop.png')))
        self.button_stop.setToolTip("Stop simulation")
        self.button_stop.triggered.connect(self.buttonStop_click)

        # text_box_step
        self.text_box_step = QtWidgets.QLineEdit()
        self.text_box_step.setEnabled(False)
        self.text_box_step.setAlignment(QtCore.Qt.AlignRight)
        self.text_box_step.setFixedSize(QtCore.QSize(80, 20))

        # slider_step
        self.slider_step = QtWidgets.QSlider()
        self.slider_step.setEnabled(False)
        self.slider_step.setOrientation(QtCore.Qt.Horizontal)
        self.slider_step.setSingleStep(1)
        self.slider_step.setRange(0, MAX_PREVIOUS_STEPS - 1)
        self.slider_step.setValue(MAX_PREVIOUS_STEPS - 1)
        self.slider_step.valueChanged.connect(self.sliderStep_valueChanged)

        # tool_bar
        self.tool_bar = QtWidgets.QToolBar()
        self.tool_bar.addAction(self.button_init)
        self.tool_bar.addAction(self.button_step)
        self.tool_bar.addAction(self.button_multiple_steps)
        self.tool_bar.addAction(self.button_stop)
        self.tool_bar.addWidget(self.text_box_step)
        self.tool_bar.addWidget(self.slider_step)

        # output_window
        self.architecture_window = ArchitectureWindow(self)
        self.architecture_window.setFocusPolicy(QtCore.Qt.StrongFocus)

        # dock_architecture
        self.dock_architecture = QtWidgets.QDockWidget()
        self.dock_architecture.setWidget(self.architecture_window)
        self.dock_architecture.setWindowTitle(self.architecture_window.windowTitle())
        self.dock_architecture.setObjectName(self.architecture_window.windowTitle())

        # simulation_window
        self.simulation_window = SimulationWindow(self)
        self.simulation_window.setFocusPolicy(QtCore.Qt.StrongFocus)

        # dock_simulation
        self.dock_simulation = QtWidgets.QDockWidget()
        self.dock_simulation.setWidget(self.simulation_window)
        self.dock_simulation.setWindowTitle(self.simulation_window.windowTitle())
        self.dock_simulation.setObjectName(self.simulation_window.windowTitle())

        # node_information_window
        self.node_information_window = NodeInformationWindow(self)
        self.node_information_window.setFocusPolicy(QtCore.Qt.StrongFocus)

        # dock_node_information
        self.dock_node_information = QtWidgets.QDockWidget()
        self.dock_node_information.setWidget(self.node_information_window)
        self.dock_node_information.setWindowTitle(self.node_information_window.windowTitle())
        self.dock_node_information.setObjectName(self.node_information_window.windowTitle())

        # output_window
        self.output_window = OutputWindow()
        self.output_window.setFocusPolicy(QtCore.Qt.StrongFocus)

        # dock_output
        self.dock_output = QtWidgets.QDockWidget()
        self.dock_output.setWidget(self.output_window)
        self.dock_output.setWindowTitle(self.output_window.windowTitle())
        self.dock_output.setObjectName(self.output_window.windowTitle())

        # self
        self.addToolBar(self.tool_bar)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock_simulation)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock_output)
        self.tabifyDockWidget(self.dock_output, self.dock_simulation)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_architecture)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_node_information)
        self.tabifyDockWidget(self.dock_node_information, self.dock_architecture)
        #self.setCentralWidget(self.dock_simulation)
        self.setWindowTitle("NuPIC Studio")
        self.setWindowIcon(ICON)

    def cleanUp(self):
        """
        Prepare UI to load a new configuration.
        """
        self.enableSimulationButtons(False)
        self.enableSteeringButtons(False)

        # Update architecture controls
        self.architecture_window.design_panel.top_region = Global.project.network.nodes[0]
        self.architecture_window.design_panel.selected_node = Global.project.network.nodes[0]
        self.architecture_window.design_panel.repaint()
        self.architecture_window.updateCode()

        # Reset the controls
        self.clearControls()

    def enableSimulationButtons(self, enable):
        """
        Enables or disables controls related to simulation.
        """
        self.button_init.setEnabled(not enable)
        if not enable:
            self.text_box_step.setText("")
            self.slider_step.setEnabled(False)
            self.slider_step.setValue(self.slider_step.maximum())

    def enableSteeringButtons(self, enable):
        """
        Enables or disables buttons in toolbar.
        """
        self.button_step.setEnabled(enable)
        self.button_multiple_steps.setEnabled(enable)
        self.button_stop.setEnabled(enable)

    def clearControls(self):
        """
        Reset the controls.
        """
        self.simulation_window.clearControls()
        self.output_window.clearControls()
        self.node_information_window.clearControls()

    def update(self):
        if self.state == State.SIMULATING:
            self.simulation.taskMgr.step()
            self.simulation_window.update()

    def getProjectPath(self):
        return os.path.dirname(Global.project.file_name)

    def getRecordPath(self):
        return os.path.join(self.getProjectPath(), "record")

    def refreshControls(self):
        """
        Refresh controls for each time step.
        """
        if self.state == State.SIMULATING:
            max_time = Global.curr_step + 1
            sel_step = max_time - (self.slider_step.maximum() - self.slider_step.value())
            self.text_box_step.setText(str(sel_step) + "/" + str(max_time))
        else:
            self.text_box_step.setText("")
        if self.dock_simulation.isVisible():
            self.simulation_window.refreshControls()
        if self.dock_node_information.isVisible():
            self.node_information_window.refreshControls()

    def loadConfig(self):
        """
        Loads the content from XML file to config the program.
        """
        file_name = os.path.join(REPO_DIR, "config.json")
        try:
            self.config = eval(open(file_name, 'r').read())
        except:
            QtWidgets.QMessageBox.warning(None, "Warning", "Cannot read the config file (" + file_name + ")! Configuration was reseted!", QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Default, QtWidgets.QMessageBox.NoButton)
            self.config = DEFAULT_CONFIGURATION

    def saveConfig(self):
        """
        Saves the content from current program's configuration.
        """
        file_name = os.path.join(REPO_DIR, "config.json")
        open(file_name, 'w').write(str(self.config))

    def markProjectChanges(self, has_changes):
        """
        Provides an UI reaction to any project changes or a new or saved unchanged project.
        """
        self.pending_project_changes = has_changes
        self.menu_file_save.setEnabled(has_changes)

    def checkCurrentConfigChanges(self):
        """
        Checks if the current file has changed.
        """
        result = QtWidgets.QMessageBox.No

        # If changes happened, ask to user if he wish saves them
        if self.pending_project_changes:
            result = QtWidgets.QMessageBox.question(self, "Question",
                                                "Current project has changed. Do you want save these changes?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
            if result == QtWidgets.QMessageBox.Yes:
                self.saveProject()

        return result

    def newProject(self):
        """
        Creates a new project.
        """

        # Check if the current project has changed before continue operation
        if self.checkCurrentConfigChanges() != QtWidgets.QMessageBox.Cancel:
            # Create new project
            Global.project.new()

            # Initialize project state
            self.setWindowTitle(Global.project.name + " - NuPIC Studio")
            self.markProjectChanges(False)
            self.cleanUp()

            return True

        return False

    def openProject(self):
        """
        Open an existing project
        """

        # Check if the current project has changed before continue operation
        if self.checkCurrentConfigChanges() != QtWidgets.QMessageBox.Cancel:

            # Ask user for an existing file
            selected_file = QtWidgets.QFileDialog().getOpenFileName(self, "Open Project", os.path.join(REPO_DIR, 'projects'), "NuPIC project files (*.nuproj)")[0]

            # If file exists, continue operation
            if selected_file != '':
                # Open the selected project
                Global.project.open(selected_file)

                # Initialize project state
                self.setWindowTitle(Global.project.name + " - [" + Global.project.file_name + "] - NuPIC Studio")
                self.markProjectChanges(False)
                self.cleanUp()

                return True

        return False

    def saveProject(self):
        """
        Save the current project
        """

        # If current project is new, ask user for valid file
        file_name = Global.project.file_name
        if file_name == '':
            # Ask user for valid file
            selected_file = QtWidgets.QFileDialog().getSaveFileName(self, "Save Project", os.path.join(REPO_DIR, 'projects'), "NuPIC project files (*.nuproj)")[0]

            # If file exists, continue operation
            if selected_file != '':
                file_name = selected_file

        # If file is Ok, continue operation
        if file_name != '':
            # Save to the selected location
            Global.project.save(file_name)

            # Initialize project state
            self.setWindowTitle(Global.project.name + " - [" + Global.project.file_name + "] - NuPIC Studio")
            self.markProjectChanges(False)

            return True

        return False

    def stopSimulation(self):

        # Destroy everything
        destroy_world = True if self.state == State.SIMULATING else False
        self.state = State.STOPPED
        self.paused = False
        self.update_timer.stop()
        if destroy_world:
            self.simulation.destroy()

        # Disable relevant buttons to reset
        self.enableSteeringButtons(False)
        self.enableSimulationButtons(False)

        # Reset controls
        self.clearControls()

    def isRunning(self):
        return self.state == State.SIMULATING or self.state == State.PLAYBACKING

    def closeEvent(self, event):
        if self.checkCurrentConfigChanges() == QtWidgets.QMessageBox.Cancel:
            event.ignore()
        else:
            if self.button_stop.isEnabled():
                self.stopSimulation()
            sys.exit()

    def menuFileExit_click(self, event):
        self.close()

    def menuProjectProperties_click(self, event):
        # Open Project properties window
        project_properties_window = ProjectPropertiesWindow()
        project_properties_window.setControlsValues()
        dialog_result = project_properties_window.exec_()
        if dialog_result == QtWidgets.QDialog.Accepted:
            self.markProjectChanges(True)

    def menuViewArchitecture_click(self, event):
        self.dock_architecture.show()

    def menuViewSimulation_click(self, event):
        self.dock_simulation.show()
        self.simulation_window.refreshControls()

    def menuViewNodeInformation_click(self, event):
        self.dock_node_information.show()
        self.node_information_window.refreshControls()

    def menuViewOutput_click(self, event):
        self.dock_output.show()

    def menuUserWiki_click(self, event):
        webbrowser.open('https://github.com/nupic-community/nupic.studio/wiki')

    def menuGoToWebsite_click(self, event):
        webbrowser.open('https://github.com/nupic-community/nupic.studio')

    def menuAbout_click(self, event):
        QtWidgets.QMessageBox.information(self, "Information", "v. " + __version__ + "\nGet more info at our home page.")

    def buttonInit_click(self, event):
        """
        Initializes the HTM-Network by creating the htm-controller to connect to events database
        """

        # Initialize the network starting from top region.
        start_time = time.time()
        end_time = time.time()
        initialized = Global.project.network.initialize()

        if initialized:
            self.state = State.SIMULATING

            # Create a simulation
            #TODO: self.simulation = Simulation(self.project, self.getProjectPath())
            self.simulation = Simulation(None, None)

            # Initialize time steps parameters
            Global.curr_step = 0
            Global.sel_step = 0
            Global.time_steps_predictions_chart = MachineState(0, MAX_PREVIOUS_STEPS_WITH_INFERENCE)

            self.output_window.addText("Initialization: " + "{0:.3f}".format(end_time - start_time) + " secs")
            self.output_window.addText("")
            self.output_window.addText("Step\tTime (secs)\tAccuracy (%)")

            # Perfoms actions related to time step progression.
            start_time = time.time()
            Global.project.network.nextStep()
            Global.project.network.calculateStatistics()
            end_time = time.time()
            self.output_window.addText(str(Global.curr_step + 1) + "\t{0:.3f}".format(end_time - start_time) + "\t{0:.3f}".format(Global.project.network.stats_precision_rate))

            # Disable relevant buttons:
            self.enableSteeringButtons(True)
            self.enableSimulationButtons(True)

            # Update controls
            self.simulation_window.viewer_3d.initializeControls(Global.project.network.nodes[0])
            self.refreshControls()

            self.update_timer.setInterval(1)
            self.update_timer.start()

    def buttonStep_click(self, event):
        """
        Performs a single simulation step.
        """

        # Update time steps parameters
        Global.curr_step += 1
        if Global.curr_step >= (MAX_PREVIOUS_STEPS - 1):
            self.slider_step.setEnabled(True)
        Global.sel_step = self.slider_step.maximum() - self.slider_step.value()
        Global.time_steps_predictions_chart.rotate()
        Global.time_steps_predictions_chart.setForCurrStep(Global.curr_step)

        # Perfoms actions related to time step progression.
        start_time = time.time()
        Global.project.network.nextStep()
        Global.project.network.calculateStatistics()
        end_time = time.time()
        self.output_window.addText(str(Global.curr_step + 1) + "\t{0:.3f}".format(end_time - start_time) + "\t{0:.3f}".format(Global.project.network.stats_precision_rate))

        # Update controls
        self.refreshControls()

    def buttonMultipleSteps_click(self, event):
        """
        Performs full HTM simulation.
        """

        # Get number of steps to perform simulation
        self.num_steps_pending = -1
        entered_integer, ok = QtWidgets.QInputDialog.getInt(self, "Input Dialog", "Enter number of steps:")
        if ok:
            if entered_integer < 2:
                QtWidgets.QMessageBox.warning(self, "Warning", "Invalid value specified!")
            else:
                self.num_steps_pending = entered_integer

        while self.num_steps_pending > 0:
            self.buttonStep_click(event)
            self.num_steps_pending -= 1

    def buttonStop_click(self, event):
        # If multiple steps processing is running just stop the loop
        # otherwise, ask user to stop the simulation
        if self.num_steps_pending > 0:
            self.num_steps_pending = 0
        else:
            dialog_result = QtWidgets.QMessageBox.question(self, "Question", "Current simulation (learning) will stop!\r\nDo you want proceed?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if dialog_result == QtWidgets.QMessageBox.Yes:
                self.stopSimulation()

    def sliderStep_valueChanged(self, value):
        Global.sel_step = Global.sel_step = self.slider_step.maximum() - self.slider_step.value()
        self.refreshControls()
