# Singular
# Copyright (C) 2021 ItsTheGuy
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from . import declarations
from . import manager
from . import frontend
from . import network
from . import helper
import argparse
import base64

class Arguments:
    @staticmethod
    def parse():
        """
        Parse arguments
        """
        arguments = argparse.ArgumentParser(prog="Singular")
        arguments.add_argument("-m", "--minerAddress", help="Pass miner address", type=str, dest="address")
        arguments.add_argument("-s", "--show", help="Display the path of the databases and the network name before start", dest="show", action="store_true")
        arguments.add_argument("-sN", "--showNetwork", help="Get network raw info", dest="showNetwork", action="store_true")
        arguments.add_argument("-fbC", "--frequencyBlockChecking", help="Set how many times have to try a hash before checking If the block Is already mined (Higher value could result In a faster mining, but you take the risk of that block being In the chain already)", type=int, dest="frequencyBlockChecking")
        arguments.add_argument("-tmP", "--toggleMultiprocessingMining", help=("Enable multiprocessing mining" if declarations.miningConfig.multiprocessingMining is False else "Disable multiprocessing mining"), action="store_true")
        arguments.add_argument("--pathChain", help="Change the default path to save the chain (Add {path} to get the Singular path)", type=str, dest="chainPath")
        arguments.add_argument("--pathNodes", help="Change the default path to save the nodes (Add {path} to get the Singular path)", type=str, dest="nodesPath")
        arguments.add_argument("--clear", help="Delete all the blocks In the chain", action="store_true")
        arguments.add_argument("-nS", "--networkSetup", help="Prompt the Network Setup Agent", action="store_true")
        arguments.add_argument("-d", "--debug", help="Enables debug mode", action="store_true")
        arguments.add_argument("-q", "--quit", help="Exit", action="store_true")
        argsReturns = arguments.parse_args()
        passedArguments = Arguments.update(argsReturns)
        # Check If networkSetup, cleared or quit was passed
        if passedArguments.get("networkSetupInitialized") or passedArguments.get("cleared") or passedArguments.get("quit"):
            # If the show argument was passed, show the paths before exiting
            if passedArguments.get("show") and passedArguments.get("quit"): print("\nChain path: {}\nNodes path: {}\nNetwork name: {}\n".format(declarations.staticConfig.dataPath["chain"], declarations.staticConfig.dataPath["nodes"], declarations.chainConfig.name))
            # If the showNetwork argument was passed, show the network info before exiting
            if passedArguments.get("showNetwork") and passedArguments.get("quit"): print("Network settings: {}\nEncoded version: {}".format(network.Network.config.getConf(),(base64.b64encode(str(network.Network.config.getConf()).encode())).decode()))
            exit()
        return passedArguments

    @staticmethod
    def update(argsReturns):
        """
        Check the arguments passed
        """
        # Check If debug was passed
        if argsReturns.debug:
            # Activate debug mode
            helper.enableDebug()
        # Check If network setup was passed
        if argsReturns.networkSetup:
            # Initialize network setup agent
            frontend.Frontend.setup.network()
        # Check If the minerAddress argument was passed
        if argsReturns.address:
            # Set the minerAddress
            declarations.dynamicConfig.minerAddress.set(str(argsReturns.address))
        # Check If chainPath was passed
        if argsReturns.chainPath:
            # Declare the newDataPath
            newDataPath = declarations.staticConfig.dataPath
            # Update newDataPath with the new chainPath
            newDataPath["chain"] = str("{}/{}".format(os.path.dirname(__file__), str(argsReturns.chainPath)[6:])) if str(argsReturns.chainPath)[:6] == "{path}" else str(argsReturns.chainPath) # If {path} was added append the Singular path
            # Save newDataPath
            declarations.dynamicConfig.dataPath.set(dict(newDataPath))
        # Check If nodesPath was passed
        if argsReturns.nodesPath:
            # Declare the newDataPath
            newDataPath = declarations.staticConfig.dataPath
            # Update newDataPath with the new nodesPath
            newDataPath["nodes"] = str("{}/{}".format(os.path.dirname(__file__), str(argsReturns.nodesPath)[6:])) if str(argsReturns.nodesPath)[:6] == "{path}" else str(argsReturns.nodesPath) # If {path} was added append the Singular path
            # Save newDataPath
            declarations.dynamicConfig.dataPath.set(dict(newDataPath))
        # Check If frequencyBlockChecking was passed
        if argsReturns.frequencyBlockChecking:
            # Set the frequencyBlockCheckingMining
            declarations.dynamicConfig.frequencyBlockCheckingMining.set(int(argsReturns.frequencyBlockChecking))
        # Check If toggleMultiprocessingMining was passed
        if argsReturns.toggleMultiprocessingMining:
            declarations.dynamicConfig.multiprocessingMining.set(True if declarations.miningConfig.multiprocessingMining is False else False)
        # Check If clear was passed
        if argsReturns.clear:
            # Remove chain
            if manager.Manager.chainMan.clearChain(): print("Chain deleted successfully!")
            else: print("There was some error while trying to delete chain")
        return dict(show=argsReturns.show, showNetwork=argsReturns.showNetwork, networkSetupInitialized=argsReturns.networkSetup, cleared=argsReturns.clear, quit=argsReturns.quit)
