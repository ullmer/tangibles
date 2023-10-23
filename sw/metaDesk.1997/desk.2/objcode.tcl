#!3wish

#Desk Object Code
#Brygg Ullmer, MIT Media Lab TMG/VLW
#March 9, 1996

global __OBJCODE__
if {[info exists __OBJCODE__]} {return}
set __OBJCODE__ 1

#source libiv.tcl
#source stack.tcl

############################## Object Registry #############################

itcl_class ObjRegistry {
  
  method registerBCPairs {bcpairs} {

  upvar #0 REG::$this:bc2obj bc2obj
  upvar #0 REG::$this:obj2bc obj2bc

    foreach pair $bcpairs {
      set bc2obj([lindex $pair 0]) [lindex $pair 1]
      lappend obj2bc([lindex $pair 1]) [lindex $pair 0] 
	 #multiple maps are kosher for obj2bc
    }
  }

  method map_bc2obj {bc} {

    upvar #0 REG::$this:bc2obj bc2obj
    if {![info exists bc2obj($bc)]} {return {}}
    return $bc2obj($bc)
  }

  method map_obj2bc {obj} {

    upvar #0 REG::$this:obj2bc obj2bc
    if {![info exists obj2bc($obj)]} {return {}}
    return $obj2bc($obj)
  }

  #Generate which instance of object is being observed 
  method get_instance {obj} { 

    if {![info exists objinstance($obj)]} {
      set objinstance($obj) 1
      return 1
    }

    return [incr objinstance($obj)]
  }
}

############################## Desk Object #############################

itcl_class DeskObject {

  inherit IvObj 

  constructor {config} {
    set members [concat $members $local_members]
  }

  method assertDesk {} {}
  method assertLens {} {}

  public local_members {location dim symname}
  public location {}
  public dim      {}
  public symname  {Unnamed} ;#for shadow, among others
}

############################## Simple Object #############################

itcl_class StackObject {

  inherit DeskObject

  constructor {config} {
    set members [concat $members $local_members]
  }

  method assertDesk {} {
    
    addNFrame $this
    texture_plane $this:plane -texture_size $dim -texture_name $keyframe \
      -transp 0 -color $color
    $this:plane assertIv xy

    #add shadow
    addNObj $this:text [format {
      Translation {translation -3 -4 0}
      FontStyle {size 1
	family SANS}
      Text3 {string "%s"}} $symname]

    assertIv
#    addNInlineObj $this:tabbox {TabBoxManip {}} pre
    moveObj $location
  }

  method assertLens {} {

    addNFrame $this
    addNObj $this:text [format {
      Translation {translation -4 -4 0}
      FontStyle {size 1
		 family SANS}
      Text3 {string "%s"}} $symname]

#antialiased fonts...
#    placeText $this:text $symname {-4 -4 0} {0 0 0} 1 0

    texture_stack $this:stack -texture_size $dim -texture_names $stackframes \
      -img_offset {0 0 2} -color $color -popout $popout

    $this:stack assertIv xy

    moveObj $location
  }

  method moveObj {pos} {

    moveNObj $this:trans $pos
    set location $pos
  }

  public local_members {keyframe stackframes color destination popout}
  public keyframe {}
  public stackframes {}
  public color {1 1 1}
  public destination {} ;#for fixed-destination demo
  public popout {1}

}

