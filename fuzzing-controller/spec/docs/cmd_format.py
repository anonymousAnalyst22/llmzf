CMD_FORMAT_DESCRIPTIONS = {
    "Groups": {
    "Add Group": {
        "fields": ["Group ID", "Group Name"],
        "intro": """
3.6.2.3.2.1 Payload Format  The Add Group command payload SHALL be formatted as illustrated in Figure 3-10. 
 Figure 3-10. Format of the Add Group Command Payload  Octets 2 Variable Data Type uint16 string Field Name Group ID Group Name
""",
   },
   "View Group": {
        "fields": ["Group ID"],
        "intro": """
3.6.2.3.3.1 Payload Format  The View Group command payload SHALL be formatted as illustrated in Figure 3-11:  Figure 3-11. Format of the View Group Command Payload  Octets 2 Data Type uint16 Field Name Group ID
"""},
    "Get Group Membership": {
        "fields": ["Group count", "Group list"],
        "intro": """
3.6.2.3.4.1 Payload Format  The get group membership command payload SHALL be formatted as illustrated in Figure 3-12.
Figure 3-12. Format of Get Group Membership Command Payload  Octets 1 Variable Data Type uint8 List of 16-bit integers Field Name Group count Group list
"""},
    "Remove Group":{
        "fields": ["Group ID"],
        "intro": """
3.6.2.3.5.1 Payload Format  The Remove Group command payload SHALL be formatted as illustrated in Figure 3-13. 
 Figure 3-13. Format of the Remove Group Command Payload  Octets 2 Data Type uint16 Field Name Group ID
"""
    },
    "Remove All Groups": {
        "fields": [],
        "intro": """
The Remove All Groups command has no payload.
"""
    },
    "Add Group If Identifying": {
        "fields": ["Group ID", "Group Name"],
        "intro": """
3.6.2.3.7.1 Payload Format  The Add Group If Identifying command payload SHALL be formatted as illustrated in Figure 3-14. 
 Figure 3-14. Add Group If Identifying Command Payload  Octets 2 Variable Data Type uint16 string Field Name Group ID Group Name
"""
    }
},
    "Identify": {
    "Identify": {
        "fields": ["Identify Time"],
        "intro": """
The identify query response command payload SHALL be formatted as illustrated in Figure 3-7.  
 Figure 3-7. Format of Identify Query Response Command Payload  Octets 2 Data Type uint16 Field Name Identify Time
"""
    },
    "Identify Query": {
        "fields": [],
        "intro": """
"""
    },
    "Trigger Effect": {
        "fields": ['Effect identifier', 'Effect variant'],
        "intro": """
The payload of this command SHALL be formatted as illustrated in Figure 3-8. 
 Figure 3-8. Format of the Trigger Effect Command  Octets 1 1 Data Type enum8 enum8 Field Name Effect identifier Effect variant
"""
    }
},
    "Scenes": {
        "Add Scene": {
            "fields": ["Group ID", "Scene ID", "Transition time", "Scene Name", "Extension field sets"],
            "intro": """
The payload SHALL be formatted as illustrated in Figure 3-19.
Figure 3-19. Format of the Add Scene Command Payload  Octets 2 1 2 Variable Variable Data Type uint16 uint8 uint16 string Variable  (multiple types) Field Name Group ID Scene ID Transition time Scene Name Extension field sets, one per cluster   The format of each extension field set is a 16 bit field carrying the cluster ID, followed by an 8 bit length  field and the set of scene extension fields specified in the relevant cluster. The length field holds the length  in octets of that extension field set. 
 Extension field sets =    {{clusterId 1, length 1, {extension field set 1}}, {clusterId 2, length 2, {extension field set 2}} ...}. 
 The attributes included in the extension field set for each cluster are defined in the specification for that  cluster in this document (the Cluster Library). The field set consists of values for these attributes concatenated  together, in the order given in the cluster specification, with no attribute identifiers or data type indicators.  
 For forward compatibility, reception of this command SHALL allow for the possible future addition of other  attributes to the trailing ends of the lists given in the cluster specifications (by ignoring them). Similarly, it  SHALL allow for one or more attributes to be omitted from the trailing ends of these lists (see 3.7.2.4.7.2). 
 It is not mandatory for a field set to be included in the command for every cluster on that endpoint that has a  defined field set. Extension field sets MAY be omitted, including the case of no field sets at all.
"""},
        "View Scene": {
            "fields": ["Group ID", "Scene ID"],
            "intro": """
The payload SHALL be formatted as illustrated in Figure 3-20. 
 Figure 3-20. Format of the View Scene Command Payload  Octets 2 1 Data Type uint16 uint8 Field Name Group ID Scene ID
"""},
        "Remove Scene": {
            "fields": ["Group ID", "Scene ID"],
            "intro": """
The Remove Scene command payload SHALL be formatted as illustrated in Figure 3-21. 
 Figure 3-21. Format of the Remove Scene Command Payload  Octets 2 1 Data Type uint16 uint8 Field Name Group ID Scene ID
"""
        },
        "Remove All Scenes": {
            "fields": ["Group ID"],
            "intro": """
The Remove All Scenes command payload SHALL be formatted as illustrated in Figure 3-22. 
 Figure 3-22. Format of the Remove All Scenes Command Payload  Octets 2 Data Type uint16 Field Name Group ID
"""
        },
        "Store Scene": {
            "fields": ["Group ID", "Scene ID"],
            "intro": """
The Store Scene command payload SHALL be formatted as illustrated in Figure 3-23.
Figure 3-23. Format of the Store Scene Command Payload  Octets 2 1 Data Type uint16 uint8 Field Name Group ID Scene ID
"""
        },
        "Recall Scene": {
            "fields": ["Group ID", "Scene ID", "Transition Time"],
            "intro": """
The Recall Scene command payload SHALL be formatted as illustrated in Figure 3-24.
Figure 3-24. Format of the Recall Scene Command Payload  Octets 2 1 0/2 Data Type uint16 uint8 uint16 Field Name Group ID Scene ID Transition Time
"""
        },
        "Get Scene Membership": {
            "fields": ["Group ID"],
            "intro": """
The Get Scene Membership command payload SHALL be formatted as illustrated in Figure 3-25.
Figure 3-25. Format of Get Scene Membership Command Payload  Octets 2 Data Type uint16 Field Name Group ID
"""
        },
        "Enhanced Add Scene": {
            "fields": ["Group ID", "Scene ID", "Transition time", "Scene Name", "Extension field sets"],
            "intro": """
The payload SHALL be formatted as illustrated in Figure 3-19.
Figure 3-19. Format of the Add Scene Command Payload  Octets 2 1 2 Variable Variable Data Type uint16 uint8 uint16 string Variable  (multiple types) Field Name Group ID Scene ID Transition time Scene Name Extension field sets, one per cluster   The format of each extension field set is a 16 bit field carrying the cluster ID, followed by an 8 bit length  field and the set of scene extension fields specified in the relevant cluster. The length field holds the length  in octets of that extension field set. 
 Extension field sets =    {{clusterId 1, length 1, {extension field set 1}}, {clusterId 2, length 2, {extension field set 2}} ...}. 
 The attributes included in the extension field set for each cluster are defined in the specification for that  cluster in this document (the Cluster Library). The field set consists of values for these attributes concatenated  together, in the order given in the cluster specification, with no attribute identifiers or data type indicators.  
 For forward compatibility, reception of this command SHALL allow for the possible future addition of other  attributes to the trailing ends of the lists given in the cluster specifications (by ignoring them). Similarly, it  SHALL allow for one or more attributes to be omitted from the trailing ends of these lists (see 3.7.2.4.7.2). 
 It is not mandatory for a field set to be included in the command for every cluster on that endpoint that has a  defined field set. Extension field sets MAY be omitted, including the case of no field sets at all.
 The Transition Time field SHALL be measured in tenths of a second rather than in seconds.
"""},
        "Enhanced View Scene": {
            "fields": ["Group ID", "Scene ID"],
            "intro": """
The payload SHALL be formatted as illustrated in Figure 3-20. 
 Figure 3-20. Format of the View Scene Command Payload  Octets 2 1 Data Type uint16 uint8 Field Name Group ID Scene ID
"""
        },
        "Copy Scene": {
            "fields": ["Mode", "Group identifier from", "Scene identifier from", "Group identifier to", "Scene identifier to"],
            "intro": """
The payload of this command SHALL be formatted as illustrated in Figure 3-26.
Figure 3-26. Format of the Copy Scene Command  Octets 1 2 1 2 1 Data Type map8 uint16 uint8 uint16 uint8 Field Name Mode Group identifier from Scene identifier from Group identifier to Scene identifier to
3.7.2.4.11.1 Mode Field  The mode field is 8-bits in length and contains information of how the scene copy is to proceed. This field  SHALL be formatted as illustrated in Figure 3-27. 
 Figure 3-27. Format of the Mode Field of the Copy Scene Command  Bits: 0 Bits: 1-7 Copy All Scenes Reserved The Copy All Scenes subfield is 1-bit in length and indicates whether all scenes are to be copied. If this value  is set to 1, all scenes are to be copied and the Scene Identifier From and Scene Identifier To fields SHALL  be ignored. Otherwise this field is set to 0.
 3.7.2.4.11.2 Group Identifier From Field  The Group Identifier From field is 16-bits in length and specifies the identifier of the group from which the  scene is to be copied. Together with the Scene Identifier From field, this field uniquely identifies the scene  to copy from the scene table. 
 3.7.2.4.11.3 Scene Identifier From Field  The Scene Identifier From field is 8-bits in length and specifies the identifier of the scene from which the  scene is to be copied. Together with the Group Identifier From field, this field uniquely identifies the scene  to copy from the scene table. 
 3.7.2.4.11.4 Group Identifier To Field  The Group Identifier To field is 16-bits in length and specifies the identifier of the group to which the scene  is to be copied. Together with the Scene Identifier To field, this field uniquely identifies the scene to copy to  the scene table. 
 3.7.2.4.11.5 Scene Identifier To Field  The Scene Identifier To field is 8-bits in length and specifies the identifier of the scene to which the scene is  to be copied. Together with the Group Identifier To field, this field uniquely identifies the scene to copy to  the scene table.
"""
        }
    },
    "OnOff": {
        "Off": {
            "fields": [],
            "intro": """
This command does not have a payload.
"""
        },
        "On": {
            "fields": [],
            "intro": """
This command does not have a payload.
"""
        },
        "Toggle": {
            "fields": [],
            "intro": """
This command does not have a payload.
"""
        },
        "Off With Effect": {
            "fields": ["Effect identifier", "Effect variant"],
            "intro": """
The Off With Effect command allows devices to be turned off using enhanced ways of fading.
The payload of this command SHALL be formatted as illustrated in Figure 3-36.
Figure 3-36. Format of the Off With Effect Command
Octets
1
1
Data Type
uint8
uint8
Field Name
Effect identifier
Effect variant
3.8.2.3.4.1
Effect Identifier Field
The Effect Identifier field is 8-bits in length and specifies the fading effect to use when switching the device off. This field SHALL contain one of the non-reserved values listed in Table 3-48.
Table 3-48. Values of the Effect Identifier Field of the Off With Effect Command
Effect Identifier Field Value
Description
0x00
Delayed All Off
0x01
Dying Light
0x02 to 0xff
Reserved
3.8.2.3.4.2
Effect Variant Field
The Effect Variant field is 8-bits in length and is used to indicate which variant of the effect, indicated in the Effect Identifier field, SHOULD be triggered. If a device does not support the given variant, it SHALL use the default variant. This field is dependent on the value of the Effect Identifier field and SHALL contain one of the nonreserved values listed in Table 3-49.
Table 3-49. Values of the Effect Variant Field of the Off With Effect Command
Effect Identifier
Effect Variant
Description
Field Value
Field Value
0x00 (default)
Fade to off in 0.8 seconds
0x01
No fade
0x00
0x02
50 dim down in 0.8 seconds then fade to off in 12 seconds
0x03 to 0xff
Reserved
0x01
0x00 (default)
20 dim up in 0.5s then fade to off in 1 second
0x01 to 0xff
Reserved
0x02 to 0xff
0x00 to 0xff
Reserved
"""
        },
        "On With Recall Global Scene": {
            "fields": [],
            "intro": """
The On With Recall Global Scene command SHALL have no parameters.
"""
        },
        
        "On With Timed Off": 
        {
            "fields": ["On/off Control", "On Time", "Off Wait Time"],
            "intro": """
The payload of this command SHALL be formatted as illustrated in Figure 3-37.
Figure 3-37. Format of the On With Timed Off Command
Octets
1
2
2
Data Type
uint8
uint16
uint16
Field Name
On/off Control
On Time
Off Wait Time
3.8.2.3.6.1
On/Off Control Field
The On/Off Control field is 8-bits in length and contains information on how the device is to be operated. This field SHALL be formatted as illustrated in Figure 3-38.
Figure 3-38. Format of the On/Off Control Field of the On With Timed Off Command
Bits: 0
1-7
Accept Only When On
Reserved
The Accept Only When On sub-field is 1 bit in length and specifies whether the On With Timed Off command is to be processed unconditionally or only when the OnOff attribute is equal to 0x01. If this sub-field is set to 1, the On With Timed Off command SHALL only be accepted if the OnOff attribute is equal to 0x01. If this sub-field is set to 0, the On With Timed Off command SHALL be processed unconditionally.
3.8.2.3.6.2
On Time Field
The On Time field is 16 bits in length and specifies the length of time (in 1/10ths second) that the device is to remain “on”, i.e., with its OnOff attribute equal to 0x01, before automatically turning “off”. This field SHALL be specified in the range 0x0000 to 0xfffe.
3.8.2.3.6.3
Off Wait Time Field
The Off Wait Time field is 16 bits in length and specifies the length of time (in 1/10ths second) that the device SHALL remain “off”, i.e., with its OnOff attribute equal to 0x00, and guarded to prevent an on command turning the device back “on”. This field SHALL be specified in the range 0x0000 to 0xfffe.
"""
        }
    },
    "Level": {
        "Move to Level": {
            "fields": ["Level", 'Transition time', 'OptionsMask', 'OptionsOverride'],
            "intro": """
3.10.2.3.1.1
Payload Format
The Move to Level command payload SHALL be formatted as illustrated in Figure 3-40.
Figure 3-40. Format of the Move to Level Command Payload
1
2
1
1
Octets
uint8
uint16
map8
map8
Data Type
Level
Transition time
OptionsMask
OptionsOverride
Field Name
n/a
n/a
0
0
Default
"""
        },
        "Move": {
            "fields": ["Move mode", "Rate", 'OptionsMask','OptionsOverride'],
            "intro": """
The Move command payload SHALL be formatted as illustrated in Figure 3-41.
Figure 3-41. Format of the Move Command Payload
1
1
1
1
Octets
enum8
uint8
map8
map8
Data Type
Move mode
Rate
OptionsMask
OptionsOverride
Field Name
n/a
n/a
0
055
Default
3.10.2.3.2.2
Move Mode Field
The Move mode field SHALL be one of the non-reserved values in Table 3-60.
Table 3-60. Values of the Move Mode Field
Fade Mode Value
Description
0x00
Up
0x01
Down
3.10.2.3.2.3
Rate Field
The Rate field specifies the rate of movement in units per second. The actual rate of movement SHOULD be as close to this rate as the device is able. If the Rate field is 0xFF, then the value in DefaultMoveRate attribute SHALL be used. If the Rate field is 0xFF and the DefaultMoveRate attribute is not supported, then the device SHOULD move as fast as it is able. If the device is not able to move at a variable rate, this field MAY be disregarded.
"""
        },
        "Step": {
            "fields": ["Step mode", 'Step size', 'Transition time', 'OptionsMask', 'OptionsOverride'],
            "intro": """
3.10.2.3.3.1
Payload Format
The Step command payload SHALL be formatted as illustrated in Figure 3-42.
Figure 3-42. Format of the Step Command Payload
1
1
2
1
1
Octets
Data Type
enum8
uint8
uint16
map8
map8
Field Name
Step mode
Step size
Transition time
OptionsMask
OptionsOverride
Default
n/a
n/a
n/a
0
056
The Step mode field SHALL be one of the non-reserved values in Table 3-62.
Table 3-62. Values of the Step Mode Field
Fade Mode Value
Description
0x00
Up
0x01
Down
The Transition time field specifies the time that SHALL be taken to perform the step, in tenths of a second. A step is a change in the CurrentLevel of 'Step size' units. The actual time taken SHOULD be as close to this as the device is able. If the Transition time field is 0xffff the device SHOULD move as fast as it is able.
If the device is not able to move at a variable rate, the Transition time field MAY be disregarded.
"""
        },
        "Stop": {
            "fields": ['OptionsMask', 'OptionsOverride'],
            "intro": """
The command payload SHALL be formatted as illustrated below.
Figure 3-43. Format of the Command Payload
1
1
Octets
Data Type
map8
map8
Field Name
OptionsMask
OptionsOverride
Default
0
057
"""
        },
        "Move to Closest Frequency": {
            "fields": ['Frequency'],
            "intro": """
The command payload SHALL be formatted as illustrated below.
Figure 3-44. Format of the Command Payload
259
Octets
Data Type
uint16
Field Name
Frequency
"""
        }
    },
    "Color": {
        "Move to Hue": {
            "fields": ['Hue', 'Direction', 'Transition Time', 'OptionsMask', 'OptionsOverride'],
            "intro": """
5.2.2.3.4.1
Payload Format
The Move to Hue command payload SHALL be formatted as illustrated in Figure 5-2.
Figure 5-2. Format of the Move to Hue Command Payload
1
1
2
1
1
Octets
uint8
enum8
uint16
map8
map8
Data Type
Hue
Direction
Transition Time
OptionsMask
OptionsOverride
Field Name
n/a
n/a
n/a
0
091
Default
5.2.2.3.4.2
Hue Field
The Hue field specifies the hue to be moved to.
5.2.2.3.4.3
Direction Field
The Direction field SHALL be one of the non-reserved values in Table 5.14.
Table 5.14. Values of the Direction Field
Fade Mode Value
Description
0x00
Shortest distance
0x01
Longest distance
0x02
Up
0x03
Down
5.2.2.3.4.4
Transition Time Field
The Transition Time field specifies, in 1/10ths of a second, the time that SHALL be taken to move to the new hue.
5.2.2.3.4.5
OptionsMask and OptionsOverride fields
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
"""
        },
        "Move Hue": {
            "fields": ['Move Mode', 'Rate', 'OptionsMask', 'OptionsOverride'],
            "intro": """
5.2.2.3.5.1
Payload Format
The Move Hue command payload SHALL be formatted as illustrated in Figure 5-3.
Figure 5-3. Format of the Move Hue Command Payload
1
1
Octets
1
1
map8
map8
Data Type
enum8
uint8
OptionsMask
OptionsOverride
Field Name
Move Mode
Rate
0
092
Default
n/a
n/a
5.2.2.3.5.2
Move Mode Field
The Move Mode field SHALL be one of the non-reserved values in Table 5.15. If the Move Mode field is equal to 0x00 (Stop), the Rate field SHALL be ignored.93
Table 5.15. Values of the Move Mode Field
Move Mode Value
Description
0x00
Stop
0x01
Up
0x02
Reserved
0x03
Down
5.2.2.3.5.3
Rate Field
The Rate field specifies the rate of movement in steps per second. A step is a change in the device’s hue of one unit. If If the Move Mode field is set to 0x01 (up) or 0x03 (down) and the Rate field has a value of zero, the command has no effect and a Default Response command (see Chapter 2) SHALL be sent in response, with the status code set to INVALID_FIELD. If the Move Mode field is set to 0x00 (stop) the Rate field SHALL be ignored.94
5.2.2.3.5.4
OptionsMask and OptionsOverride field
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
"""
        },
        "Step Hue": {
            "fields": ['Step Mode', 'Step Size', 'Transition Time', 'OptionsMask', 'OptionsOverride'],
            "intro": """
The Step Hue command payload SHALL be formatted as illustrated in Figure 5-4.
Figure 5-4. Format of the Step Hue Command Payload
1
1
Octets
1
1
1
map8
map8
Data Type
enum8
uint8
uint8
OptionsMask
OptionsOverride
Field Name
Step Mode
Step Size
Transition Time
0
095
Default
n/a
n/a
n/a
5.2.2.3.6.2
Step Mode Field
The Step Mode field SHALL be one of the non-reserved values in Table 5.17.
Table 5.17. Values of the Step Mode Field
Fade Mode Value
Description
0x00
Reserved
0x01
Up
0x02
Reserved
0x03
Down
5.2.2.3.6.3
Step Size Field
The change to be added to (or subtracted from) the current value of the device’s hue.
5.2.2.3.6.4
Transition Time Field
The Transition Time field specifies, in 1/10ths of a second, the time that SHALL be taken to perform the step. A step is a change in the device’s hue of ‘Step size’ units.
5.2.2.3.6.5
OptionsMask and OptionsOverride fields
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
"""
        },
        "Move to Saturation": {
            "fields": ['Saturation', 'Transition Time', 'OptionsMask', 'OptionsOverride'],
            "intro": """
5.2.2.3.7.1
Payload Format
The Move to Saturation command payload SHALL be formatted as illustrated in Figure 5-5.
Figure 5-5. Format of the Move to Saturation Command Payload
1
1
Octets
1
2
map8
map8
Data Type
uint8
uint16
OptionsMask
OptionsOverride
Field Name
Saturation
Transition Time
0
096
Default
n/a
n/a
5.2.2.3.7.2
OptionsMask and OptionsOverride fields
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
"""
        },
        "Move Saturation": {
            "fields": ['Move Mode', 'Rate', 'OptionsMask', 'OptionsOverride'],
            "intro": """
5.2.2.3.8.1
Payload Format
The Move Saturation command payload SHALL be formatted as illustrated in Figure 5-6.
Figure 5-6. Format of the Move Saturation Command Payload
1
1
Octets
1
1
map8
map8
Data Type
enum8
uint8
OptionsMask
OptionsOverride
Field Name
Move Mode
Rate
0
097
Default
n/a
n/a
5.2.2.3.8.2
Move Mode Field
The Move Mode field SHALL be one of the non-reserved values in Table 5.19. If the Move Mode field is equal to 0x00 (Stop), the Rate field SHALL be ignored.98
Table 5.19. Values of the Move Mode Field
Move Mode Value
Description
0x00
Stop
0x01
Up
0x02
Reserved
0x03
Down
5.2.2.3.8.3
Rate Field
The Rate field specifies the rate of movement in steps per second. A step is a change in the device’s saturation of one unit. If the Move Mode field is set to 0x01 (up) or 0x03 (down) and the Rate field has a value of zero, the command has no effect and a Default Response command (see Chapter 2) SHALL be sent in response, with the status code set to INVALID_FIELD. If the Move Mode field is set to 0x00 (stop) the Rate field SHALL be ignored.99OptionsMask and OptionsOverride fields
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
"""
        },
        "Step Saturation": {
            "fields": ['Step Mode', 'Step Size', 'Transition Time', 'OptionsMask', 'OptionsOverride'],
            "intro": """
5.2.2.3.9.1
Payload Format
The Step Saturation command payload SHALL be formatted as illustrated in Figure 5-7.
Figure 5-7. Format of the Step Saturation Command Payload
1
1
1
1
1
Octets
enum8
uint8
uint8
map8
map8
Data Type
Step Mode
Step Size
Transition Time
OptionsMask
OptionsOverride
Field Name
n/a
n/a
n/a
0
0100
Default
5.2.2.3.9.2
Step Mode Field
The Step Mode field SHALL be one of the non-reserved values in Table 5.21.
Table 5.21. Values of the Step Mode Field
Step Mode Value
Description
0x00
Reserved
0x01
Up
0x02
Reserved
0x03
Down
5.2.2.3.9.3
Step Size Field
The change to be added to (or subtracted from) the current value of the device’s saturation.
5.2.2.3.9.4
Transition Time Field
The Transition Time field specifies, in 1/10ths of a second, the time that SHALL be taken to perform the step. A step is a change in the device’s saturation of ‘Step size’ units.
"""
        },
        "Move to Hue and Saturation": {
            "fields": ['Hue', 'Saturation', 'Transition Time', 'OptionsMask', 'OptionsOverride'],
            "intro": """
The Move to Hue and Saturation command payload SHALL be formatted as illustrated in Figure 5-8.
Figure 5-8. Move to Hue and Saturation Command Payload
Octets
1
1
2
1
1
Data Type
uint8
uint8
uint16
map8
map8
Field Name
Hue
Saturation
Transition Time
OptionsMask
OptionsOverride
Default
n/a
n/a
n/a
0
0101
5.2.2.3.10.2
OptionsMask and OptionsOverride fields
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
"""
        },
        "Move to Color": {
            "fields": ['ColorX', 'ColorY', 'Transition Time', 'OptionsMask', 'OptionsOverride'],
            "intro": """
5.2.2.3.11.1
Payload Format
The Move to Color command payload SHALL be formatted as illustrated in Figure 5-9.
Figure 5-9. Format of the Move to Color Command Payload
Octets
2
2
2
1
1
Data Type
uint16
uint16
uint16
map8
map8
Field Name
ColorX
ColorY
Transition Time
OptionsMask
OptionsOverride
Default
n/a
n/a
n/a
0
0102
5.2.2.3.11.2
OptionsMask and OptionsOverride fields
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
"""
        },
        "Move Color": {
            "fields": ['RateX', 'RateY', 'OptionsMask' 'OptionsOverride'],
            "intro": """
The Move Color command payload SHALL be formatted as illustrated in Figure 5-10.
Figure 5-10. Format of the Move Color Command Payload
Octets
2
2
1
1
Data Type
int16
int16
map8
map8
Field Name
RateX
RateY
OptionsMask
OptionsOverride
Default
n/a
n/a
0
0103
5.2.2.3.12.2
RateX Field
The RateX field specifies the rate of movement in steps per second. A step is a change in the device’s Cur- rentX attribute of one unit.
5.2.2.3.12.3
RateY Field
The RateY field specifies the rate of movement in steps per second. A step is a change in the device’s Cur- rentY attribute of one unit.
5.2.2.3.12.4
OptionsMask and OptionsOverride fields
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
"""
        },
        "Step Color": {
            "fields": ['StepX', 'StepY' ,'Transition Time', 'OptionsMask', 'OptionsOverride'],
            "intro": """
5.2.2.3.13.1
Payload Format
The Step Color command payload SHALL be formatted as illustrated in Figure 5-11.
Figure 5-11. Format of the Step Color Command Payload
1
1
Octets
2
2
2
map8
map8
Data Type
int16
int16
uint16
OptionsMask
OptionsOverride
Field Name
StepX
StepY
Transition Time
0
0104
Default
n/a
n/a
n/a
5.2.2.3.13.2
StepX and StepY Fields
The StepX and StepY fields specify the change to be added to the device's CurrentX attribute and CurrentY attribute respectively.
5.2.2.3.13.3
Transition Time Field
The Transition Time field specifies, in 1/10ths of a second, the time that SHALL be taken to perform the color change. 9999
5.2.2.3.13.4
OptionsMask and OptionsOverride fields
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
"""
        },
        "Move to Color Temperature": {
            "fields": ['Color Temperature Mireds', 'Transition Time', 'OptionsMask', 'OptionsOverride'],
            "intro": """
5.2.2.3.14.1
Payload Format
The Move to Color Temperature command payload SHALL be formatted as illustrated in Figure 5-12.
Figure 5-12. Move to Color Temperature Command Payload
Octets
2
2
1
1
Data Type
uint16
uint16
map8
map8
Field Name
Color Temperature Mireds
Transition Time
OptionsMask
OptionsOverride
Default
n/a
n/a
0
0105
5.2.2.3.14.2
OptionsMask and OptionsOverride fields
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
"""
        },
        "Enhanced Move to Hue": {
            "fields": ['Enhanced Hue', 'Direction', 'Transition Time', 'OptionsMask', 'OptionsOverride'],
            "intro": """
The payload of this command SHALL be formatted as illustrated in Figure 5-13.
Figure 5-13. Format of the Enhanced Move to Hue Command
Octets
2
1
2
1
1
Data Type
uint16
enum8
uint16
map8
map8
Field Name
Enhanced Hue
Direction
Transition Time
OptionsMask
OptionsOverride
Default
n/a
n/a
n/s
0
0106
5.2.2.3.15.1
Enhanced Hue Field
The Enhanced Hue field is 16-bits in length and specifies the target extended hue for the lamp.
5.2.2.3.15.2
Direction Field
This field is identical to the Direction field of the Move to Hue command of the Color Control cluster (see sub-clause 5.2.2.3.3).
5.2.2.3.15.3
Transition Time Field
This field is identical to the Transition Time field of the Move to Hue command of the Color Control cluster (see sub-clause 5.2.2.3.3).
5.2.2.3.15.4
OptionsMask and OptionsOverride fields
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
"""
        },
        "Enhanced Move Hue": {
            "fields": ['Move Mode', 'Rate', 'OptionsMask', 'OptionsOverride'],
            "intro": """
The payload of this command SHALL be formatted as illustrated in Figure 5-14.
Figure 5-14. Format of the Enhanced Move Hue Command
Octets
1
2
1
1
Data Type
enum8
uint16
map8
map8
Field Name
Move Mode
Rate
OptionsMask
OptionsOver- ride
Default
n/a
n/a
0
0107
5.2.2.3.16.1 Move Mode Field
This field is identical to the Move Mode field of the Move Hue command of the Color Control cluster (see sub-clause 5.2.2.3.5). If the Move Mode field is equal to 0x00 (Stop), the Rate field SHALL be ignored.108
5.2.2.3.16.2
Rate field
The Rate field is 16-bits in length and specifies the rate of movement in steps per second. A step is a change in the extended hue of a device by one unit. If the Move Mode field is set to 0x01 (up) or 0x03 (down) and the Rate field has a value of zero, the command has no effect and a ZCL Default Response command SHALL be sent in response, with the status code set to INVALID_FIELD. If the Move Mode field is set to 0x00 (stop) the Rate field SHALL be ignored.
5.2.2.3.16.3
OptionsMask and OptionsOverride fields
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
"""
        },
        "Enhanced Step Hue": {
            "fields": ['Step Mode',  'Step Size',  'Transition Time',  'OptionsMask',  'OptionsOverride'],
            "intro": """
The payload of this command SHALL be formatted as illustrated in Figure 5-15.
Figure 5-15. Format of the Enhanced Step Hue Command
2
2
1
1
Octets
1
uint16
uint16
map8
map8
Data Type
enum8
Step Size
Transition Time
OptionsMask
OptionsOverride
Field Name
Step Mode
n/a
n/a
0
0109
Default
n/a
5.2.2.3.17.1
Step Mode Field
This field is identical to the Step Mode field of the Step Hue command of the Color Control cluster (see sub- clause 5.2.2.3.6).
5.2.2.3.17.2
Step Size Field
The Step Size field is 16-bits in length and specifies the change to be added to (or subtracted from) the current value of the device’s enhanced hue.
5.2.2.3.17.3
Transition Time Field
The Transition Time field is 16-bits in length and specifies, in units of 1/10ths of a second, the time that SHALL be taken to perform the step. A step is a change to the device’s enhanced hue of a magnitude corre- sponding to the Step Size field.
5.2.2.3.17.4
OptionsMask and OptionsOverride fields
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
"""
        },
        "Color Loop Set": {
            "fields": ['Update Flags',  'Action',  'Direction',  'Time',  'Start Hue',  'OptionsMask',  'OptionsOverride'],
            "intro": """
Figure 5-17. Format of the Color Loop Set Command
Octets
1
1
1
2
2
1
1
Data
map8
enum8
enum8
uint16
uint16
map8
map8
Type
Field
Update Flags
Action
Direc- tion
Time
Start Hue
Op-
tionsMask
OptionsOver- ride
Name
Default
n/a
n/a
n/a
n/a
n/a
0
0111
5.2.2.3.19.1
Update Flags Field
The Update Flags field is 8 bits in length and specifies which color loop attributes to update before the color loop is started. This field SHALL be formatted as illustrated in Figure 5-18.
Figure 5-18. Format of the Update Flags Field of the Color Loop Set Command
Bits: 0
1
2
3
4-7
Update Action
Update Direction
Update Time
Update Start Hue
Reserved
The Update Action sub-field is 1 bit in length and specifies whether the device SHALL adhere to the action field in order to process the command. If this sub-field is set to 1, the device SHALL adhere to the action field. If this sub-field is set to 0, the device SHALL ignore the action field.
The Update Direction sub-field is 1 bit in length and specifies whether the device SHALL update the Color- LoopDirection attribute with the Direction field. If this sub-field is set to 1, the device SHALL update the value of the ColorLoopDirection attribute with the value of the Direction field. If this sub-field is set to 0, the device SHALL ignore the Direction field.
The Update Time sub-field is 1 bit in length and specifies whether the device SHALL update the ColorLoop- Time attribute with the Time field. If this sub-field is set to 1, the device SHALL update the value of the ColorLoopTime attribute with the value of the Time field. If this sub-field is set to 0, the device SHALL ignore the Time field.
The Update Start Hue sub-field is 1 bit in length and specifies whether the device SHALL update the Color- LoopStartEnhancedHue attribute with the Start Hue field. If this sub-field is set to 1, the device SHALL update the value of the ColorLoopStartEnhancedHue attribute with the value of the Start Hue field. If this sub-field is set to 0, the device SHALL ignore the Start Hue field.
5.2.2.3.19.2
Action Field
The Action field is 8 bits in length and specifies the action to take for the color loop if the Update Action sub-field of the Update Flags field is set to 1. This field SHALL be set to one of the non-reserved values listed in Table 5.25.
Table 5.25. Values of the Action Field of the Color Loop Set Command
Value
Description
0x00
De-activate the color loop.
0x01
Activate the color loop from the value in the ColorLoopStartEnhancedHue field.
Value
Description
0x02
Activate the color loop from the value of the EnhancedCurrentHue attribute.
5.2.2.3.19.3
Direction Field
The Direction field is 8 bits in length and specifies the direction for the color loop if the Update Direction field of the Update Flags field is set to 1. This field SHALL be set to one of the non-reserved values listed in Table 5.26.
Table 5.26. Values of the Direction Field of the Color Loop Set Command
Direction Field
Description
Value
0x00
Decrement the hue in the color loop.
0x01
Increment the hue in the color loop.
5.2.2.3.19.4
Time Field
The Time field is 16 bits in length and specifies the number of seconds over which to perform a full color loop if the Update Time field of the Update Flags field is set to 1.
5.2.2.3.19.5
Start Hue Field
The Start Hue field is 16 bits in length and specifies the starting hue to use for the color loop if the Update Start Hue field of the Update Flags field is set to 1.
5.2.2.3.19.6
OptionsMask and OptionsOverride fields
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
"""
        },
        "Stop Move Step": {
            "fields": ['OptionsMask', 'OptionsOverride'],
            "intro": """
The Stop Move Step command payload SHALL be formatted as illustrated in Figure 5-19.
Figure 5-19. Format of the Stop Move Step Command Payload
Octets
1
1
Data Type
map8
map8
Field Name
OptionsMask
OptionsOverride
0112
Default
0
5.2.2.3.20.1
OptionsMask and OptionsOverride fields
The OptionsMask and OptionsOverride fields SHALL be processed according to section 5.2.2.3.3.
5.2.2.3.20.2
Effect on Receipt
Upon receipt of this command, any Move to, Move or Step command currently in process SHALL be termi- nated. The values of the CurrentHue, EnhancedCurrentHue and CurrentSaturation attributes SHALL be left at their present value upon receipt of the Stop Move Step command, and the RemainingTime attribute SHALL be set to zero.
"""
        }
    },
    "Alarms": {
        "Reset Alarm": {
            "fields": ['Alarm code', 'Cluster identifier'],
            "intro": """
3.11.2.4.1.1
Payload Format
The Reset Alarm command payload SHALL be formatted as illustrated in Figure 3-45.
Figure 3-45. Format of the Reset Alarm Command Payload
1
2
Octets
enum8
clusterId
Data Type
Alarm code
Cluster identifier
Field Name
"""
        },
        "Get Alarm": {
            "fields": [],
            "intro": """
This command does not have a payload.
"""
        },
        "Reset Alarm Log": {
            "fields": [],
            "intro": """
This command does not have a payload.
"""
        }
    },
    "DoorLock": {
        "Lock Door": {
            "fields": [],
            "intro": """
"""
        },
        "Unlock Door": {
            "fields": [],
            "intro": """
"""
        },
        "Toggle": {
            "fields": [],
            "intro": """
"""
        },
        "Unlock with Timeout": {
            "fields": [],
            "intro": """
"""
        },
        "Get Log Record": {
            "fields": [],
            "intro": """
"""
        },
        "Set PIN Code": {
            "fields": [],
            "intro": """
"""
        },
        "Get PIN Code": {
            "fields": [],
            "intro": """
"""
        },
        "Clear PIN Code": {
            "fields": [],
            "intro": """
"""
        },
        "Clear All PIN Codes": {
            "fields": [],
            "intro": """
"""
        },
        "Set User Status": {
            "fields": [],
            "intro": """
"""
        },
        "Get User Status": {
            "fields": [],
            "intro": """
"""
        },
        "Set Week Day Schedule": {
            "fields": [],
            "intro": """
"""
        },
        "Get Week Day Schedule": {
            "fields": [],
            "intro": """
"""
        },
        "Clear Week Day Schedule": {
            "fields": [],
            "intro": """
"""
        },
        "Set Year Day Schedule": {
            "fields": [],
            "intro": """
"""
        },
        "Get Year Day Schedule": {
            "fields": [],
            "intro": """
"""
        },
        "Clear Year Day Schedule": {
            "fields": [],
            "intro": """
"""
        },
        "Set Holiday Schedule": {
            "fields": [],
            "intro": """
"""
        },
        "Get Holiday Schedule": {
            "fields": [],
            "intro": """
"""
        },
        "Clear Holiday Schedule": {
            "fields": [],
            "intro": """
"""
        },
        "Set User Type": {
            "fields": [],
            "intro": """
"""
        },
        "Get User Type": {
            "fields": [],
            "intro": """
"""
        },
        "Set RFID Code": {
            "fields": [],
            "intro": """
"""
        },
        "Get RFID Code": {
            "fields": [],
            "intro": """
"""
        },
        "Clear RFID Code": {
            "fields": [],
            "intro": """
"""
        },
        "Clear All RFID Codes": {
            "fields": [],
            "intro": """
"""
        }
    }
}

LEGITIMATE_STATUS = [
    "SUCCESS",
    "FAILURE",
    "NOT_AUTHORIZED",
    "MALFORMED_COMMAND",
    "UNSUP_CLUSTER_COMMAND",
    "UNSUP_COMMAND",
    "UNSUP_GENERAL_COMMAND",
    "UNSUP_COMMAND",
    "UNSUP_MANUF_CLUSTER_COMMAND",
    "UNSUP_COMMAND",
    "UNSUP_MANUF_GENERAL_COMMAND",
    "UNSUP_COMMAND",
    "INVALID_FIELD",
    "UNSUPPORTED_ATTRIBUTE",
    "INVALID_VALUE",
    "READ_ONLY",
    "INSUFFICIENT_SPACE",
    "DUPLICATE_EXISTS",
    "NOT_FOUND",
    "UNREPORTABLE_ATTRIBUTE",
    "INVALID_DATA_TYPE",
    "INVALID_SELECTOR",
    "WRITE_ONLY",
    "NOT_AUTHORIZED",
    "INCONSISTENT_STARTUP_STATE",
    "FAILURE",
    "DEFINED_OUT_OF_BAND",
    "ACTION_DENIED",
    "TIMEOUT",
    "ABORT",
    "INVALID_IMAGE",
    "WAIT_FOR_DATA",
    "NO_IMAGE_AVAILABLE",
    "REQUIRE_MORE_IMAGE",
    "NOTIFICATION_PENDING",
    "HARDWARE_FAILURE",
    "SOFTWARE_FAILURE",
    "UNSUPPORTED_CLUSTER",
    "LIMIT_REACHED"
]

