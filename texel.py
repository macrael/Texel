#!/usr/bin/env python3

import sublime
import sublime_plugin

please_start_now = False


def closest_boundary_to_point(view, point):
    search_classes = sublime.CLASS_WORD_START | sublime.CLASS_WORD_END
    closest_point = point
    if not view.classify(point) & search_classes:
        fore = view.find_by_class(point, True, search_classes)
        aft = view.find_by_class(point, False, search_classes)

        if (fore - point <= point - aft):
            closest_point = fore
        else:
            closest_point = aft

    return closest_point


class BeginSnappedCursorDragCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        global please_start_now
        please_start_now = True
        self.view.run_command("drag_select", kwargs)

    def want_event(self):
        return True


class SnappedCursorDragEventListener(sublime_plugin.ViewEventListener):
    initial_a = None
    initial_b = None
    is_snap_dragging = False

    def want_event(self):
        True

    def on_selection_modified(self):
        global please_start_now
        if (self.view.is_in_edit() and (self.is_snap_dragging or please_start_now)):
            if please_start_now:
                please_start_now = False
                self.is_snap_dragging = True
                self.initial_a = None
                self.initial_b = None

            selection = self.view.selection
            # TODO: handle multiple selections correctly.
            first_region = selection[0]

            a = closest_boundary_to_point(self.view, first_region.a)
            b = closest_boundary_to_point(self.view, first_region.b)
            snapped_region = sublime.Region(a, b)

            if self.initial_a == None:
                self.initial_a = a
                self.initial_b = b

            if self.initial_a == a or self.initial_b == b:
                # This is a heuristic to check if we are in the same modification that was
                # started with BeginSnappedCursorDragCommand. There's no way
                # to know when a specifc drag_select event is complete so checking
                # that either end of the selection is the same is a good guess.
                selection.subtract(first_region)
                selection.add(snapped_region)
            else:
                self.is_snap_dragging = False
