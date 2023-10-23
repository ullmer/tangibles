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

public class GrScore {

/////////////  METHODS ///////////////

// static void main(String args[])
// public GrScatterVis()
// public run()

/////////////  MEMBERS ///////////////

  QRackVis parentVis = null;

  QRackMgr  qrackMgr = null;
  BldgDbMgr    dbMgr = null;

  Score score = null;
  ExperSet expSet = null;

  Logger logger = new Logger("whquery7");
  ControlServer controlServer = null;

  String lastQuery = "", currentQuery = "";

  Font  scoreFont  = new Font("Verdana", Font.PLAIN, 20);

  Font  doneFont   = new Font("Verdana", Font.PLAIN, 36);
//  Color doneColor  = new Color(0,175,0);
  Color doneColor  = Color.yellow;

  long currentTime;

  boolean matchInProgress = false;

  long matchBegun = -1;
  long timeThresh = 200; // 200 millis

  boolean recentExpChange = false;
  long    expChangedTime = -1;
  Color   expChangedColor = Color.yellow;

  Polygon attnPointer = null;
  int polyHeight = 25, polyWidth = -25;
  int polyX = 80, polyY = 10;
  long attnTimeThresh = 1250;

  boolean experimentComplete = false;

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

/////////////////  choose experiment set ///////////////////////

  public void chooseExpSet(int whichExpSet) {

    dbg("chooseExpSet called: " + whichExpSet);

    expSet.chooseExpSet(whichExpSet);
    logger.logStr("experiment number: " + whichExpSet);
  }

////////////////////  GrScatterVis /////////////////////////////

  public GrScore(QRackMgr mgr, QRackVis parentVis) {

    dbg("constructor called");

    this.parentVis = parentVis;

    qrackMgr = mgr;
    dbMgr    = (BldgDbMgr) qrackMgr.getInterp().getDbMgr();

    expSet = new ExperSet(dbMgr);
    expSet.setLogger(logger);

//    expSet.setCurrentExperiment(23);

    currentTime = System.currentTimeMillis();

    controlServer = new ControlServer();
    controlServer.startServer();

    controlServer.setLogger(logger);

    attnPointer = new Polygon();
    attnPointer.addPoint(polyX, polyY);
    attnPointer.addPoint(polyX - polyWidth, polyY + polyHeight/2);
    attnPointer.addPoint(polyX, polyY + polyHeight);
    attnPointer.addPoint(polyX, polyY);
   }

boolean firstTime = true;
boolean firstComplete = true;

////////////////////  paint /////////////////////////////

  public void paint(Graphics g) {

     //if (true) {return;}
     //if (dbMgr.visQueryCompleted == false) {return;}

  
 //// Draw it!

    g.setColor(Color.black);
    g.clearRect(0, 0, parentVis.panelWidth, parentVis.panelHeight);

    Graphics2D h = (Graphics2D) g;


 /// control handle

//// ANNA : REMOVE THIS COMMENT!

    if (controlServer.allowProgress == false) {return;}


    if (firstTime) {
      firstTime = false;
      logger.logStr("begin");
    }
  
 ///


//    if (dbMgr.visQueryResultsExist == ) {
//    }

// Handle experiment

    Experiment exp = expSet.getCurrentExperiment();

    if (exp == null) {
      dbg("paint problem: experiment is null! (B&A)");
      return;
    }

    double scoreVal = exp.evalByCriteria();

    String stateStr = "state: " + qrackMgr.getModel().describeState();
    logger.logStr(stateStr);

//    if (!experimentComplete) {

//      paintBars(h, 20, scoreVal, exp.expectedScore);
//      paintBars(h, 2, scoreVal, exp.expectedScore);
      paintBars(h, .5, scoreVal, exp.expectedScore);

    if (experimentComplete) {

//      displayDone(h);

      if (firstComplete) {
        firstComplete = false;
	logger.logStr("experiment complete");
	logger.flush();
      }
    }

    h.rotate(Math.PI);

// Score string

    String goalstr = "";

    if (experimentComplete) {
      goalstr = "Experiment complete";
    } else {
      goalstr = "goal: " + exp.genCriteriaStr();
    }

//    logger.logString(goalstr);

    h.setColor(Color.black);
    h.setFont(scoreFont);
    h.drawString(goalstr, -735, -15);

// Score string
/*
    String scorestr = "";

    if (scoreVal != -1) {
      scorestr = "score: " + scoreVal;
    } else {
      scorestr = "score: --";
    }

    h.setColor(Color.blue);
    h.drawString(scorestr, -150, -15);
*/
  }
 ///////////////////// paintBars///////////////////////
  
  public void displayDone(Graphics2D h) {

dbg("displayDone called");

    h.rotate(Math.PI);

    h.setColor(doneColor);
    h.setFont(doneFont);

//    h.drawString("DONE", -735, -15);
    h.drawString("DONE", -175, -10);

    h.rotate(Math.PI);
  }

 ///////////////////// paintBars///////////////////////

  Color barColor     = Color.blue;
  Color barBadColor  = Color.red;
  Color barGoodColor = Color.green;

  Color targlineColor = new Color(160,160,160);

  int barBaselineLen = 40;
  int barBaseX = 20;
  int barBaseY = 5;
  int barMaxlen = 150;

  int barTargLen = 30;

  Stroke bbstroke = new BasicStroke(1);

  int barwidth = 10;
  int barCOff  = 30;
  int barTOff  = 10;


  public void paintBars(Graphics2D h, double max, 
                                      double current, double target) {

   // draw baseline
    h.setColor(Color.black);
    h.setStroke(bbstroke);
    h.drawLine(barBaseX, barBaseY, barBaseX, barBaseY + barBaselineLen);

   // draw targline

    // double normAdjust = barTargLen/target;
    double normAdjust = 1;

    int barlen = (int) ((double)barMaxlen * target*normAdjust/max);

    h.setColor(targlineColor);

    h.drawLine(barBaseX + barlen, barBaseY, 
               barBaseX + barlen, barBaseY + barBaselineLen);

   // draw attention pointer

    if (recentExpChange) {

      long diffTime = currentTime - expChangedTime;
      if (diffTime > attnTimeThresh) {
        recentExpChange = false;
      } else { // draw the indicator

//        h.setColor(expChangedColor);
//        h.fillPolygon(attnPointer);

        displayDone(h);
  
        if (experimentComplete == false) {
 
//        logger.logStr("experiment complete");
//        logger.flush(); 
          experimentComplete = true;
        }
      }
    }

   // draw current

    boolean onTarget = false;

    if (current > 0) {

      barlen = (int) ((double)barMaxlen * current*normAdjust/max);
      if (barlen > barMaxlen) {barlen = barMaxlen;}

//      if (current < target) { // Fun for Brygg & Anna


      if (current <= target) {
        h.setColor(barGoodColor);
	onTarget = true;
      } else {
        h.setColor(barColor);
      }

      h.fillRect(barBaseX, barBaseY + barCOff, barlen, barwidth);
    } else {
      h.setColor(barBadColor);
      h.fillRect(barBaseX, barBaseY + barCOff, 20, barwidth);
    }

   // draw target

    barlen = (int) ((double)barMaxlen * target/max);
    if (barlen > barMaxlen) {barlen = barMaxlen;}

    h.setColor(barColor);
    h.fillRect(barBaseX, barBaseY + barTOff, barlen, barwidth);

   // handle other details

   //dbg("on target: " + onTarget);

   if (onTarget) {
     currentTime = System.currentTimeMillis();

     if (matchInProgress) {

       long passedTime = currentTime - matchBegun;
       //dbg("pt: " + passedTime);

       if (passedTime > timeThresh) {

//         int code = expSet.nextExperiment(); 
//	 logger.logStr("complete; next " + code);
//	 logger.logStr("complete");

/*
	 if (code == -1) {
	   experimentComplete = true;
	   return;
	 }
*/
	 expChangedTime = currentTime;
	 recentExpChange = true;
	 matchInProgress = false;
	 return;

       }
     } else {
       dbg("match begun");

      // OK, start a new match
       matchBegun = currentTime;
       matchInProgress = true;
     }
   } else { // not on target
     if (matchInProgress) {
       matchInProgress = false;
     }
   }
 }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("GrScoreVis." + (dcnt++) + ": " + s);
  } 
}

//// END ////
