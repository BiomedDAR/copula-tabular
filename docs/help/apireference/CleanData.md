---
layout: default
title: CleanData Documentation
parent: API Reference
grand_parent: Help and Reference
nav_order: 2
---

# CleanData

`class CleanData(definitions=None, debug=True)`

For data cleaning.

### Parameters

**definitions**: file (.py) containing global variables
*   `PREFIX_PATH`: define the root directory
*   `RAW_PATH`: set the folder name for all raw data files
*   `TRAIN_PATH`: set the folder name to store all the cleaned data files. If not specified, default is "`trainData`"
*   `RAWXLSX`: filename containing the raw data
*   `RAWXLSX_SHEETNAME`: if RAWXLSX is an excel file, assign the sheetname from which to load the data. If not specified, will read the first sheet.

**debug**: boolean, default None

&emsp;If `True`, print intermediate outputs for debugging purposes

### Notes

### Examples

### Attributes

### Methods