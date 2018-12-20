#!/usr/bin/env python3

# For each well, plot how many cells were measured and how many were filtered 
# by each gate.  This will require overhauling the gating mechanism to support 
# labeling, but not deleting, the gated cells.

## Data I want to see
# - The number of events, after each gate.  This would let me understand wells 
#   that seem to have very few events.  Did the well simply not generate many 
#   events?  Did a particular gate filter  a large number of events?  The 
#   current presentation shows when a well has fewer events than its peers, but 
#   it doesn't help explain why.
#
#   Implementing this would be challenging in the context of fold_change.py,
#   because the gates actually delete the offending rows.  Maybe this would be 
#   something to change.  After all, you could imagine making a gate that you 
#   want to focus on.  I could have my GateSteps add boolean columns indicating 
#   which rows pass or don't pass the gate.  Then I could provide convenience 
#   functions to delete rows that either are or are not part of particular 
#   gates.


