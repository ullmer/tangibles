/// QueryRack server thread
/// By Brygg Ullmer, MIT Media Lab
/// Begun May 2, 2001
///
/// Based on threading template by Ben Fry (fry@media.mit.edu),
/// 4/18/2001, MediaFlow DisplayServer, October 9, 2000; 
/// and Java Tutorial's KKMultiServer 
/// Reworked on September 10, 2001

import java.util.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.awt.image.*;

import javax.swing.*;
import java.net.*;
import java.io.*;

///////////////////////////////////////////////////////////
////////////////////  QRServer /////////////////////////////
///////////////////////////////////////////////////////////

public class QRServer implements Runnable {

/////////////  METHODS ///////////////

// public QRServer()
// public void run()

// public void broadcastStr(String str)

// private byte[] hexbytes(int val)

/////////////  MEMBERS ///////////////

  int     port = 4050;
  Thread  serverThread;

  ServerSocket serverSocket = null;

  boolean listening = true;
  boolean frozen  = false;

  Vector childThreads = new Vector();

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

////////////////////  QRServer /////////////////////////////

  public QRServer() {

  }

////////////////////  broadcast String /////////////////////////////

  public void broadcastStr(String str) {

    int numChildren = childThreads.size();

    for (int i=0; i < numChildren; i++) {
      ServerThread childThread = 
	(ServerThread) childThreads.elementAt(i);

      if (childThread != null && childThread.out != null) {
        childThread.out.println(str);

	childThread.out.flush(); // REMOVE?!
      }
    }
  }

////////////////////  hexbytes /////////////////////////////

  private byte hexbyte(int val) { // 1 character
    String hex = Integer.toHexString(val);
    byte result = (byte) hex.charAt(0);
    return result;
  } 

  private byte[] hexbytes(int val) { // 2 characters
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

  public void setParam(int rackId, int cellNum, int bound1, 
                       int bound2, int tokId) {

    byte outBytes[] = new byte[9];
    byte hex[];

    outBytes[0] = 'P';
    outBytes[1] = (byte) ('0' + cellNum);

    outBytes[2] = hexbyte(rackId);
    

    hex = hexbytes(bound1);
    outBytes[3] = hex[0];
    outBytes[4] = hex[1];

    hex = hexbytes(bound2);
    outBytes[5] = hex[0];
    outBytes[6] = hex[1];

    hex = hexbytes(tokId);
    outBytes[7] = hex[0];
    outBytes[8] = hex[1];

    String command = new String(outBytes);
    broadcastStr(command);
  }

////////////////////  setParam /////////////////////////////

  public void setReed(int reedLoc, int reedState) {

    byte outBytes[] = new byte[3];
    byte hex[];

    outBytes[0] = 'R';
    outBytes[1] = (byte) ('0' + reedLoc);
    outBytes[2] = (byte) ('0' + reedState);

    String command = new String(outBytes);
    broadcastStr(command);
  }

////////////////////  setParam /////////////////////////////

  public void setAxis(char axis, int bound1, int bound2, int tokId) {

    byte outBytes[] = new byte[8];
    byte hex[];

    outBytes[0] = 'X';

    if (axis != 'X' && axis != 'Y') {
      dbg("setAxis error: axis param must = 'X' or 'Y' (case sensitive");
      return;
    }

    outBytes[1] = (byte) axis;

    hex = hexbytes(bound1);
    outBytes[2] = hex[0];
    outBytes[3] = hex[1];

    hex = hexbytes(bound2);
    outBytes[4] = hex[0];
    outBytes[5] = hex[1];

    hex = hexbytes(tokId);
    outBytes[6] = hex[0];
    outBytes[7] = hex[1];

    String command = new String(outBytes);
    broadcastStr(command);
  }

////////////////////  setRelation /////////////////////////////

  public void setRelation(String relation) {

    if (relation == null) {
      dbg("Null relationship passed to setRelation; ignoring.");
      return;
    }

    int len = relation.length();

    byte outBytes[] = new byte[len + 1];

    outBytes[0] = 'R';

    for (int i=0; i<len; i++) {
      outBytes[i+1] = (byte) relation.charAt(i);
    }

    String command = new String(outBytes);
    broadcastStr(command);
  }
  
////////////////////  setAdjacencies /////////////////////////////

 // Old function, but it may prove useful

  public void setAdjacencies(String adjacencies) {

    if (adjacencies == null) {
      dbg("bogosity in setAdjacencies: null string"); return;
    }

    if (adjacencies.length() != 3) {
      dbg("bogosity in setAdjacencies: length != 3 : " + adjacencies.length());
      return;
    }

    dbg("setAdjacencies " + adjacencies);

    String command = "A" + adjacencies;
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
//    QRServer venn;
//    venn = new QRServer();
//    venn.startServer();
//  }

  ////////////////////// debug ////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("QRServer[" + (dcnt++) + "] " + s);
  }
}

//// END ////

