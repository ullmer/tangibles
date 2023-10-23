// Rfid monitor
// Based on Sun's SimpleReader.java and my QRackReader.java
// By Brygg Ullmer, MIT Media Lab
// Begun 04/30/2001

/*
 * @(#)SimpleReader.java	1.12 98/06/25 SMI
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
///////////////// Class RfidReader //////////////////////
//////////////////////////////////////////////////////////

public class RfidReader implements Runnable, SerialPortEventListener {

////////////////// members //////////////////////

    static CommPortIdentifier portId;
    static Enumeration portList;

    InputStream inputStream;
    SerialPort serialPort;
    Thread readThread;

    String incomingBuffer;

    int rfidVals[]    = new int[4];
    int oldRfidVals[] = new int[4];

    boolean rfidPresence[]    = new boolean[4];
    boolean oldRfidPresence[] = new boolean[4];

    RfidListener listener = null;

////////////////// methods //////////////////////

//    public RfidReader() 
//    public void run() 
//    public void serialEvent(SerialPortEvent event) 
//
//    public int     getRfidVal(int cellNum)
//    public Boolean getRfidState(int cellNum)
//
//    public void procRfidEvent(String rfidUpdateStr)
//
//    public void setListener(RfidListener newListener)
//    public void processString(String newChars);

///////////////////////////////////////////////
///////////////// bodies //////////////////////
///////////////////////////////////////////////

////////////////// setListener //////////////////////

  public void setListener(RfidListener newListener) {
    listener = newListener;
  }

////////////////// getRfidVal //////////////////////

  public int getRfidVal(int cellNum) {

    if (cellNum < 0 || cellNum >= 4) {
      dbg("Invalid argument passed to getRfidVal; ignoring");
      return 0; // replace with "throw BoundsException" or somesuch
    }

    return rfidVals[cellNum]; 
  }

////////////////// getRfidState //////////////////////

  public boolean getRfidState (int cellNum) {

    if (cellNum < 0 || cellNum >= 4) {
      dbg("Invalid argument passed to getRfidVal; ignoring");
      return false; // replace with "throw BoundsException" or somesuch
    }

    return rfidPresence[cellNum];
  }

////////////////// processString //////////////////////

  public void processString(String newChars) {

    char currentChar;
    boolean done = false;

    incomingBuffer += newChars;
    int bufferLen = incomingBuffer.length(); 

    //dbg("processString: received " + newChars);

    int idx = 0;
    while (idx < bufferLen && done == false) {

      //dbg("idx " + idx + ", bufferLen " + bufferLen);

      currentChar = incomingBuffer.charAt(idx);

      if (currentChar >= 'A' && currentChar <= 'D') { 
        // RFID absent
        String rfidUpdateStr = incomingBuffer.substring(idx, idx+1);
	procRfidEvent(false, rfidUpdateStr);
	idx += 1;

      } else if (currentChar >= 'a' && currentChar <= 'd') { //Rfid -- present 
        // RFID present
        if (bufferLen - idx >= 2) { // e.g., Aq
	  String rfidUpdateStr = incomingBuffer.substring(idx, idx+2);
	  procRfidEvent(true, rfidUpdateStr);
	  idx += 2;

	} else {
	  done = true; // we haven't yet received the message bytes
	} 
      } else {
        idx++; // we can't process this character (e.g., newline); move on...
      }
    }

    // OK, update incomingBuffer and continue.

    incomingBuffer = incomingBuffer.substring(idx);
  }

////////////////// procRfidEvent //////////////////////

  public void procRfidEvent(boolean state, String rfidUpdateStr) {

    //dbg("procRfidEvent: received " + rfidUpdateStr);

    if (state == true && rfidUpdateStr.length() != 2) {
      dbg("procRfidEvent error: expecting arg length of 2 (T), received " +
	  rfidUpdateStr.length());
    }

    if (state == false && rfidUpdateStr.length() != 1) {
      dbg("procRfidEvent error: expecting arg length of 1 (F), received " +
	  rfidUpdateStr.length());
    }

    char cellCh = rfidUpdateStr.charAt(0);
    int cell;

    if (state == false) {
      cell = (int) cellCh - (int) 'A';
    } else {
      cell = (int) cellCh - (int) 'a';
    }

    cell = 3 - cell; // reverse order

    int val = -1;
    if (state == true) {
      val = (int) rfidUpdateStr.charAt(1);
    }

    //dbg("potEvent: <" + selStrVal + ">/<" + potStrVal + ">");

    int     lastVal   = getRfidVal(cell);
    boolean lastState = getRfidState(cell);

    if ((state != lastState) || 
        (val   != lastVal)) { // update value, and alert listeners
      oldRfidPresence[cell] = lastState;
      rfidPresence[cell] = state;

      oldRfidVals[cell] = lastVal;
      rfidVals[cell]    = val;

      if (listener == null) {
	dbg("Wanting to dispatch potUpdate event, but no listener present");
      } else {

	listener.rfidUpdateOccurred(cell, state, val);
      }
    }
  }

////////////////// main //////////////////////

    public static void main(String[] args) {
        portList = CommPortIdentifier.getPortIdentifiers();

        while (portList.hasMoreElements()) {
            portId = (CommPortIdentifier) portList.nextElement();
            if (portId.getPortType() == CommPortIdentifier.PORT_SERIAL) {
                 if (portId.getName().equals("COM1")) {
                    RfidReader reader = new RfidReader();
                }
            }
        }
    }

////////////////// constructor //////////////////////

  public RfidReader() {

    //Initialize values

    for (int i=0; i<4; i++) { 
      rfidVals[i] = 0; 
      oldRfidVals[i] = 0;

      rfidPresence[i] = false; 
      oldRfidPresence[i] = false;
    }

    // Initialize

    Enumeration portList;

    boolean portFound = false;

    portList = CommPortIdentifier.getPortIdentifiers();

    while (portFound == false && portList.hasMoreElements()) {
      portId = (CommPortIdentifier) portList.nextElement(); 

      System.out.print("portId: " + portId.getName() + "; "); 
      
      if (portId.getPortType() == CommPortIdentifier.PORT_SERIAL) { 
        //if (portId.getName().equals("COM2")) { 
        if (portId.getName().equals("COM1")) { 
	  portFound = true;
	}
      }
    }
      
    //Fire up the serial port

    dbg("trying to launch serial port");

    try {
      serialPort = (SerialPort) portId.open("RfidReader", 2000);
    } catch (PortInUseException e) {}
    try {
      inputStream = serialPort.getInputStream();
    } catch (IOException e) {}
    try {
      serialPort.addEventListener(this);
    } catch (TooManyListenersException e) {}

    serialPort.notifyOnDataAvailable(true);

    try {
      serialPort.setSerialPortParams(9600,
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

            try {
                while (inputStream.available() > 0) {
                    int numBytes = inputStream.read(readBuffer);
                }

		processString(new String(readBuffer));
            } catch (IOException e) {}
            break;
        }
    }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("RfidReader." + (dcnt++) + ": " + s);
  } 
}

//// END ////

