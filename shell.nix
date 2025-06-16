with import <nixpkgs> {};

mkShell {
  # we need udev tools to reload rules
  nativeBuildInputs = [ udev ];
    buildInputs = [
    pkgs.python3
    pkgs.python3Packages.pyusb
    pkgs.python3Packages.keyboard
  ];

  shellHook = ''
    # our printer rule
    RULE='SUBSYSTEM=="usb", ATTR{idVendor}=="0416", ATTR{idProduct}=="5011", MODE="666'

    # write it into /run/udev (doesn’t survive reboot, but avoids touching /etc)
    echo "$RULE" | sudo tee /run/udev/rules.d/99-usb-8088_0015.rules > /dev/null

    # reload and trigger udev so it takes effect immediately
    sudo udevadm control --reload-rules
    sudo udevadm trigger

    echo "→ udev rule installed: $RULE"
  '';
}
