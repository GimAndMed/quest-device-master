from devicecommands.commandfactory import CommandFactory
from devicecommands.commandcode import Command

import serial

def testAllGetFunction(port, address):
    commandFactory = CommandFactory()

    # GetFunction
    command = commandFactory.createCommand(Command.getButtons)
    command.init(port, address)
    connection = command.execute()

    command = commandFactory.createCommand(Command.getStuckButtons)
    command.init(port, address)
    connection = command.execute()

    command = commandFactory.createCommand(Command.getADC)
    command.init(port, address)
    connection = command.execute()

    command = commandFactory.createCommand(Command.getEncoders)
    command.init(port, address)
    connection = command.execute()

    command = commandFactory.createCommand(Command.getSensor)
    command.init(port, address)
    connection = command.execute()

    command = commandFactory.createCommand(Command.getAllStates)
    command.init(port, address)
    connection = command.execute()


if __name__ == "__main__":

    ser = serial.Serial('/dev/pts/8',
                        timeout=1,
                        writeTimeout=0.1,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE)
    port = ser
    address = 1

    testAllGetFunction(port, address)


