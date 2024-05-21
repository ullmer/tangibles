for i in *jpg
  do 
  bn=`basename $i .jpg`
  convert -geometry 6%x6% $i ../x16/$bn.png
done
