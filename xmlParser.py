
import xml.etree.ElementTree as ET
import random
import os

def addActivityTime(xpdl_file_path, output_dir='output'):
    tree = ET.parse(xpdl_file_path)
    root = tree.getroot()
    
    # define namespace
    namespaces = {
        'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL'
    }
    
    # iterate and search for tasks using xpath (xml path lang)
    tasks = root.findall('.//bpmn:userTask', namespaces) + \
            root.findall('.//bpmn:manualTask', namespaces) + \
            root.findall('.//bpmn:serviceTask', namespaces)
    
    # adding random (5,15) mins per task to the xpdl
    for task in tasks:
        duration = random.randint(5, 15)
        task.set('duration', str(duration))
        print(f"Assigned {duration} minutes to task '{task.get('name')}' (ID: {task.get('id')})")
    
    # save the modified XML to a new file
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    new_file_path = os.path.join(output_dir, os.path.basename(xpdl_file_path).replace('.xpdl', '_modified.xpdl'))
    tree.write(new_file_path)
    return new_file_path

def calculateCT(modified_xpdl_file_path):
    tree = ET.parse(modified_xpdl_file_path)
    root = tree.getroot()
    
    #dDefine the XML namespaces to find elements
    namespaces = {
        'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL'
    }
    
    total_time = 0
    
    # print detailed timing infrmation for each task
    tasks = root.findall('.//bpmn:userTask', namespaces) + \
            root.findall('.//bpmn:manualTask', namespaces) + \
            root.findall('.//bpmn:serviceTask', namespaces)
    
    print("\nDetailed Task Times:")
    for task in tasks:
        duration = int(task.get('duration', '0'))
        total_time += duration
        print(f"Task '{task.get('name')}' (ID: {task.get('id')}): {duration} minutes")
        
        # Check for rework 
        for flow in root.findall('.//bpmn:sequenceFlow', namespaces):
            if flow.get('targetRef') == task.get('id'):
                source_id = flow.get('sourceRef')
                for previous_task in tasks:
                    if previous_task.get('id') == source_id:
                        print(f"Detected rework from task '{previous_task.get('name')}' to task '{task.get('name')}'")
                        # multiply duration by 0.25 for rework
                        total_time += duration * 0.25

    print(f"\nTotal cycle time: {total_time} minutes")
    return total_time

xpdl_path = 'XPDL IN BPMN.IO XML FORMAT/deployment.xpdl'
modified_xpdl_path = addActivityTime(xpdl_path)
calculateCT(modified_xpdl_path)
