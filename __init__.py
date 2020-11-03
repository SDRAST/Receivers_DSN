"""
DSN receiver descriptions with no monitor and control functions
"""
import logging

import MonitorControl as MC

module_logger = logging.getLogger(__name__)

class DSN_rx(MC.Receivers.Receiver):
  """
  Class for DSN receivers with no M&C functions

  All DSN receivers have a one-to-one input to output mapping.  They may have
  one or two polarization channels, 'R' being used for telecom.
  """
  def __init__(self, name, inputs=None, output_names=None):
    """
    Create a DSN receiver instance

    A receiver has one or more down-converters but since they have no M&C
    capability they need not be sub-classed.  Each down-converter has only one
    input and output, so their names can be the same.

    @param name : unique name for this receiver
    @type  name : str

    @param inputs : signal sources
    @type  inputs : Port instances

    @param output names : ignored; self-generated
    """
    mylogger = logging.getLogger(module_logger.name+".DSN_rx")
    self.name = name # needed by the next statement
    mylogger.debug(" initializing %s", self)
    mylogger.debug(" %s inputs: %s", name, inputs)
    MC.Receivers.Receiver.__init__(self, name, inputs=inputs,
                                               output_names=output_names)
    self.logger = mylogger
    self.name = name
    self.data['frequency'] = 0.320 # GHz
    self.data['bandwidth'] = 0.640
    # no RF section
    # no pol section
    self.DC = {}
    self.logger.debug(" Setting output properties")
    for inname in list(self.inputs.keys()):
      outname = inname+"U" # all DSN receivers are USB
      self.DC[inname] = MC.Receivers.Receiver.DownConv(self, inname,
                                       inputs={inname: self.inputs[inname]},
                                       output_names=[outname])
      self.DC[inname].outputs[outname].source = self.DC[inname].inputs[inname]
      self.DC[inname].outputs[outname].source.destinations.append(
                                             self.DC[inname].outputs[outname])
      self.DC[inname].outputs[outname].signal = MC.IF(
                           self.DC[inname].outputs[outname].source.signal,'U')
      self.DC[inname].outputs[outname].signal['IF frequency'] = self.data['frequency']
      self.DC[inname].outputs[outname].signal['IF bandwidth'] = self.data['bandwidth']
      self.outputs[outname] = self.DC[inname].outputs[outname]
    self.logger.debug(" %s outputs: %s", self, str(self.outputs))

