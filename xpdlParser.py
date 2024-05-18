import xml.etree.ElementTree as ET
import random

def addActivityTime(xpdl_file_path):
    tree = ET.parse(xpdl_file_path)
    root = tree.getroot()
    
    # Define the XML namespaces to find XPDL elements
    namespaces = {
        'xpdl': 'http://www.wfmc.org/2009/XPDL2.2'
    }
    
    # Search for task elements in XPDL
    tasks = root.findall('.//xpdl:Activity', namespaces)
    
    # Adding random duration and printing details
    for task in tasks:
        duration = random.randint(5, 15)
        task.set('Duration', str(duration))  # Set the duration attribute
        print(f"Assigned {duration} minutes to task '{task.get('Name')}' (ID: {task.get('Id')})")
    
    # Save the modified XML to a new file
    new_file_path = xpdl_file_path.replace('.xpdl', '_modified.xpdl')
    tree.write(new_file_path)
    return new_file_path

def calculateCT(modified_xpdl_file_path):
    tree = ET.parse(modified_xpdl_file_path)
    root = tree.getroot()
    
    # Define the XML namespaces to find XPDL elements
    namespaces = {
        'xpdl': 'http://www.wfmc.org/2009/XPDL2.2'
    }
    
    total_time = 0
    
    # Print detailed timing information for each task
    tasks = root.findall('.//xpdl:Activity', namespaces)
    
    print("\nDetailed Task Times:")
    for task in tasks:
        duration = int(task.get('Duration', '0'))  # Fetch the 'Duration' attribute
        total_time += duration
        print(f"Task '{task.get('Name')}' (ID: {task.get('Id')}): {duration} minutes")
        
        # Check for rework scenario
        for flow in root.findall('.//xpdl:Transition', namespaces):
            if flow.get('To') == task.get('Id'):  # Target of the flow is the current task
                source_id = flow.get('From')  # Source of the flow
                for previous_task in tasks:
                    if previous_task.get('Id') == source_id:
                        print(f"Detected rework from task '{previous_task.get('Name')}' to task '{task.get('Name')}'")
                        # Multiply duration by 0.25 for rework
                        total_time += duration * 0.25

    print(f"\nTotal cycle time: {total_time} minutes")
    return total_time

# Example usage:
xpdl_path = 'XPDL files/networkDeployment.xpdl'
modified_xpdl_path = addActivityTime(xpdl_path)
cycle_time = calculateCT(modified_xpdl_path)
