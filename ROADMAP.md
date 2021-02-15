## Done:
- PyEsmini: RoadManager (RM) API
- Basic testcase for PyEsminiRM
- Bridge between [PyEsmini and PyESminiRM](https://github.com/ebadi/esmini/commit/f8e9aa4fa9ad180dce96838acba02e0b0f629ecf)

## Priority 1

- PyEsmini: Fix remaining PyEsmini/PyEsminiRM issues
- PyEsmini: Error handling for methods that need to be called in the right order (e.g. addsensor before fetch sensor data, etc)
- PyEsmini: Convert return ctypes structures to native python data structure
- PyEsmini: API Documentation
- Formatting standard PEP8 (autopep8 --in-place --aggressive file.py)
- Git workflow (see below)
- OSI recording host
- Improve fast forwarding by running the simulation in a headless mode as described in [esmini/issues/76](https://github.com/esmini/esmini/issues/76#issuecomment-775863938)
- Identify libEsmini interfaces that are not accessible from Python (https://github.com/vedderb/rise_sdvp/blob/master/Linux/RControlStation/pagesimscen.cpp#L84)

## Priority 2
- RControlStation features.
- Use python logger
- Support for Windows platforms (build script and code)
- PyEsmini: PyPI, Python pip Package (needs exact version of dependent packages)
- Opening corresponding OpenDrive files in a separate tab/ OpenDrive editor
- Template OpenScenario XML Snippets
- Show all licenses in UI
- Split the Qt logic from pyesmini logic in gui_qt
- Search next item when the search button is clicked
- Open OSG files on external view
- Support for opening file from cli in Open Scenario Editor

## Priority 3

- handleSimpleVehicle esmini lib returns a class with several methods
- UI/UX: Disable UI elements that should not be updated
- XML/OpenScenario validator


### new branch off the develope branch
git checkout -b featureX develop 
git add CHANGEED FILES
git commit -m "CHANGES"
git push --set-upstream origin featureX

git checkout develop
git merge featureX

git push --set-upstream origin develop
