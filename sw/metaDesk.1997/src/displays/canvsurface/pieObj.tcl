# PieObject pie-menu'ish object underling
# Brygg Ullmer, MIT Media Lab TMG
# Begun 01/01/1997

package require tmg::canvsurface

package provide tmg::piemenuobj 1.0 

#################### Base Pie object ####################

itcl_class CvPieBase { ;# canvas pie base

 inherit base

 constructor {config} {
    set members [concat $members $local_members]
 }

 method constructPie {} {

   if {$canvsurface == {}} {
     puts "$this constructPie:  valid canvsurface does not exist; ignoring"
     return
   }
   
 ## Calc inner, outer diameters in canv coordspace
   set ox [$canvsurface widthWrl2Canv $outerdiameter]
   set oy [$canvsurface heightWrl2Canv $outerdiameter]
   set ox2 [expr $ox/2]
   set oy2 [expr $oy/2]
   
   set innerdiameter [expr $outerdiameter * $inoutratio]

   set ix [$canvsurface widthWrl2Canv $innerdiameter]
   set iy [$canvsurface heightWrl2Canv $innerdiameter]
   set ix2 [expr $ix/2]
   set iy2 [expr $iy/2]

   set construct {}

 ## Build wedges
   set curoffset $divoffset
   set offsetinc [expr 360. / $numdivs]

   for {set i 0} {$i < $numdivs} {incr i} {
     set color [lindex $outcolorlist $i]
     if {$color == {}} {set color [lindex $outcolorlist end]}

     lappend construct [concat \
      "arc -$ox -$oy $ox $oy -fill $color -outline $linecolor -start" \
      "$curoffset -extent $offsetinc -width $borderwidth"]

     set curoffset [expr $curoffset + $offsetinc]
   }

  ## Inner circle
   lappend construct [concat \
      "oval -$ix -$iy $ix $iy -fill $incolor -outline $linecolor" \
      "-width $borderwidth"]

 ## Submit for display

   $canvsurface addNObj $this $construct
 }

### Local members

  public local_members {
    canvsurface outerdiameter inoutratio divoffset numdivs incolor
    outcolorlist linecolor
  }

  public canvsurface {}

  public outerdiameter {7.0}
  public inoutratio    {0.4}

  public divoffset  {90}
  public numdivs    {4}

  public incolor      {red}
  public outcolorlist {
    blue yellow lightblue yellow blue yellow dodgerblue1 yellow } 
     # list of wedge colors to cycle through

  public linecolor    {black}
  public borderwidth  {3}
}

## END ##

