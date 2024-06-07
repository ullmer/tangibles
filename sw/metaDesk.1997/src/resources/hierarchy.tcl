# Hierarchy code
# Brygg Ullmer, MIT Media Lab TMG
# Begun 01/16/1997

package require Itcl
package require tmg::base

package provide tmg::hierarchy 1.0

#################### Base Server class ####################

;# Currently implement with a lookup table

itcl_class hierNode {

  inherit base
 
  public parent   {}
  parent children {}
 
  constructor {config} {
    set members [concat $members $local_members]
  }
 
  method getParent    {} {return $parent}
  method getChildList {} {return $children}
  method getNumChildren {} {return [llength $children]}
 
  method getChildTree {} {
    set result {}
 
    foreach child $children {
      set ctree [$child getChildTree]
      lappend result [list $child $ctree]
    }
    return $result
  }
}

