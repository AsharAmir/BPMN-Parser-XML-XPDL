# XPDL BPMN Task Duration Modifier and Cycle Time Calculator

This repository contains Python scripts for modifying XPDL files in BPMN format. The scripts add random task durations and calculate the total cycle time, including adjustments for detected rework.

## Features

- Add random durations to user, manual, and service tasks
- Calculate total cycle time with adjustments for rework
- Handles XML namespaces for accurate element manipulation

## Requirements

- Python 3.x
- `xml.etree.ElementTree`
- `random`
- `os`

## Usage

### Add Random Task Durations

This script adds random durations to tasks and saves the modified file.

```python
from modify_xpdl import addActivityTime

xpdl_path = 'path/to/your/deployment.xpdl'
modified_xpdl_path = addActivityTime(xpdl_path)
print(f"Modified XPDL file saved at: {modified_xpdl_path}")
