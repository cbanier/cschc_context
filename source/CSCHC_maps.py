# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ #
#                           MICROSCHC                           #
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ #

DirectionIndicator_Map = {
    'Up' : 0,
    'Dw' : 1,
    'Bi' : 2
}

MatchingOperator_Map = {
    'equal'         : 0,
    'ignore'        : 1,
    'MSB'           : 2,
    'match-mapping' : 3
}

CompressionDecompressionAction_Map = {
    'not-sent'               : 0,
    'least-significant-bits' : 1,
    'mapping-sent'           : 2,
    'value-sent'             : 3,
    'compute'                : 4
}

RuleNature_Map = {
    'compression'    : 0,
    'no-compression' : 1,
    'fragmentation'  : 2
}

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ #
#                              SIDs                             #
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ #

SID_Map = {
    'IPv6:Version'                : 5068,
    'IPv6:Traffic Class'          : 5065,
    'IPv6:Flow Label'             : 5061,
    'IPv6:Payload Length'         : 5064,
    'IPv6:Next Header'            : 5063,
    'IPv6:Hop Limit'              : 5062,
    'IPv6:Source Address'         : 5057,
    'IPv6:Destination Address'    : 5060,
    'UDP:Source Port'             : 5070,
    'UDP:Destination Port'        : 5073,
    'UDP:Length'                  : 5074,
    'UDP:Checksum'                : 5072,
    'CoAP:Version'                : 5055,
    'CoAP:Type'                   : 5054,
    'CoAP:Token Length'           : 5052,
    'CoAP:Code'                   : 5023,
    'CoAP:Message ID'             : 5026,
    'CoAP:Token'                  : 5053,
    'CoAP:Payload Marker'         : 5141,
    'CoAP:Option Delta'           : 5136,
    'CoAP:Option Length'          : 5138,
    'CoAP:Option Delta Extended'  : 5137,
    'CoAP:Option Length Extended' : 5139,
    'CoAP:Option Value'           : 5140
}