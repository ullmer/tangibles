for i in *jpg
  do 
  bn=`basename $i .jpg`
  convert -geometry 12%x12% $i ../x8/$bn.png
done
