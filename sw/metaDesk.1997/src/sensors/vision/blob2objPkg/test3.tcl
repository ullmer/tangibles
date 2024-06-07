
load ./visionPackage.so


#set out [open test.out w]

set oldBlobs {}
set newBlobs {}

listbox .l 
pack .l


proc updateList {list} {
    .l delete 0 end
    foreach el $list {
	set name [lindex $el 0]
	set xpos [lindex [lindex $el 1] 0]
	set ypos [lindex [lindex $el 1] 1]

	.l insert end "$name:$xpos:$ypos"
    }
}


while {1} {

    update idletasks
    set notdone 1
    while {$notdone} {
	
	gets stdin newBlob
	
	if { [string match "EOF" [lindex $newBlob 0]] == 1} {
	    puts "DONE."
	    exit
	}
	if { [string match "0" [lindex $newBlob 0]] == 1} {
	    set notdone 0
	    set lastBlob $newBlob
	} else {
	    lappend newBlobs $newBlob
	}
    }
    if {[llength $newBlobs] != 0} {
#	set labelRes [labelScene $oldBlobs $newBlobs {media dome}]
	set labelRes [labelScene $oldBlobs $newBlobs {dome media}]
	#set labelRes [labelScene $oldBlobs $newBlobs -autolabel]
	#set labelRes [labelScene last $newBlobs -autolabel]	
	#puts $out $labelRes
	puts $labelRes
	set oldBlobs [lindex $labelRes 0]
	updateList $oldBlobs
    }
    set newBlobs {}
    lappend newBlobs $lastBlob
    
}

