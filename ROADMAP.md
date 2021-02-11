## Priority 1

- PyEsmini: Fix remaining PyEsmini issues
- PyEsmini: Error handling for methods that need to be called in the right order (e.g. addsensor before fetch sensor data, etc)
- PyEsmini: Convert return ctypes structures to native python data structure
- PyEsmini: API Documentation
- PyEsmini: RoadManager (RM) API
- Formatting standard PEP8 (autopep8 --in-place --aggressive file.py)
- Git workflow (see below)
- OSI recording host
- Few basic test cases
- Exact version of dependency packages
- Testcase for PyEsminiRM
## Priority 2

- Use pythong logger
- Support for Windows platforms (build script and code)
- BUG: Fix methods that update road and object attributes
- BUG: Reload on specific time using stepDT does not always work correctly
- PyESmini: PyPI, Python Package
- Opening corresponding OpenDrive files in a separate tab
- Template OpenScenario XML Snippets
- Show all licenses in UI
- Rename gui_qt and split the logic
- Search next item when the search button is clicked
- Open OSG files on external view
- Open file from cli

## Priority 3

- handleSimpleVehicle esmini lib returns a class with several methods
- RM object
- UI/UX: Disable UI elements that should not be updated
- XML/OpenScenario validator
- Make UI responsive


### new branch off the develope branch
git checkout -b featureX develop 
git add CHANGEED FILES
git commit -m "CHANGES"
git push --set-upstream origin featureX

git checkout develop
git merge featureX

git push --set-upstream origin develop
