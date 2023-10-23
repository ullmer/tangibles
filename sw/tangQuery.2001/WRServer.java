/// QueryRack server thread
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
////////////////////  WRServer /////////////////////////////
///////////////////////////////////////////////////////////

public class WRServer implements Runnable {

/////////////  METHODS ///////////////

// public WRServer()
// public void run()

// public void broadcastStr(String str)

// public void clearParam(int circleNum)
// public void setParam(int circleNum, int r, int g, int b)
// public void setText(int circleNum, String text)

// private byte[] hexbytes(int val)

/////////////  MEMBERS ///////////////

  int     port = 4075;
  Thread  serverThread;

  ServerSocket serverSocket = null;

  boolean listening = true;
  boolean frozen  = false;

  Vector childThreads = new Vector();

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

////////////////////  WRServer /////////////////////////////

  public WRServer() {

  }

// N // processTokEntrance(int rackId, int cellId, int tokId);
// X // processTokExit    (int rackId, int cellId, int tokId);

// R // processTokRot  (int rackId, int cellId, int tokId, double val);
// A // processAdj     (int rackId, String adjStr);


////////////////////  broadcast String /////////////////////////////

  public void broadcastStr(String str) {

    int numChildren = childThreads.size();

    for (int i=0; i < numChildren; i++) {
      ServerThread childThread = 
	(ServerThread) childThreads.elementAt(i);

      if (childThread != null && childThread.out != null) {
        childThread.out.println(str);
      }
    }
  }

////////////////////  hexbytes /////////////////////////////

  private byte[] hexbytes(int val) {
    // creates bytes[2] rep of 8-bit val, from 00 to FF

    String hex = Integer.toHexString(val);

    byte result[] = new byte[2];

    if (hex.length() == 1) {
      result[0] = '0';
      result[1] = (byte) hex.charAt(0);
    } else {
      result[0] = (byte) hex.charAt(0);
      result[1] = (byte) hex.charAt(1);
    }

    return result;
  }

////////////////////  setParam /////////////////////////////

  public void processTokEntrance(int cellId, int tokId) {

dbg("dispatching entrance event: " + cellId + " " + tokId);

    try {

      int rackId = 0;
  
      byte outBytes[] = new byte[7];
      byte hex[] = new byte[2];
  
      outBytes[0] = 'N';
  
      hex = hexbytes(rackId);
      outBytes[1] = hex[0];
      outBytes[2] = hex[1];
  
      hex = hexbytes(cellId);
      outBytes[3] = hex[0];
      outBytes[4] = hex[1];
  
      hex = hexbytes(tokId);
      outBytes[5] = hex[0];
      outBytes[6] = hex[1];
  
      String command = new String(outBytes);
      broadcastStr(command);
    } catch (Exception e) {
      dbg("processTokEntrance exception: " + e.toString());
    }
  }
  

////////////////////  processTokExit /////////////////////////////

  public void processTokExit (int cellId, int tokId) {

dbg("dispatching exit event: " + cellId + " " + tokId);

//  dbg("setText " + circleNum + " " + text);

    int rackId = 0;

    byte outBytes[] = new byte[7];
    byte hex[] = new byte[2];

    outBytes[0] = 'X';

    hex = hexbytes(rackId );
    outBytes[1] = hex[0];
    outBytes[2] = hex[1];

    hex = hexbytes(cellId);
    outBytes[3] = hex[0];
    outBytes[4] = hex[1];

    hex = hexbytes(tokId);
    outBytes[5] = hex[0];
    outBytes[6] = hex[1];

    String command = new String(outBytes);
    broadcastStr(command);
  }
  
////////////////////  setTag /////////////////////////////

  public void processTokRot (int cellId, int rotVal) {

//  dbg("setTag " + circleNum + " " + tagId);

    int rackId = 0;

    byte outBytes[] = new byte[7];
    byte hex[] = new byte[2];

    outBytes[0] = 'R';

    hex = hexbytes(rackId );
    outBytes[1] = hex[0];
    outBytes[2] = hex[1];

    hex = hexbytes(cellId);
    outBytes[3] = hex[0];
    outBytes[4] = hex[1];

    hex = hexbytes(rotVal);
    outBytes[5] = hex[0];
    outBytes[6] = hex[1];

    String command = new String(outBytes);
    broadcastStr(command);
  }
  
////////////////////  setAdjacencies /////////////////////////////

  public void processAdjacencies (String adjStr) {
// A // 

    if (adjStr== null) {
      dbg("bogosity in setAdjacencies: null string"); return;
    }

    if (adjStr.length() != 3) {
      dbg("bogosity in setAdjacencies: length != 3 : " + adjStr.length());
      return;
    }

    dbg("setAdjacencies " + adjStr);

    String command = "A" + adjStr;
    broadcastStr(command);
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
	ServerThread servthread = 
          new ServerThread(serverSocket.accept());

        servthread.start();
	childThreads.addElement(servthread);
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

////////////////////  Main /////////////////////////////

//  static public void main(String args[]) {
//
//    WRServer venn;
//    venn = new WRServer();
//    venn.startServer();
//  }

  ////////////////////// debug ////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("WRServer[" + (dcnt++) + "] " + s);
  }
}

//// END ////

