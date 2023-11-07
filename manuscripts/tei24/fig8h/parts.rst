.. list-table:: Headers
   :widths: 30 70
   :header-rows: 0

   * - *model name*   
     - hexPlinth62a
   * - *model author* 
     - Brygg Ullmer
   * - *author org*   
     - Clemson University
   * - *details*     
     - `YAML description <parts.yaml>`_

.. list-table:: Constituent parts
   :widths: 10 10 10 60 10 10
   :header-rows: 1

   * - vendor
     - quantity
     - item number
     - short description
     - cost per item
     - total cost

   * - adafruit
     - 1
     - 4022
     - Wide-range triple-axis magnetometer
     - $9.95
     - $9.95

   * - 
     - 1
     - 5544
     - Raspberry Pi Pico WH
     - $7.00
     - $7.00


vendors:
  adafruit: [4022, 5544]
  mcmaster: [7113k552, 91844A410, 92165A029, 92174A029, 93140A239, 96169A468]
  pololu:   []
  oshpark:  [pcb]

parts:
  4022: {metafamily: sensor,   familyDescr: magnetometer,
     detailDescr: 'Adafruit Wide-Range Triple-axis Magnetometer - MLX90393 - STEMMA QT',
     quantRequired: 1, pricePerUnit: 9.95}

  5544: {metafamily: processor, familyDescr: rpi pico,
     detailDescr: 'Raspberry Pi Pico WH - Pico Wireless with Headers Soldered',
     quantRequired: 1, price: 7.00}

  7113K552:  {metafamily: terminal, familyDescr: ring terminal, 
     detailDescr: 'Noninsulated, for 22-18 Wire Gauge and 1/4" Screw', 
     quantPerPkg: 100, quantRequired: 6, pricePerUnit: 0.18, matchedScrew: '.25"'}

  91844A410: {metafamily: washer, familyDescr: saddle washer, 
     detailDescr: ['Zinc-Plated Steel Curved Washer for 1" Tube OD', 
                   '1/4" Screw Size, 0.28" ID, 1" OD'],
     quantPerPkg: 25, quantRequired: 6, pricePerUnit: 1.00, id: .280, od: 1., 
     matchedScrew: '.25"'}

  93140A239: {metafamily: screw, familyDescr: polycarbonate screw, color: clear,
     detailDescr: ['Impact-Resistant Polycarbonate Screws',
                   'Pan Head Phillips, 1/4"-20 Thread, 3/4" Long'],
     quantPerPkg: 10, quantRequired: 6, pricePerUnit: 0.53, screwThread: '1/4"-20'}

  92165A029: {metafamily: washer, familyDescr: lock washer,
     detailDescr: ['Bronze Internal-Tooth Lock Washer',
                   'for 1/4" Screw Size, 0.256" ID, 0.478" OD'],
     quantPerPkg: 100, quantRequired: 6, pricePerUnit: .128, id: .256, od: .478,
     matchedScrew: '.25"'}

  92174A029: {metafamily: nut, familyDescr: hex nut,
     detailDescr: 'Brass Thin Hex Nut, 1/4"-20 Thread Size',
     quantPerPkg: 50, quantRequired: 6, pricePerUnit: .229, screwThread: '1/4"-20'}

96169A468_Chemical-Resistant Polypropylene Hex Nut.dae

### end ###
