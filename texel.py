#!/usr/bin/env python3

import sublime
import sublime_plugin

def closestBoundaryToPoint(view, point):
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

def move_insertion_to_nearest_boundary(view, point):
	insertion_point = closestBoundaryToPoint(view, point)
	view.sel().clear()
	view.sel().add(sublime.Region(insertion_point))

class SnappedCursorCommand(sublime_plugin.TextCommand):
	def run(self, edit, event, press=True):
		point = self.view.window_to_text((event['x'], event['y']))
		move_insertion_to_nearest_boundary(self.view, point)

	def want_event(self):
		return True

