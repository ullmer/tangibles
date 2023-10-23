// Display server for QueryUI
// By Brygg Ullmer, MIT Media Lab

// Descended from MediaFlow QRClient
// Begun October 9, 2000
// Reworked on May 2, 2001
// Reworked on September 10, 2001

import java.net.*;
import java.io.*;
import java.util.*;

//////////////////////////////////////////////////////
//////////////////// Venn Client /////////////////////
//////////////////////////////////////////////////////


public class QRClient extends Thread {

//////////////////// members /////////////////////

  private Socket socket = null; 

  Socket indcomSocket = null;
  PrintWriter out   = null;
  BufferedReader in = null;

  Vector listeners = null;

  //String server = "18.85.46.122";

  String server = "tsunami";
  int    port   = 4050;

//////////////////// methods /////////////////////

//  public QRClient(Venn qrDisplay) 
//  public void run() 

/////////////////////////////////////////////////
//////////////////// bodies /////////////////////
/////////////////////////////////////////////////

///////////// constructor ///////////////

  public QRClient() {
    super("QRClient");

    listeners = new Vector();
    dbg("started");
  }

  public QRClient(QRCListener listener) {

    this();
    addListener(listener);
  }

/////////////////////// addListener ///////////////////////

  public void addListener(QRCListener listener) {

    listeners.addElement(listener);
  }

///////////// run ///////////////

  public void run() {
  dbg("running");

    try {
      indcomSocket = new Socket(server, port);
      out = new PrintWriter(indcomSocket.getOutputStream(), true);
      in  = new BufferedReader(
	            new InputStreamReader(indcomSocket.getInputStream()));

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

/// Pxyyzzt*: Receive parameter presence & bounds from QRackServer

       if (fromServer.startsWith("P")) {

	 int cellId, tokId, rackId;
	 int bound1, bound2;
	 String param;

	 try {
           char cid = fromServer.charAt(1);
	   cellId   = (int) (cid - '0');

	   String r1  = fromServer.substring(2,3);
	   rackId     = Integer.valueOf(r1, 16).intValue();

	   String sb1 = fromServer.substring(3,5);
	   bound1     = Integer.valueOf(sb1, 16).intValue();

	   String sb2 = fromServer.substring(5,7);
	   bound2     = Integer.valueOf(sb2, 16).intValue();

	   String tokstr = fromServer.substring(7,9);
	   tokId         = Integer.valueOf(tokstr, 16).intValue();

	 } catch (Exception e) {

	   dbg("Exception in processing Clear command argument; ignoring");
	   continue;
	 }

	 processParamUpdate(rackId, cellId, tokId, bound1, bound2);

	 continue;
       }

/// Rxy: Receive reed state from QRackServer

       if (fromServer.startsWith("R")) {

	 int reedLoc, reedState;

	 try {
           char ch = fromServer.charAt(1);
	   reedLoc   = (int) (ch - '0');

           ch        = fromServer.charAt(2);
	   reedState = (int) (ch - '0');

	 } catch (Exception e) {

	   dbg("Exception in processing Clear command argument; ignoring");
	   continue;
	 }

	 int rackId = 0; // CHANGE

	 processReedUpdate(reedLoc - (int)'0', reedState - (int)'0');

	 continue;
       }

/// Xxyyzzt*: Receive axis presence & bounds from QRackServer

       if (fromServer.startsWith("X")) {

       char axis; 
       int bound1, bound2; 
       String param;

       dbg("processAxis has been temporarily disabled; fix it!");
       if (true) {return;}

	 try {
           axis = fromServer.charAt(1);

	   String sb1 = fromServer.substring(2,4);
	   bound1 = Integer.valueOf(sb1, 16).intValue();

	   String sb2 = fromServer.substring(4,6);
	   bound2 = Integer.valueOf(sb2, 16).intValue();

	   param = fromServer.substring(6);

	 } catch (Exception e) {

	   dbg("Exception in processing Clear command argument; ignoring");
	   continue;
	 }

//	 processAxisUpdate(id, bound1, bound2);

	 continue;
       }
      } 
      sleep(2);
     }
    } catch (Exception e) {dbg("close exception 1: " + e.getMessage());}

    try {
      in.close();
      stdIn.close();
      indcomSocket.close();
    } catch (Exception e) {dbg("close exception 2: " + e.getMessage());}
  }

/////////////////////// process Param Presence ///////////////////////

  public void processParamUpdate(int rackId, int cellId, int tokId,
                                         int bound1, int bound2) {

    int numListeners = listeners.size();

    try {

      for (int i=0; i < numListeners; i++) {
        QRCListener listener = (QRCListener) listeners.elementAt(i);

        listener.processParamUpdate(rackId, cellId, tokId, 
                                     bound1, bound2);
      }
    } catch (Exception e) {
      dbg("processParamUpdate exception: " + e.getMessage());
    }
  }

/////////////////////// process Reed Update ///////////////////////

  public void processReedUpdate(int reedLoc, int reedState) {

    int numListeners = listeners.size();

    try {

      for (int i=0; i < numListeners; i++) {
        QRCListener listener = (QRCListener) listeners.elementAt(i);

        listener.processReedUpdate(reedLoc, reedState);
      }
    } catch (Exception e) {
      dbg("processParamUpdate exception: " + e.getMessage());
    }
  }

/////////////////////// process Axis Presence ///////////////////////

  public void processAxisUpdate(int id, int bound1, int bound2) {

   dbg("processAxisUpdate: foobar, this needs reworking.  Do it!"); 
   if (true) {return;}

    int numListeners = listeners.size();

    for (int i=0; i < numListeners; i++) {
      QRCListener listener = (QRCListener) listeners.elementAt(i);

//      listener.updateAxisPresence(id, bound1, bound2);
    }
  }


/////////////////////// dbg ///////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("QRClient[" + (dcnt++) + "] " + s);
  }
}

/// END ///

 
