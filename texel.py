#!/usr/bin/env python3

import sublime
import sublime_plugin

# sublime.log_input(False)

print("LOADING TEXEL!")

isPressing = False

def closestBoundaryToPoint(view, point):
	search_classes = sublime.CLASS_WORD_START | sublime.CLASS_WORD_END
	fore = view.find_by_class(point, True, search_classes)
	aft = view.find_by_class(point, False, search_classes)

	print("PREESS")
	print(isPressing)

	closest_point = None
	if (fore - point < point - aft):
		closest_point = fore
	else:
		closest_point = aft

	return closest_point

def move_insertion_to_nearest_boundary(view, point):
	insertion_point = closestBoundaryToPoint(view, point)
	print("NEW POINT", insertion_point)
	view.sel().clear()
	view.sel().add(sublime.Region(insertion_point))

class SnappedCursorCommand(sublime_plugin.TextCommand):
	def run(self, edit, event, press=True):
		print("running SNAPPED CMD")
		print(press)
		print(event)
		global isPressing
		isPressing = press
		point = self.view.window_to_text((event['x'], event['y']))
		move_insertion_to_nearest_boundary(self.view, point)

	def want_event(self):
		return True


class TexelContext(sublime_plugin.ViewEventListener):
	def on_hover(self, point, hover_zone):
		print('We Hovering!')
		print(point)
		print(self)
		print(self.view)
		print(hover_zone)
		print(isPressing)
		if (isPressing):
			print("moving to ")
			print(point)
			move_insertion_to_nearest_boundary(self.view, point)

