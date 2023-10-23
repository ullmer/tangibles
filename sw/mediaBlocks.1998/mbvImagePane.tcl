# ImagePane code
# By Phillip Tiongson and Brygg Ullmer, MIT Media Lab
# Begun 02/12/1998
# John Alex began modifications 02/23/98

package require pdf::base 1.0
package require pdf::digitals:textureCache 2.0
package require pdf::visuals:IvEngines 2.0

package require mbv::ivBase 1.0

package provide mbv::imagePane 1.0

#################### mbvImagePane #########################

itcl_class mbvImagePane {
  inherit ivBase

    constructor {config} {if {$verbose} {puts "Evaluating $this (pvImagePane)"}}

  method assertIv {} {}
  method retractIv {} {}

  method setTransp    {transpval} {}
  method setDrawStyle {drawstyle} {}

#transparency node for special highlight
  method getSpecTranspNode {} {return [format {%s:spectransp} $iv_name]}

  method getTranspNode {} {return [format {%s:transp} $iv_name]}
  method getScaleNode {} {return [format {%s:scale} $iv_name]}
  method getExtraTransNode {} {return [format {%s:extratrans} [getIvName]]}
  method getExtraRotNode1 {} {return [format {%s:extrarot1} [getIvName]]}
  method getExtraRotNode2 {} {return [format {%s:extrarot2} [getIvName]]}
  method getExtraRotNode3 {} {return [format {%s:extrarot3} [getIvName]]}
  method getExtraRotNode4 {} {return [format {%s:extrarot4} [getIvName]]}

  method containsPt {relpt} {}
  method enableTexture {} {}
  method disableTexture {} {}

  method highlight {} {}
  method unhighlight {} {}
  method isHighlighted {} {return is_highlighted;}

  method specHighlight {} {}
  method specUnhighlight {} {}
  method isSpecHighlighted {} {return is_highlighted;}
 ## Local members

  public anim_mgr      {}
  public texture_cache {}
  public texture_name  {}
  public image_fname   {}

  public line_width {1}

  public x_dim     {40}
  public y_dim     {30}
  public z_offset  {0}

  public scale_ {1 1 1}
  public transparency_val {0.}
  public draw_style    {FILLED}

  protected is_highlighted {0}
  protected is_spec_highlighted {0}
}


########################################################
#################### mbvImagePane #########################
########################################################

#################### mbvImagePane assertIv #########################

body mbvImagePane::assertIv {} {

    if {$iv_asserted != 0} {return;}

  set hx [expr $x_dim / 2.]
  set hy [expr $y_dim / 2.]

 set texture_name [format {%s:texture} [getIvName]]
  if {$texture_cache != {}} { ;# Use texture cache
    set tname [$texture_cache getTextureHandle $image_fname]

    set textureLine "DEF ivUse Info \{string \"$tname\"\}"
    #set textureLine "USE $t" ;#DOESN'T WORK because of way Iv execution
    #context is managed

  } else {
    puts "not using texcache"
    set textureLine \
	"DEF $texture_name Texture2 \{filename \"\" model DECAL\}"
#	"DEF $texture_name Texture2 \{filename \"$image_fname\" model DECAL\}"

#for debugging
#    puts "textureline is $textureLine"
  }

  set draw_style [format {%s:draw_style} [getIvName]]
  set transp  [getTranspNode]
  set spectransp  [getSpecTranspNode]
  set linecolor  [format {%s:linecolor}  [getIvName]]
  set coord  [format {%s:coordinate}  [getIvName]]
  set scale  [getScaleNode]
  set trans [getPosNode]
  set extratrans [getExtraTransNode]
  set extrarot1 [getExtraRotNode1]
  set extrarot2 [getExtraRotNode2]
  set extrarot3 [getExtraRotNode3]
  set extrarot4 [getExtraRotNode4]

  set ivgeom {
    DEF $extrarot1 Rotation {rotation 1 0 0   0.}
    DEF $extrarot2 Rotation {rotation 1 0 0   0.}
    DEF $extrarot3 Rotation {rotation 1 0 0   0.}
    DEF $extratrans Translation {translation 0 0 0}
    DEF $extrarot4 Rotation {rotation 1 0 0   0.}
    TextureCoordinate2 {point [0 1, 1 1, 1 0, 0 0]}
    Complexity {textureQuality 1.0}
    $textureLine
    NormalBinding {value PER_FACE}
    Normal {vector 0 1 0}
    DEF $scale Scale {scaleFactor $scale_}
    DEF $coord Coordinate3 {point [-$hx $hy $z_offset, $hx $hy $z_offset, $hx -$hy $z_offset, 
       -$hx -$hy $z_offset, -$hx $hy $z_offset]}
    DEF $draw_style DrawStyle {style LINES lineWidth 1}
#    DEF $transp  Material  {transparency $transparency_val}
    FaceSet {numVertices 4}
    Translation {translation 0 0 .1}
    Texture2 {filename ""}
    DrawStyle {style LINES lineWidth $line_width}
    DEF $linecolor BaseColor {rgb 1 1 1}
    FaceSet {numVertices 4}
    Translation {translation 0 0 -.05}
    DEF $spectransp Material {transparency 1}
    BaseColor {rgb 0 1 0}
    FaceSet {numVertices 4}
  }
  #set xivgeom [expandVar $ivgeom]
  set xivgeom [subst -nocommands $ivgeom]

  if {$verbose} {puts "$this double check -- [getNObj $t]"}

  ## Add image to scene 
  addNObj [getIvName] $xivgeom

#  puts "[getNObj [getIvName]]"
#  puts "ivname is [getIvName]"
  ## Move image into place

  rotNObj  [getRotNode] $rotation_
  moveNObj [getPosNode] $position_

  set iv_asserted 1
}

#################### enableTexture/disableTexture #########################

body mbvImagePane::enableTexture {} {
#    puts "enabling texture $image_fname"
  if {$texture_cache != {}}  {
      puts "haven't written enabletextures for texture cache"
      setDrawStyle "FILLED"
  } else {
      set texture_name [format {%s:texture} [getIvName]]
      tweakNObj $texture_name "filename \"$image_fname\" model DECAL"
      setDrawStyle "FILLED"
  }

}

body mbvImagePane::disableTexture {} {
  if {$texture_cache != {}}  {
      puts "haven't written disabletextures for texture cache"
      setDrawStyle "LINES"
  } else {
      set texture_name [format {%s:texture} [getIvName]]
      tweakNObj $texture_name "filename \"\" model DECAL"
      setDrawStyle "LINES"
  }

}

#################### setTransp / DrawStyle #########################

body mbvImagePane::setTransp    {transpval} {
  tweakNObj [getTranspNode] "transparency $transpval"
}

body mbvImagePane::setDrawStyle {ndraw_style} {
  set drawst [format {%s:draw_style} [getIvName]]
  set draw_style $ndraw_style

  tweakNObj $drawst "style $draw_style"
}

#################### mbvImagePane retractIv #########################

body mbvImagePane::retractIv {} {

  if {$iv_asserted == 0} {return}
  delNObj [getIvName]
  set iv_asserted 0
}

body mbvImagePane::highlight {} {
  set linecolor  [format {%s:linecolor}  [getIvName]]

  tweakNObj $linecolor "rgb 1 0 0"
  set is_highlighted 1
}

body mbvImagePane::unhighlight {} {
  set linecolor  [format {%s:linecolor}  [getIvName]]

  tweakNObj $linecolor "rgb 1 1 1"
  set is_highlighted 0
}

body mbvImagePane::specHighlight {} {
    
  tweakNObj [getSpecTranspNode] "transparency 0"
  puts "tweaked [getSpecTranspNode] [getNObj [getIvName]]"
  set is_spec_highlighted 1
}

body mbvImagePane::specUnhighlight {} {
  set spectransp [getSpecTransp]

  tweakNObj [getSpecTranspNode] "transparency 1"
  set is_spec_highlighted 0
}

#1 if it does, 0 if it doesn't
body mbvImagePane::containsPt {relpt} {
    set x [lindex $relpt 0]
    set y [lindex $relpt 1]
    set z [lindex $relpt 2]

    if {$z != 0} {puts "asking imagepane for pt $relpt that has a non-zero z component! this is worrisome, but we're ignoring z anyway";}

    set yhalf [expr $y_dim * [lindex $scale_ 1] * .5]
    set xhalf [expr $x_dim * [lindex $scale_ 0] * .5]
    if {$y < [expr -$yhalf]} {return 0;}
    if {$x < [expr -$xhalf]} {return 0;}

    if {$y > $yhalf} {return 0;}
    if {$x > $xhalf} {return 0;}
    return 1;
}

itcl_class fallableImagePane {
    inherit mbvImagePane

    constructor {config} {}
    method makeCopy {} {}
    method fall {start end} {}

    public newcopynum {0}
    public animduration {.5}
}

#start and end should be in the form "x.0, y.0, z.0"
#so that floating-point arithmetic is used

body fallableImagePane::fall {start end} {
    set transEventName "::fallevent[getIvName]"

    set x1 [lindex $start 0]
    set y1 [lindex $start 1]
    set z1 [lindex $start 2]
    set x2 [lindex $end 0]
    set y2 [lindex $end 1]
    set z2 [lindex $end 2]

    set anum [expr $y2 - $y1]
    set adenom [expr ($x2 * $x2) - ($x1 * $x1)]
    if {$adenom == 0.0} {
	#not going anywhere in x; just translate directly!
	moveNObj [getPosNode] $end
	set endevent [$anim_mgr genName]
	manualFireEngine $endevent -autoDelete 1;
	$anim_mgr addEvent $endevent;

	tiAfter .1 "$endevent fire";
	return $endevent;
    }
    set a [expr $anum / $adenom]
    set b [expr $y1 - [expr $a * $x1 * $x1]]

#    puts "a is $anum / $adenom == $a, b is $b"
#    puts "$x1, $y1, calced y [expr ($a * $x1 * $x1) + $b]"
#    puts "$x2, $y2, calced y [expr ($a * $x2 * $x2) + $b]"
    set calcFxn {
        set xt [expr $x1 + ($x2 - $x1) * $t];      
        set zt [expr $z1 + ($z2 - $z1) * $t];      
        set yt [expr $a * $xt * $xt + $b];      
#	puts "$x1 - $xt - $x2, y is $yt"
        set newpos [list $xt $yt $zt];       
#	set newpos [add3D "$basepos" $offset];   
        return $newpos 
    }

    #replace the vars in calcFxn that we already know
    regsub -all {\$basepos} $calcFxn $position_ calcFxn
    regsub -all {\$x2} $calcFxn $x2 calcFxn
    regsub -all {\$x1} $calcFxn $x1 calcFxn
    regsub -all {\$z2} $calcFxn $z2 calcFxn
    regsub -all {\$z1} $calcFxn $z1 calcFxn
    regsub -all {\$a} $calcFxn $a calcFxn
    regsub -all {\$b} $calcFxn $b calcFxn

#    puts "calcFxn is $calcFxn" 
    shiftCurveEngine $transEventName -transName [getPosNode] -endVal 1.0 \
           -beginVal 0.0 -autoDelete 1 -fullDuration $animduration \
	   -calc_pos_fxn $calcFxn
    
    $anim_mgr addEvent $transEventName
    return $transEventName
}


body fallableImagePane::makeCopy {} {

    set newname ::[getIvName]copy$newcopynum
    fallableImagePane $newname \
            -animduration $animduration \
	    -texture_cache $texture_cache \
	    -texture_name $texture_name \
	    -image_fname $image_fname \
	    -x_dim $x_dim \
	    -y_dim $y_dim \
	    -z_offset $z_offset \
	    -transparency_val $transparency_val \
	    -draw_style $draw_style  \
     -line_width $line_width \
     -position_ $position_ \
     -anim_mgr $anim_mgr
    set newcopynum [expr 1+ $newcopynum];
    return $newname;
}

#################### magnifiableImagePane  #########################

itcl_class magnifiableImagePane {
  inherit mbvImagePane

    constructor {config}  {set basepos $position_}

    method magnify {} {}
    method unmagnify {} {}
    method setBasePos {p} {set basepos $p}
    method makeCopy {} {}

##Local members
    public magval {3.0}
    public magoffset {200 100 10}

    public basepos {0 0 0}
    public animduration {.5}

    public newcopynum {0}
}


body magnifiableImagePane::makeCopy {} {

#    puts "newcopynum is $newcopynum"
    set newname ::[getIvName]$newcopynum
#    puts "newname is $newname"
    magnifiableImagePane $newname -magval $magval \
	    -magoffset $magoffset \
	    -basepos $basepos \
	    -animduration $animduration \
	    -texture_cache $texture_cache \
	    -texture_name $texture_name \
	    -image_fname $image_fname \
	    -x_dim $x_dim \
	    -y_dim $y_dim \
	    -z_offset $z_offset \
	    -transparency_val $transparency_val \
	    -draw_style $draw_style  \
            -position_ $position_
    set newcopynum [expr 1+ $newcopynum];
#    puts "new num is $newcopynum"
    return $newname;
}

#################### magnifiableImagePane magnify  #########################

body magnifiableImagePane::magnify {} {
    set magEventName event1[getIvName]

    scaleEngine $magEventName -scale_name [$this getScaleNode] \
	 -endVal "$magval $magval $magval" -beginVal "1 1 1"  \
	 -autoDelete 1 -fullDuration $animduration
    $anim_mgr addEvent $magEventName

    set newpos [add3D $basepos $magoffset]

    $anim_mgr shiftObj [getPosNode] $basepos $newpos $animduration
}


#################### magnifiableImagePane unmagnify  #########################

body magnifiableImagePane::unmagnify {} {
    set magEventName "::event3[getIvName]"

    puts "adding resize engine"
    scaleEngine $magEventName -scale_name [$this getScaleNode] \
	    -beginVal "$magval $magval $magval" -endVal "1 1 1"  \
	    -autoDelete 1 -fullDuration $animduration
    $anim_mgr addEvent $magEventName

    set newpos [add3D $basepos $magoffset]

    $anim_mgr shiftObj [getPosNode] $newpos $basepos $animduration
}

## END ##

