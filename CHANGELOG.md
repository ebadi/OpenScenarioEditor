## Unreleased

### OpenScenarioEditor 2.0 
- pyesmini dependency removed entirely (`pyesmini/` directory, clone and build steps)
- `esmini.py`: direct ctypes wrapper for `libesminiLib.so`, replacing the pyesmini dependency
  - Struct definitions (`ScenarioObjectState`, `RoadInfo`) updated to use `c_double`
  - New fields included: `junctionId`, `objectType`, `objectCategory`, `wheel_angle`, `wheel_rot`, `visibilityMask`, `trail_wheel_angle`
- `Dockerfile`: containerised build using `ubuntu:latest`; esmini built directly into `/app/esmini/`
- `docker-compose.yml`: X11 display forwarding

## OpenScenarioEditor 1.0

- OpenSCENARIO v1.0
- esmini 2.1.5 (build 1108)
- PyEsmini v1.0
- Ubuntu 20.04 build script
- Qt5 based Graphical User Interface
- Configure viewer settings
- Configure simulation settings (log files)
- Scenario object information list, viewer and editor
- Road information viewer
- Basic controls for the simulator (play, resume, step for/backward and reload)
- XML viewer and editor for editing Open Scenario files based on AXE
- OpenScenario object and road element search functionality
