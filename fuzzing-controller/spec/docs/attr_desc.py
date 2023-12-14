CLUSTER_ATTR_DESCRIPTION = {
    "Groups": {
        "attrs": ["NameSupport"],
        "intro": """
The server supports the attribute shown in Table 3-36. 
 Table 3-36. Attributes of the Groups Server Cluster  Identifier Name Type Range Acc Def M/O 0x0000 NameSupport map8 desc R 0 M
 3.6.2.2.1 NameSupport Attribute  The most significant bit of the NameSupport attribute indicates whether or not group names are supported. A value of 1 indicates that they are supported, and a value of 0 indicates that they are not supported.
 3.6.2.2.2 Group Names Group names are between 0 and 16 characters long. Support of group names is optional, and is indicated by  the NameSupport attribute. Group names, if supported, must be stored in a separate data structure managed  by the application in which the entries correspond to group table entries.
"""
    },
    "Identify": {
        "attrs": ["IdentifyTime"],
        "intro": """
The server supports the attribute shown in Table 3-31. 
Table 3-31. Attributes of the Identify Server Cluster Identifier Name Type Range Access Default M/O 0x0000 IdentifyTime uint16 0x0000 to 0xffff RW 0 M 3.5.2.2.1 IdentifyTime Attribute  The IdentifyTime attribute specifies the remaining length of time, in seconds, that the device will continue to  identify itself. 
If this attribute is set to a value other than 0x0000 then the device SHALL enter its identification procedure,  in order to indicate to an observer which of several devices it is. It is recommended that this procedure con sists of flashing a light with a period of 0.5 seconds. The IdentifyTime attribute SHALL be decremented every  second. 
If this attribute reaches or is set to the value 0x0000 then the device SHALL terminate its identification procedure.
"""
    },
    "Scenes": {
        "attrs": ["SceneCount", "CurrentScene", "CurrentGroup", "SceneValid", "NameSupport", "LastConfiguredBy"],
        "intro": """
The Scene Management Information attribute set contains the attributes summarized in Table 3-40. 
 Table 3-40. Scene Management Information Attribute Set  Id Name Type Range Access Default M/O 0x0000 SceneCount uint8 0x00 to 0xff  (see 3.7.2.3.2 ) R 0 M 0x0001 CurrentScene uint8 0x00 to 0xff (see 3.7.2.3.2) R 0 M 0x0002 CurrentGroup uint16 0x0000 to 0xfff7 R 0 M 0x0003 SceneValid bool 0 or 1 R 0 M 0x0004 NameSupport map8 desc R 0 M 0x0005 LastConfiguredBy EUI64 R non O
 3.7.2.2.1.1 SceneCount Attribute   The SceneCount attribute specifies the number of scenes currently in the device's scene table.  
 3.7.2.2.1.2 CurrentScene Attribute   The CurrentScene attribute holds the Scene ID of the scene last invoked. 
 3.7.2.2.1.3 CurrentGroup Attribute   The CurrentGroup attribute holds the Group ID of the scene last invoked, or 0 if the scene last invoked is  not associated with a group. 
 3.7.2.2.1.4 SceneValid Attribute   The SceneValid attribute indicates whether the state of the device corresponds to that associated with the  CurrentScene and CurrentGroup attributes. TRUE indicates that these attributes are valid, FALSE indicates  that they are not valid.  
 Before a scene has been stored or recalled, this attribute is set to FALSE. After a successful Store Scene or  Recall Scene command it is set to TRUE. If, after a scene is stored or recalled, the state of the device is  modified, this attribute is set to FALSE.  
 3.7.2.2.1.5 NameSupport Attribute The most significant bit of the NameSupport attribute indicates whether or not scene names are supported. A  value of 1 indicates that they are supported, and a value of 0 indicates that they are not supported. 
 3.7.2.2.1.6 LastConfiguredBy Attribute   The LastConfiguredBy attribute is 64 bits in length and specifies the IEEE address of the device that last  configured the scene table. 
 The non-value indicates that the device has not been configured, or that the address of the device that last  configured the scenes cluster is not known
"""
    },
    "OnOff": {
        "attrs": ['OnOff', 'GlobalSceneControl', 'OnTime','OffWaitTime', 'StartUpOnOff'],
        "intro": """
3.8.2.2 Attributes
The server supports the attributes shown in Table 3-45.
Table 3-45. Attributes of the On/Off Server Cluster
Identifier
Name
Type
Range
Acc
Def
M
0x0000
OnOff
bool
value
RPS
0
M
0x4000
GlobalSceneControl
bool
value
R
1
O
0x4001
OnTime
uint16
full-non
RW
0
O
0x4002
OffWaitTime
uint16
full
RW
0
O
Identifier
Name
Type
Range
Acc
Def
M
0x4003
StartUpOnOff
enum8
desc
RW
MS
O
3.8.2.2.1
OnOff Attribute
The OnOff attribute has the following values: 0 = Off, 1 = On.
3.8.2.2.2
GlobalSceneControl Attribute
In order to support the use case where the user gets back the last setting of the devices (e.g. level settings for lamps), a global scene is introduced which is stored when the devices are turned off and recalled when the devices are turned on. The global scene is defined as the scene that is stored with group identifier 0 and scene identifier 0.
The GlobalSceneControl attribute is defined in order to prevent a second off command storing the all-devices- off situation as a global scene, and to prevent a second on command destroying the current settings by going back to the global scene.
The GlobalSceneControl attribute SHALL be set to TRUE after the reception of a command which causes the OnOff attribute to be set to TRUE, such as a standard On command, a Move to level (with on/off) com- mand, a Recall scene command or a On with recall global scene command (see Section 3.8.2.3.5).
The GlobalSceneControl attribute is set to FALSE after reception of a Off with effect command.
3.8.2.2.3
OnTime Attribute
The OnTime attribute specifies the length of time (in 1/10ths second) that the “on” state SHALL be main- tained before automatically transitioning to the “off” state when using the On with timed off command. If this attribute is set to 0x0000 or 0xffff, the device SHALL remain in its current state.
3.8.2.2.4
OffWaitTime Attribute
The OffWaitTime attribute specifies the length of time (in 1/10ths second) that the “off” state SHALL be guarded to prevent an on command turning the device back to its “on” state (e.g., when leaving a room, the lights are turned off but an occupancy sensor detects the leaving person and attempts to turn the lights back on). If this attribute is set to 0x0000, the device SHALL remain in its current state.
3.8.2.2.5
StartUpOnOff Attribute
The StartUpOnOff attribute SHALL define the desired startup behavior of a 50device when it is supplied with power and this state SHALL be reflected in the OnOff attribute. The values of the StartUpOnOff attribute are listed below.
Table 3-46. Values of the StartUpOnOff Attribute
Value
Action on power up
0x00
Set the OnOff attribute to 0 (off).
0x01
Set the OnOff attribute to 1 (on).
0x02
If the previous value of the OnOff attribute is equal to 0, set the OnOff attribute to 1. If the previous value of the OnOff attribute is equal to 1, set the OnOff attribute to 0 (toggle).
0x03 to 0xfe
These values are reserved. No action.
0xff
Set the OnOff attribute to its previous value.
"""
    },
    "Level": {
        "attrs": ["CurrentLevel", "RemainingTime", 'MinLevel', 'MaxLevel', 'CurrentFrequency', 'MinFrequency', 'MaxFrequency', 'OnOffTransitionTime', 'OnLevel', 'OnTransitionTime', 'OffTransitionTime', 'DefaultMoveRate', 'Options', 'StartUpCurrentLevel'],
        "intro": """
The attributes of the Level Control server cluster are summarized in Table 3-56.
Table 3-56. Attributes of the Level Control Server Cluster
Id
Name
Type
Range
Acc
Default
M/O
0x0000
CurrentLevel
uint8
MinLevel to MaxLevel
RPS
0xff
M
0x0001
RemainingTime
uint16
0x0000 to 0xffff
R
0
O
0x0002
MinLevel
uint8
0 to MaxLevel
R
0
O
0x0003
MaxLevel
uint8
MinLevel to 0xff
R
0xff
O
0x0004
CurrentFrequency
uint16
MinFrequency to MaxFrequency
RPS
0
O
0x0005
MinFrequency
uint16
0 to MaxFrequency
R
0
O
0x0006
MaxFrequency
uint16
MinFrequency to 0xffff
R
0
O
0x0010
OnOffTransitionTime
uint16
0x0000 to 0xffff
RW
0
O
0x0011
OnLevel
uint8
MinLevel to MaxLevel
RW
0xff
O
0x0012
OnTransitionTime
uint16
0x0000 to 0xfffe
RW
0xffff
O
0x0013
OffTransitionTime
uint16
0x0000 to 0xfffe
RW
0xffff
O
0x0014
DefaultMoveRate
uint851
0x00 to 0xfe
RW
MS
O
0x000F
Options
map8
descr
RW
0
O
0x4000
StartUpCurrentLevel
uint8
0x00 to 0xff
RW
MS
O
3.10.2.2.1 CurrentLevel Attribute
The CurrentLevel attribute represents the current level of this device. The meaning of 'level' is device de- pendent.
3.10.2.2.2 RemainingTime Attribute
The RemainingTime attribute represents the time remaining until the current command is complete - it is specified in 1/10ths of a second.
3.10.2.2.3 MinLevel Attribute
The MinLevel attribute indicates the minimum value of CurrentLevel that is capable of being assigned.
3.10.2.2.4 MaxLevel Attribute
The MaxLevel attribute indicates the maximum value of CurrentLevel that is capable of being assigned.
3.10.2.2.5 CurrentFrequency Attribute
The CurrentFrequency attribute represents the frequency that the devices is at CurrentLevel. A CurrentFre- quency of 0 is unknown.
3.10.2.2.6 MinFrequency Attribute
The MinFrequency attribute indicates the minimum value of CurrentFrequency that is capable of being as- signed. MinFrequency shall be less than or equal to MaxFrequency. A value of 0 indicates undefined.
3.10.2.2.7 MaxFrequency Attribute
The MaxFrequency attribute indicates the maximum value of CurrentFrequency that is capable of being assigned. MaxFrequency shall be greater than or equal to MinFrequency. A value of 0 indicates undefined.
3.10.2.2.8 Options Attribute
The Options attribute is meant to be changed only during commissioning. The Options attribute is a bitmap that determines the default behavior of some cluster commands. Each command that is dependent on the Options attribute SHALL first construct a temporary Options bitmap that is in effect during the command processing. The temporary Options bitmap has the same format and meaning as the Options attribute, but includes any bits that may be overridden by command fields.
Below is the format and description of the Options attribute and temporary Options bitmap and the effect on dependent commands.
Table 3-57. Options Attribute
Bit
Name
Values & Summary
0 – Do not execute command if OnOff is 0x00 (FALSE)
0
ExecuteIfOff
1 – Execute command if OnOff is 0x00 (FALSE)
This bit has been defined in these derived clusters for a specific application:
1
Reserved for Derived Clusters
Level Control for Lighting
3.10.2.2.8.1
ExecuteIfOff Options Bit
Command execution SHALL NOT continue beyond the Options processing if all of these criteria are true:
• The command is one of the ‘without On/Off’ commands: Move, Move to Level, Stop, or Step.
• The On/Off cluster exists on the same endpoint as this cluster.
• The OnOff attribute of the On/Off cluster, on this endpoint, is 0x00 (FALSE).
• The value of the ExecuteIfOff bit is 0.
3.10.2.2.9 OnOffTransitionTime Attribute
The OnOffTransitionTime attribute represents the time taken to move to or from the target level when On of Off commands are received by an On/Off cluster on the same endpoint. It is specified in 1/10ths of a second.
The actual time taken SHOULD be as close to OnOffTransitionTime as the device is able. N.B. If the device is not able to move at a variable rate, the OnOffTransitionTime attribute SHOULD NOT be implemented.
3.10.2.2.10 OnLevel Attribute
The OnLevel attribute determines the value that the CurrentLevel attribute is set to when the OnOff attribute of an On/Off cluster on the same endpoint is set to On, as a result of processing an On/Off cluster command. If the OnLevel attribute is not implemented, or is set to the non-value, it has no effect. For more details see 3.10.2.1.1.
3.10.2.2.11 OnTransitionTime Attribute
The OnTransitionTime attribute represents the time taken to move the current level from the minimum level to the maximum level when an On command is received by an On/Off cluster on the same endpoint. It is specified in 10ths of a second. If this command is not implemented, or contains a non-value, the On/OffTran- sitionTime will be used instead.
3.10.2.2.12 OffTransitionTime Attribute
The OffTransitionTime attribute represents the time taken to move the current level from the maximum level to the minimum level when an Off command is received by an On/Off cluster on the same endpoint. It is specified in 10ths of a second. If this command is not implemented, or contains a non-value, the On/OffTran- sitionTime will be used instead.
3.10.2.2.13 DefaultMoveRate Attribute
The DefaultMoveRate attribute determines the movement rate, in units per second, when a Move command is received with a non-value Rate parameter.
3.10.2.2.14 StartUpCurrentLevel Attribute
The StartUpCurrentLevel attribute SHALL define the desired startup level for a device when it is supplied with power and this level SHALL be reflected in the CurrentLevel attribute. The values of the StartUpCur- rentLevel attribute are listed below:
Table 3-58. Values of the StartUpCurrentLevel attribute
Value
Action on power up
0x00
Set the CurrentLevel attribute to the minimum value permitted on the device
0xff
Set the CurrentLevel attribute to its previous value
other values
Set the CurrentLevel attribute to this value
"""
    },
    "Color": {
        "attrs": ["CurrentHue", 'CurrentSaturation', 'RemainingTime', 'CurrentX', 'CurrentY', 'DriftCompensation', 'CompensationText', 'ColorTemperatureMireds', 'ColorMode', 'Options', 'EnhancedCurrentHue', 'EnhancedColorMode', 'ColorLoopActive', 'ColorLoopDirection', 'ColorLoopTime',\
                'ColorLoopStartEnhancedHue', 'ColorLoopStoredEnhancedHue', 'ColorCapabilities', 'ColorTempPhysicalMinMireds', 'ColorTempPhysicalMaxMireds', 'CoupleColorTempToLevelMinMireds', 'StartUpColorTemperatureMireds'],
        "intro": """
M/
Id
Name
Type
Range
Acc
Def
O
0x0000
CurrentHue
uint8
0x00 – 0xfe
RP
0x00
M0
0x0001
CurrentSaturation
uint8
0x00 – 0xfe
RPS
0x00
M0
0x0002
RemainingTime
uint16
0x0000 – 0xfffe
R
0x00
O
0x0003
CurrentX
uint16
0x0000 - 0xfeff
RPS
0x616b (0.381)
M3
0x0004
CurrentY
uint16
0x0000 - 0xfeff
RPS
0x607d (0.377)
M3
0x0005
DriftCompensation
enum8
0x00 – 0x04
R
-
O
0x0006
CompensationText
string
0 to 254 chars
R
-
O
0x0007
ColorTemperatureMireds
uint16
0x0000 - 0xfeff
RPS
0x00fa
(4000K)
M4
0x0008
ColorMode
enum8
0x00 – 0x02
R
0x01
M
0x000f
Options
map8
RW
0x00
M
0x4000
EnhancedCurrentHue
uint16
0x0000 – 0xffff
RS
0x0000
M1
0x4001
EnhancedColorMode
enum8
0x00 – 0xff
R
0x01
M
0x4002
ColorLoopActive
uint8
0x00 – 0xff
RS
0x00
M2
0x4003
ColorLoopDirection
uint8
0x00 – 0xff
RS
0x00
M2
0x4004
ColorLoopTime
uint16
0x0000 – 0xffff
RS
0x0019
M2
0x4005
ColorLoopStartEnhancedHue
uint16
0x0000 – 0xffff
R
0x2300
M2
0x4006
ColorLoopStoredEnhancedHue
uint16
0x0000 – 0xffff
R
0x0000
M2
0x400a
ColorCapabilities
map16
0x0000 – 0x001f
R
0x0000
M
0x400b
ColorTempPhysicalMinMireds
uint16
0x0000 – 0xfeff
R
0x0000
M4
0x400c
ColorTempPhysicalMaxMireds
uint16
0x0000 – 0xfeff
R
0xfeff
M4
0x400d
CoupleColorTempToLev- elMinMireds
uint16
ColorTempPhysicalMinMireds to ColorTemperatureMireds
R
MS
M4*
0x4010
StartUpColorTemperatureMireds
uint16
0x0000-0xfeff88
RW
MS
M4*
* Mandatory if ColorTemperatureMireds is supported.
5.2.2.2.1.1
CurrentHue Attribute
The CurrentHue attribute contains the current hue value of the light. It is updated as fast as practical during commands that change the hue.
The hue in degrees SHALL be related to the CurrentHue attribute by the relationship
Hue = CurrentHue x 360 / 254 (CurrentHue in the range 0 - 254 inclusive)
If this attribute is implemented then the CurrentSaturation and ColorMode attributes SHALL also be imple- mented.
5.2.2.2.1.2
CurrentSaturation Attribute
The CurrentSaturation attribute holds the current saturation value of the light. It is updated as fast as practical during commands that change the saturation.
The saturation SHALL be related to the CurrentSaturation attribute by the relationship
Saturation = CurrentSaturation/254 (CurrentSaturation in the range 0 - 254 inclusive)
If this attribute is implemented then the CurrentHue and ColorMode attributes SHALL also be implemented.
5.2.2.2.1.3
RemainingTime Attribute
The RemainingTime attribute holds the time remaining, in 1/10ths of a second, until the currently active command will be complete.
5.2.2.2.1.4
CurrentX Attribute
The CurrentX attribute contains the current value of the normalized chromaticity value x, as defined in the CIE xyY Color Space. It is updated as fast as practical during commands that change the color.
The value of x SHALL be related to the CurrentX attribute by the relationship x = CurrentX / 65536 (CurrentX in the range 0 to 65279 inclusive)
5.2.2.2.1.5
CurrentY Attribute
The CurrentY attribute contains the current value of the normalized chromaticity value y, as defined in the CIE xyY Color Space. It is updated as fast as practical during commands that change the color.
The value of y SHALL be related to the CurrentY attribute by the relationship y = CurrentY / 65536 (CurrentY in the range 0 to 65279 inclusive)
5.2.2.2.1.6
DriftCompensation Attribute
The DriftCompensation attribute indicates what mechanism, if any, is in use for compensation for color/in- tensity drift over time. It SHALL be one of the non-reserved values in Table 5.4.
Table 5.4. Values of the DriftCompensation Attribute
Attribute Value
Description
0x00
None
0x01
Other / Unknown
0x02
Temperature monitoring
0x03
Optical luminance monitoring and feedback
0x04
Optical color monitoring and feedback
5.2.2.2.1.7
CompensationText Attribute
The CompensationText attribute holds a textual indication of what mechanism, if any, is in use to compensate for color/intensity drift over time.
5.2.2.2.1.8
ColorTemperatureMireds Attribute
The ColorTemperatureMireds attribute contains a scaled inverse of the current value of the color tempera- ture. The unit of ColorTemperatureMireds is the mired (micro reciprocal degree), AKA mirek (micro recip- rocal kelvin). It is updated as fast as practical during commands that change the color.
The color temperature value in kelvins SHALL be related to the ColorTemperatureMireds attribute in mireds by the relationship
Color temperature in kelvins = 1,000,000 / ColorTemperatureMireds, where ColorTemperatureMireds is in the range 1 to 65279 mireds inclusive, giving a color temperature range from 1,000,000 kelvins to 15.32 kelvins.
The value ColorTemperatureMireds = 0x0000 indicates an undefined value. The value ColorTemperature- Mireds = 0xffff indicates an invalid value.
If this attribute is implemented then the ColorMode attribute SHALL also be implemented.
5.2.2.2.1.9
ColorMode Attribute
The ColorMode attribute indicates which attributes are currently determining the color of the device. If either the CurrentHue or CurrentSaturation attribute is implemented, this attribute SHALL also be implemented, otherwise it is optional.
The value of the ColorMode attribute cannot be written directly - it is set upon reception of any command in section 5.2.2.3 to the appropriate mode for that command.
Table 5.5. Values of the ColorMode Attribute
Attribute Value
Attributes that Determine the Color
0x00
CurrentHue and CurrentSaturation
0x01
CurrentX and CurrentY
0x02
ColorTemperatureMireds
"""
    },
    "Alarms": {
        "attrs": ["AlarmCount"],
        "intro": """
The Alarm Information attribute set contains the attributes summarized in Table 3-65.
Table 3-65. Attributes of the Alarm Information Attribute Set
Identifier
Name
Type
Range
Access
Default
M/O
0x0000
AlarmCount
uint16
0x00 to 0xff
R
0
O
3.11.2.2.1.1
AlarmCount Attribute
The AlarmCount attribute is 16 bits in length and specifies the number of entries currently in the alarm table. If alarm logging is not implemented this attribute SHALL always take the value 0.
"""
    }
}