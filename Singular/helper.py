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

from . import declarations
import superPrinter

def report(caller, message, level=superPrinter.levels.info):
    """
    Print messages
    """
    if level == superPrinter.levels.info and declarations.debugConfig.debug: declarations.helpers.printer.sprint(caller, message, level=level); return
    elif level != superPrinter.levels.info: declarations.helpers.printer.sprint(caller, message, level=level); return

def enableDebug():
    """
    Enables debug mode
    """
    # Set the debug var to true
    declarations.debugConfig.debug = True
    # Enable debugging behaviours
    declarations.miningConfig.maxDiff = declarations.debugConfig.maxDiff_debug
    declarations.miningConfig.minDiff = declarations.debugConfig.minDiff_debug
