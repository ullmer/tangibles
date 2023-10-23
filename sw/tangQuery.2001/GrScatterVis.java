/// Plot test
/// By Brygg Ullmer, MIT Media Lab
/// Begun November 1, 2001
///
/// Based on threading template by Ben Fry (fry@media.mit.edu),
/// 4/18/2001, and WinHelp Java Tutorial: AnimatorApplication.java,
/// Arthur van Hoff

import java.util.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.awt.image.*;

import javax.swing.*;
import java.io.*;
import java.lang.reflect.*;

///////////////////////////////////////////////////////////
////////////////////  GrScatterVis ////////////////////////////
///////////////////////////////////////////////////////////

public class GrScatterVis {

/////////////  METHODS ///////////////

// static void main(String args[])
// public GrScatterVis()
// public run()

/////////////  MEMBERS ///////////////

  QRackVis parentVis = null;

  QRackMgr  qrackMgr = null;
  BldgDbMgr    dbMgr = null;

  String lastQuery = "", currentQuery = "";

  PTokModel xAxisTok = null, yAxisTok = null;

 // Axis description

  //Color axisColor = new Color(100, 100, 0);
  Color axisColor = new Color(100, 100, 100);

  int axisWidth = 2;

//  int yaxisX  = 300;
//  int yaxisY1 = 50;
//  int yaxisY2 = 800;
//
//  int xaxisY  = 800;
//  int xaxisX1 = 300;
//  int xaxisX2 = 1200;

//380

  int yaxisX  = 290;
  int yaxisY1 = 340;
  int yaxisY2 = 50;

  int xaxisY  = 50;
  int xaxisX1 = 290;
  int xaxisX2 = 25;

  String xAxisLabel = "";
  String yAxisLabel = "";
//  Color  axisLabelColor = new Color(50, 50, 50);
  Color  axisLabelColor = new Color(225, 225, 225);

  int xAxisTextY = 16;
  int yAxisTextX = 318;

  int colorTagSize = 8;
  int colorTagPadX = -5;
  int colorTagPadY = -7;

  Font axisLabelFont = new Font("Verdana", Font.PLAIN, 18);
  Font tickFont      = new Font("Verdana", Font.PLAIN, 8);
  Font discreteFont  = new Font("Verdana", Font.PLAIN, 12);

  Color tickFontColor = new Color(50, 50, 50);

  // Axis guide

   //Color guideColor = new Color(150, 150, 150);
   //Color guideColor = new Color(200, 200, 200);
   //Color guideColor = new Color(175, 175, 175);

   Color guideColor = new Color(230, 230, 230);

   int guideWidth = 2;
   //int guideWidth = 4;

   Color zeroXingColor = new Color(120, 120, 120);

//   Jitter yJitter = new Jitter(16, 500);
//   Jitter xJitter = new Jitter(16, 500);

   Jitter jitterX = new Jitter(16, 500);
   Jitter jitterY = new Jitter(16, 500);
   int jitterBase  = 18;

   int discreteHighlightWidth = 24;

   Color discreteBarInactive = new Color(190, 190, 190);
   Color discreteBarActive   = new Color(140, 140, 140);


  // Data 

    //Color brightDataColor = new Color(225, 225, 225);
    //Color dimDataColor    = new Color(150, 150, 150);

    Color brightDataColor = new Color(240, 240, 240);
    Color dimDataColor    = new Color(160, 160, 160);

    //int   dataLineWidth = 1;
    int   dataLineWidth = 5;

    //int   dataSqWidth   = 4;
    //int   dataSqWidth   = 8;
    int   dataSqWidth   = 2;
//    int   dataSqWidth   = 3;

    //int  tickLength = 4;
    int  tickLength = 5;

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

////////////////////  GrScatterVis /////////////////////////////

  public GrScatterVis(QRackMgr mgr, QRackVis parentVis) {

    this.parentVis = parentVis;

    qrackMgr = mgr;
    dbMgr    = (BldgDbMgr) qrackMgr.getInterp().getDbMgr();

  }
////////////////////  leftmost Ptok Vect /////////////////////////////

  // calculates the indices of the "first" and "second" ptoks (mapping
  // to X and Y), returning their indices in an int[2].  -1 = not present

  // this is a bit crazy, but... it appears it's necessary, given the 
  // current code state

 public int[] leftmostPTokVect(Vector ptokVect) {

   int result[] = new int[2];

   int numEls = ptokVect.size();

   if (numEls == 0) {
     result[0] = -1;
     result[1] = -1;
     return result;
   }

   if (numEls == 1) {
     result[0] = 0;
     result[1] = -1;
     return result;
   }

   // otherwise, search for min; scratch that, now Max

   //int minLoc = 12;
   //int minIdx = -1;

   int maxLoc = -1;
   int maxIdx = -1;

   for (int i=0; i<numEls; i++) {

     PTokModel ptok = (PTokModel) ptokVect.elementAt(i);
     if (ptok.currentCell > maxLoc) {
       maxLoc = ptok.currentCell;
       maxIdx = i;
     }
   }

   result[0] = maxIdx;

   // OK, find the next smallest

   int maxLoc2 = -1;
   int maxIdx2 = -1;

   for (int i=0; i<numEls; i++) {
     PTokModel ptok = (PTokModel) ptokVect.elementAt(i);
     if (ptok.currentCell != maxLoc && ptok.currentCell > maxLoc2) {
       maxLoc2 = ptok.currentCell;
       maxIdx2 = i;
     }
   }

   if (result[1] == -1) {
     dbg("leftmostPTokVect: problematic bogosity.");
   }

   result[1] = maxIdx2;

   return result;  // gakk....
 }

////////////////////  additionalCellsEmpty /////////////////////////////

  public boolean additionalCellsEmpty() {

    WRackModel wrackModel = qrackMgr.getModel();

    if (wrackModel.getCellContents(1) == null &&
        wrackModel.getCellContents(0) == null) {return true;}
    return false;
  }

////////////////////  update Axes /////////////////////////////

//  Reworking this : hard linking to particular cells.

  public void updateAxesFromModel() {

   try {

    WRackModel wrackModel = qrackMgr.getModel();

    if (wrackModel == null) {
      dbg("updateAxesFromModel problem: model is null!");
      return;
    }

    Vector ptoks = wrackModel.ptoksActive.getActivePToks();

    int numEls  = ptoks.size();
//    int xyIdx[] = leftmostPTokVect(ptoks);

    xAxisLabel = "x";
    xAxisTok   = null;

    yAxisLabel = "y";
    yAxisTok   = null;

    PTokModel ptok = wrackModel.getCellContents(2);

    if (ptok != null) { // X

      if (ptok.discreteParam) { 
        xAxisTok = ptok;
	xAxisLabel = ptok.paramName;
      } else {

        xAxisTok   = ptok;
        xAxisLabel = ptok.visLabel;
      }
    } else {
      xAxisTok = null;
    } 
 
    ptok = wrackModel.getCellContents(3);
  
    if (ptok != null) { // Y

      if (ptok.discreteParam) { 
        yAxisTok = ptok;
	yAxisLabel = ptok.paramName;
      } else {

        yAxisTok   = ptok;
        yAxisLabel = ptok.visLabel;
      }
    } else {
      yAxisTok = null;
    } 
  
    if (xAxisTok != null && xAxisTok.boolParam) { // this isn't yet supported

      dbg("bool Param for X axis isn't yet supported.  swapping");
 
      PTokModel tmpTok = xAxisTok; 
      String  tmpLabel = xAxisLabel; 
      
      xAxisTok   = yAxisTok; 
      xAxisLabel = yAxisLabel; 
      
      yAxisTok   = tmpTok; 
      yAxisLabel = tmpLabel; 
    } 
   } catch (Exception e) {
     dbg("updateAxesFromModel exception: " + e.toString());
     e.printStackTrace();
   }
  }

////////////////////  scale coord /////////////////////////////

/*
  public int[] scaleCoord(float lat, float lon) {

    float relX = (lat - minLat) / latRange;
    float relY = (lon - minLon) / lonRange;

    int result[] = new int[2];

    result[0] = (int)(relX * (float) parentVis.panelWidth);
    result[1] = (int)(relY * (float) parentVis.panelHeight);

    return result;
  }
*/

//////////////////// plotAxis /////////////////////////////

  public void plotAxis(Graphics2D h) {

    AffineTransform baseTransform = h.getTransform();

    h.setColor(axisColor);
    h.setStroke(new BasicStroke(axisWidth));

  // Draw axis text -- X

    if (xAxisTok != null && xAxisTok.discreteParam == true) {
      plotDiscreteGuides(h, xAxisTok, 0, false);
    } 

    h.setFont(axisLabelFont);
    int textWidth = h.getFontMetrics().stringWidth(xAxisLabel);

    int x1 = xaxisX1 + (xaxisX2 - xaxisX1)/2;
    int y1 = xAxisTextY;

//    h.fillRect(x1, y1 + 20, 2, 2);

    x1 = xaxisX1 + (xaxisX2 - xaxisX1)/2 + textWidth/2;

//    h.fillRect(x1, y1 + 20, 2, 2);

    if (xAxisTok != null) {

      x1 -= textWidth;
      y1 -= 3;

      h.setColor(xAxisTok.paramColor);
      h.fillRoundRect(x1, y1, textWidth+6, 21, 5, 5);

      x1 += textWidth + 3;
      y1 += 5;
    }

    h.translate(x1,y1);
    h.rotate(Math.PI);

    if (xAxisTok != null) {
      h.setColor(axisLabelColor);
    } else {
      h.setColor(Color.gray);
    }

//    if (xAxisTok == null || xAxisTok.discreteParam == false) {
//    if (xAxisTok == null || xAxisTok.discreteParam == false) {
    h.drawString(xAxisLabel, 0, 0);
//    }

    h.setTransform(baseTransform);

  // Draw axis text -- Y

    if (yAxisTok != null && yAxisTok.discreteParam == true) {
      plotDiscreteGuides(h, yAxisTok, 1, false);

      if (xAxisTok != null && xAxisTok.discreteParam == true) {
        plotDiscreteGuides(h, xAxisTok, 0, true);
      }
    } 

    h.setColor(axisLabelColor);
    h.setFont(axisLabelFont);

    textWidth = h.getFontMetrics().stringWidth(yAxisLabel);

    x1 = yAxisTextX + textWidth;
    y1 = yaxisY1 + (yaxisY2 - yaxisY1)/2;

    if (yAxisTok != null && yAxisTok.discreteParam == true) {
      y1 -= 180;
      //y1 += 155;

      x1 = parentVis.panelWidth - 20 - textWidth;

      //if (textWidth < 80) { x1 -= textWidth/2; }
      // complete hack, but running out of time
    }

    if (yAxisTok != null) {

      if (yAxisTok.discreteParam) {
        //x1 += textWidth;
      } else {
        x1 -= textWidth;
      }

      y1 -= 3;

      h.setColor(yAxisTok.paramColor);
      h.fillRoundRect(x1, y1, textWidth + 6, 21, 5, 5);

      x1 += textWidth + 3;

      y1 += 5;
    }

    h.translate(x1,y1);
    h.rotate(Math.PI);

    if (yAxisTok != null) { 
      h.setColor(axisLabelColor);
    } else {
      h.setColor(Color.gray);
    }
 
//    if (yAxisTok != null) { 
      h.drawString(yAxisLabel, 0, 0);
//    }

    h.setTransform(baseTransform);

   // Draw axis lines

    h.setColor(axisColor);

    h.drawLine(yaxisX, yaxisY1, yaxisX, yaxisY2);
    h.drawLine(xaxisX1, xaxisY, xaxisX2, xaxisY);


/*
    x1 = yAxisTextX;
    y1 = yaxisY1 + (yaxisY2 - yaxisY1)/2 - textWidth/2;

    AffineTransform baseTransform = h.getTransform();
    h.translate(x1, y1);
    h.rotate(Math.PI/2);

    h.drawString(yAxisLabel, 0, 0);
    h.rotate(3*Math.PI/2);
    h.setTransform(baseTransform);
*/
  }

//////////////////// plotDiscreteGuides /////////////////////////////


  public void plotDiscreteGuides(Graphics2D h, PTokModel ptok, int axis,
                                boolean plotSelectedOnly) {

// axis: 0->x, 1->y

  // Check for problems

    if (ptok == null) {
      dbg("plotDiscreteGuides: null ptok!"); 
      return;
    }

    if (ptok.pwheel == null) {
      dbg("plotDiscreteGuides: null ptok.pwheel!"); 
      return;
    }

    if (ptok.discreteParam == false) {

      dbg("plotDiscreteGuides bug: passed non-discrete param " +
          ptok.paramName);
      return;
    }

   // Setup vals

/* // oops; didn't need any of those! :-)

    Vector allRecs = dbMgr.getAllRecs();
    BldgRecord br = (BldgRecord) allRecs.elementAt(0);

    String fieldName = ptok.pwheel.valsName;
    dbg("field name: " + fieldName);

    Field pfield = br.brGetField(fieldName);
    if (pfield == null) {dbg("pDG problem: pfield = null!"); return;}

    String param = br.getString(pfield); 
    if (param == null) { dbg("pDG: null param"); return; }  // RETHINK?
*/

    int xPixRange = (int) xaxisX1 - xaxisX2;
    int yPixRange = (int) yaxisY1 - yaxisY2;

    int pixBase  = (axis == 1 ? xaxisX2 - 25: yaxisY2 - 30);
    int pixRange = (axis == 1 ? xPixRange + 120: yPixRange + 30);

    int opixBase  = (axis == 0 ? xaxisX1 : yaxisY1);  // orthogonal axis
    int opixRange = (axis == 0 ? xPixRange : yPixRange);

    int numEls   = ptok.pwheel.getSize(); 

    if (numEls == 0) {return;}

    int axIncr   = opixRange / numEls;
    int selectedVal = ptok.pwheel.selectedVal;

   // Plot bars

    int orthogOffset = 0;

    if (axis == 0) {
      orthogOffset = opixRange - opixBase + discreteHighlightWidth / 2 + 40;
    } else {
      orthogOffset = opixBase - discreteHighlightWidth/2 - 24;
    }


    AffineTransform baseTransform = h.getTransform();

    if (axis == 1) {
      h.setFont(discreteFont);
    } else {
      h.setFont(tickFont);
    }

    for (int i=0; i<numEls; i++) {

      String field = ptok.pwheel.getVal(numEls - i - 1); 
      boolean drawit = true;

    // select color
      if (i == numEls - selectedVal - 1) {
	h.setColor(discreteBarActive);

      } else {
	h.setColor(discreteBarInactive);
        if (plotSelectedOnly == true) {drawit = false;}
      }

    //draw bar  

    if (drawit) {
      if (axis == 1) {
        h.fillRect(pixBase, orthogOffset, 
	           pixRange, discreteHighlightWidth);
      } else {
        h.fillRect(orthogOffset, pixBase + 18,
	           discreteHighlightWidth, pixRange);
      }

    //draw text

      if (axis == 1) {
        h.translate(pixBase + pixRange - 18, orthogOffset + 8);
        h.rotate(Math.PI);
        h.setColor(new Color(220, 220, 220));

        h.drawString(field, 0, 0);
        h.setTransform(baseTransform);

      } else { // axis == 0

        int textWidth = h.getFontMetrics().stringWidth(field);
        int xstr      = orthogOffset + 12 + textWidth/2;

        h.translate(xstr, pixBase + 20);

        h.rotate(Math.PI);
        h.setColor(new Color(50, 50, 50));

        h.drawString(field, 0, 0);
        h.setTransform(baseTransform);
      }
    }

      if (axis == 1) {
        orthogOffset -= axIncr;
      } else {
        orthogOffset += axIncr;
      }
    }
  }

//////////////////// plotAxisGuides /////////////////////////////

  public void plotAxisGuides(Graphics2D h) {

   // Handle X grids

     //h.setStroke(new BasicStroke(guideWidth));
     float dash[] = {10.0f};

     h.setStroke(new BasicStroke(guideWidth, BasicStroke.CAP_BUTT, 
                  BasicStroke.JOIN_MITER, 2.0f, dash, 0.0f));

    if (xAxisTok != null && xAxisTok.discreteParam == false) {

      double x1f = xAxisTok.getRatioUpper(); 

      int x1 = (int) (xaxisX1 + (xaxisX2 - xaxisX1) * x1f);

      int y1 = yaxisY1;
      int y2 = yaxisY2;

// dbg("x axis guide (" + xAxisTok.paramName + "): " + x1f + " + " + x1);

      h.setColor(guideColor);

      h.drawLine(x1, y1, x1, y2);
    }


   // Handle Y grids

    if (yAxisTok != null && yAxisTok.discreteParam == false) {

      double y1f = 1. - yAxisTok.getRatioUpper(); 

      int y1 = (int) (yaxisY1 + (yaxisY2 - yaxisY1) * y1f);

//dbg("y axis guide: " + y1f + " + " + y1);

      int x1 = xaxisX1;
      int x2 = xaxisX2;

      h.setColor(guideColor);

      h.drawLine(x1, y1, x2, y1);
    }
  }

////////////////////  plotXZeroCrossing /////////////////////////////

  public void plotXZeroCrossing(Graphics2D h) {

     if (xAxisTok == null || xAxisTok.getAbsLower() >= 0) { 
       return; // we're not needed
     }

     int xPixRange = (int) xaxisX2 - xaxisX1;

     double xval =    0 - xAxisTok.getAbsLower();
     double x1f  = xval / xAxisTok.getAbsRange();

     int x0 = xaxisX1 - dataSqWidth;
     int x1 = (int) (x0 + xPixRange * x1f);

     int y1 = yaxisY1;
     int y2 = yaxisY2;

   // Draw it
     float dash[] = {3.0f};

     h.setStroke(new BasicStroke(1, BasicStroke.CAP_BUTT, 
                  BasicStroke.JOIN_MITER, 2.0f, dash, 0.0f));

     h.setColor(zeroXingColor);

     h.drawLine(x1, y1, x1, y2);
   }

////////////////////  plotYZeroCrossing /////////////////////////////

  public void plotYZeroCrossing(Graphics2D h) {

     if (yAxisTok == null || yAxisTok.getAbsLower() >= 0) { 
       return;  // we're not needed
     }

     int yPixRange = yaxisY2 - yaxisY1;

     double yval =    0 - yAxisTok.getAbsLower();
     double y1f  = yval / yAxisTok.getAbsRange();

     int y0 = yaxisY1 + dataSqWidth;
     int y1      = (int) (y0 + yPixRange * y1f);

     int x1 = xaxisX1;
     int x2 = xaxisX2;

   // Draw it
     float dash[] = {3.0f};

     h.setStroke(new BasicStroke(1, BasicStroke.CAP_BUTT, 
                  BasicStroke.JOIN_MITER, 2.0f, dash, 0.0f));

     h.setColor(zeroXingColor);

     h.drawLine(x1, y1, x2, y1);
  };

////////////////////  calcTickIncrement /////////////////////////////

  public int calcTickIncr(int range) {

     int tikIncrement = 1; // make assumption that all tik spans are >= 1 unit
     int tikMultiplier = 1;

     if (range > 100) { //we need to find the multiplier

       int tikMag = (int) ((Math.log(range)/Math.log(10)) - 1);
       tikMultiplier = (int) Math.pow(10, tikMag);
       range /= tikMultiplier;
     }

     if        (range < 10)  {
       tikIncrement = 1;

     } else if (range < 20) {
       tikIncrement = 2;

     } else if (range < 50) {
       tikIncrement = 5;

     } else { // up to 100
       tikIncrement = 10;
     }

     tikIncrement *= tikMultiplier;
     return tikIncrement;
   }

////////////////////  calcMinTick /////////////////////////////

  public int calcMinTick(int minVal, int tikIncr) {

     if (minVal % tikIncr == 0) {return minVal;}

     int result = tikIncr * (minVal / tikIncr + 1);
     return result;
  }

////////////////////  plotXTick /////////////////////////////

  public void plotXTicks(Graphics2D h) {

    if (xAxisTok == null || xAxisTok.discreteParam) {
      return; 
    }

    int tikIncr = 1; // make assumption that all tik spans are >= 1 unit

    int    xPixRange = xaxisX2 - xaxisX1;
    double xValRange = xAxisTok.getAbsRange();

    int xValMin = (int) xAxisTok.getAbsLower();
    int xValMax = (int) xAxisTok.getAbsUpper();

    int x0 = xaxisX1;

  // Draw it

    h.setStroke(new BasicStroke(axisWidth));
    h.setFont(tickFont);

    int tickIncr = calcTickIncr((int) xValRange);
    int minTick  = calcMinTick(xValMin, tickIncr);

    //dbg("minTick: " + minTick + " | tickIncr: " + tickIncr);
    AffineTransform baseTransform = h.getTransform();

    for (int x = minTick; x <= xValMax; x += tickIncr) {
      double x1f = (double) (x - xValMin) / xValRange;
      int x1      = (int) (x0 + xPixRange * x1f);

      plotXTick(h, x1, x);
      h.setTransform(baseTransform);
    }
  }

////////////////////  plotXTick /////////////////////////////

  public void plotXTick(Graphics2D h, int xPix, int xVal) {
    int y1 = yaxisY2;
    int y2 = y1 - tickLength;

    h.setColor(axisColor);
    h.drawLine(xPix, y1, xPix, y2);

    String tickText = Integer.toString(xVal);
    int textWidth = h.getFontMetrics().stringWidth(tickText);

    int x1 = xPix + textWidth/2;
    y1 -= 13;

    h.setColor(tickFontColor);
    h.translate(x1,y1);
    h.rotate(Math.PI);

    h.drawString(tickText, 0, 0);
  }

////////////////////  plotYTick /////////////////////////////

  public void plotYTicks(Graphics2D h) {

    if (yAxisTok == null || yAxisTok.discreteParam) {
      return; 
    }

    int tikIncr = 1; // make assumption that all tik spans are >= 1 unit

    int    yPixRange = yaxisY2 - yaxisY1;
    double yValRange = yAxisTok.getAbsRange();

    int yValMin = (int) yAxisTok.getAbsLower();
    int yValMax = (int) yAxisTok.getAbsUpper();

    int y0 = yaxisY1;

  // Draw it

    h.setStroke(new BasicStroke(axisWidth));
    h.setFont(tickFont);

    int tickIncr = calcTickIncr((int) yValRange);
    int minTick  = calcMinTick(yValMin, tickIncr);

    //dbg("minTick: " + minTick + " | tickIncr: " + tickIncr);
    AffineTransform baseTransform = h.getTransform();

    for (int y = minTick; y <= yValMax; y += tickIncr) {
      double y1f = (double) (y - yValMin) / yValRange;
      int y1      = (int) (y0 + yPixRange * (1. - y1f));

      plotYTick(h, y1, y);
      h.setTransform(baseTransform);
    }
  }

////////////////////  plotYTick /////////////////////////////

  public void plotYTick(Graphics2D h, int yPix, int yVal) {
    int x1 = xaxisX1;
    int x2 = x1 + tickLength;

    h.setColor(axisColor);
    h.drawLine(x1, yPix, x2, yPix);

    String tickText = Integer.toString(yVal);
    int textWidth = h.getFontMetrics().stringWidth(tickText);

    int y1 = yPix - 2;
        x1 += (textWidth + 10);

    h.setColor(tickFontColor);
    h.translate(x1,y1);
    h.rotate(Math.PI);

    h.drawString(tickText, 0, 0);
  }

////////////////////  ptokEnters /////////////////////////////

  public void ptokEnters(PTokModel ptok) {

  }

////////////////////  ptokExits /////////////////////////////

  public void ptokExits(PTokModel ptok) {

  }

////////////////////  ptokChanges /////////////////////////////

  public void ptokChanges(PTokModel ptok) {

  }

//////////////////// plotCoords /////////////////////////////

  public void plotCoords(Graphics2D h) {

//  public boolean additionalCellsEmpty() {

   try {
     if (xAxisTok == null && yAxisTok == null) {return;}

     if (xAxisTok != null && xAxisTok.discreteParam == true & 
         yAxisTok == null) {return;}

     if (yAxisTok != null && yAxisTok.discreteParam == true & 
         xAxisTok == null) {return;}

     h.setStroke(new BasicStroke(dataLineWidth));
  
     int xPixRange = xaxisX2 - xaxisX1;
     int yPixRange = yaxisY2 - yaxisY1;

//     int x0 = xaxisX1 - dataSqWidth/2;
//     int y0 = yaxisY1 + dataSqWidth/2;

     int x0 = xaxisX1; 
     int y0 = yaxisY1;

     int x02 = yaxisX - dataSqWidth/2;
     int y02 = xaxisY - dataSqWidth/2;
  
     double xValRange = 1;
     double xValMin   = 0;

     if (xAxisTok != null) {

       xValRange = xAxisTok.getAbsRange();
       xValMin   = xAxisTok.getAbsLower();
     }

     double yValRange = 1;
     double yValMin   = 0;

     if (yAxisTok != null) {
       yValRange = yAxisTok.getAbsRange();
       yValMin   = yAxisTok.getAbsLower();
     }
  
     Vector allRecs = dbMgr.getAllRecs();
     int numEls     = allRecs.size();
  
     if (numEls == 0) {return;}
  
     BldgRecord br = (BldgRecord) allRecs.elementAt(0);

     Field xfield = null, yfield = null;

     if (xAxisTok != null) {
       if (xAxisTok.boolParam) { 
         xfield = br.brGetField(xAxisTok.getBoolName());

       } else if (xAxisTok.discreteParam) {
         xfield = br.brGetField(xAxisTok.pwheel.valsName);

       } else {
         xfield = br.brGetField(xAxisTok.paramName);
       }	 
     }

     if (yAxisTok != null) {

       if (yAxisTok.boolParam ) {
	 yfield = br.brGetField(yAxisTok.getBoolName());

       } else if (yAxisTok.discreteParam) {
         yfield = br.brGetField(yAxisTok.pwheel.valsName);

       } else {
         yfield = br.brGetField(yAxisTok.paramName);
       }
     }

//dbg("y lowerval: " + yValMin);
//dbg("x lowerval: " + xValMin);

     int coordCount = 0;

     int numXEls=-1, xIncr=-1;
     int numYEls=-1, yIncr=-1;

     if (xAxisTok != null && xAxisTok.discreteParam == true) { 

       if (xAxisTok.pwheel == null) {
         dbg("plotCoords bogosity: xAxisTok.pwheel == null!"); 
	 return;
       }
     
       numXEls = xAxisTok.pwheel.getSize(); 
       xIncr   = (int) (xPixRange / numXEls);
     }

     if (yAxisTok != null) {

       if (yAxisTok.discreteParam == true) { 

         if (yAxisTok.pwheel == null) {
           dbg("plotCoords bogosity: yAxisTok.pwheel == null!");
  	   return;
         }
     
         numYEls = yAxisTok.pwheel.getSize(); 
         yIncr   = (int) (yPixRange / numYEls);
       }
     }

     String xTypeStr = null, yTypeStr = null;
     int    xTypeInt = 0, yTypeInt = 0;

     if (xfield != null) {
       xTypeStr = xfield.getType().toString();

       if (xTypeStr != null) {
         if (xTypeStr.compareTo("float") == 0) {
	   xTypeInt = 1;
	 }
	 if (xTypeStr.compareTo("boolean") == 0) {
	   xTypeInt = 2;
	 }
       }

       //dbg("x type: " + xTypeStr);
     }
     
     if (yfield != null) {
       yTypeStr = yfield.getType().toString();
       
       if (yTypeStr != null) {
         if (yTypeStr.compareTo("float") == 0) {
	   yTypeInt = 1;
	 }
	 if (yTypeStr.compareTo("boolean") == 0) {
	   yTypeInt = 2;
	 }
       }

       //dbg("y type: " + yTypeStr);
     }

     int pwheelSize = -1;


// prepare for boolean params

     Field boolFields[] = null;
     
     if (yAxisTok != null && yAxisTok.boolParam && 
        yAxisTok.pwheel != null && numEls >= 0) {

       br = (BldgRecord) allRecs.elementAt(0);
       pwheelSize = yAxisTok.pwheel.size();

       boolFields = new Field[pwheelSize];

       for (int i=0; i < pwheelSize; i++) {
         String boolStr = yAxisTok.pwheel.getBVal(i);

         boolFields[i] = br.brGetField(boolStr);
       }
     }

// ok, work through it all

     for (int i=0; i < numEls; i++) {
  
       br = (BldgRecord) allRecs.elementAt(i);
       boolean selected = dbMgr.visResultsContainEl(br.bldg_id);

       int x1 = 0;
       double xval=0, x1f;

     // calc X position

       if (xAxisTok != null) {
       
         if (xAxisTok.discreteParam == true) {

           String param = null;

           switch (xTypeInt) { 
	     case 0: param = br.getString(xfield); break; 
	     case 1: param = Float.toString(br.getFloat(xfield)); break; 
//	     case 2: param = Boolean.toString(br.getBoolean(xfield)); break;
  	   }

	   if (param == null) { continue;  }  // RETHINK?
	 
	   int idx = xAxisTok.pwheel.getVal(param); 
	
//	 x1 = x0 + (xPixRange - idx * xIncr) + jitterX.addJitter(i)
//	           + jitterBase;

	   x1 = x0 + (idx * xIncr) - jitterX.addJitter(i)
	           - jitterBase - 14;

	   if (numXEls > 5) {x1 += 8;}


         } else {

           xval = br.getFloat(xfield) - xValMin;
           x1f = xval / xValRange;
           x1 = (int) (x0 + xPixRange * x1f);
         }
       } else {

         x1 = x02 - 2*jitterBase + 
                    jitterX.addJitter(i); // just above baseline
       }

       if (xval < xValMin) {continue;}

     // calc Y position

       double yval=0, y1f;
       int y1 = 0;

       if (yAxisTok != null) {

         if (yAxisTok.discreteParam == true && yAxisTok.boolParam == false) {

           String param = null;

           switch (yTypeInt) {
	     case 0: param = br.getString(yfield); break; 
	     case 1: param = Float.toString(br.getFloat(yfield)); break;
	   }

	   if (param == null) { continue;  } // RETHINK?

	   int idx = yAxisTok.pwheel.getVal(param); 
	   
	   y1 = y0 + (yPixRange - idx * yIncr) + jitterY.addJitter(i)
	           + jitterBase + 7;

	   if (numYEls > 5) {y1 -= 8;}

	 } else if (yAxisTok.discreteParam == false) {
	   
           yval = br.getFloat(yfield) - yValMin;
           y1f  = 1. - (yval / yValRange);
           y1   = (int) (y0 + yPixRange * y1f);
	 }

         if (yval < yValMin) {continue;}

       } else {
         y1 = y02 + jitterBase + jitterY.addJitter(i); // just above baseline

       }	
  
       if (selected) {
	 h.setColor(brightDataColor);
         h.fillRect(x1, y1, dataSqWidth, dataSqWidth);
  
       } else {
	 h.setColor(dimDataColor);
         h.fillRect(x1, y1, dataSqWidth, dataSqWidth);
       }

/// BOOL CASE; trickier, because multiple Y's possible

       if (yAxisTok != null && yAxisTok.boolParam) { //boolean param

         if (pwheelSize == -1) {

	   dbg("plotCoords: boolPlot bogosity: pwheelSize == 1!");
	   return;
	 }

         y1 = y0 + jitterBase + yPixRange + 7 + jitterY.addJitter(i); 

         //y1 = y0 + yPixRange + jitterY.addJitter(i) + jitterBase;

	 for (int j=0; j < pwheelSize; j++) {
	   boolean bpresent = br.getBoolean(boolFields[j]);

	   if (bpresent) {

	   //dbg("bpresent: " + y1);

	     if (selected) {
	       h.setColor(brightDataColor); 
	       h.fillRect(x1, y1, dataSqWidth, dataSqWidth);
  
             } else {
	       h.setColor(dimDataColor);
               h.fillRect(x1, y1, dataSqWidth, dataSqWidth);
             }
	   }

	   y1 -= yIncr;
	 }
       }

       coordCount++;
     }

 //    dbg("coordCount: " + coordCount);

    } catch (Exception e) {
      dbg("plotCoords exception: " + e.toString());
      e.printStackTrace();
    }
  }

////////////////////  plotPattern /////////////////////////////

  public void plotPattern(int x, int y) {

    //buffImg.setRGB(x, y, 9, 9, pat, 0, 9);
  }

////////////////////  draw label /////////////////////////////

  public void drawLabel(Graphics h, int x, int y, Color labelColor,
                        String paramName, String lower, String upper) {

    int height = 75;
    int width  = 200;

    int padX = 10;
    int padY = 10;

    int colorTagSize = 20;

    Color bgColor   = new Color(75, 75, 75);
    Color textColor = Color.white;

    h.setColor(bgColor);
    h.fillRect(x, y, height, width);

    h.setColor(labelColor);
    h.fillRect(x + padX, y - padY, colorTagSize, colorTagSize);
  }

////////////////////  paint /////////////////////////////

  public void paint(Graphics g) {

//if (true) {return;}

  if (dbMgr.visQueryCompleted == false) {return;}

//    qrackMgr.scatterVis.rootFrame.setBackground(Color.green);
// (debugging)

 //// draw top label

//  Font axisLabelFont = new Font("Verdana", Font.PLAIN, 36);
  
 //// Draw it!

    updateAxesFromModel();

    g.setColor(Color.black);
    g.clearRect(0, 0, parentVis.panelWidth, parentVis.panelHeight);

    Graphics2D h = (Graphics2D) g;

    plotAxis(h);

    if (dbMgr.visQueryResultsExist == true) {

      plotXZeroCrossing(h);
      plotYZeroCrossing(h);

      plotAxisGuides(h);
      
      plotXTicks(h);
      plotYTicks(h);

      plotCoords(h);
    }

/*
    if (qrackMgr.wrackModel.ptoksActive.isPTokPresent("price")) {
      grRange.drawRange(gbi);
    }

    if (qrackMgr.wrackModel.ptoksActive.isPTokPresent("acreage")) {
      grRange2.drawRange(gbi);
    }
 */

  // Draw framerate

    //g.drawString((int)updateRate + " fps", 5, 450);

  }


 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("GrScatterVis." + (dcnt++) + ": " + s);
  } 
}

//// END ////
