// Interface to QRackMgr
// Brygg Ullmer, MIT Media Lab
// Interface sprouted on November 13, 2001

// @author  Brygg Ullmer
// @version v0.1

public interface QRackMgr {

  public QRackInterp getInterp();
  public WRackModel  getModel();
//  public String      getDatasetName();

  public void iconify  (int dataType);
  public void deiconify(int dataType);

}

//// END ////

