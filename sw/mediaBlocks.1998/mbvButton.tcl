package require mbv::imagePane 1.0

package provide mbv::ivButton 1.0

itcl_class ivButton {
    inherit ivBase

    constructor {config} {}

    method assertIv {} {}

    public x_dim     {40}
    public y_dim     {30}

    public text_ {}
    public text_size {1}
    public click_handler {}
}

body ivButton::assertIv {} {
    if {$iv_asserted != 0} {return;}
    
  set hx [expr $x_dim / 2.]
  set hy [expr $y_dim / 2.]

    set ivgeom {
	NormalBinding {value PER_FACE}
	Normal {vector 0 1 0}
	Scale {scaleFactor 1 1 1}
	Coordinate3 {point [-$hx $hy 0, $hx $hy 0, $hx -$hy 0, 
	-$hx -$hy 0, -$hx $hy 0]}
	DrawStyle {style LINES lineWidth 1}
	FaceSet {numVertices 4}
	Translation {translation 0 0 1}
	DrawStyle {style FILLED lineWidth 0}
	Font  {name "Helvetica" size $text_size}    
	Text3 {string "$text_" justification CENTER}
    }
    set xivgeom [expandVar $ivgeom]

    if {$verbose} {puts "$this double check -- [getNObj $t]"}
    
    ## Add image to scene 
    addNObj [getIvName] $xivgeom
    
    ## Move image into place
    rotNObj  [getRotNode] $rotation_
    moveNObj [getPosNode] $position_

    bindNObj [getIvName] $click_handler

    set iv_asserted 1
}




