for i in *jpg
  do 
  bn=`basename $i .jpg`
  convert -geometry 25%x25% $i ../x4/$bn.png
done
