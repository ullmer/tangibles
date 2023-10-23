/// Query UI code 
/// By Brygg Ullmer, MIT Media Lab
///
/// Begun October 23, 2001
/// Borrowing code begun April 20, 2001, & reworked September 10, 2001.
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

///////////////////////////////////////////////////////////
////////////////////  GrRelVis /////////////////////////////
///////////////////////////////////////////////////////////

public class GrRelVis extends QRackVis {

/////////////  METHODS ///////////////

// public GrRelVis()
// public run()

/////////////  MEMBERS ///////////////

  static JFrame     rootFrame;
  static JComponent rootComponent;

  Thread animationThread;
  long startTime, lastTime, currentTime;
  int  elapsedInterval = 0;
  double updateRate    = 0.;

  int frameNumber = -1;
  boolean frozen  = false;

  boolean isDisplayBound = false;

// Model of the workspace

   WRackModel wrackModel = null;

// Geometry dimensions

   //int    tokPixWidth  = 85;
   int    tokPixWidth  = 98;
   int    tokPixHeight = 205;
   int screenPixHeight = 84;
   int screenPixBottom = 136;

   int boolLabelHeight = 9;
   int  tokLabelHeight = 16;

   //int labelsXOffset = 10;
   int labelsXOffset = -52;
   int labelsYOffset = 10;

   int tokYOffset = 30;
//   int andYOffset = 26;
//   int  orYOffset = 30;

   int andYOffset = 28;
   int  orYOffset = 34;

   int  tokTextPad       = 4;
   int  tokTextYOffset   = 3;
   int  tokLowerbYOffset = 4;
   int  tokUpperbYOffset = 10;
   int  boolTextYOffset  = 1;

// Colors

  //Color andBgColor = new Color(150, 150, 150);
  //Color andBgColor = new Color(100,100,100);
  Color andBgColor = new Color(130,130,130);

  Color  orBgColor = new Color(50, 50, 50);

  Color     textColor = Color.white;
  //Color boolTextColor = new Color(175, 175, 175);
  Color boolTextColor = new Color(200, 200, 200);

// Text elements

  Font   labelFont;
  int    labelFontSize   = 15;
  Color  labelFontColor  = new Color(75,75,75);
  //String labelFontName   = "Verdana";
  String labelFontName   = "System";

  Font   boolFont;
  int    boolFontSize    = 9;
  Color  boolFontColor   = new Color(75,75,75);
  String boolFontName    = "Verdana";
//  String boolFontName    = "System";

  Font   boundsFont;
  int    boundsFontSize  = 5;
  Color  boundsFontColor = new Color(75,75,75);
  String boundsFontName  = "Verdana";

// Geometries

//  static int panelWidth = 800, panelHeight = 200;

  //static int panelWidth  = 580, 

  static int panelWidth  = 620, 
             panelHeight = 75,
             ppOffset    = 170;

  static int ppanelHeight = panelHeight + ppOffset;

  //static int baseX = 1465, baseY = 365;
  //static int baseX = 1425, baseY = 365;
  //static int baseX = 1425, baseY = 465; 
//  static int baseX = 420, baseY = 1250;
  static int baseX = 385, baseY = 1250;

  static int xoff = panelWidth / 3 - 25, 
             yoff = panelHeight / 3 - 10;

  RenderingHints qualityHints;
  boolean antialiasingActive = true; 
    //Use antialiased text, by default

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

////////////////////  GrRelVis /////////////////////////////

  public GrRelVis(QRackMgr mgr, String title) {

    //super(mgr, ' ', title, panelWidth, panelHeight, baseX, baseY);
    super(mgr, ' ', title, panelWidth, ppanelHeight, baseX, baseY-ppOffset);

    wrackModel = qrackMgr.getModel();

    labelFont  = new Font(labelFontName,  Font.PLAIN, labelFontSize);
    boolFont   = new Font(boolFontName,   Font.PLAIN, boolFontSize);
    boundsFont = new Font(boundsFontName, Font.PLAIN, boundsFontSize);
  }

////////////////////  paint /////////////////////////////

  public void paint(Graphics g) {

  //  rootFrame.setBackground(Color.black); 

//  dbg(">>> why so fast?");

    // Update timing info

    frameNumber++;
    lastTime    = currentTime;
    currentTime = System.currentTimeMillis();
    elapsedInterval = (int) (currentTime - lastTime);

    if (elapsedInterval != 0) {
      updateRate = 1000. / (double) elapsedInterval;
    }

    //Activate antialiasing (in particular, of text)

    Graphics2D h = (Graphics2D) g;

    if (qualityHints != null) {
       h.setRenderingHints(qualityHints);
    }

  // Erase screen
  
//    g.setColor(Color.black);
    g.setColor(Color.white);
    //g.clearRect(0, 0, panelWidth, panelHeight);
    g.fillRect(0, 0, panelWidth, panelHeight + ppOffset);

    //g.fillRect(x1, y1, tokPixWidth, tokLabelHeight);
    //g.fillRect(0, 0, panelWidth, ppOffset);

    //g.clearRect(baseX, baseY, panelWidth, panelHeight);

  // prep

    if (wrackModel == null) { 
      dbg("paint: wrackModel is null!  dunno what to do...");
      return;
    }

  // Draw the token labels

    Vector ptoksActive = wrackModel.ptoksActive.getActivePToks();
 
    int len = ptoksActive.size();

    double lowerVal, upperVal;

    for (int i=0; i < len; i++) {

      PTokModel ptok = (PTokModel) ptoksActive.elementAt(i);


      String label = ptok.visLabel;

      if (i == 0) {
        if (len == 1) {
          label += "  (X)";
	} else {
	  label += "  (Y)";
	}
      }

      if (i == 1) {
        label += "  (X)";
      }

      paintLabel(h, ptok.currentCell, label, ptok.paramColor);

      lowerVal = ptok.getRatioLower();
      upperVal = ptok.getRatioUpper();

      paintTok(h, ptok.currentCell, ptok.visLabel, ptok.projectColor,
         lowerVal, upperVal);


/*
                    Integer.toString(ptok.lowerBound),
                    Integer.toString(ptok.upperBound),
 		   ptok.paramUnits);
*/
    }

   // Draw the AND relations

    Vector adjRels = wrackModel.wrackRels.getAdjRels();

    len = adjRels.size();

    for (int i=0; i < len; i++) {

      PTokAdjRel adjRel = (PTokAdjRel) adjRels.elementAt(i);

      //if (adjRel.size() == 1) {continue;}

      if (adjRel.size() == 1) {

        if (len < 2) {continue;} // don't show a "loner"

        //paintAndNoLab(h, adjRel.leftmostCell - 1, adjRel.rightmostCell - 1);
        //paintAndNoLab(h, adjRel.leftmostCell, adjRel.rightmostCell);
        paintAndNoLab(h, adjRel.leftmostCell - 2, adjRel.rightmostCell - 2);
	continue;
      }

      int l = adjRel.leftmostCell;
      int r = adjRel.rightmostCell;

      if (adjRel.size() == 3) { l += 2; r += 2;}

      paintAnd(h, l, r);
    }

   // Draw the OR relations 

    for (int i=0; i < len - 1; i++) {

      PTokAdjRel lAdjRel = (PTokAdjRel) adjRels.elementAt(i);
      PTokAdjRel rAdjRel = (PTokAdjRel) adjRels.elementAt(i+1);
 
      int leftSlot  = lAdjRel.rightmostCell + 1;
      int rightSlot = rAdjRel.leftmostCell - 1;

      paintOr(h, leftSlot, rightSlot);
    }
  }

////////////////////  paint Parameter Label ////////////////////////

  public void paintLabel(Graphics2D h, int slotNumber, 
                         String paramName, Color paramColor) {
//                         String lowerBound, String upperBound, String units) {


  // paint the box

   int x1 = labelsXOffset + tokPixWidth/2 * (11 - slotNumber);
   //int y1 = labelsYOffset;
   int y1 = labelsYOffset + ppOffset;

   h.setColor(paramColor);

//   h.fillRect(x1, y1, tokPixWidth, tokLabelHeight);
//   h.fillRoundRect(x1, y1, tokPixWidth, tokLabelHeight, 4, 4);
//   h.fillRoundRect(x1+1, y1, tokPixWidth-2, tokLabelHeight, 5, 5);
   h.fillRoundRect(x1+2, y1, tokPixWidth-4, tokLabelHeight, 5, 5);

  // draw the token text

   h.setColor(textColor);
   h.setFont(labelFont);

   int textWidth = h.getFontMetrics().stringWidth(paramName);

   //int x2 = x1 + tokPixWidth - textWidth - tokTextPad;

   int x2 = x1 + tokPixWidth - tokTextPad;
   int y2 = y1 + tokTextYOffset; 

   AffineTransform baseTransform = h.getTransform();
   h.translate(x2, y2);
   h.rotate(Math.PI);

   h.drawString(paramName, 0, 0);
   h.rotate(Math.PI);
   h.setTransform(baseTransform);

/*
  // draw the bounds

   h.setFont(boundsFont);

   String lowerBound = "lower: " + lowerBound;
   String upperBound = "upper: " + upperBound;

   x2 = x1 + tokTextPad;
   y2 = y1 + tokLowerbYOffset;
   h.drawString(x2, y2, lowerBound);


   y2 = y1 + tokUpperbYOffset;
   h.drawString(x2, y2, upperBound);
*/
  }

////////////////////  paint Parameter Label ////////////////////////

  public void paintTok(Graphics2D h, int slotNumber, 
                         String paramName, Color projectColor,
			 double lowerVal, double upperVal) {
//                         String lowerBound, String upperBound, String units) {


  // paint the box

   int x1 = labelsXOffset + tokPixWidth/2 * (11 - slotNumber);
   int y1 = labelsYOffset + ppOffset;

   h.setColor(projectColor);

//   h.fillRect(x1, y1, tokPixWidth, tokLabelHeight);
//   h.fillRoundRect(x1, y1, tokPixWidth, tokLabelHeight, 4, 4);
//   h.fillRoundRect(x1+1, y1, tokPixWidth-2, tokLabelHeight, 5, 5);
//   h.fillRoundRect(x1+2, y1, tokPixWidth-4, tokLabelHeight, 5, 5);

   //int y2 = y1 + tokLabelHeight;
   int y2 = y1 - tokPixHeight - 5;

  // dbg("y2: " + y2);

   h.fillRect(x1+2, y2, tokPixWidth-4, tokPixHeight);


  // draw selected area

   int yrange = (int)((upperVal - lowerVal) * screenPixHeight);
   y2 = y1 - screenPixBottom - 5 + (int) (lowerVal * screenPixHeight);
   //y2 = y1 - screenPixBottom - 5;

//dbg("u: " + upperVal + "; l: " + lowerVal + "; range: " + yrange);

   h.setColor(Color.white);
   h.fillRect(x1+2, y2, tokPixWidth-4, yrange);
  // h.fillRect(x1+2, y2, tokPixWidth-4, screenPixHeight);

  }

//////////////////  paint "And" label ///////////////////////////

  public void paintAnd(Graphics2D h, int beginSlot, int endSlot) {

  //dbg("paint AND " + beginSlot + " " + endSlot);

  // paint the box

   int x1 = labelsXOffset + tokPixWidth/2 * (9 - beginSlot);
   //int y1 = andYOffset;
   int y1 = andYOffset + ppOffset;

   int numSlots = endSlot - beginSlot;
   int relWidth = tokPixWidth / 2 * (numSlots + 1);

   h.setColor(andBgColor);
   h.fillRect(x1, y1, relWidth, boolLabelHeight);

  // draw the text

   h.setColor(boolTextColor);
   h.setFont(boolFont);

   String text = "AND";
   int htextWidth = h.getFontMetrics().stringWidth(text) / 2;

   int x2 = x1 + htextWidth + relWidth/2;
   int y2 = y1 + boolTextYOffset;

   AffineTransform baseTransform = h.getTransform();
   h.translate(x2, y2);
   h.rotate(Math.PI);

   h.drawString(text, 0, 0);
   h.rotate(Math.PI);
   h.setTransform(baseTransform);
  }

//////////////////  paint "And" label ///////////////////////////

  public void paintAndNoLab(Graphics2D h, int beginSlot, int endSlot) {

  //dbg("paint AND " + beginSlot + " " + endSlot);

  // paint the box

   int x1 = labelsXOffset + tokPixWidth/2 * (9 - beginSlot);
   //int y1 = andYOffset;
   int y1 = andYOffset + ppOffset;

   int numSlots = endSlot - beginSlot;
   int relWidth = tokPixWidth / 2 * (numSlots + 1);

   h.setColor(andBgColor);
   h.fillRect(x1, y1, relWidth, boolLabelHeight);

  // draw the text

/*
   h.setColor(boolTextColor);
   h.setFont(boolFont);

   String text = "AND";
   int htextWidth = h.getFontMetrics().stringWidth(text) / 2;

   int x2 = x1 + htextWidth + relWidth/2;
   int y2 = y1 + boolTextYOffset;

   AffineTransform baseTransform = h.getTransform();
   h.translate(x2, y2);
   h.rotate(Math.PI);

   h.drawString(text, 0, 0);
   h.rotate(Math.PI);
   h.setTransform(baseTransform);
*/
  }

//////////////////  paint "Or" label ///////////////////////////

  public void paintOr(Graphics2D h, int beginSlot, int endSlot) {

//  dbg("paint OR " + beginSlot + " " + endSlot);

  // paint the box

//   int x1 = labelsXOffset + tokPixWidth/2 * (10 - beginSlot);

   int x1 = labelsXOffset + tokPixWidth/2 * (12 - endSlot);
   //int y1 = orYOffset;
   int y1 = orYOffset + ppOffset;

   int numSlots = endSlot - beginSlot;
   int relWidth = tokPixWidth / 2 * (numSlots + 1);

   h.setColor(orBgColor);
   h.fillRect(x1, y1, relWidth, boolLabelHeight);

  // draw the text

   h.setColor(boolTextColor);
   h.setFont(boolFont);

   String text = "OR";
   int htextWidth = h.getFontMetrics().stringWidth(text) / 2;

   int x2 = x1 + htextWidth + relWidth/2;
   int y2 = y1 + boolTextYOffset;

   AffineTransform baseTransform = h.getTransform();
   h.translate(x2, y2);
   h.rotate(Math.PI);

   h.drawString(text, 0, 0);
   h.rotate(Math.PI);
   h.setTransform(baseTransform);
  }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("GrRelVis." + (dcnt++) + ": " + s);
  } 

}

//// END ////

