# split list for excel
# brygg, 2002-05-12

while {![eof stdin]} {
  set inline [gets stdin]
  if {[llength $inline] != 3} {puts $inline; continue}
  set a1 [lindex $inline 0]
  set a2 [lindex $inline 1]
  set a3 [lindex $inline 2]
  puts "$a1,$a2,$a3"
}

