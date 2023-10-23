// Graphical axis (& timeline)
// By Brygg Ullmer, MIT Media Lab

// Begun September 10, 2001

import java.util.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.awt.image.*;

import javax.swing.*;
import java.io.*;

//////////////////////////////////////////////////////
///////////////// Graphical axis /////////////////////
//////////////////////////////////////////////////////


public class GrRange {

//////////////////// members /////////////////////

  double minVal, maxVal; // from 0 .. 1.
  int    minPix, maxPix;

  int   refPix = 80;
  int   height = 50;
  int   lineOffset = 30;

  Color labelTagColor = Color.red;
  int   colorTagSize = 20;

 // Text and line config info

  Color axisColor = new Color(90, 90, 90);
  int   axisWidth = 3;

  String axisLabel;
  Color  axisLabelColor = new Color(225, 225, 225);
  int    axisLabelFSize  = 18;
  String axisLabelFont  = "Arial Narrow";
  Font   axLabelFont;

  //Color  rangeColor = new Color(125, 125, 0);
  Color  rangeColor = new Color(200, 200, 0);
  int    rangeFSize = 14;
  String rangeFont  = "Verdana";
  Font   axRangeFont;

  int    rangeFontOffset = 12;

  String label = null;

  Color   backgroundColor = new Color(100, 100, 100);
  boolean fillBackground = true;

  int bgPadX  = 12;
  int bgPadY1 = 6; // lower side
  int bgPadY2 = 35; // text side

//////////////////// methods /////////////////////

/////////////////////////////////////////////////
//////////////////// bodies /////////////////////
/////////////////////////////////////////////////

///////////// constructor ///////////////

  public GrRange() {
    //super("QRClient");

    axLabelFont = new Font(axisLabelFont, Font.PLAIN, axisLabelFSize);
    axRangeFont = new Font(rangeFont,  Font.PLAIN, rangeFSize);

    minVal = 0;
    maxVal = 0;
  }

///////////// setBounds ///////////////

  public void setFontSize(int fontSize) {

    rangeFSize = fontSize;
    axRangeFont = new Font(rangeFont,  Font.PLAIN, rangeFSize);
  }

///////////// setBounds ///////////////

  public void setBounds(double newMin, double newMax) {

    minVal = newMin;
    maxVal = newMax;
  }

///////////// setBounds ///////////////

  public void setPixBounds(int left, int right, int y) {

    minPix = left;
    maxPix = right;
    refPix = y;
  }

///////////// drawRange ///////////////

  public void drawRange(Graphics2D h) {

    if (fillBackground) {
      h.setColor(backgroundColor);

      int width = maxPix - minPix + bgPadX * 2;

      int x1 = minPix - bgPadX;
      int y1 = refPix - bgPadY1;

      h.fillRect(x1, y1, width, height);
    }

    int lineY = refPix + lineOffset;

  // Draw baseline

    h.setColor(axisColor);
    h.setStroke(new BasicStroke(axisWidth));
      
    h.drawLine(minPix, lineY, maxPix, lineY);

  // Draw selected line

    h.setColor(rangeColor);

    int pos1 = ratio2pos(minVal);
    int pos2 = ratio2pos(maxVal);

    h.drawLine(pos1, lineY, pos2, lineY);

  // Add text

    h.setColor(labelTagColor);

    int x1 = minPix;
    int y1 = refPix + rangeFontOffset;

    h.fillRect(x1, refPix, colorTagSize, colorTagSize);

    if (label != null) {

      h.setColor(axisLabelColor);
      h.setFont(axRangeFont);

      h.drawString(label, x1 + bgPadX + colorTagSize - 2, y1);
    }
  }

/////////////////////// time 2 xpos ///////////////////////

 public int ratio2pos(double ratio) {

   double valRange = maxVal - minVal;
   int pixRange   = maxPix - minPix;

//   int xpos       = minPix + (int) (ratio * pixRange);

   int xpos       = minPix + (int) (ratio * pixRange);

   return xpos;
 }

/////////////////////// dbg ///////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("GrRange[" + (dcnt++) + "] " + s);
  }
}

/// END ///

 
