# Find points inside bbox, reporting their numbers
# Brygg Ullmer, MIT Media Lab TMG
# Begun 01/06/1997

# Again -- efficiency is *NOT* the goal! 8-)

proc between {a b test} {
  if {$a > $b} {
    if {$a >= $test && $test >= $b} {return 1}
  } else {
    if {$b >= $test && $test >= $a} {return 1}
  }
  return 0
}

proc inside {a b filename} {

  set index 0
  set f [open $filename r]

  set ax [lindex $a 0]
  set ay [lindex $a 1]
  set az [lindex $a 2]

  set bx [lindex $b 0]
  set by [lindex $b 1]
  set bz [lindex $b 2]

  while {![eof $f]} {
    set inline [gets $f]
    regsub {,} $inline {} inline

    set x [lindex $inline 0]
    set y [lindex $inline 1]
    set z [lindex $inline 2]

    if {[between $ax $bx $x] &&
	[between $ay $by $y] &&
	[between $az $bz $z]} {
      puts "$index   $x $y $z"
    }

    incr index
  }

  close $f
}

