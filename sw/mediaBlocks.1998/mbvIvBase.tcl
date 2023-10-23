# MoveMoov code
# By Phillip Tiongson and Brygg Ullmer, MIT Media Lab
# Begun 02/12/1998
# John Alex began modifications 02/23/98


package require pdf::base 1.0

package provide mbv::ivBase 1.0

#################### imagePane #########################

itcl_class ivBase {
  inherit pdfBase

  constructor {config} {
    if {$verbose} {puts "Evaluating $this ivBase constructor"}
    regsub {^.*::([^:].*)$} $this {\1} iv_name
    if {$parent_ != ""} {set iv_name "$parent_:$iv_name"; 
    #puts "adding object $iv_name"
}
  }
  destructor {retractIv}

  method assertIv {}  {puts "$this calls dummy assertIv";  set iv_asserted 1}
  method retractIv {} {puts "$this calls dummy retractIv"; set iv_asserted 0} 
  method getIvName {} {return $iv_name}

  method getPosition {} {return $position_}
  method getPosNode {}  {return [format {%s:trans} $iv_name]}
  method getRotNode {}  {return [format {%s:rot} $iv_name]}

  method isAsserted {} {return $iv_asserted}
  public position_ {0 0 0}
  public rotation_ {0 0 0}

  public iv_name  {}
  public parent_ {} ;# if this is non-empty, our iv_name becomes parent:name, so we're automatically added into parent's soSeparator in the iv scene graph.
  public iv_asserted {0}
}

## END ##

