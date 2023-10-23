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
import javax.swing.*;
import java.io.*;

///////////////////////////////////////////////////////////
////////////////////  SpinCirc /////////////////////////////
///////////////////////////////////////////////////////////

public class SpinCirc extends JComponent
		     implements Runnable {

/////////////  METHODS ///////////////

// static void main(String args[])
// public SpinCirc()
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

// Sample circle element

  int circDiam   = 80;
  int pathRadius = 150;
  double circAngle  = 0;
  double dthetaPerSec = 150;
  int cx = 200, cy = 200;

  Color circColor = new Color(110,50,60);

  RenderingHints qualityHints;
  boolean antialiasingActive = true; 
    //Use antialiased text, by default

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

////////////////////  SpinCirc /////////////////////////////

  public SpinCirc() {
    // do your app setup stuff here...

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

  // Erase screen
  
    g.setColor(Color.black);
    g.clearRect(0, 0, 500, 500);

  // Determine change in theta

    circAngle += dthetaPerSec * (double) elapsedInterval / 1000.;

  // Draw circle

    int x, y;
    x = cx + (int) (pathRadius * Math.cos(circAngle * 17.45e-3));
    y = cy + (int) (pathRadius * Math.sin(circAngle * 17.45e-3));

    h.setColor(circColor);
    h.fillOval(x, y, circDiam, circDiam);

  // Draw framerate

    //g.drawString((int)updateRate + " fps", 5, 450);

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
	Thread.sleep(5);
      } catch (InterruptedException e) { }

      // the exception isn't important, it's only called if
      // the thread is awakened by some other process
    }
  }

////////////////////  Main /////////////////////////////

  static public void main(String args[]) {

    SpinCirc spinCirc = null;

    // light it up

    spinCirc = new SpinCirc();

    rootFrame = new JFrame("Query UI");
    rootComponent = spinCirc;

    spinCirc.setSize(500, 500);

    rootFrame.setContentPane(rootComponent);

    rootFrame.addWindowListener(new WindowAdapter() {
      public void windowClosing(WindowEvent e) {
        System.exit(0);
      }
    });

    rootFrame.pack();
    rootFrame.setSize(500, 500);
    rootFrame.setVisible(true);

    rootFrame.setBackground(Color.black);
    rootFrame.setForeground(Color.gray);

    spinCirc.startAnimation();
  }
}

//// END ////

