# Bit mappings for /driver/stat
bit_messages = {
    0: "[OverCurrent]",
    1: "[UnderVoltage]",
    2: "[OverTemp]",
    3: "[OverVoltage]",
    4: "[Sensor]",
    5: "[AnalogError]",
    6: "[SyncError]",
    7: "[RangeExceed]",
}

# Bit mappings for /driver/limit
limit_messages = {
    0: "[IBPOS]",
    1: "[IBNEG]",
    2: "[UBMIN]",
    3: "[UBMAX]",
    4: "[PPOS]",
    5: "[PNEG]",
    6: "[RPOS]",
    7: "[RNEG]",
    8: "[MOTORTEMP]",
    9: "[MRES]",
    10: "[BTEMP]",
    11: "[BCELL]",
    12: "[CSR]",
    13: "[EXT]",
    14: "[IMULT]",
    15: "[UMULT]",
}


def stat2string(status_value):
    status_text = ""
    status_present = False
    # Update for status
    for bit, message in bit_messages.items():
        if status_value & (1 << bit):
            status_text += message + "\n"
            status_present = True

    if not status_present:
        status_text = "no status"

    return status_text


def limit2string(limit_value):
    limit_text = ""
    limit_present = False
    # Update for limit
    for bit, message in limit_messages.items():
        if limit_value & (1 << bit):
            limit_text += message + "\n"
            limit_present = True

    if not limit_present:
        limit_text = "no limit"

    return limit_text


# Define constants
ERRC_INPUT = 0x00
ERRC_PHASEA = 0x10
ERRC_PHASEB = 0x20
ERRC_PHASEC = 0x30
ERRC_PHASEDIFF = 0x40

ERRD_INPUTABSMIN = 0x01
ERRD_INPUTABSMAX = 0x02
ERRD_INPUTABSDIFF = 0x03
ERRD_INPUTOUTOFRANGE = 0x04
ERRD_INPUTOUTOFRANGELO = 0x05
ERRD_INPUTOUTOFRANGEHI = 0x06

ERRD_VM = 0x00
ERRD_SHORTU = 0x01
ERRD_SHORTGND = 0x02
ERRD_SHORTGNDCM = 0x03
ERRD_CM = 0x04
ERRD_CMLOHI = 0x05
ERRD_CMCHARGE = 0x06
ERRD_CMBOOT = 0x07
ERRD_SW = 0x08
ERRD_LOWSW = 0x09
ERRD_HISW = 0x0A
ERRD_SWBOOT = 0x0B

ERRD_CURRNEG = 0x0C
ERRD_CURRPOS = 0x0D
ERRD_VOLTNEG = 0x0E
ERRD_VOLTPOS = 0x0F

ERRD_ABVMDIFF = 0x00
ERRD_ACVMDIFF = 0x01
ERRD_BCVMDIFF = 0x02
ERRD_ABCMDIFF = 0x03
ERRD_ACCMDIFF = 0x04
ERRD_BCCMDIFF = 0x05
ERRD_AORCCM = 0x06


def error2string(err):
    if not err:
        return "no error"

    if err & 0x8000:
        err &= 0x7FFF

        if err < 0x7FF0:
            return f"high-level {err}"

    if err >= 0x7FF0:
        if err == 0x7FFF:
            return "deinitialized"

        elif err == 0x7FFE:
            return "service"

        else:
            err = 0x8000 - err
            str_out = f"pre-init {err} : "

            if err == 10:
                str_out += "gate driver error"
            elif err == 11:
                str_out += "overvoltage"
            elif err == 12:
                str_out += "undervoltage or SMPS off"
            elif err == 13:
                str_out += "all phases to GND or SMPS off"
            elif err == 14:
                str_out += "powered from the motor"
            elif err == 15:
                str_out += "input voltage fluctuation"
            elif err == 16:
                str_out += "analog circuitry error"
            else:
                str_out += "unknown"

            return str_out

    level = (err >> 12) & 0x07
    stage = (err >> 10) & 0x03
    pass_ = (err >> 7) & 0x07
    codeC = (err >> 0) & 0x70
    codeD = (err >> 0) & 0x0F

    str_out = f"level {chr(ord('A') + level)} stage {stage} pass {pass_} : "

    if codeC == ERRC_INPUT:
        str_out += "input voltage "

        if codeD == ERRD_INPUTABSMIN:
            str_out += "abs min"
        elif codeD == ERRD_INPUTABSMAX:
            str_out += "abs max"
        elif codeD == ERRD_INPUTABSDIFF:
            str_out += "abs diff"
        elif codeD == ERRD_INPUTOUTOFRANGE:
            str_out += "out of range"
        elif codeD == ERRD_INPUTOUTOFRANGELO:
            str_out += "out of range lo"
        elif codeD == ERRD_INPUTOUTOFRANGEHI:
            str_out += "out of range hi"

    elif codeC == ERRC_PHASEDIFF:
        str_out += "phase "

        if codeD == ERRD_ABVMDIFF:
            str_out += "A/B VM diff"
        elif codeD == ERRD_ACVMDIFF:
            str_out += "A/C VM diff"
        elif codeD == ERRD_BCVMDIFF:
            str_out += "B/C VM diff"
        elif codeD == ERRD_ABCMDIFF:
            str_out += "A/B CM diff"
        elif codeD == ERRD_ACCMDIFF:
            str_out += "A/C CM diff"
        elif codeD == ERRD_BCCMDIFF:
            str_out += "B/C CM diff"
        elif codeD == ERRD_AORCCM:
            str_out += "A or C CM"

    elif codeC == ERRC_PHASEA:
        str_out += "phase A "

    elif codeC == ERRC_PHASEB:
        str_out += "phase B "

    elif codeC == ERRC_PHASEC:
        str_out += "phase C "

    if codeC in (ERRC_PHASEA, ERRC_PHASEB, ERRC_PHASEC):
        if codeD == ERRD_VM:
            str_out += "VM"
        elif codeD == ERRD_SHORTU:
            str_out += "short to B+"
        elif codeD == ERRD_SHORTGND:
            str_out += "short to B-"
        elif codeD == ERRD_SHORTGNDCM:
            str_out += "short to B- / CM"
        elif codeD == ERRD_CM:
            str_out += "CM"
        elif codeD == ERRD_CMLOHI:
            str_out += "CM LO/HI"
        elif codeD == ERRD_CMCHARGE:
            str_out += "CM charge"
        elif codeD == ERRD_CMBOOT:
            str_out += "CM boot"
        elif codeD == ERRD_SW:
            str_out += "SW"
        elif codeD == ERRD_LOWSW:
            str_out += "SW to B-"
        elif codeD == ERRD_HISW:
            str_out += "SW to B+"
        elif codeD == ERRD_SWBOOT:
            str_out += "SW boot"
        elif codeD == ERRD_CURRPOS:
            str_out += "positive overcurrent"
        elif codeD == ERRD_CURRNEG:
            str_out += "negative overcurrent"
        elif codeD == ERRD_VOLTPOS:
            str_out += "positive overvoltage"
        elif codeD == ERRD_VOLTNEG:
            str_out += "negative overvoltages"

    return str_out
