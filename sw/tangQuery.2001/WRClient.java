// Display server for QueryUI
// By Brygg Ullmer, MIT Media Lab

// Descended from MediaFlow WRClient
// Begun October 9, 2000
// Reworked on May 2, 2001

import java.net.*;
import java.io.*;
import java.util.*;

//////////////////////////////////////////////////////
//////////////////// Venn Client /////////////////////
//////////////////////////////////////////////////////


public class WRClient extends Thread {

//////////////////// members /////////////////////

  private Socket socket = null; 

  Socket rfidSocket = null;
  PrintWriter out   = null;
  BufferedReader in = null;

  //String server = "baram";
  String server = "tsunami";
  int    port   = 4075;

  Vector listeners = null;

// N // processTokEntrance(int rackId, int cellId, int tokId);
// X // processTokExit    (int rackId, int cellId, int tokId);

// R // processTokRot  (int rackId, int cellId, int rotVal);
// A // processAdjacencies     (int rackId, String adjStr);


//////////////////// methods /////////////////////

//  public WRClient(Venn wrDisplay) 
//  public void run() 

/////////////////////////////////////////////////
//////////////////// bodies /////////////////////
/////////////////////////////////////////////////

///////////// constructor ///////////////

  public WRClient() {
    super("WRClient");
    //this.ui   = ui;

    listeners = new Vector();

    dbg("started");
  }

  public WRClient(WRCListener listener) {

    this();
    addListener(listener);
  }

/////////////////////// addListener ///////////////////////

  public void addListener(WRCListener listener) {

    listeners.addElement(listener);
  } 

///////////// run ///////////////

  public void run() {
  dbg("running");

    try {
      rfidSocket = new Socket(server, port);
      out = new PrintWriter(rfidSocket.getOutputStream(), true);
      in  = new BufferedReader(
	            new InputStreamReader(rfidSocket.getInputStream()));

    } catch (UnknownHostException e) {

      dbg("Don't know about host: " + server);
      System.exit(1);

    } catch (IOException e) {
      dbg("Couldn't get I/O for the connection to: " + server);
      System.exit(1);
    }

    BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));

    String fromServer; 
    String fromUser;

    try {
    while (true) {
    while ((fromServer = in.readLine()) != null) { 

// N // processTokEntrance(int rackId, int cellId, int tokId);
// X // processTokExit    (int rackId, int cellId, int tokId);

// R // processTokRot  (int rackId, int cellId, int rotVal);
// A // processAdjacencies     (int rackId, String adjStr);

/// Nx: Tok entrance param "x"

       if (fromServer.startsWith("N")) {

	 int rackId, cellId, tokId;
	 String sr;

	 try {
           sr = fromServer.substring(1,3);
	   rackId = Integer.valueOf(sr, 16).intValue();

           sr = fromServer.substring(3,5);
	   cellId = Integer.valueOf(sr, 16).intValue();

           sr = fromServer.substring(5,7);
	   tokId = Integer.valueOf(sr, 16).intValue();

	 } catch (Exception e) {

	   dbg("Exception in processing Entrance command argument; ignoring");
	   continue;
	 }

//	 dbg("received entrance event: " + cellId + " " + tokId);

	 processTokEntrance(rackId, cellId, tokId);
	 continue;
       }

/// Xx: Tok exit param "x"

       if (fromServer.startsWith("X")) {

	 int rackId, cellId, tokId;
	 String sr;

	 try {
           sr = fromServer.substring(1,3);
	   rackId = Integer.valueOf(sr, 16).intValue();

           sr = fromServer.substring(3,5);
	   cellId = Integer.valueOf(sr, 16).intValue();

           sr = fromServer.substring(5,7);
	   tokId = Integer.valueOf(sr, 16).intValue();

	 } catch (Exception e) {

	   dbg("Exception in processing Exit command argument; ignoring");
	   continue;
	 }

//	 dbg("received exit event: " + cellId + " " + tokId);

	 processTokExit(rackId, cellId, tokId);
	 continue;
       }

/// Rx: Tok rotate param "x"

       if (fromServer.startsWith("R")) {

	 int rackId, cellId, rotVal;
	 String sr;

	 try {
           sr = fromServer.substring(1,3);
	   rackId = Integer.valueOf(sr, 16).intValue();

           sr = fromServer.substring(3,5);
	   cellId = Integer.valueOf(sr, 16).intValue();

           sr = fromServer.substring(5,7);
	   rotVal = Integer.valueOf(sr, 16).intValue();

	 } catch (Exception e) {

	   dbg("Exception in processing Rotate command argument: " 
                + e.toString());
	   continue;
	 }

	 processTokRot(rackId, cellId, rotVal);
	 continue;
       }

/// A: tok adjacencies
       if (fromServer.startsWith("A")) { // text

         int len = fromServer.length();

	 String adjacencies = fromServer.substring(1,len-1);
	 processAdjacencies(adjacencies);
	 continue;
       }
    } sleep(2);}
    } catch (Exception e) {dbg("close exception: " + e.toString());}

    try {
      in.close();
      stdIn.close();
      rfidSocket.close();
    } catch (Exception e) {dbg("close exception: " + e.toString());}
  }

///////////////////////////////////////////////////////
/////////////////////// process ///////////////////////

// N // processTokEntrance(int rackId, int cellId, int tokId);
// X // processTokExit    (int rackId, int cellId, int tokId);

// R // processTokRot  (int rackId, int cellId, int rotVal);
// A // processAdjacencies     (int rackId, String adjStr);

/////////////////////// process Tok Entrance ///////////////////////
  
  public void processTokEntrance(int rackId, int cellId, int tokId) {

    if (listeners == null) {
       dbg("processTokEntrance major weirdness: null listeners!");
    }

    int numListeners = listeners.size();

dbg("tok entrance: cell " + cellId + ", tok " + tokId);

    try {


      for (int i=0; i < numListeners; i++) {
        WRCListener listener = (WRCListener) listeners.elementAt(i);

        if (listener == null) {
	  dbg("processTokEntrance bug: problem addressing listener!");
	  continue;
	}

        listener.processTokEntrance(rackId, cellId, tokId);
      }
    } catch (Exception e) {
      dbg("processTokEntrance exception: " + e.toString());
    }
  }

/////////////////////// process Tok Entrance ///////////////////////
  
  public void processTokExit(int rackId, int cellId, int tokId) {

    int numListeners = listeners.size();

    try {

      for (int i=0; i < numListeners; i++) {
        WRCListener listener = (WRCListener) listeners.elementAt(i);

        listener.processTokExit(rackId, cellId, tokId);
      }
    } catch (Exception e) {
      dbg("processTokExit exception: " + e.toString());
    }
  }

/////////////////////// process Tok Rot ///////////////////////
  
  public void processTokRot (int rackId, int cellId, int rotVal) {

    int numListeners = listeners.size();

    try {

      for (int i=0; i < numListeners; i++) {
        WRCListener listener = (WRCListener) listeners.elementAt(i);

        listener.processTokRot(rackId, cellId, rotVal);
      }
    } catch (Exception e) {
      dbg("processTokRot exception: " + e.toString());
    }
  }

/////////////////////// process Tok Entrance ///////////////////////
  
  public void processAdjacencies(String adjacencies) {

    int numListeners = listeners.size();

    int rackId = 0;

    try {

      for (int i=0; i < numListeners; i++) {
        WRCListener listener = (WRCListener) listeners.elementAt(i);

        listener.processAdjacencies(rackId, adjacencies);
      }
    } catch (Exception e) {
      dbg("processAdjacencies exception: " + e.toString());
    }
  }

/////////////////////// dbg ///////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("WRClient[" + (dcnt++) + "] " + s);
  }
}

/// END ///

 
