/// Parameter token 
/// By Brygg Ullmer, MIT Media Lab
/// Begun July 13, 2001

import java.util.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import javax.swing.*;
import java.io.*;

///////////////////////////////////////////////////////////
//////////////////  Parameter token ///////////////////////
///////////////////////////////////////////////////////////

public class TokSerialRelayer 
    implements SerialPListener, SerialRPListener, Runnable {

/////////////  METHODS ///////////////

// public TokSerialRelayer()


/////////////  MEMBERS ///////////////

  boolean verbose = true;

  QRServer  qrServer     = null;
  SerialPacket serialPacket1 = null;
  SerialPacket serialPacket2 = null;
  SerialRPacket serialRPacket = null;

  int rackId, cellLoc, tokId;
  int lowerSelPos, upperSelPos;

  int reedLoc, reedState;

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

////////////////////  constructor /////////////////////////////

  //public TokSerialRelayer(QRServer server) {

  public TokSerialRelayer() {

    qrServer      = new QRServer(); 
    qrServer.startServer();

    //serialPacket  = new SerialPacket();
    serialPacket1  = new SerialPacket(0,"COM3");
    serialPacket1.listener = this;

    serialPacket2  = new SerialPacket(1,"COM4");
    serialPacket2.listener = this;

    serialRPacket  = new SerialRPacket("COM5");
    serialRPacket.listener = this;
  }
  

////////////////////// process RACK packet ////////////////

  public void processPacket(int packetSource, int packetData[], int packetSize) {

    if (packetSize != 5) {
      dbg("processPacket error: " + 
           "expected packetSize 5, received " + packetSize);
      return;
    }

    rackId     = packetSource;
    cellLoc    = packetData[1];
    tokId      = packetData[2]; 

    upperSelPos = packetData[3]; 
    lowerSelPos = (packetData[4] - 128)*2;  // not sure what's going on, but..

    int temp;
    if (upperSelPos > lowerSelPos) { // weirdness; sigh...
      temp = upperSelPos;
      upperSelPos = lowerSelPos;
      lowerSelPos = temp;
    }

    dbg("processPacket: " + tokId + 
        " (" + lowerSelPos + " / " + upperSelPos + ")");

    issueNetUpdate();
  }

////////////////////// process REED packet ////////////////

  public void processRPacket(int packetData[], int packetSize) {

    if (packetSize != 3) {
      dbg("processRPacket error: expected packetSize 3, received " + packetSize);
      return;
    }

    reedLoc   = packetData[1]; 
    reedState = packetData[2]; 

    dbg("processPacket: " + tokId + 
        " (" + lowerSelPos + " / " + upperSelPos + ")");

    issueRNetUpdate();
  }

////////////////////// Issue RACK Net Update ////////////////

  public void issueNetUpdate() {
  
//    int upperSelPos    = 100; // currently selected "top pixel"
//    int lowerSelPos    = 50;  // currently selected "bottom pixel"

//    dbg("upper: " + upperSelPos + "; lower:"  + lowerSelPos);

    qrServer.setParam(rackId, cellLoc, upperSelPos, lowerSelPos, tokId);
  }

////////////////////// Issue REED Net Update ////////////////

  public void issueRNetUpdate() {
  
//    int upperSelPos    = 100; // currently selected "top pixel"
//    int lowerSelPos    = 50;  // currently selected "bottom pixel"

//    dbg("upper: " + upperSelPos + "; lower:"  + lowerSelPos);

    qrServer.setReed(reedLoc, reedState);
  }

////////////////////// main ////////////////

  public void run() {

    while (true) {
      try {Thread.sleep(100);} catch (InterruptedException e) {} 
    }
  }

////////////////////// main ////////////////

  static public void main(String args[]) {

    TokSerialRelayer tsr = new TokSerialRelayer();
  }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("TokSerialRelayer." + (dcnt++) + ": " + s);
  }   
}

//// END ////

