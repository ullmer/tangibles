
#Sample app to stick a barcode into 3D

global bc_num
set bc_num 0

proc barcodeCallback {barcode} {

	global bc_num
	incr bc_num

	addNObj bc$bc_num [format {Text3 {string "%s"}} $barcode]
	winMessage "barcode loaded"
}

initDDE barcodeCallback

addNObj cube {Cube {}}