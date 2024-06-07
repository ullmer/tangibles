proc intersect3 {l1 l2} {

    #puts "lopes intersect3"

    set intersect {}
    set justl1 {}
    set justl2 {}

    foreach el $l1 {

	set match 0

	foreach el2 $l2 {
	    
	    if {[string match $el $el2]} {
		set match 1
	    
		if {[lsearch $intersect $el]==-1} {
		    #puts "adding $el to intersect"
		    lappend intersect $el
		}
	    }
	}
	
	if {$match == 0 && [lsearch $justl1 $el]==-1} {
	    #puts "adding $el to justl1"
	    lappend justl1 $el
	}
	
    }
    
    foreach el $l2 {

	set match 0

	foreach el2 $l1 {
	    
	    if {[string match $el $el2]} {
		set match 1
	    }

	}
	if {$match == 0 && [lsearch $justl2 $el]==-1} {
	    #puts "adding $el to justl2"
	    lappend justl2 $el
	}
    }

    return [list $justl1 $intersect $justl2]
    

}

