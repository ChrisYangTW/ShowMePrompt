# Show Me Prompt
A simple program for displaying and editing an image's prompts.

![sample.png](examples/sample2_v0_1_4.png)

## Installation
Use the git clone command to clone the repository.
```
git clone https://github.com/ChrisYangTW/ShowMePrompt.git
```
Switch to the folder where you have placed the repository,
and install the necessary dependencies. (Recommend using a virtual environment)
```
pip3 install -r requirements.txt
```
Finally, run the main.py
```
python3 main.py
```

## Usage
![usage](examples/usage_v0_1_4.png)
* Open an image
  * Method 1: Click the 'Open' button in the top left to choose an image.
  * Method 2: Using drag-and-drop.
* The gallery section below will display all images in the same folder as the currently viewed image. You can choose which image to display
  * Method 1: Click on the image in the gallery section.
  * Method 2: Use the 'a' or 's' keys on your keyboard to select the image.
* Open the image using 'Preview.app' (only applicable to MacOS)
  * Method 1: Click the 'Preview' button in the top right.
  * Method 2: Double left-click on the image.
* Rename and Save an image as ...
  * Right-click on the image to display a menu.
* (Not necessary) Clicking on the 'Refresh' icon will update the content in the gallery.
  * Only need to manually click this button when images are added to the current folder.
* Editable image prompts are allowed, but they must follow a specific format.
  * Positive, Negative, and settings should be separated by an enter.(As shown in the figure below, make sure to separate these three paragraphs with an "enter" between them)
  * ![editor](examples/editor.png)

## Test environment
```
Python 3.12 (on macOS 14.2.1)
```

## Note
If crash after update PySide6 >= 6.6.2  
Just remove and reinstall it. (Have to remove all PySide6 packages)
>pip uninstall -qy shiboken6 PySide6 PySide6_Addons PySide6_Essentials