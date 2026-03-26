import sublime, sublime_plugin, re

def cursorPerLine(view):
  """
  Put a cursor on every line of the
  selected region.
  
  :param      view:  The view
  :type       view:  sublime.View
  """
  s = view.sel()[0]                     # Get the selection of the first cursor.
                                        # 
  rb, _ = view.rowcol(s.begin())        # Get the start and end of the
  re, _ = view.rowcol(s.end())          # selection.
                                        # 
  view.sel().clear()                    # Clear the current selection.
                                        # 
  while (rb <= re):                     # Iterate through each line of the 
                                        # original selection:
                                        # 
    pt = view.text_point(rb, 0)         # Calculate a point at the begining of
                                        # each row.
                                        # 
    view.sel().add(sublime.Region(pt))  # Add a new cursor at each new point.
                                        # 
    rb += 1                             # Increment to the next line.


def cursorsEol(view):
  """
  Place all cursors at the end of their respective lines.

  :param      view:  The view
  :type       view:  sublime.View
  """
  lines = []                            # Initialize empty array to store 
                                        # targets.
                                        # 
  for s in view.sel():                  # For each cursor:
    p = s.begin()                       # Get the begining of each selection.
                                        # 
    l = view.line(p)                    # Get the line to which the begining of 
                                        # the selection belongs.
                                        # 
    lines.append(l)                     # Append that line to the array of 
                                        # targets.
                                        # 
  view.sel().clear()                    # Clear the current selection.
                                        # 
  for l in lines:                       # For each line:
    view.sel().add(                     # 
      sublime.Region(l.end()))          # Add a cursor at the end of the line.

def gotoCol(edit, view, col):
  """
  Move all cursors to the right to rach
  a target column. If a cursor is
  already passed the desired column,
  then it does not move.
  
  :param      edit:  The edit
  :type       edit:  sublime.Edit
  :param      view:  The view
  :type       view:  sublime.View
  :param      col:   The col
  :type       col:   int
  """
  for s in view.sel():                  # For each cursor:
                                        #
    _ , x = view.rowcol(s.a)            # Get the column of the cursor.
                                        # 
    dif = col - x                       # Find how far it is from the desired
                                        # column.
                                        # 
    if dif > 0:                         # If it is not passed the desired column
      view.insert(edit, s.a, ' '*dif)   # Then insert spaces until we have 
                                        # reached the desired column.    

def insertComment(view):
  """
  Insert a comment character(s) at each
  cursor
  
  :param      view:  The view
  :type       view:  sublime.View
  """
  view.run_command(                     # 
      cmd="insert_snippet",             # 
      args={                            # 
        "contents": "$TM_COMMENT_START" # 
      }                                 #
    )                                   # Insert a comment at each cursor.

class CommentWallCommand(sublime_plugin.TextCommand):
  def run(self, edit, col=40):
    if (len(self.view.sel()) <= 1):     # If there is only one active cursor:
      cursorPerLine(self.view)          # Then place cursors at every line of
                                        # its selection.
                                        # 
    cursorsEol(self.view)               # Place every cursor at the end of its
                                        # respective line.
                                        # 
    gotoCol(edit, self.view, col)       # Place each cursor at the desired 
                                        # column.
                                        # 
    insertComment(self.view)            # 
                                        # 
    first = self.view.sel()[0]          # 
    self.view.sel().clear()             # 
    self.view.sel().add(first)          # Remove all cursors except the first.        

class CommentWallInsertCommand(sublime_plugin.TextCommand):
  def run(self, edit, characters, col=40):
    for s in self.view.sel():           # For each cursor:
      self.view.insert(                 # 
        edit, s.a, characters)          # Insert the desired string.
                                        # 
    gotoCol(edit, self.view, col)       # Place all cursors at desired column.
                                        # 
    insertComment(self.view)            # Insert a comment at each cursor.