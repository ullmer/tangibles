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
////////////////////  QRackMgr /////////////////////////////
///////////////////////////////////////////////////////////

public class QRackVis extends JComponent {

/////////////  METHODS ///////////////

// static void main(String args[])
// public QRackMgr()
// public run()

/////////////  MEMBERS ///////////////

//  CircTest qrackMgr    = null;

  QRackMgr    qrackMgr    = null;
  QRackInterp qrackInterp = null;

  GrGeoVis      geoVis      = null;
  GrScatterVis  scatterVis  = null;
  GrScore       scoreVis    = null;

//  GrGeoBaseline geoBaseline = null;
//  GrMutualVis     mutualVis  = null;

// Java Frames

  long startTime, lastTime, currentTime;
  int  elapsedInterval = 0;
  double updateRate    = 0.;
 
  int frameNumber = -1;

  JFrame rootFrame;

  RenderingHints qualityHints;
  RenderingHints alphaHints;

  boolean antialiasingActive = true;

  //int panelWidth = 1095, panelHeight = 975;
  int panelWidth, panelHeight;

  int winX=0, winY=0;
  
  String title = "viewer";

// Other

  char whichVis; //g = Geo, s = Scatter
  boolean isIconified = false;

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

////////////////////  QRackVis /////////////////////////////

//  public QRackVis(CircTest mgr, char whichVis, String title) {

  public QRackVis(QRackMgr mgr, char whichVis, String title,
                  int panelWidth, int panelHeight) {

     this(mgr, whichVis, title, panelWidth, panelHeight, 0, 0);
  }

  public QRackVis(QRackMgr mgr, char whichVis, String title,
                  int panelWidth, int panelHeight, int baseX, int baseY) {

    qrackMgr   = mgr;
    this.whichVis = whichVis;
    this.title = title; 
    
    this.panelWidth  = panelWidth;
    this.panelHeight = panelHeight;

    switch (whichVis) {

      case 'g': geoVis      = new GrGeoVis(mgr, this); break;
      case 's': scatterVis  = new GrScatterVis(mgr, this); break;
      case 'e': scoreVis    = new GrScore(mgr, this); break;

//    case 'm': mutualVis   = new GrMutualVis(mgr, this); break;
//    case 'c': geoBaseline = new GrGeoBaseline(mgr, this); break;
    }

  // Java vis setup

    rootFrame = new JFrame(title);

    setSize(panelWidth, panelHeight);

    rootFrame.setContentPane(this);

    rootFrame.addWindowListener(new WindowAdapter() {
      public void windowClosing(WindowEvent e) {
        System.exit(0);
      }
    });

    rootFrame.pack();
    rootFrame.setSize(panelWidth, panelHeight); 
    rootFrame.setVisible(true);

    //rootFrame.setBackground(Color.black);
    //rootFrame.setBackground(Color.gray);
    //rootFrame.setBackground(Color.green);
    rootFrame.setBackground(new Color(180, 180, 180));
    rootFrame.setForeground(Color.white);

    //rootFrame.setBounds(baseX, baseY, panelWidth, panelHeight);
    moveWin(baseX, baseY);

    rootFrame.show();
    rootFrame.toBack();

    // Set crosshair cursor
    setCursor(Cursor.getPredefinedCursor(Cursor.CROSSHAIR_CURSOR));

    if (antialiasingActive) {
       qualityHints = new RenderingHints(
          RenderingHints.KEY_ANTIALIASING, 
	  RenderingHints.VALUE_ANTIALIAS_ON);

       qualityHints.put(RenderingHints.KEY_RENDERING,
                        RenderingHints.VALUE_RENDER_QUALITY);
    }

/*
    alphaHints = new RenderingHints(
      RenderingHints.KEY_ALPHA_INTERPOLATION, 
      RenderingHints.VALUE_ALPHA_INTERPOLATION_QUALITY);

    alphaHints.put(RenderingHints.KEY_RENDERING,
                   RenderingHints.VALUE_RENDER_QUALITY);
*/

  // Timing details

    //Remember the starting time.
    startTime   = System.currentTimeMillis();
    lastTime    = startTime;
    currentTime = startTime;

  }

 ////////////////////  moveWin ////////////////////

  public void moveWin(int newX, int newY) {

    winX = newX; winY = newY;
    rootFrame.setBounds(newX, newY, panelWidth, panelHeight);
  }

 ////////////////////  get Win Coords ////////////////////

  public int[] getWinCoords() {

    int coord[] = new int[2];

    coord[0] = winX;
    coord[1] = winY;

    return coord;
  }

 //////////////////// iconify ////////////////////

  public void iconify() {
    if (isIconified == false) {

      rootFrame.setState(Frame.ICONIFIED);
      isIconified = true;
    }
  }

  public void deiconify() {
    if (isIconified == true) {

      rootFrame.setState(Frame.NORMAL);
      rootFrame.toFront();
      isIconified = false;
    }
  }
 ////////////////////  ptokEnters ////////////////////

  public void ptokEnters(PTokModel ptok) {
    if (whichVis == 'g' && geoVis != null) {
      geoVis.ptokEnters(ptok);
    }

    //scatterVis.ptokEnters(ptok);
  }

 ////////////////////  ptokChanges ////////////////////

  public void ptokChanges(PTokModel ptok) {
    if (whichVis == 'g' && geoVis != null) {
      geoVis.ptokChanges(ptok);
    }

    //scatterVis.ptokEnters(ptok);
  }

 ////////////////////  paint ////////////////////

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

//    h.setRenderingHints(alphaHints);

    switch (whichVis) {

      case 'g': geoVis.paint(g); return;
      case 's': scatterVis.paint(g); return;
      case 'e': scoreVis.paint(g); return;

//      case 'm': mutualVis.paint(g); return;

//      case 'c': geoBaseline.paint(g); break;
    }
  }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("QRackVis." + (dcnt++) + ": " + s);
  } 
}

//// END ////

