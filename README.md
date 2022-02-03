# PyStackXRD
A Python/tk UI to merge histogram CSV exports from GSAS-II into a single CSV file.

Possible vulnerabilities to address:
    1. The GetThetaValues function relies on pandas finding a column labeled "x". This may
       cause problems reading CSV files. As long as GSAS-II output remains the same, there
       should be no problems. If a csv file is not intended to be read, and an "x" column
       is found, the file will be unintentionally read and cause issues. Both of these can
       be addressed, but not currently worthwhile.
    2. The csv files are organized in chronological order using the os.path.getctime()
       function, which assumes the files were created in the correct chronological order.
       This can be addressed in many ways, and it may be more desirable to have an export
       using alphanumeric order. An option may be added to chose either alphanumeric or
       chronological option. Not currently worthwhile.
    3. The exe takes a long time to load. Limited by PyInstaller --onefile option.
    4. There is no plotting functionality. Even a primitive one that exports plot images
       may be desirable. Not currently worthwhile, plotting the csv in excel takes
       seconds.
    5. Major changes to GSAS-II output using the Export->Powder Data->Histogram as csv
       may render the entire StackDiffraction class defunct. This will be patched as 
       changes in GSAS-II export behavior are found.
    6. Parameters for the Savinstky-Golay function used in the "Smooth" option. Not
       curretnly worthwhile.