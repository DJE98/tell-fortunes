# 🧾 Tell-Fortunes

Press **Enter**, print a paper fortune.  
This tiny Python script sends a procedurally generated fortune to a POS58 USB thermal receipt printer.

![demo](docs/demo.gif) <!-- optional GIF if you add one -->

---

## ✨ Features

* Generates playful “science-and-software” themed fortunes  
* Works out-of-the-box with the common **0x0416 : 0x5011 POS58** thermal receipt printer  
* ASCII art robot for extra delight  
* Simple keyboard trigger (the **Enter** key)  
* Fortune lists are plain Python lists—edit freely

---

## 🛠️ Hardware

| Component | Tested model | Notes |
|-----------|--------------|-------|
| Thermal printer | Generic POS-58 / Vendor 0x0416, Product 0x5011 | 58-mm roll, ESC/POS compatible |
| USB cable | Standard USB-A ↔ USB-B | Provided with most printers |

Any ESC/POS-compatible thermal printer that shows up as a USB bulk device should work if you adjust the `idVendor` / `idProduct` values.

---

## 📦 Dependencies

```bash
pip install pyusb keyboard
