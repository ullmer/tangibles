// QueryRack pot/switch monitor
// Based on Sun's WRackReader.java
// By Brygg Ullmer, MIT Media Lab
// Begun 04/29/2001

/*
 * @(#)WRackReader.java	1.12 98/06/25 SMI
 *
 * Copyright (c) 1998 Sun Microsystems, Inc. All Rights Reserved.
 *
 * Sun grants you ("Licensee") a non-exclusive, royalty free, license 
 * to use, modify and redistribute this software in source and binary
 * code form, provided that i) this copyright notice and license appear
 * on all copies of the software; and ii) Licensee does not utilize the
 * software in a manner which is disparaging to Sun.
 *
 * This software is provided "AS IS," without a warranty of any kind.
 * ALL EXPRESS OR IMPLIED CONDITIONS, REPRESENTATIONS AND WARRANTIES,
 * INCLUDING ANY IMPLIED WARRANTY OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE OR NON-INFRINGEMENT, ARE HEREBY EXCLUDED. SUN AND
 * ITS LICENSORS SHALL NOT BE LIABLE FOR ANY DAMAGES SUFFERED BY
 * LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THE
 * SOFTWARE OR ITS DERIVATIVES. IN NO EVENT WILL SUN OR ITS LICENSORS
 * BE LIABLE FOR ANY LOST REVENUE, PROFIT OR DATA, OR FOR DIRECT,
 * INDIRECT, SPECIAL, CONSEQUENTIAL, INCIDENTAL OR PUNITIVE DAMAGES,
 * HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY, ARISING
 * OUT OF THE USE OF OR INABILITY TO USE SOFTWARE, EVEN IF SUN HAS BEEN
 * ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
 *
 * This software is not designed or intended for use in on-line control
 * of aircraft, air traffic, aircraft navigation or aircraft
 * communications; or in the design, construction, operation or
 * maintenance of any nuclear facility. Licensee represents and
 * warrants that it will not use or redistribute the Software for such
 * purposes.
 */

import java.io.*;
import java.util.*;
import javax.comm.*;

//////////////////////////////////////////////////////////
///////////////// Class WRackReader //////////////////////
//////////////////////////////////////////////////////////

public class WRackReader implements Runnable, SerialPortEventListener {

////////////////// members //////////////////////

    static CommPortIdentifier portId;
    static Enumeration portList;

    InputStream inputStream;
    SerialPort serialPort;
    Thread readThread;

    String incomingBuffer;

    int potStates[]    = new int[4];
    int oldPotStates[] = new int[4];

    byte switchStates[]    = new byte[8];
    byte oldSwitchStates[] = new byte[8];
    int  switchState, oldSwitchState;

    public    int padPos[] = new int[4];
    ReedTrans reedTranslator = new ReedTrans();

    WRListener listener = null;

    boolean verbose = true;

////////////////// methods //////////////////////

//    public WRackReader() 
//    public void run() 
//    public void serialEvent(SerialPortEvent event) 
//
//    public byte getPotVal(int potNum)
//    public byte getSwitchVal(int switchNum)
//
//    public void procPotEvent(String potUpdateStr)
//    public void procSwitchEvent(String switchUpdateStr)
//
//    public void setListener(WRackListener newListener)
//    public void processString(String newChars);

///////////////////////////////////////////////
///////////////// bodies //////////////////////
///////////////////////////////////////////////

////////////////// setListener //////////////////////

  public void setListener(WRListener newListener) {
    listener = newListener;
  }

////////////////// getPotVal //////////////////////

  public int getPotVal(int potNum) {

    if (potNum < 0 || potNum >= 4) {
      dbg("Invalid argument passed to getPotVal; ignoring");
      return 0; // replace with "throw BoundsException" or somesuch
    }

    return potStates[potNum];
  }

////////////////// getSwitchVal //////////////////////

  public byte getSwitchVal(int switchNum) {

    if (switchNum < 0 || switchNum >= 8) {
      dbg("Invalid argument passed to getSwitchVal; ignoring");
      return 0; // replace with "throw BoundsException" or somesuch
    }

    return switchStates[switchNum];
  }


////////////////// processString //////////////////////

  public void processString(String newChars) {

    char currentChar;
    Boolean done = Boolean.FALSE;

    incomingBuffer += newChars;
    int bufferLen = incomingBuffer.length(); 

    //dbg("processString: received " + newChars);

    int idx = 0;
    while (idx < bufferLen && done == Boolean.FALSE) {

      //dbg("idx " + idx + ", bufferLen " + bufferLen);

      currentChar = incomingBuffer.charAt(idx);

      if (currentChar == 'P') { //Pot update
        if (idx + 4 < bufferLen) { // e.g., P003 
          idx++;
	  String potUpdateStr = incomingBuffer.substring(idx, idx+3);

	  if (potUpdateStr.length() < 3) { // should this ever happen?  sigh...
	    idx--; done = Boolean.TRUE; continue;
	  }

	  procPotEvent(potUpdateStr);
	  idx += 3;
	} else {
	  done = Boolean.TRUE; // we haven't yet received the message bytes
	} 
      } else if (currentChar == 'S') { //Switch update 
        //if (bufferLen - idx >= 3) { // e.g., S02
        if (bufferLen - idx >= 4) { // e.g., S002
          idx++;
	  String portNum         = incomingBuffer.substring(idx, idx+1);

	  idx++;
	  String switchUpdateStr = incomingBuffer.substring(idx, idx+2);

	  procSwitchEvent(portNum, switchUpdateStr);
	  idx += 2;
	} else {
	  done = Boolean.TRUE; // we haven't yet received the message bytes
	} 
      } else {
        idx++; // we can't process this character (e.g., newline); move on...
      }
    }

    // OK, update incomingBuffer and continue.

    incomingBuffer = incomingBuffer.substring(idx);
  }

////////////////// procPotEvent //////////////////////

  public void procPotEvent(String potUpdateStr) {

    //dbg("procPotEvent: received " + potUpdateStr);

    if (potUpdateStr.length() != 3) {
//      dbg("procPotEvent error: expecting arg length of 3, received " +
//	  potUpdateStr.length());
        return;
    }

    String selStrVal = potUpdateStr.substring(0,1);
    String potStrVal = potUpdateStr.substring(1);

    //dbg("potEvent: <" + selStrVal + ">/<" + potStrVal + ">");

    int whichPot, whatVal;

    try {
      whichPot = Integer.valueOf(selStrVal).intValue();
      whichPot = 3 - whichPot;

      whatVal  = Integer.valueOf(potStrVal, 16).intValue();
    } catch (Exception e) { 

      //dbg("Exception in numeric conversion on procPotEvent; ignoring bytes.");
      return;
    } 

    int lastVal = getPotVal(whichPot);

    if (whatVal != lastVal) { // update value, and alert listeners
      oldPotStates[whichPot] = potStates[whichPot];
      potStates[whichPot]    = (byte) whatVal;

      if (listener == null) {
	dbg("Wanting to dispatch potUpdate event, but no listener present");
      } else {

	listener.potUpdateOccurred(whichPot, whatVal);
      }
    }
  }

////////////////// to16Bit //////////////////////

  private String to16Bit(int val) {

    String result = Integer.toBinaryString(val);
    int len = 16 - result.length();
    for (int i=0; i<len; i++) {
      result = "0" + result;
    }

    return result;
  }

////////////////// twiddleSwitchBits//////////////////////

  private int twiddleSwitchBits(int rawState) {

    int order[] = {5,4,6,7,14,15,2,3,10,11,12,-1,-1,-1,8,-1};
    int normedState = rawState ^ 0x40B8; // NBv32p28

    int result = 0;
    int currentBit = 1;

    for (int i=0; i<16; i++) {
      if (order[i] == -1) {continue;} // ignore broken bits

      int targetBit = 1 << (15 - order[i]); 

    /*
      if (i==0) {
        dbg("A: " + to16Bit(targetBit));
        dbg("B: " + to16Bit(normedState));
      }
     */

      int bitPresent = targetBit & normedState;
      if (bitPresent != 0) {

        if (i == 4 || i== 9) {continue;} // broken bits

        dbg("targetBit: " + i);
        result |= currentBit;
      }
      currentBit <<= 1;
    }

    return result;
  }

////////////////// twiddleSwitchBits//////////////////////

  public void setPadPositions(int cleanSwitchState) {

// should be private, but...
//  private void setPadPositions(int cleanSwitchState) {

    int transState = cleanSwitchState;
    int transBits, transPos;

//    padPos[2] = 11; // hardwire these for the moment; BAU 05/07/02
//    padPos[3] = 15;

  // hardwire all for experiments -- BAU 05/09/02


    padPos[0] = 0;
    padPos[1] = 4;
    padPos[2] = 8; 
    padPos[3] = 12;

/*
    for (int i=0; i<2; i++) {

      transBits = transState & 0xF;
      transPos  = -1;

      switch (transBits) {
        case 1: transPos = 0; break;
	case 2: transPos = 1; break;
	case 4: transPos = 2; break;
	case 8: transPos = 3; break;
      }

      if (transPos != -1) {
        padPos[i] = i*4 + transPos;
      }

      transState >>= 4;
    }
*/
//    if (padPos[1] == 7) {padPos[2] = 11;} // tidy up

  }

////////////////// procSwitchEvent //////////////////////

  int mswitchState = 0;

  public void procSwitchEvent(String portNum, String switchUpdateStr) {

    //dbg("procSwitchEvent: received " + switchUpdateStr);

    if (switchUpdateStr.length() != 2) {
      dbg("procSwitchEvent error: expecting arg length of 2, received " +
	  switchUpdateStr.length());
    }

    int whatPort, whatVals;
    
    try {
      whatVals = (int) Integer.valueOf(switchUpdateStr, 16).intValue();
      whatPort = (int) Integer.valueOf(portNum, 16).intValue();
    } catch (Exception e) {
      dbg("Exception in numeric conversion on procSwitchEvent; " +
          "ignoring bytes.");
      return;
    } 

    if (whatVals != switchState) { // some bits have flipped

      oldSwitchState = switchState;
      switchState = whatVals & 0xFF; // keep it to 8 bits
      
      int workingVals = whatPort;

      // Walk through the bits...

      for (int i=0; i<8; i++) {

        int state = workingVals & 1;

	oldSwitchStates[i] = switchStates[i];
	switchStates[i] = (byte) state;
      
        workingVals >>= 1;
      }

      if (whatPort == 0) {
        mswitchState &= 0xFF00;
	mswitchState += whatVals;
      } else {
        mswitchState &= 0x00FF;
	mswitchState += (whatVals << 8);
      }

      //int normedState = mswitchState ^ 0x40B8; // NBv32p28
      int cleanState = twiddleSwitchBits(mswitchState);

      String strState = to16Bit(cleanState);

      dbg("CURRENT STATE: " + strState);
      dbg("-------------: " +"0123456789ABCDEF\n"); 

      setPadPositions(cleanState);

      // Fire an update

      if (listener == null) {
	dbg("Wanting to dispatch switchUpdate event, but no listener present");
      } else {

	listener.switchUpdateOccurred();
      }
    }
  }


////////////////// main //////////////////////

    public static void main(String[] args) {
        portList = CommPortIdentifier.getPortIdentifiers();

        while (portList.hasMoreElements()) {
            portId = (CommPortIdentifier) portList.nextElement();
            if (portId.getPortType() == CommPortIdentifier.PORT_SERIAL) {
                 if (portId.getName().equals("COM5")) {
                    WRackReader reader = new WRackReader();
                }
            }
        }
    }

////////////////// constructor //////////////////////

  public WRackReader() {

    //Initialize values

    for (int i=0; i<4; i++) { 
      potStates[i] = 0; 
      oldPotStates[i] = 0;
      padPos[i] = i * 4; 
    }
    padPos[3] = 15;

    for (int i=0; i<8; i++) { 
      switchStates[i] = 0; 
      oldSwitchStates[i] = 0;
    }

    // Initialize

    Enumeration portList;

    Boolean portFound = Boolean.FALSE;

    portList = CommPortIdentifier.getPortIdentifiers();

    while (portFound == Boolean.FALSE && portList.hasMoreElements()) {
      portId = (CommPortIdentifier) portList.nextElement(); 

      System.out.print("portId: " + portId.getName() + "; "); 
      
      if (portId.getPortType() == CommPortIdentifier.PORT_SERIAL) { 
        //if (portId.getName().equals("COM1")) { 
        if (portId.getName().equals("COM5")) { 
	  portFound = Boolean.TRUE;
	}
      }
    }
      
    //Fire up the serial port

    dbg("trying to launch serial port");

    try {
      serialPort = (SerialPort) portId.open("WRackReader", 2000);
    } catch (PortInUseException e) {}
    try {
      inputStream = serialPort.getInputStream();
    } catch (IOException e) {}
    try {
      serialPort.addEventListener(this);
    } catch (TooManyListenersException e) {}

    serialPort.notifyOnDataAvailable(true);

    try {
      serialPort.setSerialPortParams(19200,
         SerialPort.DATABITS_8,
         SerialPort.STOPBITS_1,
         SerialPort.PARITY_NONE);
    } catch (UnsupportedCommOperationException e) {}

    readThread = new Thread(this);
    readThread.start();
  }

////////////////// run //////////////////////

    public void run() {
        try {
            Thread.sleep(20000);
        } catch (InterruptedException e) {}
    }

////////////////// serialEvent //////////////////////

    public void serialEvent(SerialPortEvent event) {
      switch(event.getEventType()) {
        case SerialPortEvent.BI:
        case SerialPortEvent.OE:
        case SerialPortEvent.FE:
        case SerialPortEvent.PE:
        case SerialPortEvent.CD:
        case SerialPortEvent.CTS:
        case SerialPortEvent.DSR:
        case SerialPortEvent.RI:
        case SerialPortEvent.OUTPUT_BUFFER_EMPTY:
            break;

        case SerialPortEvent.DATA_AVAILABLE:
            byte[] readBuffer = new byte[20];
	    int numBytes = 0;

            try {
	        if (inputStream.available() > 0) {
                  numBytes = inputStream.read(readBuffer);
                }
            } catch (IOException e) {return;}

	    String incoming = new String(readBuffer);
	    String trim = incoming.substring(0,numBytes); 
	    
	    processString(trim);
            break;
        }
    }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("WRackReader." + (dcnt++) + ": " + s);
  } 
}

//// END ////

