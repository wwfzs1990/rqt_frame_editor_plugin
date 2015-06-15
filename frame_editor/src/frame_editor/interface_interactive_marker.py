#!/usr/bin/env python


## TODO: DISCLAIMER, LICENSE, STUFF,...

import rospy
import rosparam

import tf

from frame_editor.objects import *
from frame_editor.constructors_geometry import *
from frame_editor.constructors_std import *

from geometry_msgs.msg import Pose

from interactive_markers.interactive_marker_server import *
from visualization_msgs.msg import InteractiveMarkerControl, Marker


class FrameEditor_InteractiveMarker:

    def __init__(self, frame_editor):
        self.editor = frame_editor

        self.server = InteractiveMarkerServer("frame_editor_interactive")

        self.set_marker_settings(["x", "y", "z", "a", "b", "c"])


    def make_interactive(self, frame):

        ## Stop currently active frame
        if self.editor.active_frame is not None:
            self.server.erase(self.editor.active_frame.name)
            self.server.applyChanges()

        self.editor.active_frame = frame

        if frame is not None:
            self.set_marker_settings(["x", "y", "z", "a", "b", "c"], frame)

            self.int_marker.name = frame.name
            self.int_marker.header.frame_id = frame.parent
            self.int_marker.pose = frame.pose

            self.server.insert(self.int_marker, self.callback_marker)
            self.server.applyChanges()

        self.editor.update_obsevers(2)

    def callback_marker(self, feedback):
        self.editor.active_frame.position = FromPoint(feedback.pose.position)
        self.editor.active_frame.orientation = FromQuaternion(feedback.pose.orientation)

        self.editor.update_obsevers(4)


    def set_marker_settings(self, arrows, frame=None, scale=0.25):
        '''arrows is a list with any number of the following strings: ["x", "y", "z", "a", "b", "c"].'''

        if frame:
            style = frame.style
        else:
            style = "none"

        ## Marker
        int_marker = InteractiveMarker()
        int_marker.header.frame_id = ""
        int_marker.name = ""
        int_marker.description = "Frame Editor"
        int_marker.pose = Pose()
        int_marker.scale = scale

        if "x" in arrows:
            control = InteractiveMarkerControl()
            control.name = "move_x"
            control.orientation = NewQuaternion(1, 0, 0, 1)
            control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
            int_marker.controls.append(control);

        if "y" in arrows:
            control = InteractiveMarkerControl()
            control.name = "move_y"
            control.orientation = NewQuaternion(0, 1, 0, 1)
            control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
            int_marker.controls.append(control);

        if "z" in arrows:
            control = InteractiveMarkerControl()
            control.name = "move_z"
            control.orientation = NewQuaternion(0, 0, 1, 1)
            control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
            int_marker.controls.append(control);

        if "a" in arrows:
            control = InteractiveMarkerControl()
            control.name = "rotate_x"
            control.orientation = NewQuaternion(1, 0, 0, 1)
            control.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
            int_marker.controls.append(control);

        if "b" in arrows:
            control = InteractiveMarkerControl()
            control.name = "rotate_y"
            control.orientation = NewQuaternion(0, 1, 0, 1)
            control.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
            int_marker.controls.append(control);


        if "c" in arrows:
            control = InteractiveMarkerControl()
            control.name = "rotate_z"
            control.orientation = NewQuaternion(0, 0, 1, 1)
            control.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
            int_marker.controls.append(control);


        ## Style ##
        ##
        style_marker = Marker()
        style_marker.scale = NewVector3(0.75*scale, 0.75*scale, 0.75*scale)
        style_marker.color = NewColor(0.0, 0.5, 0.5, 0.75)

        if style != "none":
            style_marker = frame.marker

        style_control = InteractiveMarkerControl()
        style_control.always_visible = True
        style_control.markers.append(style_marker)

        if style != "none":
            int_marker.controls.append(style_control)


        self.int_marker = int_marker

# eof