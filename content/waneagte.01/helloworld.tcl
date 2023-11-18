# Hello, World Wish3 example
# Brygg Ullmer, MIT Media Lab VLW
# 11/22/1995

############################## Multiline ##############################

proc multiline {objlist offset} {

  set result "Separator \{\n"

  set vec [format {
     Translation {
       translation 0 %s 0
     }
    } $offset]

  append result {
    Scale {
      scaleFactor .1 .1 .1
    }
  }

  foreach obj $objlist {
    append result "Text3 \{\nstring \"" $obj "\"\n\}\n"
    append result $vec
  }

  append result "\}\n"

  return $result
}


proc hello {} {
  addNObj hello [multiline {{Hello,} {World}} -10]
}

proc shift {} {
  shiftNObj hello {0 0 0} {0 0 -15} 3 30
  tiAfter 5 {shiftNObj hello {0 0 0} {0 0 +15} 3 30}
  tiAfter 10 {shift}
}


hello
shift

