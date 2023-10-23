// QRack server for MediaFlow 
// By Brygg Ullmer, MIT Media Lab
// Begun October 9, 2000

import java.net.*;
import java.io.*;
import java.awt.*;

//////////////////////////////////////////////////////////////
////////////////////// ServerThread /////////////////////
//////////////////////////////////////////////////////////////

public class ServerThread extends Thread {

////////////////////// members /////////////////////

  private Socket socket = null; 

  public PrintWriter out = null;
  BufferedReader in = null;

////////////////////// methods /////////////////////

//  public ServerThread(Socket socket)
//  public void run() 

///////////////////////////////////////////////////
////////////////////// BODIES /////////////////////
///////////////////////////////////////////////////

///////////// constructor ///////////////

  public ServerThread(Socket socket) {
    super("ServerThread");
    this.socket = socket;

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
	     
	if (command.equals("hide")) { 
	  dbg("hide window"); 
	}

	if (command.equals("show")) {
	  dbg("show window"); 
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
    System.out.println("ServerThread[" + (dcnt++) + "] " + s);
  }
}

/// END ///

