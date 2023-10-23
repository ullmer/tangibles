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
////////////////////  GrParamBind /////////////////////////////
///////////////////////////////////////////////////////////

public class GrParamBind extends QRackVis {

/////////////  METHODS ///////////////

// public GrParamBind()
// public run()

/////////////  MEMBERS ///////////////

// Model of the workspace

   WRackModel wrackModel = null;
   char dataType = ' ';

// Geometry dimensions

   int    tokPixWidth  = 85;

   int boolLabelHeight = 9;
   int  tokLabelHeight = 16;

   int labelsXOffset = 10;
   int labelsYOffset = 10;

   int tokYOffset = 30;
   int andYOffset = 30;
   int  orYOffset = 26;

   int  tokTextPad       = 4;
   int  tokTextYOffset   = 3;
   int  tokLowerbYOffset = 4;
   int  tokUpperbYOffset = 10;
   int  boolTextYOffset  = 1;

// Colors

  //Color andBgColor = new Color(150, 150, 150);
  Color andBgColor = new Color(100,100,100);

  Color  orBgColor = new Color(50, 50, 50);

  Color     textColor = Color.white;
  Color boolTextColor = new Color(175, 175, 175);

// Text elements

  Font   labelFont;
  int    labelFontSize   = 24;
  Color  labelFontColor  = new Color(75,75,75);
  //String labelFontName   = "Verdana";
  String labelFontName   = "System";

// Color labels

    Color labelColors[];

    int labelColorVals[][] = {{242, 50, 50}, 
                              {255, 116, 0}, 
			      {220, 210, 30},
			      {0, 174, 81},
			      {0, 139, 207},
			      {187, 180, 214},
			      {142, 133, 183}};
/*
    int labelColorVals[][] = {
                              {255, 116, 0}, 
			      {220, 210, 30},
			      {0, 174, 81},
			      {239, 95, 173},
			      {142, 133, 183}, 
			      {242, 50, 50},
			      {187, 180, 214}};
*/


//  static int panelWidth = 800, panelHeight = 200;

  static int panelWidth  = 1280, 
             panelHeight  = 150;

  int labelHeight = 150;
  int labelWidth  = 100;

  static int baseX = 0, baseY = 900;

  static int xoff = panelWidth / 3 - 25, 
             yoff = panelHeight / 3 - 10;

  RenderingHints qualityHints;
  boolean antialiasingActive = true; 
    //Use antialiased text, by default

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

////////////////////  GrParamBind /////////////////////////////

  public GrParamBind(QRackMgr mgr, String title, char whichData) {

    super(mgr,' ', title, panelWidth, panelHeight, baseX, baseY);

    dataType = whichData;

    wrackModel = qrackMgr.getModel();

    labelFont  = new Font(labelFontName,  Font.PLAIN, labelFontSize);

    labelColors = new Color[7];
    for (int i=0; i<7; i++) {
      labelColors[i] = new Color(labelColorVals[i][0],
                                 labelColorVals[i][1],
                                 labelColorVals[i][2]);
    }
  }

////////////////////  paint /////////////////////////////

  public void paint(Graphics g) {

  //  rootFrame.setBackground(Color.black); 

    Graphics2D h = (Graphics2D) g;

    if (qualityHints != null) {
       h.setRenderingHints(qualityHints);
    }

  // Erase screen
  
    g.setColor(Color.black);
    g.clearRect(0, 0, panelWidth, panelHeight);

  // prep

    switch (dataType) {

      case 'b': // bldg
/*
        paintLabel(h, 1, "price",    labelColors[0]);
	paintLabel(h, 2, "acreage",  labelColors[1]);
	paintLabel(h, 3, "sq_ft",    labelColors[2]);
	paintLabel(h, 4, "taxes",    labelColors[3]);
	paintLabel(h, 5, "# floors", labelColors[4]);
	paintLabel(h, 6, "# bedrm",  labelColors[5]); 
*/
/*
        paintLabel(h, 1, "price",    labelColors[5]);
	paintLabel(h, 2, "# floors", labelColors[1]);
	paintLabel(h, 3, "# bedrm",  labelColors[2]); 
	paintLabel(h, 4, "taxes",    labelColors[0]);
	paintLabel(h, 5, "acreage",  labelColors[4]);
	paintLabel(h, 6, "sq_ft",    labelColors[3]);
       break;
*/
        paintLabel(h, 1, "taxes",    labelColors[5]);
	paintLabel(h, 2, "# floors", labelColors[1]);
	paintLabel(h, 3, "# bedrm",  labelColors[2]); 
	paintLabel(h, 4, "price",    labelColors[0]);
	paintLabel(h, 5, "sq_ft",    labelColors[4]);
	paintLabel(h, 6, "acreage",  labelColors[3]);
       break;

      case 'm': // funds

        paintLabel(h, 1, "ytd rtn",    labelColors[0]);
	paintLabel(h, 2, "5yr rtn",    labelColors[1]);
	paintLabel(h, 3, "10y rtn",    labelColors[2]);
	paintLabel(h, 4, "price",      labelColors[3]);
	paintLabel(h, 5, "charges",    labelColors[4]);
	paintLabel(h, 6, "rtn cat",    labelColors[5]);
	paintLabel(h, 7, "risk cat",   labelColors[6]);
       break;
    }

/*
        paintLabel(h, 1, "price", new Color(195,85,85)); 
	paintLabel(h, 2, "sq_ft", new Color(150,10,75)); 
	paintLabel(h, 3, "acreage", new Color(100,120,250)); 
	paintLabel(h, 6, "# floors", Color.orange); 
	paintLabel(h, 7, "# bedr", Color.magenta); 
	paintLabel(h, 8, "taxes", Color.green);
*/

/*
  // Draw the token labels

    Vector ptoksActive = wrackModel.ptoksActive.getActivePToks();
 
    paintLabel(h, ptok.currentCell, ptok.visLabel, ptok.paramColor);

   // Draw the OR relations 

    for (int i=0; i < len - 1; i++) {

      PTokAdjRel lAdjRel = (PTokAdjRel) adjRels.elementAt(i);
      PTokAdjRel rAdjRel = (PTokAdjRel) adjRels.elementAt(i+1);
 
      int leftSlot  = lAdjRel.rightmostCell + 1;
      int rightSlot = rAdjRel.leftmostCell - 1;

      paintOr(h, leftSlot, rightSlot);
    }
*/
  }

////////////////////  paint Parameter Label ////////////////////////

  public void paintLabel(Graphics2D h, int slotNumber, 
                         String paramName, Color paramColor) {

  // paint the box

   //int x1 = labelWidth * (slotNumber - 1);
   int x1 = (int) (labelWidth * (slotNumber - 0.5));
   int y1 = 0;

   h.setColor(paramColor);
   h.fillRect(x1, y1, labelWidth, labelHeight);

  // draw the token text

   h.setColor(textColor);
   h.setFont(labelFont);

   int textWidth = h.getFontMetrics().stringWidth(paramName);

   int x2 = x1 + (labelWidth - textWidth)/2;
   int y2 = labelHeight/2 - 20;

   h.drawString(paramName, x2, y2);

  }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("GrParamBind." + (dcnt++) + ": " + s);
  } 

}

//// END ////

