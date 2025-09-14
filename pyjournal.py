# CS50P Final Project
# Making a basic python application using PyQt6 for a journaling app where users can save and display their entries, edit
# or create new entries and delete them.
# Additional functionalities include a dynamic font size updating system and a dark theme for better visibility.

# Importing necessary libraries and classes from said libraries
import sys
import os
from PyQt6.QtWidgets import (QApplication,QMainWindow, QSplitter, QTextEdit, QLineEdit, QListWidget, QWidget,
                             QVBoxLayout, QLabel, QHBoxLayout, QPushButton)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont
from datetime import date

# Creating a class for the main window using the parent class QMainWindow
class MainWindow(QMainWindow):

    # Setting the theme by using PyQt6's CSS-like abilities (QSS)
    theme = """
        QWidget { background-color: #1e1e1e; color: white; }
        QMainWindow { background-color: #141617; }
        QListWidget { background-color: #2a2a2a; border: 1px solid #3c3c3c; border-radius: 5px; }
        QListWidget::item:hover { background-color: #3e3e3e; }
        QListWidget::item:selected { background-color: #007acc; color: #ffffff; }
        QLabel { font-weight: bold; color: white; background-color: #2a2a2a; border: 1px solid #3c3c3c; border-radius: 5px; padding: 5px; }
        QLineEdit, QTextEdit { color: white; selection-background-color: #007acc;
        selection-color: white; background-color: #2a2a2a; border: 1px solid #3c3c3c; border-radius: 5px; padding: 5px; }
        QPushButton { background-color: #3c3c3c; border: 1px solid #555555; padding: 8px; border-radius: 5px; }
        QSplitter::handle { background-color: #3c3c3c; }
            """
    # Creating a folder to save entries incase it doesn't exist
    # (Opening app for the first time or deletion of folder off of the disk)
    if not os.path.exists("entries/"):
        os.makedirs("entries/")
    
    # Initializing the window
    def __init__(self):
        super().__init__()
        # Setting up the window
        self.setWindowTitle("PyJournal")
        self.setWindowIcon(QIcon("pyjournal.png"))
        self.setStyleSheet(MainWindow.theme)
        self.setGeometry(440, 200, 1000, 600)
        # Calling the initUI() method
        self.initUI()
    
    # Initializing the UI by calling the necessary methods
    def initUI(self):
        self.leftLayout()
        self.rightLayout()
        self.splitter()

    # Creating a splitter to display the files and the entries
    def splitter(self):
        # Creating a horizontal splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        # Adding the left and right panels from the layout methods
        self.splitter.addWidget(self.leftPaneContainer)
        self.splitter.addWidget(self.rightPaneContainer)
        # Setting the size of the panels
        self.splitter.setSizes([250, 750])
        
        # Updating font sizes when splitter is moved
        self.splitter.splitterMoved.connect(self.updateFontSizes)
        # Setting the splitter
        self.setCentralWidget(self.splitter)
    
    # Creating the left panel containing the title, date and list of files
    def leftLayout(self):
        # Creating the left panel
        self.leftPaneContainer = QWidget()
        # Storing the contents in a vertical layout
        leftPaneLayout = QVBoxLayout()
        
        # Storing the title and date in a horizontal layout
        titleLayout = QHBoxLayout()
        # Creating the appLabel and dateLabel
        self.appLabel = QLabel("PyJournal")
        self.appLabel.setStyleSheet("color: white;")
        self.dateLabel = QLabel(date.today().strftime("%d/%m/%Y"))
        self.dateLabel.setStyleSheet("color: white;")
        # Adding both to the titleLayout
        titleLayout.addWidget(self.appLabel)
        titleLayout.addWidget(self.dateLabel)

        # Calling the entryList() function to initiate the listWidget
        self.entryList()
        # Displaying the contents of the widget clicked
        self.listWidget.currentItemChanged.connect(self.displayContents)

        # Adding the layout and listWidget to the panel
        leftPaneLayout.addLayout(titleLayout)
        leftPaneLayout.addWidget(self.listWidget)
        self.leftPaneContainer.setLayout(leftPaneLayout)

    # Creating the listWidget
    def entryList(self):
        # Creating the listWidget using the QListWidget class
        self.listWidget = QListWidget()
        
        # Getting all the text files in the folder
        textFiles = sorted(os.listdir("entries/"))

        # Creating a file if no file exists
        if len(textFiles) == 0:
            with open("entries/new entry 1", "w") as entry1:
                entry1.write("type here to start journaling." \
                            "\n\n     click on edit to start writing," \
                            "\n     click on save to save the entry," \
                            "\n     click on delete twice to delete a entry" \
                            "\n     click on new to create a new entry")
        textFiles = sorted(os.listdir("entries/"))
        # Adding all files to the widget
        for file in textFiles:
            self.listWidget.addItem(f"{file}")

    # Creating the right panel containing the name and content of files along with the action buttons
    def rightLayout(self):
        # Creating the right panel
        self.rightPaneContainer = QWidget()
        # Storing the contents in a vertical layout
        rightPaneLayout = QVBoxLayout()

        # Creating the entryTitle and entry content(entryEditor) variables using QLine and QTestEdit
        self.entryTitle = QLineEdit()
        self.entryTitle.setPlaceholderText("Title of Entry")
        self.entryEditor = QTextEdit()
        self.entryEditor.setPlaceholderText("Entry")

        # Creating the action button container in a horizontal layout for our four buttons
        self.actionButtonContainer = QWidget()
        actionButtonLayout = QHBoxLayout()

        # Creating the Save, Edit, Delete and New buttons and connecting the clicked events to their respective methods
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.saveEntry)

        self.editButton = QPushButton("Edit")
        self.editButton.clicked.connect(self.editEntry)

        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteEntry)

        self.newButton = QPushButton("New")
        self.newButton.clicked.connect(self.newEntry)

        # Addding all the widgets and layouts to the panel
        actionButtonLayout.addWidget(self.saveButton)
        actionButtonLayout.addWidget(self.editButton)
        actionButtonLayout.addWidget(self.deleteButton)
        actionButtonLayout.addWidget(self.newButton)
        self.actionButtonContainer.setLayout(actionButtonLayout)

        rightPaneLayout.addWidget(self.entryTitle)
        rightPaneLayout.addWidget(self.entryEditor)
        rightPaneLayout.addWidget(self.actionButtonContainer)
        self.rightPaneContainer.setLayout(rightPaneLayout)

    # Method to create a new file
    def newEntry(self):
        # Checks the entry Name and if it exists or not in a while loop
        i = 1
        while True:
            entryName = f"new entry {i}"
            # If file doesn't exist, creates it
            if not os.path.exists(f"entries/{entryName}"):
                break
            i += 1
        
        # Adds the new file to a sorted listWidget
        self.listWidget.addItem(entryName)
        self.listWidget.sortItems()
        # Adds a statement to the newly created file
        with open(f"entries/{entryName}", "w") as entryX:
            entryX.write(f"start writing in entry {i}")
        # Opens the newly created file in the listWidget
        if item:= self.listWidget.findItems(entryName, Qt.MatchFlag.MatchExactly):
            self.listWidget.setCurrentItem(item[0])
        # Enable the entry
        self.checkEntry(True)
    
    # Method to enable and disable the input from user
    def checkEntry(self, booleanParam):
        if booleanParam is True:
            self.entryTitle.setEnabled(True)
            self.entryEditor.setEnabled(True)
        else:
            self.entryTitle.setEnabled(False)
            self.entryEditor.setEnabled(False)

    # Method to save the current file
    def saveEntry(self):
        # Sets the item
        item = self.listWidget.currentItem()
        # If item not selected, does nothing
        if not item:
            return
        # Checks for the title inputted by the user
        enteredName = self.entryTitle.text().strip()
        # Variable to check for directory of the file
        directory = f"entries/{enteredName}"
        # If blank name, assings name: "unnamed file"
        if not enteredName:
            enteredName = "unnamed file"
            directory = f"entries/{enteredName}"
        # Checks if file has the same name as the current file
        if enteredName != item.text():
            # If another named file exists, prompts user to change file name and returns
            if os.path.exists(directory):
                self.entryTitle.setText(f"{enteredName} already exists")
                return
            # Else, renames the current file and sets title to current name
            os.rename(f"entries/{item.text()}", directory)
            item.setText(enteredName)
            self.entryTitle.setText(enteredName)
        
        # Trying to check if user inputted file name is valid
        try:
            # Writes the new and edited input over the file
            with open(f"{directory}", "w") as savedFile:
                savedFile.write(self.entryEditor.toPlainText())
        # If OSError occurs, tell user that file name isn't valid
        except OSError:
            self.entryTitle.setText("Invalid file name")
        
        # Sorts the list an disables the input untis edit is clicked again
        self.listWidget.sortItems()
        self.checkEntry(False)

    # Method to edit the current file
    def editEntry(self):
        # Sets the item
        item = self.listWidget.currentItem()
        # If item not selected, does nothing
        if not item:
            return
        # Sets editing mode
        self.checkEntry(True)

    # Method to delete the current file
    def deleteEntry(self):
        # Sets the item
        item = self.listWidget.currentItem()
        # If item not selected, does nothing
        if not item:
            return
        
        # Checks for deletion
        if self.deleteButton.text() != "Confirm Delete":
            # Asks user to confirm deletion by changing the button
            self.deleteButton.setText("Confirm Delete")
            self.deleteButton.setStyleSheet("background-color: red; color: white; border-radius: 5px;")
            # Timer to change button, returns if user doesn't click again
            QTimer.singleShot(1500, lambda: (self.deleteButton.setText("Delete"), self.deleteButton.setStyleSheet("background-color: #3c3c3c; border: 1px solid #555555; border-radius: 5px;")))
            return
        
        # Checks if file exits then deletes it and removes it from the listWidget
        if os.path.exists(f"entries/{item.text()}"):
            os.remove(f"entries/{item.text()}")
            self.listWidget.takeItem(self.listWidget.row(item))
        
        # If no files exist, sets placeholders to prompt user to create a new file
        if self.listWidget.count() == 0:
            self.entryEditor.clear()
            self.entryTitle.clear()
            self.entryTitle.setPlaceholderText("Create new file to start journaling")
            self.entryEditor.setPlaceholderText("...")

    # Method to display current file's contents
    def displayContents(self, block):
        # If no file is selected, returns
        if block is None:
            return
        
        # Trying to display the contents of the file
        try:
            # Setting the entryTitle and entryEditor to the name of the file and its contents respectively
            textFile = f"entries/{block.text()}"
            with open(textFile) as f:
                content = f.read()
            self.entryTitle.setText(block.text())
            self.entryEditor.setText(content)
            # Enables the entry when file is selected
            self.checkEntry(True)
            # Resets the delete button if user clicks on delete but changes the file
            self.deleteButton.setText("Delete")
            self.deleteButton.setStyleSheet("background-color: #3c3c3c; border: 1px solid #555555; border-radius: 5px;")
        # Handles the FileNotFoundError if file is misplaced by informing the user
        except FileNotFoundError:
            self.entryTitle.setText("File Not Found")
            self.entryEditor.setText("Error in file placement")

    # Method to dynamically update the font size when splitter is moved
    def updateFontSizes(self):
        # Getting the current widths of both panels
        rightPaneWidth = self.rightPaneContainer.width()
        leftPaneWidth = self.leftPaneContainer.width()

        # Setting the sizes of everything to change
        titleSize = rightPaneWidth / 25
        entrySize = rightPaneWidth / 35
        buttonSize = rightPaneWidth / 50
        appLabelSize = leftPaneWidth / 20
        dateLabelSize = leftPaneWidth / 20
        listWidgetSize = leftPaneWidth / 25

        # Dynamically changing the sizes on a set range
        titleSize = max(15, min(titleSize, 25) )
        entrySize = max(10, min(entrySize, 22))
        buttonSize = max(10, min(buttonSize, 20))
        listWidgetSize = max(15, min(listWidgetSize, 50) )
        appLabelSize = max(15, min(appLabelSize, 25) )
        dateLabelSize = max(15, min(dateLabelSize, 20) )

        # Finally updating the font sizes for each and every font
        titleFont = QFont()
        titleFont.setPointSize(int(titleSize))
        self.entryTitle.setFont(titleFont)

        entryFont = QFont()
        entryFont.setPointSize(int(entrySize))
        self.entryEditor.setFont(entryFont)

        buttonFont = QFont()
        buttonFont.setPointSize(int(buttonSize))
        for _ in [self.saveButton, self.editButton, self.deleteButton, self.newButton]:
            _.setFont(buttonFont)

        listWidgetFont = QFont()
        listWidgetFont.setPointSize(int(listWidgetSize))
        self.listWidget.setFont(listWidgetFont)

        appLabelFont = QFont()
        appLabelFont.setPointSize(int(appLabelSize))
        self.appLabel.setFont(appLabelFont)

        dateLabelFont = QFont()
        dateLabelFont.setPointSize(int(dateLabelSize))
        self.dateLabel.setFont(dateLabelFont)

    # Checking for resizeEvents by using a super-class automatically
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateFontSizes()

# Creating a main() function
def main():
    # Creating an instance of the window
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.updateFontSizes()
    app.exec()

# Executing the file
if __name__ == "__main__":
    main()