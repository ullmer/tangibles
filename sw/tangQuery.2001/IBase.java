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

///////////////////////////////////////////////////////////
////////////////////  IBase /////////////////////////////
///////////////////////////////////////////////////////////

public class IBase implements Runnable, QRackMgr {

/////////////  METHODS ///////////////

// static void main(String args[])
// public IBase()
// public run()

/////////////  MEMBERS ///////////////

  Thread animationThread;

  boolean frozen  = false;

//  static int panelWidth = 512, panelHeight = 512;
//  static int panelWidth = 730, panelHeight = 650;

//  static int panelWidth = 1095, panelHeight = 975; // MOVE TO VIS!
//  static int panelWidth = 1024, panelHeight = 1024; // MOVE TO VIS!
  static int panelWidth = 380, panelHeight = 400; // MOVE TO VIS!

  int scatterX = 0;
  int geoX     = -1024;

  int expSet = -1; // experiment set

/// Content management

  QRackInterp qrackInterp = null;

//  QRackVis    qrackVis    = null;

  QRackVis    scatterVis = null;
  QRackVis    geoVis     = null;
  QRackVis    scoreVis   = null;

//  GrRelVis    relVis    = null;
//  GrRRelVis   rrelVis    = null;
//  GrParamBind paramBind = null;

// Temporary flags
  static boolean renderGeoOnly   = false;
  static boolean renderAllButGeo = false;

  boolean handleIconification = true;

//  boolean geoIconified  = true; 
  boolean geoIconified  = false; 
  boolean fundIconified = true; 

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

  public QRackInterp getInterp() {return qrackInterp;}
  public WRackModel  getModel()  {return getInterp().getModel();}

////////////////////  IBase /////////////////////////////

  public IBase() {
    // do your app setup stuff here...

    qrackInterp = new QRackInterp(this, 'b');

    //qrackVis    = new QRackVis(this);

    if (renderAllButGeo == false) {

      geoVis     = new QRackVis(this, 'g', "map viewer", 
//                                  panelWidth, panelHeight, 1030, 145);
                                  panelWidth, panelHeight, 830, 145);

//                                  panelWidth, panelHeight, -895, 145);

//                                  panelWidth, panelHeight, 295, 1190);
//                                  panelWidth, panelHeight, 62, 1466);
//                                  panelWidth, panelHeight, 62, 1466);
//                                  panelWidth, panelHeight, 125, 1466);
//                                  panelWidth, panelHeight, 360, 1190);
//                                  panelWidth, panelHeight, 380, 1190);
//                                  panelWidth, panelHeight, 380, 1240);
//                                  panelWidth, panelHeight, 300, 1240);
//                                  panelWidth, panelHeight, 300, 1305);
//                                  panelWidth, panelHeight, 680, 1305);

//                                  panelWidth, panelHeight, 1685, 280);

      scoreVis = new QRackVis(this, 'e', "score viewer",
                              800, 75, 830, 520);
//                              800, 75, -895, 520);

      qrackInterp.addVis(geoVis);
      qrackInterp.addVis(scoreVis);
    }

    if (renderGeoOnly == false) {

      scatterVis = new QRackVis(this, 's', "scatter viewer",
                                panelWidth, panelHeight, -515, 145);
//                                panelWidth, panelHeight, 675, 1190);
//                                panelWidth, panelHeight, 442, 1466);
//                                panelWidth, panelHeight, 505, 1466);
//                                panelWidth, panelHeight, 740, 1190);
//                                panelWidth, panelHeight, 740, 1240);
//                                panelWidth, panelHeight, 680, 1240);
//                                panelWidth, panelHeight, 300, 1305);

//                                panelWidth, panelHeight, 1300, 280);
//      relVis      = new GrRelVis(this, "relations");
//      paramBind  = new GrParamBind(this, "parameter bindings", 'b');

      qrackInterp.addVis(scatterVis);
    }


    if (geoIconified && handleIconification) {
      iconify(0);
    }

    // ...then start the thread
    // (make sure you do this after setup, seems obvious,
    // until you forget and get really confusing inconsistent
    // problems as your app starts up in stochastically half-
    // initialized states)

    // Moved the following Fry code to startAnimation
    //  thread = new Thread(this);
    //  thread.start();

  }

////////////////////  deiconify /////////////////////////////

  public void deiconify(int containerID) {
    dbg("deiconify called");

    if (handleIconification == false) {return;}

    if (containerID == 0) { // GEO

      if (getInterp().dataType == 'b') { // we need to be ASSIGNING this! 

        geoIconified = false;

	if (renderGeoOnly == false) {
	  scatterVis.deiconify();
	  scoreVis.deiconify();
	}

	if (renderAllButGeo == false) {
	  geoVis.deiconify();
	}
      }
    }
  }

////////////////////  iconify /////////////////////////////

  public void iconify(int containerID) {

   try {
    dbg("iconify called");

    if (handleIconification == false) {return;}

    if (containerID == 0) { // GEO

      if (getInterp().dataType == 'b') { // we need to be ASSIGNING this! 

        geoIconified = true;

	if (renderGeoOnly == false) {
	  scatterVis.iconify();
	}

	if (renderAllButGeo == false) {
	  geoVis.iconify();
	}
      }
    }
   } catch (Exception e) {dbg("iconify exception: " + e.toString());}
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

////////////////////  Run /////////////////////////////

  boolean firstIter= true;

  // this gets kicked on by start()
  public void run() {

    // loop until app death
    while (Thread.currentThread() == animationThread) {

      // do some fancy animation stuff...

      //qrackVis.repaint(); 

      getModel().update();

      if (qrackInterp.dbMgr.visQueryCompleted == true) {

        if (renderAllButGeo == false && geoIconified == false) {
          geoVis.repaint(); 
          scoreVis.repaint(); 
	}

	if (renderGeoOnly == false && geoIconified == false) {
          scatterVis.repaint(); 
	}
      }

      // ...then blit it to the screen
      // using BufferedImage or whatever

      try {  // let the OS and the GC do their things
	//Thread.sleep(5);
	//Thread.sleep(50);
	Thread.sleep(150);
      } catch (InterruptedException e) { }

      // the exception isn't important, it's only called if
      // the thread is awakened by some other process
    }
  }

/////////////////  choose Experiment Set ///////////////////////

  public void chooseExpSet(String sExpSet) {

    try {
      expSet = Integer.parseInt(sExpSet);
      dbg("Experiment set: " + expSet);

      if (scoreVis != null) {

        scoreVis.scoreVis.chooseExpSet(expSet); // cute, eh? sigh...
      } else {
        dbg("chooseExpSet: scoreVis is null!");
      }

    } catch (Exception e) {

      dbg("chooseExpSet exception: " + e.toString());
    }
  }

////////////////////  Main /////////////////////////////

  static public void main(String args[]) {

  // use args to pass in command line arguments -- e.g., 
  //  for temporarily specifying different data sets

  if (args.length > 0) {
    dbg("Arg received: " + args[0]);

    if (args[0].compareTo("geo") == 0) {
      renderGeoOnly = true;
    } 

    if (args[0].compareTo("nogeo") == 0) {
      renderAllButGeo = true;
    }

  } else {
    dbg("No args");
  }

  // start up rack monitor

    IBase qrackMgr = null;
    qrackMgr = new IBase();

   if (args.length > 1) {
     qrackMgr.chooseExpSet(args[1]);
   }
  

    qrackMgr.startAnimation();
  }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  static public void dbg(String s) {

    System.out.println("IBase." + (dcnt++) + ": " + s);
  } 
}

//// END ////

