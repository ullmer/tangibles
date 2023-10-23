/// ControlServer server thread
/// By Brygg Ullmer, MIT Media Lab
/// Begun May 2, 2001
///

import java.util.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.awt.image.*;

import javax.swing.*;
import java.net.*;
import java.io.*;

///////////////////////////////////////////////////////////
////////////////////  ControlServer /////////////////////////////
///////////////////////////////////////////////////////////

public class ControlServer implements Runnable {

  boolean allowProgress = false;

/////////////  METHODS ///////////////

// public ControlServer()
// public void run()

// public void broadcastStr(String str)

// public void clearParam(int circleNum)
// public void setParam(int circleNum, int r, int g, int b)
// public void setText(int circleNum, String text)

// private byte[] hexbytes(int val)

/////////////  MEMBERS ///////////////

  int     port = 5000;
  Thread  serverThread;

  ServerSocket serverSocket = null;

  boolean listening = true;
  boolean frozen  = false;

  Vector childThreads = new Vector();

  Logger logger = null;

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

////////////////////  ControlServer /////////////////////////////

  public ControlServer() {

  }

////////////////////  startServer /////////////////////////////
  
  public void startServer() {

    if (frozen) {

    } else {

      if (serverThread == null) {
        serverThread = new Thread(this);
      }
      serverThread.start();
    }
  }

////////////////////  Run /////////////////////////////

  public void run() {

    try {
        serverSocket = new ServerSocket(port);
    } catch (IOException e) {
        System.err.println("Could not listen on port: " + port);
        System.exit(-1);
    }

    //Remember the starting time.
    //startTime   = System.currentTimeMillis();

    // loop until app death
    while (Thread.currentThread() == serverThread && listening) {

      try { 
	ControlThread servthread = 
          new ControlThread(serverSocket.accept(), this);

        servthread.start();
	childThreads.addElement(servthread);

	servthread.logger = logger;
      } catch (Exception e) {

	dbg("Exceptions generated on creation of child server thread");
	dbg("Ignoring, but may be unsafe; check it out.");
	continue;
      }
    }

    try {serverSocket.close();} catch (Exception e) {
      dbg("Exception generated on attempt to close serverSocket.");
    }
  }

////////////////////  broadcast String /////////////////////////////

  public void setLogger(Logger logger) {
    int numChildren = childThreads.size();

    this.logger = logger;

    for (int i=0; i < numChildren; i++) {
      ControlThread childThread = 
	(ControlThread) childThreads.elementAt(i);

      childThread.logger = logger;
    }
  }

////////////////////  broadcast String /////////////////////////////

  public void broadcastStr(String str) {

    int numChildren = childThreads.size();

    for (int i=0; i < numChildren; i++) {
      ControlThread childThread = 
	(ControlThread) childThreads.elementAt(i);

      if (childThread != null && childThread.out != null) {
        childThread.out.println(str);
      }
    }
  }
////////////////////  Main /////////////////////////////

  static public void main(String args[]) {

    ControlServer ctrl;
    ctrl = new ControlServer();
    ctrl.startServer();
  }

  ////////////////////// debug ////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("ControlServer[" + (dcnt++) + "] " + s);
  }
}

//// END ////

