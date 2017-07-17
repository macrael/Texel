#!/usr/bin/env python3

import sublime
import sublime_plugin

is_doing_it_right = False

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

class SnappedCursorSwitchCommand(sublime_plugin.TextCommand):
	def want_event(self):
		return True

	def run(self,edit):
		print(self)
		print("WE DURNING ")

class SnappedCursorCommand(sublime_plugin.TextCommand):
	def run(self, edit, event, press=True):
		print("SNAPPING dAT YA")
		print(press)
		global is_doing_it_right
		is_doing_it_right = press
		# if press:
		# 	print("dsruning")
		# 	self.view.run_command('drag_select', event)
		point = self.view.window_to_text((event['x'], event['y']))
		move_insertion_to_nearest_boundary(self.view, point)

	def want_event(self):
		return True


class DraggingEventListener(sublime_plugin.ViewEventListener):
	is_dragging = False

	def want_event(self):
		True

	def on_selection_mortified(self):
		print("selection Modified")
		if (self.view.is_in_edit()):
			print("modifying selection")
			print(self.view.is_in_edit()) # This is exactly what I need, during the drag it's true.
			selection = self.view.selection
			# TODO: handle multiple selections correctly.
			first_region = selection[0]
			print(first_region)

			a = closestBoundaryToPoint(self.view, first_region.a)
			b = closestBoundaryToPoint(self.view, first_region.b)
			snapped_region = sublime.Region(a,b)

			print(snapped_region)

			selection.subtract(first_region)
			selection.add(snapped_region)

		# word_region = self.view.word(first_region)
		# sview.sel().add(word_region)

		# if not self.is_dragging:
		# 	print("INITIAL DRAG START")
		# 	self.is_dragging = True

	def on_modified(self):
		print("MODIFIED")


	def on_text_command(self, command_name, args):
		print("HI")
		print("Text Command")
		print(command_name)
		print(args)
