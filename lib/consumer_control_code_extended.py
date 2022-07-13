"""
`consumer_control_code_extended`
========================================================

* Author(s): thnikk
"""

class CCCX:
    """ This adds some extra keys not included
    in consumer_control_code. Good list of consumer
    codes can be found here: 
    https://github.com/NicoHood/HID/blob/master/src/HID-APIs/ConsumerAPI.h
    """

    # pylint: disable-msg=too-few-public-methods

    MAIL = 0x18A
    """Open email"""
    CALCULATOR = 0x192
    """Open calculator"""
    EXPLORER = 0x194
    """Open file explorer"""
