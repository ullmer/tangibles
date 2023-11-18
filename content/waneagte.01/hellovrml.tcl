# Hello, World Wish3 example
# Brygg Ullmer, MIT Media Lab VLW
# 11/22/1995

source filter-html.tcl

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
  addNObj hello [multiline {{Hello,} {VRML!}} -10]
  shiftNObj hello {0 0 0} {-2 6 0} 2 30
}

proc vrml {} {
 
  set url {http://www.virtualvegas.com/vrml/vvlink2.wrl}
  set virtualvegas [load_html $url]

  addNObj vv $virtualvegas
  bindNObj vv {puts "Gambling's bad for your health!"}
}

hello
vrml


