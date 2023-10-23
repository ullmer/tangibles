// Indcom monitor
// Based on RfidReader.java
// Based on Sun's SimpleReader.java and my QRackReader.java
// By Brygg Ullmer, MIT Media Lab
// Begun on 08/10/2001
// RfidReader.java begun 04/30/2001

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
///////////////// Class SerialPacket //////////////////////
//////////////////////////////////////////////////////////

public class SerialPacket implements Runnable, SerialPortEventListener {

////////////////// members //////////////////////

    static CommPortIdentifier portId;
    static Enumeration portList;

    String ComPortId = null;

    InputStream inputStream;
    SerialPort serialPort;
    Thread readThread;

    int startCharacter = (int) '*';

    static int packetSize = 5;
    int       packetBuffer[] = new int[packetSize];
    int       packetIndex = 0;
    int       packetSource = 0; // ID for this serialPacket receiver


    int rfidVals[]    = new int[4];
    int oldIndcomVals[] = new int[4];

    boolean rfidPresence[]    = new boolean[4];
    boolean oldIndcomPresence[] = new boolean[4];

    SerialPListener listener = null;

////////////////// methods //////////////////////

//    public SerialPacket() 
//    public void run() 
//    public void serialEvent(SerialPortEvent event) 
//
//    public int     getIndcomVal(int cellNum)
//    public Boolean getIndcomState(int cellNum)
//
//    public void procIndcomEvent(String rfidUpdateStr)
//
//    public void setListener(IndcomListener newListener)
//    public void processBytes(byte[] array, int numBytes);

///////////////////////////////////////////////
///////////////// bodies //////////////////////
///////////////////////////////////////////////

////////////////// setListener //////////////////////

/*
  public void setListener(IndcomListener newListener) {
    listener = newListener;
  }
*/

////////////////// getIndcomVal //////////////////////

  public int getIndcomVal(int cellNum) {

    if (cellNum < 0 || cellNum >= 4) {
      dbg("Invalid argument passed to getIndcomVal; ignoring");
      return 0; // replace with "throw BoundsException" or somesuch
    }

    return rfidVals[cellNum]; 
  }

////////////////// getIndcomState //////////////////////

  public boolean getIndcomState (int cellNum) {

    if (cellNum < 0 || cellNum >= 4) {
      dbg("Invalid argument passed to getIndcomVal; ignoring");
      return false; // replace with "throw BoundsException" or somesuch
    }

    return rfidPresence[cellNum];
  }

////////////////// processBytes //////////////////////

  public void processBytes(byte[] newBytes, int numBytes) {

    boolean done = false;

    for (int i=0; i < numBytes; i++) {

      int newByte;

      if (newBytes[i] >= 0) {
        newByte = newBytes[i];
      } else {
        newByte = newBytes[i] + 256;
      }

      String dbgString = ">>> " + newByte + "\t" + (char) newByte;
     
      //dbg(dbgString);

     // Check for clean start of new packet

      if (packetIndex == 0 && newByte == startCharacter) {
        packetBuffer[packetIndex++] = newByte;
	continue;
      }

     // Check for data characters

      if (packetIndex > 0 && packetIndex < packetSize) {

        packetBuffer[packetIndex++] = newByte;

	if (packetIndex == packetSize) {
	  processPacket();
	  packetIndex = 0;
	}
      }
     // otherwise, ignore incoming character
    }
  }

////////////////// processPacket //////////////////////

  public void processPacket() {

    String debugOutput = "";

    for (int i=0; i < packetSize; i++) {
      debugOutput += packetBuffer[i] + "\t";
    }

    if (listener != null) {
      listener.processPacket(packetSource, packetBuffer, packetSize);
    }

    debugOutput += "(";

    for (int i=0; i < packetSize; i++) {
      debugOutput += (char) packetBuffer[i];
    }

    debugOutput += ")";

    dbg(debugOutput);
  }

////////////////// main //////////////////////

    public static void main(String[] args) {

        portList = CommPortIdentifier.getPortIdentifiers();

        while (portList.hasMoreElements()) {
            portId = (CommPortIdentifier) portList.nextElement();
            if (portId.getPortType() == CommPortIdentifier.PORT_SERIAL) {
//                 if (portId.getName().equals("COM1")) {
                 if (portId.getName().equals("COM3")) {
                    SerialPacket reader = new SerialPacket(0, "COM3");
                }
            }
        }
    }

////////////////// constructor //////////////////////

  public SerialPacket(int packetSource, String ComPortId) {

  this.packetSource = packetSource;
  this.ComPortId = ComPortId;

  byte foo = 127;
  Byte bar;
  dbg("test");

  bar = new Byte(foo++);
  dbg(bar.toString());

  bar = new Byte(foo++);
  dbg(bar.toString());

  bar = new Byte(foo++);
  dbg(bar.toString());

    //Initialize values

    for (int i=0; i<4; i++) { 
      rfidVals[i] = 0; 
      oldIndcomVals[i] = 0;

      rfidPresence[i] = false; 
      oldIndcomPresence[i] = false;
    }

    // Initialize

    Enumeration portList;

    boolean portFound = false;

    portList = CommPortIdentifier.getPortIdentifiers();

    while (portFound == false && portList.hasMoreElements()) {
      portId = (CommPortIdentifier) portList.nextElement(); 

      System.out.print("portId: " + portId.getName() + "; "); 
      
      if (portId.getPortType() == CommPortIdentifier.PORT_SERIAL) { 
//        if (portId.getName().equals("COM1")) { 
//        if (portId.getName().equals("COM3")) { 
        if (portId.getName().equals(ComPortId)) { 
	  portFound = true;
	}
      }
    }
      
    //Fire up the serial port

    dbg("trying to launch serial port");

    try {
      serialPort = (SerialPort) portId.open("SerialPacket", 2000);
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
                while (inputStream.available() > 0) {
                    numBytes = inputStream.read(readBuffer);
                }

		processBytes(readBuffer, numBytes);
            } catch (IOException e) {}
            break;
        }
    }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("SerialPacket." + (dcnt++) + ": " + s);
  } 
}

//// END ////

