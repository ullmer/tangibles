// Event interface to DbThread
// Brygg Ullmer, MIT Media Lab
// Begun April 28, 2001

// @author  Brygg Ullmer
// @version v0.1

public interface WRModelListener {

  public void processPTokUpdate(PTokModel ptok);

  public void processPTokExit(PTokModel ptok);
  public void processPTokEntrance(PTokModel ptok);

  public void processCTokExit(int containerId);
  public void processCTokEntrance(int containerId);

  public void processWRelUpdate(WRackRels wrackRels);

  public void procRackAdj(char state);
}

//// END ////

