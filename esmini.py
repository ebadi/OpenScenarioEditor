import ctypes
import os
import sys
from ctypes import Structure, c_int, c_uint, c_double, c_char, c_char_p, c_bool, POINTER, byref, CFUNCTYPE


class ScenarioObjectState(Structure):
    _fields_ = [
        ("id",             c_int),
        ("model_id",       c_int),
        ("ctrl_type",      c_int),
        ("timestamp",      c_double),
        ("x",              c_double),
        ("y",              c_double),
        ("z",              c_double),
        ("h",              c_double),
        ("p",              c_double),
        ("r",              c_double),
        ("roadId",         c_uint),
        ("junctionId",     c_uint),
        ("t",              c_double),
        ("laneId",         c_int),
        ("laneOffset",     c_double),
        ("s",              c_double),
        ("speed",          c_double),
        ("centerOffsetX",  c_double),
        ("centerOffsetY",  c_double),
        ("centerOffsetZ",  c_double),
        ("width",          c_double),
        ("length",         c_double),
        ("height",         c_double),
        ("objectType",     c_int),
        ("objectCategory", c_int),
        ("wheel_angle",    c_double),
        ("wheel_rot",      c_double),
        ("visibilityMask", c_int),
    ]


class RoadInfo(Structure):
    _fields_ = [
        ("global_pos_x",     c_double),
        ("global_pos_y",     c_double),
        ("global_pos_z",     c_double),
        ("local_pos_x",      c_double),
        ("local_pos_y",      c_double),
        ("local_pos_z",      c_double),
        ("angle",            c_double),
        ("road_heading",     c_double),
        ("road_pitch",       c_double),
        ("road_roll",        c_double),
        ("trail_heading",    c_double),
        ("curvature",        c_double),
        ("speed_limit",      c_double),
        ("roadId",           c_uint),
        ("junctionId",       c_uint),
        ("laneId",           c_int),
        ("laneOffset",       c_double),
        ("s",                c_double),
        ("t",                c_double),
        ("road_type",        c_int),
        ("road_rule",        c_int),
        ("lane_type",        c_int),
        ("trail_wheel_angle", c_double),
    ]


# Integer values passed to SE_RegisterStoryBoardElementStateChangeCallback.
# Source: StoryboardElement.hpp, class StoryBoardElement
ELEMENT_TYPES = {
    0: "UNDEFINED",
    1: "STORY_BOARD",
    2: "STORY",
    3: "ACT",
    4: "MANEUVER_GROUP",
    5: "MANEUVER",
    6: "EVENT",
    7: "ACTION",
}

ELEMENT_STATES = {
    0: "UNDEFINED",
    1: "STANDBY",
    2: "RUNNING",
    3: "COMPLETE",
}

# ctypes function-pointer types for the two callbacks
_StoryboardCbType = CFUNCTYPE(None, c_char_p, c_int, c_int, c_char_p)
_ConditionCbType  = CFUNCTYPE(None, c_char_p, c_double)


class EsminiLib:

    def __init__(self, osc_file, disable_ctrls=False, use_viewer=True,
                 threads=False, recordFile=""):
        lib_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "esmini")
        if sys.platform in ("linux", "linux2"):
            lib_path = os.path.join(lib_dir, "libesminiLib.so")
        elif sys.platform == "darwin":
            lib_path = os.path.join(lib_dir, "libesminiLib.dylib")
        elif sys.platform == "win32":
            lib_path = os.path.join(lib_dir, "esminiLib.dll")
        else:
            raise RuntimeError(f"Unsupported platform: {sys.platform}")

        self._lib = ctypes.CDLL(lib_path)
        self._declare_signatures()

        # Held to prevent garbage collection while the simulation runs
        self._storyboard_cb = None
        self._condition_cb  = None

        args = ["OpenScenarioEditor", "--osc", osc_file]
        if disable_ctrls:
            args.append("--disable_controllers")
        if threads:
            args.append("--threads")
        if recordFile:
            args += ["--record", recordFile]
        args += ["--window", "60 60 800 400"] if use_viewer else ["--headless"]

        argv = (ctypes.c_char_p * len(args))(*[a.encode() for a in args])
        if self._lib.SE_InitWithArgs(len(args), argv) < 0:
            raise RuntimeError("SE_InitWithArgs failed — check the .xosc file path")

        # Register the bundled resources directory so esmini can locate built-in
        # road networks and 3D models referenced by relative paths in .xosc files.
        resources_dir = os.path.join(lib_dir, "resources")
        if os.path.isdir(resources_dir):
            self._lib.SE_AddPath(resources_dir.encode())

    def _declare_signatures(self):
        lib = self._lib

        lib.SE_InitWithArgs.argtypes          = [c_int, POINTER(c_char_p)]
        lib.SE_InitWithArgs.restype           = c_int

        lib.SE_AddPath.argtypes               = [c_char_p]
        lib.SE_AddPath.restype                = c_int

        lib.SE_ClearPaths.argtypes            = []
        lib.SE_ClearPaths.restype             = None

        lib.SE_StepDT.argtypes                = [c_double]
        lib.SE_StepDT.restype                 = c_int

        lib.SE_Step.argtypes                  = []
        lib.SE_Step.restype                   = c_int

        lib.SE_Close.argtypes                 = []
        lib.SE_Close.restype                  = None

        lib.SE_GetSimulationTime.argtypes     = []
        lib.SE_GetSimulationTime.restype      = c_double

        lib.SE_GetODRFilename.argtypes        = []
        lib.SE_GetODRFilename.restype         = c_char_p

        lib.SE_GetSceneGraphFilename.argtypes = []
        lib.SE_GetSceneGraphFilename.restype  = c_char_p

        lib.SE_GetNumberOfObjects.argtypes    = []
        lib.SE_GetNumberOfObjects.restype     = c_int

        lib.SE_GetObjectState.argtypes        = [c_int, POINTER(ScenarioObjectState)]
        lib.SE_GetObjectState.restype         = c_int

        lib.SE_GetObjectName.argtypes         = [c_int]
        lib.SE_GetObjectName.restype          = c_char_p

        lib.SE_ReportObjectPos.argtypes       = [c_int, c_double, c_double, c_double,
                                                  c_double, c_double, c_double]
        lib.SE_ReportObjectPos.restype        = c_int

        lib.SE_ReportObjectRoadPos.argtypes   = [c_int, c_uint, c_int, c_double, c_double]
        lib.SE_ReportObjectRoadPos.restype    = c_int

        lib.SE_GetRoadInfoAtDistance.argtypes = [c_int, c_double, POINTER(RoadInfo),
                                                  c_int, c_bool]
        lib.SE_GetRoadInfoAtDistance.restype  = c_int

        lib.SE_EnableOSIFile.argtypes         = [c_char_p]
        lib.SE_EnableOSIFile.restype          = None

        lib.SE_RegisterStoryBoardElementStateChangeCallback.argtypes = [_StoryboardCbType]
        lib.SE_RegisterStoryBoardElementStateChangeCallback.restype  = None

        lib.SE_RegisterConditionCallback.argtypes = [_ConditionCbType]
        lib.SE_RegisterConditionCallback.restype  = None

    def step(self):
        return self._lib.SE_Step() >= 0

    def stepDT(self, dt):
        return self._lib.SE_StepDT(dt)

    def close(self):
        self._lib.SE_Close()

    def getSimulationTime(self):
        return self._lib.SE_GetSimulationTime()

    def getODRFilename(self):
        return self._lib.SE_GetODRFilename().decode()

    def getSceneGraphFilename(self):
        return self._lib.SE_GetSceneGraphFilename().decode()

    def getNumberOfObjects(self):
        return self._lib.SE_GetNumberOfObjects()

    def getObjectName(self, index):
        return self._lib.SE_GetObjectName(index).decode()

    def getObjectState(self, index):
        state = ScenarioObjectState()
        if self._lib.SE_GetObjectState(index, byref(state)) < 0:
            raise RuntimeError(f"SE_GetObjectState failed for index {index}")
        return state

    def reportObjectPos(self, object_id, x, y, z, h, p, r):
        return self._lib.SE_ReportObjectPos(object_id, x, y, z, h, p, r)

    def reportObjectRoadPos(self, object_id, roadId, laneId, laneOffset, s):
        return self._lib.SE_ReportObjectRoadPos(object_id, roadId, laneId, laneOffset, s)

    def getRoadInfoAtDistance(self, object_id, lookahead_distance, lookAheadMode):
        info = RoadInfo()
        if self._lib.SE_GetRoadInfoAtDistance(
                object_id, lookahead_distance, byref(info), lookAheadMode, True) < 0:
            return None
        return info

    def addPath(self, path):
        self._lib.SE_AddPath(path.encode())

    def clearPaths(self):
        self._lib.SE_ClearPaths()

    def OSIFileOpen(self, filename):
        self._lib.SE_EnableOSIFile(filename.encode() if filename else b"")

    def registerStoryboardCallback(self, fn):
        """Register a callback invoked on every storyboard element state change.

        fn(name: str, element_type: int, state: int, full_path: str)

        Use ELEMENT_TYPES[element_type] and ELEMENT_STATES[state] to decode
        the integer values into readable strings.

        Callbacks are cleared automatically by esmini on the next SE_Init call.
        """
        def _wrapper(name, element_type, state, full_path):
            fn(name.decode(), element_type, state, full_path.decode())
        self._storyboard_cb = _StoryboardCbType(_wrapper)
        self._lib.SE_RegisterStoryBoardElementStateChangeCallback(self._storyboard_cb)

    def registerConditionCallback(self, fn):
        """Register a callback invoked every time a condition is triggered.

        fn(name: str, timestamp: float)
        """
        def _wrapper(name, timestamp):
            fn(name.decode(), timestamp)
        self._condition_cb = _ConditionCbType(_wrapper)
        self._lib.SE_RegisterConditionCallback(self._condition_cb)


# ─── esminiRMLib structs ──────────────────────────────────────────────────────

class RM_PositionXYZ(Structure):
    _fields_ = [
        ("x", c_double),
        ("y", c_double),
        ("z", c_double),
    ]


class RM_PositionData(Structure):
    _fields_ = [
        ("x",          c_double),
        ("y",          c_double),
        ("z",          c_double),
        ("h",          c_double),
        ("p",          c_double),
        ("r",          c_double),
        ("hRelative",  c_double),
        ("roadId",     c_uint),
        ("junctionId", c_uint),
        ("laneId",     c_int),
        ("laneOffset", c_double),
        ("s",          c_double),
    ]


class RM_RoadLaneInfo(Structure):
    _fields_ = [
        ("pos",         RM_PositionXYZ),
        ("heading",     c_double),
        ("pitch",       c_double),
        ("roll",        c_double),
        ("width",       c_double),
        ("curvature",   c_double),
        ("speed_limit", c_double),
        ("roadId",      c_uint),
        ("junctionId",  c_uint),
        ("laneId",      c_int),
        ("laneOffset",  c_double),
        ("s",           c_double),
        ("t",           c_double),
        ("road_type",   c_int),
        ("road_rule",   c_int),
        ("lane_type",   c_int),
    ]


class RM_RoadProbeInfo(Structure):
    _fields_ = [
        ("road_lane_info", RM_RoadLaneInfo),
        ("relative_pos",   RM_PositionXYZ),
        ("relative_h",     c_double),
    ]


class RM_PositionDiff(Structure):
    _fields_ = [
        ("ds",      c_double),
        ("dt",      c_double),
        ("dLaneId", c_int),
    ]


_RM_NAME_SIZE = 32


class RM_RoadSign(Structure):
    _fields_ = [
        ("id",          c_int),
        ("x",           c_double),
        ("y",           c_double),
        ("z",           c_double),
        ("z_offset",    c_double),
        ("h",           c_double),
        ("s",           c_double),
        ("t",           c_double),
        ("roadId",      c_uint),
        ("name",        c_char * _RM_NAME_SIZE),
        ("orientation", c_int),
        ("length",      c_double),
        ("height",      c_double),
        ("width",       c_double),
    ]


# ─── RoadManagerLib ───────────────────────────────────────────────────────────

class RoadManagerLib:
    """Thin ctypes wrapper around libesminiRMLib — standalone road-network queries.

    Load an OpenDRIVE file directly (no scenario required):

        rm = RoadManagerLib("my_map.xodr")
        h  = rm.createPosition()
        rm.setLanePosition(h, road_id=1, lane_id=-1, lane_offset=0.0, s=10.0)
        data = rm.getPositionData(h)
        rm.deletePosition(h)
        rm.close()
    """

    def __init__(self, odr_file):
        lib_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "esmini")
        if sys.platform in ("linux", "linux2"):
            lib_path = os.path.join(lib_dir, "libesminiRMLib.so")
        elif sys.platform == "darwin":
            lib_path = os.path.join(lib_dir, "libesminiRMLib.dylib")
        elif sys.platform == "win32":
            lib_path = os.path.join(lib_dir, "esminiRMLib.dll")
        else:
            raise RuntimeError(f"Unsupported platform: {sys.platform}")

        self._lib = ctypes.CDLL(lib_path)
        self._declare_signatures()

        if self._lib.RM_Init(odr_file.encode()) < 0:
            raise RuntimeError(f"RM_Init failed for {odr_file!r}")

    def _declare_signatures(self):
        lib = self._lib

        lib.RM_Init.argtypes                = [c_char_p]
        lib.RM_Init.restype                 = c_int

        lib.RM_Close.argtypes               = []
        lib.RM_Close.restype                = None

        lib.RM_CreatePosition.argtypes      = []
        lib.RM_CreatePosition.restype       = c_int

        lib.RM_DeletePosition.argtypes      = [c_int]
        lib.RM_DeletePosition.restype       = c_int

        lib.RM_GetNumberOfRoads.argtypes    = []
        lib.RM_GetNumberOfRoads.restype     = c_int

        lib.RM_GetIdOfRoadFromIndex.argtypes = [c_int]
        lib.RM_GetIdOfRoadFromIndex.restype  = c_int

        lib.RM_GetRoadLength.argtypes       = [c_int]
        lib.RM_GetRoadLength.restype        = c_double

        lib.RM_GetNumberOfLanesAtS.argtypes = [c_int, c_double]
        lib.RM_GetNumberOfLanesAtS.restype  = c_int

        lib.RM_GetLaneIdByIndex.argtypes    = [c_int, c_double, c_int]
        lib.RM_GetLaneIdByIndex.restype     = c_int

        lib.RM_SetLanePosition.argtypes     = [c_int, c_uint, c_int, c_double, c_double, c_bool]
        lib.RM_SetLanePosition.restype      = c_int

        lib.RM_SetWorldPosition.argtypes    = [c_int, c_double, c_double, c_double,
                                               c_double, c_double, c_double]
        lib.RM_SetWorldPosition.restype     = c_int

        lib.RM_SetWorldXYHPosition.argtypes = [c_int, c_double, c_double, c_double]
        lib.RM_SetWorldXYHPosition.restype  = c_int

        lib.RM_GetPositionData.argtypes     = [c_int, POINTER(RM_PositionData)]
        lib.RM_GetPositionData.restype      = c_int

        lib.RM_GetSpeedLimit.argtypes       = [c_int]
        lib.RM_GetSpeedLimit.restype        = c_double

        lib.RM_GetLaneInfo.argtypes         = [c_int, c_double, POINTER(RM_RoadLaneInfo),
                                               c_int, c_bool]
        lib.RM_GetLaneInfo.restype          = c_int

        lib.RM_GetProbeInfo.argtypes        = [c_int, c_double, POINTER(RM_RoadProbeInfo),
                                               c_int, c_bool]
        lib.RM_GetProbeInfo.restype         = c_int

        lib.RM_GetNumberOfRoadSigns.argtypes = [c_int]
        lib.RM_GetNumberOfRoadSigns.restype  = c_int

        lib.RM_GetRoadSign.argtypes         = [c_int, c_int, POINTER(RM_RoadSign)]
        lib.RM_GetRoadSign.restype          = c_int

    def close(self):
        self._lib.RM_Close()

    def createPosition(self):
        """Allocate a new position object; returns an integer handle."""
        return self._lib.RM_CreatePosition()

    def deletePosition(self, handle):
        return self._lib.RM_DeletePosition(handle)

    def getNumberOfRoads(self):
        return self._lib.RM_GetNumberOfRoads()

    def getIdOfRoadFromIndex(self, index):
        return self._lib.RM_GetIdOfRoadFromIndex(index)

    def getRoadLength(self, road_id):
        return self._lib.RM_GetRoadLength(road_id)

    def getNumberOfLanesAtS(self, road_id, s):
        return self._lib.RM_GetNumberOfLanesAtS(road_id, s)

    def getLaneIdByIndex(self, road_id, s, lane_index):
        return self._lib.RM_GetLaneIdByIndex(road_id, s, lane_index)

    def setLanePosition(self, handle, road_id, lane_id, lane_offset, s, align=True):
        return self._lib.RM_SetLanePosition(handle, road_id, lane_id, lane_offset, s, align)

    def setWorldPosition(self, handle, x, y, z, h, p, r):
        return self._lib.RM_SetWorldPosition(handle, x, y, z, h, p, r)

    def setWorldXYHPosition(self, handle, x, y, h):
        return self._lib.RM_SetWorldXYHPosition(handle, x, y, h)

    def getPositionData(self, handle):
        """Return RM_PositionData for *handle*, or None on failure."""
        data = RM_PositionData()
        if self._lib.RM_GetPositionData(handle, byref(data)) < 0:
            return None
        return data

    def getSpeedLimit(self, handle):
        return self._lib.RM_GetSpeedLimit(handle)

    def getLaneInfo(self, handle, lookahead_dist, look_ahead_mode=0, in_driving_direction=True):
        """Return RM_RoadLaneInfo at *lookahead_dist* ahead of *handle*, or None."""
        info = RM_RoadLaneInfo()
        if self._lib.RM_GetLaneInfo(
                handle, lookahead_dist, byref(info),
                look_ahead_mode, in_driving_direction) < 0:
            return None
        return info

    def getProbeInfo(self, handle, lookahead_dist, look_ahead_mode=0, in_driving_direction=True):
        """Return RM_RoadProbeInfo at *lookahead_dist* ahead of *handle*, or None."""
        info = RM_RoadProbeInfo()
        if self._lib.RM_GetProbeInfo(
                handle, lookahead_dist, byref(info),
                look_ahead_mode, in_driving_direction) < 0:
            return None
        return info

    def getNumberOfRoadSigns(self, road_id):
        return self._lib.RM_GetNumberOfRoadSigns(road_id)

    def getRoadSign(self, road_id, sign_index):
        """Return RM_RoadSign at *sign_index* on *road_id*, or None."""
        sign = RM_RoadSign()
        if self._lib.RM_GetRoadSign(road_id, sign_index, byref(sign)) < 0:
            return None
        return sign
