# Quick graphic vis of vision outputs
# Brygg Ullmer
# Begun 11/05/1996

package require Itcl
package provide tmg::graphview 1.0

itcl_class visionMonitor {

  method init {} {
    toplevel $top
    canvas $top.c \
      -width [expr $maxx * $resmult] -height [expr $maxy * $resmult]
    pack $top.c
  }

  method displayTags {taglist} {

    set last_frame $current_frame
    set current_frame {}

#    puts ">> $taglist"

    foreach el $taglist {
      set x [expr [lindex $el 0] * $resmult]
      set y [expr ($maxy - [lindex $el 1]) * $resmult]

      set id [$top.c create rectangle \
	[expr $x - $objwidth] [expr $y - $objwidth] \
	[expr $x + $objwidth] [expr $y + $objwidth] \
	-fill black]
      lappend current_frame $id
    }

    foreach id $last_frame {
      $top.c delete $id
    }

   update
  }

  method displayVistags {taglist} {
    set result {}

    foreach el $taglist {
      #set position [lindex $el 2]
      set position [lrange $el 2 3]
      lappend result $position
    }

    displayTags $result
  }


  method displayScenetags {taglist} {
    set result {}

    foreach el $taglist {
      set position [lindex $el 1]
      lappend result $position
    }

    displayTags $result
  }

  public top  {.vismon}
  public maxx {80}
  public maxy {60}
  public resmult  {5}
  public objwidth {4}
  public last_frame {}
  public current_frame {}
}

