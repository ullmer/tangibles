/// Query UI code 
/// By Brygg Ullmer, MIT Media Lab
/// Begun April 20, 2001
///
/// Based on threading template by Ben Fry (fry@media.mit.edu),
/// 4/18/2001, and WinHelp Java Tutorial: AnimatorApplication.java,
/// Arthur van Hoff

import java.util.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import javax.swing.*;
import java.io.*;

///////////////////////////////////////////////////////////
////////////////////  WRack /////////////////////////////
///////////////////////////////////////////////////////////

public class WRack extends JComponent
		     implements Runnable, WRListener, RfidListener {

/////////////  METHODS ///////////////

// static void main(String args[])
// public WRack()
// public run()

//  public int mapTag2Idx (int whichTagVal) 


/////////////  MEMBERS ///////////////

  static JFrame     rootFrame;
  static JComponent rootComponent;

  Thread animationThread;
  long startTime, lastTime, currentTime;
  int  elapsedInterval = 0;
  double updateRate    = 0.;

  int frameNumber = -1;
  boolean frozen  = false;
  boolean damage  = true;

  TokMWatchdog rfidMWatchdog[];
  boolean rfidExitPending[];

// Text elements

  Font labelFont  = new Font("Verdana", Font.PLAIN, 16);
  Font label2Font = new Font("Arial Narrow", Font.PLAIN, 14);
  Font label3Font = new Font("Arial Narrow", Font.PLAIN, 12);
  Font bigFont    = new Font("Arial", Font.BOLD, 48);

  Color  labelFontColor   = Color.white;
  Color  label2FontColor  = Color.white;
  Color  bigLabelColor    = new Color(60,60,60);
//  Color  bigLabelColor    = new Color(100,100,100);

// Sample circle element

  //int circDiam       = 40;
  //int circDiam       = 12;
  int dotDiam        = 5;

//  int centerCircDiam = 70;
//  int centerCircDiam = 13;
//  int centerCircDiam = 67;
  int centerCircDiam = 65;
//  Color centerCircColor = new Color(150,150,150);
  Color centerCircColor = Color.white;

  int pathRadius = 55;
  double circAngle  = 0;
  double dthetaPerSec = 200;
  int cx = 80, cy = 60;

//  static int winXOrig = 1175, winYOrig = 75;
//  static int winXOrig = 155, winYOrig = 1140;


  static int winXOrig = 796, winYOrig = -25;
//  static int winXOrig = 706, winYOrig = -25;
//  static int winXOrig = 706, winYOrig = -25; // good, w/ 

//  static int winXOrig = 806, winYOrig = -25;
//  static int winXOrig = -1018, winYOrig = -25;

//  static int winXOrig = -1018, winYOrig = -25;
//  static int winXOrig = -1015, winYOrig = -10;
//  static int winXOrig = -910, winYOrig = -10;
//  static int winXOrig = -974, winYOrig = -10;
//  static int winXOrig = -1000, winYOrig = -10;
//  static int winXOrig = 170, winYOrig = 1024;

//  static int winXOrig = 155, winYOrig = 1075;
//  static int winXOrig = 235, winYOrig = 1075;
//  static int winXOrig = 235, winYOrig = 1024;
//  static int winXOrig = 0, winYOrig = 1300;
//  static int winXOrig = -63, winYOrig = 1200;

//  static int panelWidth = 180, panelHeight = 165;
//  static int panelWidth = 144, panelHeight = 120;
//  static int panelWidth = 163, panelHeight = 129;
//  static int panelWidth = 154, panelHeight = 129;
//  static int panelWidth = 160, panelHeight = 129;
  static int panelWidth = 156, panelHeight = 129;

//  static int winWidth = 1024, winHeight = 190;
//  static int winWidth = 1024, winHeight = 188;
//  static int winWidth = 1100, winHeight = 600;
//  static int winWidth = 1024, winHeight = 195;
  static int winWidth = 900, winHeight = 195;


  int yBase = 17;

  //Color circColor = new Color(110,50,60);
  Color circColor = Color.gray;

  RenderingHints qualityHints;
  boolean antialiasingActive = true; 
    //Use antialiased text, by default

// State and handles on readers

  int numCells = 4;

  int currentCell[] = new int[numCells];
  int lastCell[]    = new int[numCells];

  //int cellInc = 36;
  //int cellInc = 36;
//  int cellInc = 41;
//  int cellInc = 40;
//  double cellInc = 39.1;
  double cellInc = 39.5;


  //int cellOffset = 90;
  int cellOffset = 110;


  double radsPerInc = .02; // .03 is perhaps overly sensitive
  double lastTagRot[] = new double[10];

  double rotVals[] = new double[numCells];
  double rotStartSpin[] = new double[numCells];

//  double minRot  = -Math.PI/3.;
//  double maxRot  =  Math.PI/3.;

  double minRot  = -Math.PI/4.;
  double maxRot  =  Math.PI/4.;

  int potVals[] = new int[numCells];
  int potStartSpin[] = new int[numCells];

  int switchVals[] = new int[16];

  boolean firstRotUpdate[] = new boolean[numCells];
  boolean rfPresence[] = new boolean[numCells];
  int     rfVals[]     = new int[numCells];
  int     lastRfVals[] = new int[numCells];
  double  levels[]     = new double[10];

  WRackReader ps_reader = null;
  RfidReader  rf_reader = null;

  WRServer   wrack_server = null;
  ParamWheelMgr paramMgr = null;

  DbThread dbthread = null;

  int Remote[][]       = new int[numCells][3];
  String RemoteLabel[] = new String[numCells];

  int          RemoteTag[] = new int[numCells];
  int          RemoteSel[] = new int[numCells];
  int  currentSelected[] = new int[numCells];

  String adjacencies = "";

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

/////////////////  map Tag 2 Idx //////////////////////

  public int mapTag2Idx (int whichTagVal) {
    if (whichTagVal == 190) {return 1;}
    if (whichTagVal == 207) {return 2;}
    if (whichTagVal == 65533) {return 3;}
    if (whichTagVal == 172) {return 4;}
    if (whichTagVal == 76) {return 5;}
    return 0;
  }

/////////////////  potUpdateOccurred //////////////////////

  public void potUpdateOccurred(int whichPot, int whichVal) {

    potVals[whichPot] = whichVal;

    if (potStartSpin[whichPot] == -1) {
      potStartSpin[whichPot] = whichVal;
    } else if (firstRotUpdate[whichPot] == true) {

// BAU -- 06/17/02 -- new addition to tackle jumping-toks
      firstRotUpdate[whichPot] = false;
      potStartSpin[whichPot] = whichVal;
    }

/*
    dbg("potUpdateOccurred: " + 
         whichPot + " pot, " + 
         whichVal + " val");
*/
//    wrack_server.processTokRot(whichPot, whichVal);
  }

////////////////// updateAdjacencies //////////////////////

  public void updateAdjacencies(String nadjacencies) {

    if (adjacencies.compareTo(nadjacencies) == 0) { // no change
      return;
    }

    adjacencies = nadjacencies;

    wrack_server.processAdjacencies(adjacencies);
  }

////////////////// switchUpdateOccurred //////////////////////

  int last_sw5_state = 1;

  public void switchUpdateOccurred() {

    dbg("switchUpdateOccurred: switchState " + Integer.toBinaryString(ps_reader.switchState));

//    for (int i=0; i<8; i++) {
//      dbg("switch " + i + ": " + ps_reader.getSwitchVal(i));
//    }

/*
    currentCell[3] = 16 - ps_reader.padPos[0]; 
//    currentCell[2] = 15 - ps_reader.padPos[1]; 
    currentCell[2] = 16 - ps_reader.padPos[1];  // "it varies" :-/
    currentCell[1] = 16 - ps_reader.padPos[2];
    currentCell[0] = 16 - ps_reader.padPos[3];
*/

    currentCell[3] = 16;
    currentCell[2] = 12;
    currentCell[1] = 8;
    currentCell[0] = 4;

//    dbg("actual pos: " + currentCell[0] + " " + currentCell[1]);
  }

////////////////// rfidUpdateOccurred //////////////////////

  public void rfidUpdateOccurred(int whichCell, 
     boolean whatState, int whatVal) {

    rfPresence[whichCell] = whatState;
    lastRfVals[whichCell] = rfVals[whichCell];

   if (whatVal == 8226) {whatVal = 99;} // quick hack for extra tok

    rfVals[whichCell] = whatVal; 
    
    if (rfidMWatchdog[whichCell] == null) { 
      dbg("rfidUpdateOccurred: rfidMWatchdog isn't yet ready; punting."); 
      return; 
    }

    // Make rotation values "persistent"


  if (whatState == true) { // entrance event

    int idx     = mapTag2Idx(whatVal);

//    if (rfidMWatchdog[whichCell].isTokPresent() == false) {
// Experimenting with disabling this

// entrance event

      ParamWheel wheel = paramMgr.getId(whatVal);

      if (wheel == null) {

        dbg("rfidUpdateOccurred, but wheel is null; id = " + whatVal);
	return;
      }

      double ratio     = wheel.defaultVal;
      double desiredRot  = (ratio * (maxRot-minRot) + minRot);

      potStartSpin[whichCell] = potVals[whichCell] 
                                - (int) (desiredRot / radsPerInc);

//      potStartSpin[i] = (ratio * (maxRot-minRot) + minRot) 
//                         / radsPerInc  - rotVals[i];

      wrack_server.processTokEntrance(whichCell, whatVal);

/*    } else {

      dbg("RFIDUPDATE: not dispatching entrance event on advice of " +
          "isTokPresent");
    }
*/
    rfidMWatchdog[whichCell].tokWitnessed();
//    rotStartSpin[whichCell] = lastTagRot[idx];

  } else {

  // exit event 

     int lastVal = lastRfVals[whichCell];

  // see if token has already reentered elsewhere

     boolean tokWitnessedElsewhere = false;

     for (int i=0; i<numCells; i++) {
       if (i != whichCell && rfVals[i] == lastVal) {
         tokWitnessedElsewhere = true;
       }
     }

     if (tokWitnessedElsewhere) {
       dbg("rfidUpdate: tok witnessed elsewhere; suppressing exit event");

       // Should we do any cleanup here first?
       return;
     } 

     rfidMWatchdog[whichCell].tokClaimsDeparture();
     rfidExitPending[whichCell] = true;
  }


    dbg("rfidUpdateOccurred: " + 
         whichCell + " cell, " + 
         whatState + " state, " + 
         whatVal   + " val");
  }

////////////////////  WRack /////////////////////////////

  public WRack() {

    // do your app setup stuff here...

    ps_reader = new WRackReader();
    rf_reader = new RfidReader();

    rfidMWatchdog = new TokMWatchdog[numCells];
    rfidExitPending = new boolean[numCells];

    dbthread = new DbThread("realestate", "tmg-internal2.media.mit.edu");

    paramMgr  = new ParamWheelMgr();
    paramMgr.loadDefaultWheels(dbthread);

    ps_reader.setListener(this);
    rf_reader.setListener(this);

    wrack_server = new WRServer();
    wrack_server.startServer();

   dbg("WRack: forcing pad positions");
//    ps_reader.setPadPositions(0); // this could be problematic later. :-)
  switchUpdateOccurred();

    // zero the state

    for (int i=0; i<numCells; i++) {

      rotVals[i] = 0.;
      potStartSpin[i] = -1; 
      rotStartSpin[i] = 0;

      RemoteTag[i] = 0;
      RemoteSel[i] = -1;
      currentSelected[i] = -1;

      rfVals[i] = -1;
      rfidExitPending[i] = false;
      rfidMWatchdog[i] = new TokMWatchdog();
      firstRotUpdate[i] = true;
    }

/*
    currentCell[0] = 1; //2
    lastCell[0]    = 1;

    currentCell[1] = 5; //7
    lastCell[1]    = 5;

    currentCell[2] = 10; //11 //10 //12
    lastCell[2]    = 10;

    currentCell[3] = 15; //15 //16
    lastCell[3]    = 15;
*/

    for (int i=0; i<10; i++) {
      lastTagRot[i] = 0.;   // rotations associated with tags
      levels[i] = 0.5;      // levels associated with tags
    } 

    for (int i=0; i<numCells; i++) {
      for (int j=0; j<3; j++) {
        Remote[i][j] = -1;
      }
    }

    // Set crosshair cursor
    setCursor(Cursor.getPredefinedCursor(Cursor.CROSSHAIR_CURSOR));

    // ...then start the thread
    // (make sure you do this after setup, seems obvious,
    // until you forget and get really confusing inconsistent
    // problems as your app starts up in stochastically half-
    // initialized states)

    // Moved the following Fry code to startAnimation
    //  thread = new Thread(this);
    //  thread.start();
  }
  
////////////////////  startAnimation /////////////////////////////
  
  public void startAnimation() {
    if (frozen) {
      //Do nothing.  The user has requested that we
      //stop changing the image.

    } else {
      //Start animating!
      if (animationThread == null) {
        animationThread = new Thread(this);
      }
      animationThread.start();
    }
  }

////////////////////  paint /////////////////////////////

  public void paint(Graphics g) {

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

    h.translate(-106,0);
//    h.translate(-94,0);
//    h.translate(-14,0);

    AffineTransform baseTransform = h.getTransform();

  // check for any buffered exit events (this really should live somewhere else)

    for (int i=0; i<numCells; i++) {
      if (rfidExitPending[i] == true) { 
        if (rfidMWatchdog[i].isTokPresent() == false) {

          int lastVal = lastRfVals[i];
          wrack_server.processTokExit(i, lastVal);
          rfidExitPending[i] = false;

          int idx     = mapTag2Idx(lastVal);
          lastTagRot[idx] = rotVals[i];

        } else {
          //dbg("pending exit");
        }
      }
    }

  // Erase screen
  
    g.setColor(Color.black);
    g.clearRect(0, 0, winWidth, winHeight);

  // Paint Boxes

    for (int i=0; i<numCells; i++) {
      int x1 = (int) (currentCell[i] * cellInc + cellOffset);
      int y1 = yBase;

      int tagnum = -1;

      if (rfVals[i] == -1) { // no one here
        g.setColor(Color.gray);
        g.drawRect(x1, y1, panelWidth, panelHeight);
        //paintLabel(h, i);
	continue;
      } 

      int idx      = mapTag2Idx(rfVals[i]);
      double level = levels[idx];
      int c = (int) (256 * level);
      if (c > 255) {c=255;}
      if (c < 0)   {c = 0;}

      int tagId = rfVals[i];

      ParamWheel wheel = paramMgr.getId(tagId);

      if (wheel == null) {
        continue;
      } 

//      dbg("found tag: " + wheel.paramName);

      int  color[] = wheel.getColor();
      int nc[] = new int[3];

      for (int j=0; j < 3; j++) {
        nc[j] = (int) (color[j] * level);

	if (nc[j] < 0)   {nc[j] = 0;}
	if (nc[j] > 255) {nc[j] = 255;}

      }

      g.setColor(new Color(nc[0], nc[1], nc[2]));
      g.fillRect(x1, y1, panelWidth, panelHeight);
    }
    

  // Determine change in theta

    //circAngle += dthetaPerSec * (double) elapsedInterval / 1000.;

  // Draw selectors

    for (int i=0; i < numCells; i++) {

      if (rfVals[i] == -1) {
        continue;
      } 

      ParamWheel wheel = paramMgr.getId(rfVals[i]);

      if (wheel == null) {
        continue;
      } 
      
      int x1 = (int) ((currentCell[i] + 2) * cellInc + cellOffset);
      int y1 = yBase + 35;

      // draw bounding lines

      h.setStroke(new BasicStroke(3));

      h.setTransform(baseTransform);
      h.translate(x1, y1);

      AffineTransform cellTransform = h.getTransform();

      // calc pointer location

      int dPot = potVals[i] - potStartSpin[i];
//    rotVals[i] = rotStartSpin[i] + dPot * radsPerInc;
      rotVals[i] = dPot * radsPerInc;

      int idx      = mapTag2Idx(rfVals[i]);
      double level = (rotVals[i] * 3 / Math.PI / 2.) + .5;
      levels[idx] = level;

    int whichPot = i;

      double ratio = (rotVals[i] - minRot) / (maxRot - minRot);
      int broadcastVal = (int) (256. * ratio);

      wheel.defaultVal = ratio; // cache our state, in case we move

    wrack_server.processTokRot(whichPot, broadcastVal);

// back-solve:  minRot = (potVals[i] - potStartSpin[i]) * radsPerInc

      if (rotVals[i] < minRot) {
        rotVals[i] = minRot;
	potStartSpin[i] = potVals[i] - (int) (minRot / radsPerInc);

      } else if (rotVals[i] > maxRot) {

        rotVals[i] = maxRot;
	potStartSpin[i] = potVals[i] - (int) (maxRot / radsPerInc);
      }

/// discrete routines

//     if (rfVals[i] == 172 || rfVals[i] == 76 || rfVals[i] == 207 || 
//         rfVals[i] == 51 || rfVals[i] == 181) {

     if (wheel.continParam) {
       paintWheelContinuous(h, i, cellTransform, baseTransform);
     } else {
       paintWheelDiscrete(h, i, cellTransform, baseTransform);
     }

     h.setTransform(cellTransform);
     h.setColor(centerCircColor);
     h.fillOval(-centerCircDiam/2, -centerCircDiam/2 + 6, 
                 centerCircDiam, centerCircDiam);

   }
  
  // Look for "ands"
    h.setTransform(baseTransform);

    String nadjacencies = "";

    for (int i=0; i<3; i++) {
      int x1 = (int) ((currentCell[i] + 4) * cellInc + cellOffset - 6);
      if (rfVals[i] == -1 || rfVals[i+1] == -1) {continue;}

      int diff = currentCell[i+1] - currentCell[i];

      if (diff == 4) { // we have an "and"
        h.setColor(Color.white);
        g.fillRect(x1, 50, 12, 60);

	nadjacencies += "1";
      } else {
	nadjacencies += "0";
      }
    }

  //  updateAdjacencies(nadjacencies);

  // Draw framerate

    //g.drawString((int)updateRate + " fps", 5, 450);

  }

////////////////////  paint label /////////////////////////

 public void paintLabel(Graphics2D h, int whichPos) {

    int x1 = 
       (int) ((currentCell[whichPos] + 2) * cellInc + cellOffset) + 65;
    int y1 = yBase + 90;

    h.setFont(bigFont);
    h.setColor(bigLabelColor);

    AffineTransform baseTransform = h.getTransform();

    h.translate(x1, y1);
    h.rotate(Math.PI); //rotate by 180 degres

    String str = "";

    switch (whichPos) {
      case 0: str = "+"; break;
      case 1: str = "+"; break;
      case 2: str = "x"; break;
      case 3: str = "y"; break;
    }

    h.drawString(str, 0, 0);

    h.setTransform(baseTransform);
 }

////////////////////  paint wheel -- discrete vals /////////////////////////

private void paintWheelDiscrete(Graphics2D h, int wheelNum, 
          AffineTransform cellTransform, AffineTransform baseTransform) {

      h.rotate(rotVals[wheelNum]); 

      h.setStroke(new BasicStroke(12));
      h.setColor(new Color(50, 50, 50));
      h.drawLine(0, -10, 0, 75);

      h.setTransform(cellTransform);

   // bounding lines

      h.setStroke(new BasicStroke(3));

      h.rotate(minRot); 

      h.setColor(Color.gray);
      h.drawLine(0, 70, 0, 80);

      h.rotate(maxRot * 2.);
      h.drawLine(0, 70, 0, 80);

      h.rotate(minRot);

      h.setColor(new Color(50, 50, 50));

    // draw selector dots

      int diam = centerCircDiam + 65;

      h.rotate(minRot);

      int tagId = rfVals[wheelNum];
      ParamWheel wheel = paramMgr.getId(tagId);

      double range = (maxRot - minRot);

      if (wheel == null) {
        dbg("wheel of null size");
	return;
      }

      int numDots = wheel.size();
      double rotInc = range / numDots;

      h.rotate(rotInc/2.);
      double currentRot = minRot + rotInc/2.;

      for (int j=0; j<numDots; j++) {

        if (Math.abs(rotVals[wheelNum] - currentRot) < (rotInc/2.)) {
          h.setColor(Color.yellow); 
	  currentSelected[wheelNum] = j;
          wheel.selectedVal = j;

	} else {
          h.setColor(Color.gray); 
	}

        h.fillOval(-dotDiam/2, -dotDiam/2 + 68, dotDiam, dotDiam);  

           //these will become selectors
        h.rotate(rotInc);
	currentRot += rotInc;
      }


  // DRAW TEXT

      h.setFont(labelFont);
      h.setTransform(baseTransform);

    int x1 = (int) ((currentCell[wheelNum] + 4) * cellInc + cellOffset - 10);
    int y1 = yBase + 105;

      h.translate(x1, y1);
      h.rotate(Math.PI); //rotate by 180 degres

      //String label = wheel.paramName + " (" + wheel.size() + ")";
      String label = wheel.paramName;

      h.setColor(Color.white);
//      h.drawString(label, -8, +3);
      h.drawString(label, -8, -9);

      // SHOW PARAM VAL

      String value = wheel.getVal(currentSelected[wheelNum]);

      if (value.length() > 20) {
        value = value.substring(0, 14);
      }

      h.setFont(label2Font);
      int width =  h.getFontMetrics().stringWidth(value);

      h.drawString(value, 145 - width, -10);

    }

////////////////////  paint wheel -- continuous vals /////////////////////////

private void paintWheelContinuous(Graphics2D h, int wheelNum, 
          AffineTransform cellTransform, AffineTransform baseTransform) {

      int tagId = rfVals[wheelNum];
      ParamWheel wheel = paramMgr.getId(tagId);

      h.rotate(rotVals[wheelNum]); 

      h.setStroke(new BasicStroke(4));
      h.setColor(new Color(50, 50, 50));
      h.drawLine(0, -10, 0, 75);

      h.setTransform(cellTransform);

  // bounding lines

      h.setStroke(new BasicStroke(3));

      h.rotate(minRot); 

      h.setColor(Color.gray);
      h.drawLine(0, 70, 0, 80);

      h.rotate(maxRot * 2.);
      h.drawLine(0, 70, 0, 80);

      h.rotate(minRot);

      h.setColor(new Color(50, 50, 50));

  // baseArc

      h.setTransform(cellTransform);

      h.setStroke(new BasicStroke(5));
      h.setColor(new Color(90, 90, 90));

//      int diam = centerCircDiam + 55;
      int diam = centerCircDiam + 65;

      int arcBegin = (int) (minRot * 180. / Math.PI) - 90 - 3;
      int arcFull  = (int) ((maxRot - minRot) * 180. / Math.PI) + 6;


      h.drawArc (-diam/2, -diam/2+6, diam, diam, arcBegin, arcFull);

  // selected arc

      h.setStroke(new BasicStroke(6));
      h.setColor(Color.yellow);

      double ratio = (rotVals[wheelNum] - minRot) / (maxRot - minRot);
      int selectedArc = (int) (ratio * arcFull * -1);	 

      if (wheel.invertTok == false) {

        h.drawArc (-diam/2, -diam/2+6, diam, diam, 
                    arcBegin + arcFull, selectedArc);
		    
      } else { // invert

        h.drawArc (-diam/2, -diam/2+6, diam, diam, 
                    arcBegin,
		    arcFull + selectedArc);
      }

  // DRAW TEXT

      h.setFont(labelFont);
      h.setTransform(baseTransform);

    int x1 = (int) ((currentCell[wheelNum] + 4) * cellInc + cellOffset - 15);
    int y1 = yBase + 105;

      h.translate(x1, y1);
      h.rotate(Math.PI); //rotate by 180 degres

      //String label = wheel.paramName + " (" + wheel.size() + ")";

      String label = "";

      if (wheel != null) {
        label = wheel.paramName;
      } 

      h.setColor(Color.white);
//      h.drawString(label, -8, +3);
      h.drawString(label, -8, -9);

      // SHOW PARAM VAL

//      String value = wheel.getVal(currentSelected[wheelNum]);

      double paramRange = wheel.max - wheel.min;
      double val  = ratio * paramRange + wheel.min;

      String value = wheel.cleanupNumber(val);

      h.setFont(label2Font);
      int width =  h.getFontMetrics().stringWidth(value);

      h.drawString(value, 132 - width, -10); 

// BAU -- 06/17/02 -- DISPLAY L/R BOUNDS

      String minStr = wheel.cleanupNumber(wheel.min);
      String maxStr = wheel.cleanupNumber(wheel.max);

      h.setFont(label3Font);
      width =  h.getFontMetrics().stringWidth(minStr);

      h.drawString(minStr, 7 - width,  8); 
      h.drawString(maxStr, 120 - width, 8);
    }

////////////////////  Run /////////////////////////////

  // this gets kicked on by start()
  public void run() {

    //Remember the starting time.
    startTime   = System.currentTimeMillis();
    lastTime    = startTime;
    currentTime = startTime;

    if (antialiasingActive) {
       qualityHints = new RenderingHints(
          RenderingHints.KEY_ANTIALIASING, 
	  RenderingHints.VALUE_ANTIALIAS_ON);

       qualityHints.put(RenderingHints.KEY_RENDERING,
                        RenderingHints.VALUE_RENDER_QUALITY);
    }

    // loop until app death
    while (Thread.currentThread() == animationThread) {


      // do some fancy animation stuff...

         repaint(); //Reconsider in favor of BufferedImage?

      // ...then blit it to the screen
      // using BufferedImage or whatever

      try {  // let the OS and the GC do their things
	Thread.sleep(15);
      } catch (InterruptedException e) { }

      // the exception isn't important, it's only called if
      // the thread is awakened by some other process
    }
  }

////////////////////  Main /////////////////////////////

  static public void main(String args[]) {

  // start up rack monitor

    // QRackTest rackTest = new QRackTest();
    // RfidTest  rfidTest = new RfidTest();

  // light it up

    WRack queryUI = null;
    queryUI = new WRack();

    rootFrame = new JFrame("Query UI");
    rootComponent = queryUI;

    //queryUI.setSize(panelWidth, panelHeight);
    queryUI.setSize(winWidth, winHeight);

    rootFrame.setContentPane(rootComponent);

    rootFrame.addWindowListener(new WindowAdapter() {
      public void windowClosing(WindowEvent e) {
        System.exit(0);
      }
    });

    rootFrame.pack();
    rootFrame.setSize(winWidth, winHeight);

    rootFrame.setBounds(winXOrig, winYOrig, winWidth, winHeight);


    rootFrame.setVisible(true);

    rootFrame.setBackground(Color.black);
    rootFrame.setForeground(Color.gray);

    queryUI.startAnimation();
  }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("WRack." + (dcnt++) + ": " + s);
  } 
}

//// END ////

