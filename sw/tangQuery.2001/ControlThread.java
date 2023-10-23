// QRack server for MediaFlow 
// By Brygg Ullmer, MIT Media Lab
// Begun October 9, 2000

import java.net.*;
import java.io.*;
import java.awt.*;

//////////////////////////////////////////////////////////////
////////////////////// ControlThread /////////////////////
//////////////////////////////////////////////////////////////

public class ControlThread extends Thread {

////////////////////// members /////////////////////

  private Socket socket = null; 

  public PrintWriter out = null;
  BufferedReader in = null;

  ControlServer parent = null;

  Logger logger = null;

////////////////////// methods /////////////////////

//  public ControlThread(Socket socket)
//  public void run() 

///////////////////////////////////////////////////
////////////////////// BODIES /////////////////////
///////////////////////////////////////////////////

///////////// constructor ///////////////

  public ControlThread(Socket socket, ControlServer parent) {
    super("ControlThread");
    this.socket = socket;

    this.parent = parent;

    dbg("started");
  }

///////////// run ///////////////

  public void run() {
    dbg("running");

    try {
      out = new PrintWriter(socket.getOutputStream(), true); // autoflush
      in = new BufferedReader(
		 new InputStreamReader(socket.getInputStream()));

      String inputLine, outputLine;

      while ((inputLine = in.readLine()) != null) {

	java.util.StringTokenizer st = 
	   new java.util.StringTokenizer(inputLine);

	if (st.hasMoreTokens() == false) { // strange, but...
	  continue;
	}

	String command = st.nextToken(); 
	     
	if (command.equals("start")) { 
	  dbg("start"); 
	  parent.allowProgress = true;
	}

	if (command.equals("stop")) {
	  dbg("stop"); 
	  parent.allowProgress = false;
	}

	if (command.equals("exit")) {
	  dbg("exiting"); 

	  if (logger != null) {
	    logger.flush();
	  } else {
	    dbg("exiting, logger isn't answering, sigh...");
	  }

	  System.exit(0);
	}
      }

      in.close();
      out.close();
      socket.close();

    } catch (IOException e) {
        e.printStackTrace();
    }
  }

  ////////////////////// debug ////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("ControlThread[" + (dcnt++) + "] " + s);
  }
}

/// END ///

