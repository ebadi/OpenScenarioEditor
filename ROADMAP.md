## Priority 1

- PyESmini: Fix remaining pyesmini issues
- PyESmini: Error handling for methods that need to be called in the right order (e.g. addsensor before fetch sensor data, etc)
- PyESmini: Convert return ctypes structures to native python data structure
- PyESmini: API Documentation
- PyESmini: RoadManager (RM) API
- Formatting standard PEP8 (autopep8 --in-place --aggressive file.py)
- Git workflow (see below)
- OSI recording host
- Few basic test cases
- Exact version of dependency packages

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

## Bugs and limitations

#### SE_GetRoadInfoAtDistance
SE_GetRoadInfoAtDistance returns SE_RoadInfo which does not have roadID or objectId and therefore we cannot update it!

```
typedef struct
{
	float global_pos_x;     // target position, in global coordinate system
	float global_pos_y;     // target position, in global coordinate system
	float global_pos_z;     // target position, in global coordinate system
	float local_pos_x;      // target position, relative vehicle (pivot position object) coordinate system
	float local_pos_y;      // target position, relative vehicle (pivot position object) coordinate system
	float local_pos_z;      // target position, relative vehicle (pivot position object) coordinate system
	float angle;			// heading angle to target from and relatove to vehicle (pivot position)
	float road_heading;		// road heading at steering target point
	float road_pitch;		// road pitch (inclination) at steering target point
	float road_roll;		// road roll (camber) at target point
	float trail_heading;	// trail heading (only when used for trail lookups, else equals road_heading)
	float curvature;		// road curvature at steering target point
	float speed_limit;		// speed limit given by OpenDRIVE type entry
} SE_RoadInfo;
```

### StepDP
StepDP does not update the other actor

### Update obj/road
Not all attributes can be updated, why?

### new branch off the develope branch
git checkout -b featureX develop 
git add CHANGEED FILES
git commit -m "CHANGES"
git push --set-upstream origin featureX

git checkout develop
git merge featureX

git push --set-upstream origin develop
