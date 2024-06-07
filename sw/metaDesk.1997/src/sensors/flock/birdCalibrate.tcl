# Bird calibration code for reference frame of the metaDESK
# Brygg Ullmer, MIT Media Lab TMG
# Begun ~ 10/01/1996
# Itcl'ified 11/23/1996

package require tmg::base

package provide tmg:metadesk::sensor:flock.calibrate 1.0

##################### Flock Desk Calibration ########################

itcl_class flockDeskCalibration {

  inherit baseServer

  constructor {config} {
    set members [concat $members $local_members]
  }

  method mapAPos {pos} {
  
    set x [lindex $pos 0]
    set y [lindex $pos 1]
    set z [lindex $pos 2]
  
    set xa [expr $xs * ($x - $x_origin)  * $bird_to_world]
    set ya [expr $ys * ($y - $y_origin)  * $bird_to_world]
    set za [expr $zs * ($z - $z_origin)  * $bird_to_world]
  
    return [list $xa $ya $za] 
  }
  
  method mapAOrient {orient} {
  
    set h [lindex $orient 0]
    set p [lindex $orient 1]
    set r [lindex $orient 2]
  
    set ra [expr $hs * $h]
    set pa [expr $ps * $p]
    set ha [expr $rs * $r]
  
  ## adjust back to 0..360 degrees
    foreach el {ha pa ra} {
  
      if {[expr $$el > 360]} {set $el [expr $$el-360]}
      if {[expr $$el < 0]} {set $el [expr $$el+360]}
    }
  
    return [list $ha $pa $ra] 
  }

##### Local Members ####

  public local_members  {
    x_origin y_origin z_origin 
    h_origin p_origin r_origin
    lens_xoffset lens_yoffset lens_zoffset
    x_max y_max z_max
    xs ys zs hs ps ss
  }

  # Default origins (from left-bottom display corner)
  
  public x_origin 435
  public y_origin 790
  public z_origin 45
  
  public h_origin 0
  public p_origin 0
  public r_origin 0
  
  # Lens offsets
  
  public lens_xoffset -8.9
  public lens_yoffset 12.1
  public lens_zoffset -6.35
  
  # Active Envelope

  public x_max 80
  public y_max 65
  public z_max 100 ;# no actual bound, but...
  
  # Multiplicative between bird-units (mm) and worldspace-units (cm)
  
  public bird_to_world 0.1
  
  # Signs on degrees-of-freedom
  
  public xs -1.
  public ys -1.
  public zs +1.
  
  public hs +1.
  public ps -1.
  public rs -1.
 
}  

### END ###
  
