import random
import textwrap

import keyboard
import usb.core
import usb.util

# In Linux, you must:
#
# 1) Add your user to the Linux group "lp" (line printer), otherwise you will
#    get a user permissions error when trying to print.
#
# 2) Add a udev rule to allow all users to use this USB device, otherwise you
#    will get a permissions error also. Example:
#
#    In /etc/udev/rules.d create a file ending in .rules, such as
#    33-receipt-printer.rules with the contents:
#
#   # Set permissions to let anyone use the thermal receipt printer
#   SUBSYSTEM=="usb", ATTR{idVendor}=="0416", ATTR{idProduct}=="5011", MODE="666"

fortune_intros = [
    "You will",
    "Soon you will",
    "In the near future, you will",
    "Your future holds",
    "A surprise awaits as you",
    "Destiny will guide you to",
    "Prepare yourself, for you will",
    "Unexpectedly, you will",
    "Without warning, you will",
    "Fortune favors you as you",
    "According to quantum mechanics, you will",
    "In the matrix of life, you will",
    "Algorithmically, you will",
    "In a parallel universe, you will",
    "As the bits align, you will",
    "As the laws of physics decree, you will",
    "In the lab of life, you will",
    "In the cosmic dance of atoms, you will",
    "By the principles of evolution, you will",
    "As the stars whisper, you will",
    "Under the gaze of the cosmos, you will" "As the planets align, you will",
    "Beneath a starlit sky, you will",
]

fortune_actions = [
    "find great",
    "experience unexpected",
    "discover hidden",
    "uncover amazing",
    "be blessed with",
    "embark on an incredible journey to",
    "receive surprising",
    "witness a transformation through",
    "embrace the unexpected",
    "unlock the secret of",
    "debug a complex",
    "optimize a convoluted",
    "compile an error-free",
    "decrypt an encrypted",
    "simulate a flawless",
    "observe remarkable",
    "measure peculiar",
    "experiment with groundbreaking",
    "synthesize innovative",
    "calculate improbable",
    "unravel the mysteries of",
    "soar among the constellations with",
    "navigate the celestial map to",
    "dive into the nebula of",
    "chart the course of",
]

fortune_conclusions = [
    "success in your career.",
    "joy in your relationships.",
    "opportunities at every turn.",
    "a breakthrough in your personal growth.",
    "the chance to meet someone remarkable.",
    "an exciting adventure.",
    "a moment of clarity that changes your life.",
    "abundance in all aspects of life.",
    "a successful new beginning.",
    "the key to your destiny.",
    "a revelation that inspires you.",
    "a discovery that even Turing would applaud.",
    "a solution to problems unsolvable by brute force.",
    "an insight worthy of a Nobel Prize.",
    "a code that runs in O(1) time.",
    "the secrets of dark matter.",
    "a new element on the periodic table.",
    "the cure to a longstanding mystery.",
    "a proof of Einstein's theories in action.",
    "a scientific breakthrough that rewrites textbooks.",
    "a revolution in our understanding of the universe.",
    "balance in the chaos of the cosmos.",
    "harmony with the rhythms of the universe.",
]


def configure_printer():
    # Find our device
    # 0416:5011 is POS58 USB thermal receipt printer
    dev = usb.core.find(idVendor=0x0416, idProduct=0x5011)

    # Was it found?
    if dev is None:
        raise ValueError("Device not found")

    # Disconnect it from kernel
    needs_reattach = False
    if dev.is_kernel_driver_active(0):
        needs_reattach = True
        dev.detach_kernel_driver(0)

    # Set the active configuration. With no arguments, the first
    # configuration will be the active one
    dev.set_configuration()

    # get an endpoint instance
    cfg = dev.get_active_configuration()
    intf = cfg[(0, 0)]

    ep = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
        == usb.util.ENDPOINT_OUT,
    )

    return dev, needs_reattach, ep


def generate_fortune():
    intro = random.choice(fortune_intros)
    action = random.choice(fortune_actions)
    conclusion = random.choice(fortune_conclusions)
    fortune = f"{intro} {action} {conclusion}"
    return fortune


def print_text(ep, text):
    lines = textwrap.wrap(text, width=30)
    for line in lines:
        ep.write(line + "\n")


def print_robot(ep):
    ep.write(
        """
::::::::::::::::::::::::::::::
::::::::::==########=:::::::::
:::== =::=@#@@@@@@@@#:== ==:::
:::#= =#:#@#@  @@  @#:#= =#:::
:::=###==###@@@# @@@#:=###=:::
:::=#@#=:=@=@@@# @@@#:=#@#=:::
:::=###==#################=:::
:::=@@@@##@@@@@@@@@@@@@@@@=:::
:::#@@@@@@@@@@@@@@@@@@@@@@#:::
::::===##====@#====@@=:#@#::::
:::.:==#:.=:.@=.=:.##..:#:..::
:::.:==#.::.#@:.:.=@=.=.:=.:::
::::@@@=.##.:#.=@::#::@=#=.:::
:::=@@@##@@#####@#####@@@#=:::
    """
    )


def reattach(dev, needs_reattach):
    dev.reset()
    if needs_reattach:
        dev.attach_kernel_driver(0)
        print("Reattached USB device to kernel driver")


def main():
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == "enter":
            dev, needs_reattach, ep = configure_printer()
            assert ep is not None
            fortune = generate_fortune()
            print_text(ep, fortune)
            print_robot(ep)
            ep.write("\n\n")
            reattach(dev, needs_reattach)


main()
