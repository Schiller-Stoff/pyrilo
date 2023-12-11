# created via github copilot
# /generate I need a script that loops through all folders in a directory. Each folder contains a  vor*.xml files that needs to be renamed to TEI_SOURCE.xml.

import os

directory = 'C:\\Users\\sebas\\Documents\\programming\\gams\\gams5-client\\project\sips'  # Replace with the actual directory path

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.startswith('TEI_SOURCE') and file.endswith('.xml'):
            old_path = os.path.join(root, file)
            new_path = os.path.join(root, 'SOURCE.xml')
            os.rename(old_path, new_path)
