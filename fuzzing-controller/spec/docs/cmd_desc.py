CLUSTER_CMD_DESCRIPTIONS = {
    "Groups": {
    "Add Group": """
If the device is unable to store the contents of the Group Name field, the Group Name field can be ignored.

On receipt of the Add Group command, the device SHALL perform the following procedure:

1. The device verifies that the Group ID field contains a valid group identifier in the range 0x0001 0xfff7. If the Group ID field contains a group identifier outside this range, the status SHALL be INVALID_VALUE and the device continues from step 5.

2. The device verifies that it does not already have an entry in its Group Table that corresponds to the value of the Group ID field. If it already has the requested entry in its Group Table, the Group Name SHALL be updated (if supported), the status SHALL be SUCCESS, and the device continues from step 5.

3. The device verifies that it has free entries in its Group Table. If the device has no free entries in its Group Table, the status SHALL be INSUFFICIENT_SPACE and the device continues from step 5.

4. The device adds the values of the Group ID and Group Name (if supported) fields to its Group Table and the status SHALL be SUCCESS.

5. If the Add Group command was received as a unicast, the device SHALL generate an Add Group Response command with the Status field set to the evaluated status and SHALL transmit it back to the originator of the Add Group command.
""",
    "View Group": """
On receipt of the View Group command, the device SHALL perform the following procedure:

1. The device verifies that the Group ID field contains a valid group identifier in the range 0x0001 0xfff7. If the Group ID field contains a group identifier outside this range, the status SHALL be INVALID_VALUE and the device continues from step 4.

2. The device attempts to retrieve the entry in its Group Table corresponding to the group identifier contained in the Group ID field. If no such entry exists in the Group Table, the status SHALL be NOT_FOUND and the device continues from step 4.

3. The device retrieves the requested entry from its Group Table and the status SHALL be SUCCESS.

4. If the View Group command was received as a unicast, the device SHALL generate a View Group Response command with the retrieved group entry and the Status field set to the evaluated status and SHALL transmit it back to the originator of the View Group command.
""",
    "Get Group Membership": """
On receipt of the get group membership command, each receiving entity SHALL respond with group membership information using the get group membership response frame as follows:

If the group count field of the command frame has a value of 0 indicating that the group list field is empty, the entity SHALL respond with all group identifiers of which the entity is a member.

If the group list field of the command frame contains at least one group of which the entity is a member, the entity SHALL respond with each entity group identifier that match a group in the group list field.

If the group count is non-zero, and the group list field of the command frame does not contain any group of which the entity is a member, the entity SHALL only respond if the command is unicast. The response SHALL return a group count of zero.
""",
    "Remove Group": """
On receipt of the Remove Group command, the device SHALLperform the following procedure:

1. The device verifies that the Group ID field contains a valid group identifier in the range 0x0001 0xfff7. If the Group ID field contains a group identifier outside this range, the status SHALL be INVALID_VALUE and the device continues from step 4.

2. The device attempts to remove the entry in its Group Table corresponding to the group identifier contained in the Group Id field. If no such entry exists in the Group Table, the status SHALL be NOT_FOUND and the device continues from step 4.

3. The device removes the requested entry from its Group Table and the status SHALL be SUCCESS.

4. If the Remove Group command was received as a unicast, the device SHALL generate a Remove Group Response command with the Status field set to the evaluated status and SHALL transmit it back to the originator of the Remove Group command.
""",
    "Remove All Groups": """
On receipt of this command, the device SHALL remove all groups on this endpoint from its Group Table. If the Remove All Groups command was received as unicast and a default response is requested, the device SHALL generate a Default Response command with the Status field set to SUCCESS and SHALL transmit it back to the originator of the Remove All Groups command.
""",
    "Add Group If Identifying": """
If the device is unable to store the contents of the Group Name field, the Group Name field MAY be ignored.

On receipt of the Add Group If Identifying command, the device SHALL perform the following procedure:

1. The device verifies that it is currently identifying itself. If the device it not currently identifying itself, the Add Group If Identifying command was received as unicast and a default response is requested, the device SHALL generate a Default Response command with the Status field set to SUCCESS and SHALL transmit it back to the originator of the Add Group If Identifying command. If the device it not currently identifying itself and the Add Group If Identifying command was not received as unicast, no further processing SHALL be performed.

2. The device verifies that the Group ID field contains a valid group identifier in the range 0x0001 0xfff7. If the Group ID field contains a group identifier outside this range, the status SHALL be INVALID_VALUE and the device continues from step 6.

3. The device verifies that it does not already have an entry in its Group Table that corresponds to the value of the Group ID field. If it already has the requested entry in its Group Table, the status SHALL be SUCCESS and the device continues from step 6.

4. The device verifies that it has free entries in its Group Table. If the device has no free entries in its Group Table, the status SHALL be INSUFFICIENT_SPACE and the device continues from step 6.

5. The device adds the values of the Group ID and Group Name (if supported) fields to its Group Table and the status SHALL be SUCCESS.

6. If the Add Group If Identifying command was received as unicast and the evaluated status is not SUCCESS, the device SHALL generate a Default Response command with the Status field set to the evaluated status and SHALL transmit it back to the originator of the Add Group If Identifying command.

No response is defined as this command is EXPECTED to be multicast or broadcast.

If the command is unicast, with the Disable Default Response bit not set, and there is no error (or the endpoint is not identifying), then there SHALL be a Default Response with a Status of SUCCESS.
"""
},
    "Identify": {
    "Identify": """
On receipt of this command, the device SHALL set the IdentifyTime attribute to the value of the Identify Time field. This then starts, continues, or stops the device's identification procedure as detailed in 3.5.2.2.1.
""",
    "Identify Query": """
On receipt of this command, if the device is currently identifying itself then it SHALL generate an appropriate Identify Query Response command, see 3.5.2.4.1 and unicast it to the requestor.
If the device is not currently identifying itself it SHALL take no further action.
""",
    "Trigger Effect": """
On receipt of this command, the device SHALL execute the trigger effect indicated in the Effect Identifier and Effect Variant fields.
If the Effect Variant field specifies a variant that is not supported on the device, it SHALL execute the default variant.
"""
},
    "Scenes": {
        "Add Scene": """
On receipt of the Add Scene command, the device SHALL perform the following procedure:

1. The device verifies that the Group ID field contains a valid group identifier in the range 0x0000 0xfff7. If the Group ID field contains a group identifier outside this range, the status SHALL be INVALID_VALUE and the device continues from step 5.

2. If the value of the Group ID field is non-zero, the device verifies that it corresponds to an entry in its Group Table. If there is no such entry in its Group Table, the status SHALL be INVALID_FIELD and the device continues from step 5.

3. The device verifies that it has free entries in its Scene Table. If the device has no further free entries in its Scene Table, the status SHALL be INSUFFICIENT_SPACE and the device continues from step 5.

4. The device adds the scene entry into its Scene Table with fields copied from the Add Scene command payload and the status SHALL be SUCCESS. If there is already a scene in the Scene Table with the same Scene ID and Group ID, it SHALL overwrite it.

5. If the Add Scene command was received as a unicast, the device SHALL then generate an Add Scene Response command with the Status field set to the evaluated status and SHALL transmit it back to the originator of the Add Scene command.
""",
        "View Scene": """
On receipt of the View Scene command, the device SHALL perform the following procedure:

1. The device verifies that the Group ID field contains a valid group identifier in the range 0x0000 0xfff7. If the Group ID field contains a group identifier outside this range, the status SHALL be INVALID_VALUE and the device continues from step 5.

2. If the value of the Group ID field is non-zero, the device verifies that it corresponds to an entry in its Group Table. If there is no such entry in its Group Table, the status SHALL be INVALID_FIELD and the device continues from step 5.

3. The device verifies that the scene entry corresponding to the Group ID and Scene ID fields exists in its Scene Table. If there is no such entry in its Scene Table, the status SHALL be NOT_FOUND and the device continues from step 5.

4. The device retrieves the requested scene entry from its Scene Table and the status SHALL be SUCCESS.

5. If the View Scene command was received as a unicast, the device SHALL then generate a View Scene Response command with the retrieved scene entry and the Status field set to the evaluated status and SHALL transmit it back to the originator of the View Scene command.
""",
        "Remove Scene": """
On receipt of the Remove Scene command, the device SHALL perform the following procedure:

1. The device verifies that the Group ID field contains a valid group identifier in the range 0x0000 0xfff7. If the Group ID field contains a group identifier outside this range, the status SHALL be INVALID_VALUE and the device continues from step 5.

2. If the value of the Group ID field is non-zero, the device verifies that it corresponds to an entry in its Group Table. If there is no such entry in its Group Table, the status SHALL be INVALID_FIELD and the device continues from step 5.

3. The device verifies that the scene entry corresponding to the Group ID and Scene ID fields exists in its Scene Table. If there is no such entry in its Scene Table, the status SHALL be NOT_FOUND and the device continues from step 5.

4. The device removes the requested scene entry from its Scene Table and the status SHALL be SUCCESS.

5. If the Remove Scene command was received as a unicast, the device SHALL then generate a Remove Scene Response command with the Status field set to the evaluated status and SHALL transmit it back to the originator of the Remove Scene command.
""",
        "Remove All Scenes": """
On receipt of the Remove All Scenes command, the device SHALL perform the following procedure:

1. The device verifies that the Group ID field contains a valid group identifier in the range 0x0000 0xfff7. If the Group ID field contains a group identifier outside this range, the status SHALL be INVALID_VALUE and the device continues from step 4.

2. If the value of the Group ID field is non-zero, the device verifies that it corresponds to an entry in its Group Table. If there is no such entry in its Group Table, the status SHALL be INVALID_FIELD and the device continues from step 4.

3. The device SHALL remove all scenes, corresponding to the value of the Group ID field, from its Scene Table and the status SHALL be SUCCESS.

4. If the Remove All Scenes command was received as a unicast, the device SHALL then generate a Remove All Scenes Response command with the Status field set to the evaluated status and SHALL transmit it back to the originator of the Remove All Scenes command.
""",
        "Store Scene": """
On receipt of the Store Scene command, the device SHALL perform the following procedure:

1. The device verifies that the Group ID field contains a valid group identifier in the range 0x0000 0xfff7. If the Group ID field contains a group identifier outside this range, the status SHALL be INVALID_VALUE and the device continues from step 5.

2. If the value of the Group ID field is non-zero, the device verifies that it corresponds to an entry in its Group Table. If there is no such entry in its Group Table, the status SHALL be INVALID_FIELD and the device continues from step 5.

3. The device verifies that it has free entries in its Scene Table. If the device has no further free entries in its Scene Table, the status SHALL be INSUFFICIENT_SPACE and the device continues from step 5.

4. The device adds the scene entry into its Scene Table along with all extension field sets corresponding to the current state of other clusters on the same endpoint on the device and the Transition Time and Scene Name entries set to 0 and the null string, respectively. If there is already a scene in the Scene Table with the same Scene ID and Group ID, it SHALL overwrite it, i.e., it SHALL first remove all information included in the original scene entry except for the Transition Time and Scene Name entries, which are left unaltered. The status SHALL be SUCCESS.

5. If the Store Scene command was received as a unicast, the device SHALL then generate a Store Scene Response command with the Status field set to the evaluated status and SHALL transmit it back to the originator of the Store Scene command.

Note that if a scene to be stored requires a transition time field and/ or a scene name field, these must be set up by a prior Add Scene command, e.g., with no scene extension field sets.

If the Group ID field is not zero, and the device is not a member of this group, the scene will not be added.
""",
        "Recall Scene": """
On receipt of the Recall Scene command, the device SHALL perform the following procedure:

1. The device verifies that the Group ID field contains a valid group identifier in the range 0x0000 0xfff7. If the Group ID field contains a group identifier outside this range, the status SHALL be INVALID_VALUE and the device continues from step 5.

2. If the value of the Group ID field is non-zero, the device verifies that it corresponds to an entry in its Group Table. If there is no such entry in its Group Table, the status SHALL be INVALID_FIELD and the device continues from step 5.

3. The device verifies that the scene entry corresponding to the Group ID and Scene ID fields exists in its Scene Table. If there is no such entry in its Scene Table, the status SHALL be NOT_FOUND and the device continues from step 5.

4. The device retrieves the requested scene entry from its Scene Table. For each other cluster on the device, it SHALL retrieve any corresponding extension fields from the Scene Table and set the attributes and corresponding state of the cluster accordingly. If there is no extension field set for a cluster, the state of that cluster SHALL remain unchanged. If an extension field set omits the values of any trailing attributes, the values of these attributes SHALL remain unchanged.

5. This command does not result in a corresponding response command unless:

the command is unicast, and an error occurs during its processing, a Default Response SHALL be generated with the Status code set to the error status.

OR

the command is unicast, no error occurs, and a Default Response is requested, a Default Response command SHALL be generated with the Status code field set to SUCCESS.38 

If the Transition Time field is present in the command payload and its value is not equal to 0xffff, this field SHALL indicate the transition time in 1/10ths of a second. In all other cases (command payload field not present or value equal to 0xffff), the scene transition time field of the Scene Table entry SHALL indicate the transition time. The transition time determines how long the transition takes from the old cluster state to the new cluster state. It is recommended that, where possible (e.g., it is not possible for attributes with Boolean data type), a gradual transition SHOULD take place from the old to the new state over this time. However, the exact transition is manufacturer dependent.
""",
        "Get Scene Membership": """
On receipt of the Get Scene Membership command, the device SHALL perform the following procedure:

1. The device verifies that the Group ID field contains a valid group identifier in the range 0x0000 0xfff7. If the Group ID field contains a group identifier outside this range, the status SHALL be INVALID_VALUE and the device continues from step 3.

2. If the value of the Group ID field is non-zero, the device verifies that it corresponds to an entry in its Group Table. If there is no such entry in its Group Table, the status SHALL be INVALID_FIELD and the device continues from step 3.

3. If the Get Scene Membership command was received as a unicast, the device SHALL then generate a Get Scene Membership Response command with the Status field set to the evaluated status and SHALL transmit it back to the originator of the Get Scene Membership command. If the Get Scene Membership command was not received as a unicast, the device SHALL only generate a Get Scene Membership Response command with the Status field set to the evaluated status if an entry within the Scene Table corresponds to the Group ID; the device SHALL then transmit it back to the originator of the Get Scene Membership command
""",
        "Enhanced Add Scene": """
On receipt of the Enhanced Add Scene command, the device SHALL perform the following procedure:

1. The device verifies that the Group ID field contains a valid group identifier in the range 0x0000 0xfff7. If the Group ID field contains a group identifier outside this range, the status SHALL be INVALID_VALUE and the device continues from step 5.

2. If the value of the Group ID field is non-zero, the device verifies that it corresponds to an entry in its Group Table. If there is no such entry in its Group Table, the status SHALL be INVALID_FIELD and the device continues from step 5.

3. The device verifies that it has free entries in its Scene Table. If the device has no further free entries in its Scene Table, the status SHALL be INSUFFICIENT_SPACE and the device continues from step 5.

4. The device adds the scene entry into its Scene Table with fields copied from the Enhanced Add Scene command payload and the status SHALL be SUCCESS. If there is already a scene in the Scene Table with the same Scene ID and Group ID, it SHALL overwrite it, i.e., it SHALL first remove all information included in the original scene entry. The Transition Time (measured in tenths of a second) SHALL be separated into whole seconds for the standard Transition Time field of the scene table entry and the new TransitionTime100ms field, as specified.

5. If the Enhanced Add Scene command was received as a unicast, the device SHALL then generate an Enhanced Add Scene Response command with the Status field set to the evaluated status and SHALL transmit it back to the originator of the Enhanced Add Scene command.
""",
        "Enhanced View Scene": """
On receipt of the Enhanced View Scene command, the device SHALL perform the following procedure:

1. The device verifies that the Group ID field contains a valid group identifier in the range 0x0000 0xfff7. If the Group ID field contains a group identifier outside this range, the status SHALL be INVALID_VALUE and the device continues from step 5.

2. If the value of the Group ID field is non-zero, the device verifies that it corresponds to an entry in its Group Table. If there is no such entry in its Group Table, the status SHALL be INVALID_FIELD and the device continues from step 5.

3. The device verifies that the scene entry corresponding to the Group ID and Scene ID fields exists in its Scene Table. If there is no such entry in its Scene Table, the status SHALL be NOT_FOUND and the device continues from step 5.

4. The device retrieves the requested scene entry from its Scene Table and the status SHALL be SUCCESS.

5. If the Enhanced View Scene command was received as a unicast, the device SHALL then generate an Enhanced View Scene Response command with the Status field set to the evaluated status and SHALL transmit it back to the originator of the Enhanced View Scene command.
""",
        "Copy Scene": """
On receipt of the Copy Scene command, the device SHALL perform the following procedure:

1. The device verifies that the Group Identifier From and Group Identifier To fields contain a valid group identifier in the range 0x0000 – 0xfff7. If either the Group Identifier From field or the Group Identifier To field contains a group identifier outside this range, the status SHALL be INVALID_VALUE and the device continues from step 6.

2. If the value of either the Group Identifier From field or the Group Identifier To field is non-zero, the device verifies that it corresponds to an entry in its Group Table. If there is no such entry in its Group Table, the status SHALL be INVALID_FIELD and the device continues from step 6.

3. The device verifies that the scene entry corresponding to the Group Identifier From and Scene Identifier From fields exists in its Scene Table. If there is no such entry in its Scene Table, the status SHALL be NOT_FOUND and the device continues from step 6.

4. If the Copy All Scenes sub-field of the Mode field is set to 1 or the scene entry corresponding to the Group Identifier To and Scene Identifier To fields does not exist in the scene table and if the device has no further free entries in its Scene Table, the status SHALL be INSUFFICIENT_SPACE and the device continues from step 6.

5. The status SHALL be SUCCESS. If the Copy All Scenes sub-field of the Mode field is set to 1, the device SHALL copy all its available scenes with group identifier equal to the Group Identifier From field under the group identifier specified in the Group Identifier To field, leaving the scene identifiers the same. In this case, the Scene Identifier From and Scene Identifier To fields are ignored. If the Copy All Scenes sub-field of the Mode field is set to 0, the device SHALL copy the scene table entry corresponding to the Group Identifier From and Scene Identifier From fields to the scene table entry corresponding to the Group Identifier To and Scene Identifier To fields. If a scene already exists under the same group/scene identifier pair, it SHALL be overwritten.

6. If the Copy Scene command was received as a unicast, the device SHALL then generate a Copy Scene Response command with the Status field set to the evaluated status and SHALL transmit it back to the originator of the Copy Scene command.
"""
    },
    "OnOff": {
        "Off": """
On receipt of this command, a device SHALL enter its 'Off' state. This state is device dependent, but it is recommended that it is used for power off or similar functions.
On receipt of the Off command, the OnTime attribute SHALL be set to 0x0000.
""",
        "On": """
On receipt of this command, a device SHALL enter its 'On' state. This state is device dependent, but it is recommended that it is used for power on or similar functions.
On receipt of the On command, if the value of the OnTime attribute is equal to 0x0000, the device SHALL set the OffWaitTime attribute to 0x0000.
""",
        "Toggle": """
On receipt of this command, if a device is in its 'Off' state it SHALL enter its 'On' state.
Otherwise, if it is in its 'On' state it SHALL enter its 'Off' state.
On receipt of the Toggle command, if the value of the OnOff attribute is equal to 0x00 and if the value of the OnTime attribute is equal to 0x0000, the device SHALL set the OffWaitTime attribute to 0x0000.
If the value of the OnOff attribute is equal to 0x01, the OnTime attribute SHALL be set to 0x0000.
""",
        "Off With Effect": """
On receipt of the Off With Effect command and if the GlobalSceneControl attribute is equal to TRUE, the application on the associated endpoint SHALL store its settings in its global scene then set the GlobalSceneControl attribute to FALSE.
The application SHALL then enter its “off” state, update the OnOff attribute accordingly and set the OnTime attribute to 0x0000.
In all other cases, the application on the associated endpoint SHALL enter its “off” state and update the OnOff attribute accordingly.
""",
        "On With Recall Global Scene": """
On receipt of the On With Recall Global Scene command, if the GlobalSceneControl attribute is equal to TRUE, the application on the associated endpoint SHALL discard the command.

If the GlobalSceneControl attribute is equal to FALSE, the application on the associated endpoint SHALL recall its global scene, entering the appropriate state and updating the OnOff attribute accordingly. It SHALL then set the GlobalSceneControl attribute to TRUE.
If the value of the OnTime attribute is equal to 0x0000, the device SHALL then set the OffWaitTime attribute to 0x0000.
""",
        "On With Timed Off": """
On receipt of this command, if the accept only when on sub-field of the on/off control field is set to 1and the value of the OnOff attribute is equal to 0x00 (off), the command SHALL be discarded.

If the value of the OffWaitTime attribute is greater than zero and the value of the OnOff attribute is equal to 0x00, then the device SHALL set the OffWaitTime attribute to the minimum of the OffWaitTime attribute and the value specified in the off wait time field.

In all other cases, the device SHALL set the OnTime attribute to the maximum of the OnTime attribute and the value specified in the on time field, set the OffWaitTime attribute to the value specified in the off wait time field and set the OnOff attribute to 0x01 (on).

If the values of the OnTime and OffWaitTime attributes are both less than 0xffff, the device SHALL then update the device every 1/10 th second until both the OnTime and OffWaitTime attributes are equal to 0x0000, as follows:

If the value of the OnOff attribute is equal to 0x01 (on) and the value of the OnTime attribute is greater than zero, the device SHALL decrement the value of the OnTime attribute. If the value of the OnTime attribute reaches 0x0000, the device SHALL set the OffWaitTime and OnOff attributes to 0x0000 and 0x00, respectively.
If the value of the OnOff attribute is equal to 0x00 (off) and the value of the OffWaitTime attribute is greater than zero, the device SHALL decrement the value of the OffWaitTime attribute. If the value of the OffWaitTime attribute reaches 0x0000, the device SHALL terminate the update.
""",
    },
    "Level": {
        "Move to Level": """
The OptionsMask & OptionsOverride fields SHALL both be present53 . Default values are provided to interpret missing fields from legacy devices. A temporary Options bitmap SHALL be created from the Options attribute, using the OptionsMask & OptionsOverride fields. Each bit of the temporary Options bitmap SHALL be determined as follows:

Each bit in the Options attribute SHALL determine the corresponding bit in the temporary Options bitmap, unless the OptionsMask field is present and has the corresponding bit set to 1, in which case the corresponding bit in the OptionsOverride field SHALL determine the corresponding bit in the temporary Options bitmap.

The resulting temporary Options bitmap SHALL then be processed as defined in section 3.10.2.2.854 .

On receipt of this command, a device SHALL move from its current level to the value given in the Level field. The meaning of 'level' is device dependent - e.g., for a light it MAY mean brightness level.

The movement SHALL be as continuous as technically practical, i.e., not a step function, and the time taken to move to the new level SHALL be equal to the value of the Transition time field, in tenths of a second, or as close to this as the device is able.

If the Transition time field takes the value 0xffff then the time taken to move to the new level SHALL instead be determined by the OnOffTransitionTime attribute. If OnOffTransitionTime, which is an optional attribute, is not present, the device SHALL move to its new level as fast as it is able.

If the device is not able to move at a variable rate, the Transition time field MAY be disregarded.
""",
        "Move": """
On receipt of this command, a device SHALL first create and process a temporary Options bitmap as described in section 3.10.2.3.1.2.

On receipt of this command, a device SHALL move from its current level in an up or down direction in a continuous fashion, as detailed in Table 3-61.
Table 3-61 Actions on Receipt for Move Command
Fade Mode Action on Receipt
Up Increase the device's level at the rate given in the Rate field. If the level reaches the maximum allowed for the device, stop.
Down Decrease the device's level at the rate given in the Rate field. If the level reaches the minimum allowed for the device, stop.
""",
        "Step": """
On receipt of this command, a device SHALL first create and process a temporary Options bitmap as described in section 3.10.2.3.1.2.
On receipt of this command, a device SHALL move from its current level in an up or down direction as detailed in Table 3-63.
Fade Mode Action on Receipt
Up Increase CurrentLevel by 'Step size' units, or until it reaches the maximum level allowed for the device if this reached in the process. In the latter case, the transition time SHALL be proportionally reduced
Down Decrease CurrentLevel by 'Step size' units, or until it reaches the minimum level allowed for the device if this reached in the process. In the latter case, the transition time SHALL be proportionally reduced.
""",
        "Stop": """
On receipt of this command, a device SHALL first create and process a temporary Options bitmap as described in section 3.10.2.3.1.2.

Upon receipt of this command, any Move to Level, Move or Step command (and their 'with On/Off' variants) currently in process SHALL be terminated.
The value of CurrentLevel SHALL be left at its value upon receipt of the Stop command, and RemainingTime SHALL be set to zero.
""",
        "Move to Closest Frequency": """
Upon receipt of this command, the device shall change its current frequency to the requested frequency, or to the closest frequency that it can generate.
If the device cannot approximate the frequency, then it shall return a default response with an error code of INVALID_VALUE.
Determining if a requested frequency can be approximated by a supported frequency is a manufacturer-specific decision.
"""
    },
    "Color": {
        "Move to Hue": """
On receipt of this command, a device SHALL also set the ColorMode attribute to the value 0x00 and then SHALL move from its current hue to the value given in the Hue field.

The movement SHALL be continuous, i.e., not a step function, and the time taken to move to the new hue SHALL be equal to the Transition Time field.

As hue is effectively measured on a circle, the new hue MAY be moved to in either direction. The direction of hue change is given by the Direction field.
If Direction is 'Shortest distance', the direction is taken that involves the shortest path round the circle. This case corresponds to expected normal usage.
If Direction is 'Longest distance', the direction is taken that involves the longest path round the circle. This case can be used for 'rainbow effects'.
In both cases, if both distances are the same, the Up direction SHALL be taken.
""",
        "Move Hue": """
On receipt of this command, a device SHALL set the ColorMode attribute to the value 0x00 and SHALL then move from its current hue in an up or down direction in a continuous fashion, as detailed in Table 5.16.
Table 5.16
Fade Mode Action on Receipt
Stop If moving, stop, else ignore the command (i.e., the command is accepted but has no effect). NB This MAY also be used to stop a Move to Hue command, a Move to Saturation command, or a Move to Hue and Saturation command.
Up Increase the device's hue at the rate given in the Rate field. If the hue reaches the maximum allowed for the device, then proceed to its minimum allowed value.
Down Decrease the device's hue at the rate given in the Rate field. If the hue reaches the minimum allowed for the device, then proceed to its maximum allowed value.
""",
        "Step Hue": """
On receipt of this command, a device SHALL set the ColorMode attribute to the value 0x00 and SHALL then move from its current hue in an up or down direction by one step, as detailed in Table 5.18.
Fade Mode Action on Receipt
Up Increase the device's hue by one step, in a continuous fashion. If the hue value reaches the maximum value then proceed to the minimum allowed value
Down Decrease the device's hue by one step, in a continuous fashion. If the hue value reaches the minimum value then proceed to the maximum allowed value.
""",
        "Move to Saturation": """
On receipt of this command, a device set the ColorMode attribute to the value 0x00 and SHALL then move from its current saturation to the value given in the Saturation field.

The movement SHALL be continuous, i.e., not a step function, and the time taken to move to the new saturation SHALL be equal to the Transition Time field, in 1/10ths of a second.
""",
        "Move Saturation": """
On receipt of this command, a device SHALL set the ColorMode attribute to the value 0x00 and SHALL then move from its current saturation in an up or down direction in a continuous fashion, as detailed in Table 5.20.
Table 5.20
Fade Mode Action on Receipt
Stop If moving, stop, else ignore the command (i.e., the command is accepted but has no affect). NB This MAY also be used to stop a Move to Saturation command, a Move to Hue command, or a Move to Hue and Saturation command.
Up Increase the device's saturation at the rate given in the Rate field. If the saturation reaches the maximum allowed for the device, stop.
Down Decrease the device's saturation at the rate given in the Rate field. If the saturation reaches the minimum allowed for the device, stop.
""",
        "Step Saturation": """
On receipt of this command, a device SHALL set the ColorMode attribute to the value 0x00 and SHALL then move from its current saturation in an up or down direction by one step, as detailed in Table 5.22.
Table 5.22
Step Mode Action on Receipt
Up Increase the device's saturation by one step, in a continuous fashion. However, if the saturation value is already the maximum value then do nothing.
Down Decrease the device's saturation by one step, in a continuous fashion. However, if the saturation value is already the minimum value then do nothing.
""",
        "Move to Hue and Saturation": """
On receipt of this command, a device SHALL set the ColorMode attribute to the value 0x00 and SHALL then move from its current hue and saturation to the values given in the Hue and Saturation fields.

The movement SHALL be continuous, i.e., not a step function, and the time taken to move to the new color SHALL be equal to the Transition Time field, in 1/10ths of a second.

The path through color space taken during the transition is not specified, but it is recommended that the shortest path is taken though hue/saturation space, i.e., movement is 'in a straight line' across the hue/saturation disk.
""",
        "Move to Color": """
On receipt of this command, a device SHALL set the value of the ColorMode attribute, where implemented, to 0x01, and SHALL then move from its current color to the color given in the ColorX and ColorY fields.

The movement SHALL be continuous, i.e., not a step function, and the time taken to move to the new color SHALL be equal to the Transition Time field, in 1/10ths of a second.

The path through color space taken during the transition is not specified, but it is recommended that the shortest path is taken though color space, i.e., movement is 'in a straight line' across the CIE xyY Color Space.
""",
        "Move Color": """
On receipt of this command, a device SHALL set the value of the ColorMode attribute, where implemented, to 0x01, and SHALL then move from its current color in a continuous fashion according to the rates specified.
This movement SHALL continue until the target color for the next step cannot be implemented on this device.

If both the RateX and RateY fields contain a value of zero, no movement SHALL be carried out, and the command execution SHALL have no effect other than stopping the operation of any previously received command of this cluster.
This command can thus be used to stop the operation of any other command of this cluster.
""",
        "Step Color": """
On receipt of this command, a device SHALL set the value of the ColorMode attribute, where implemented, to 0x01, and SHALL then move from its current color by the color step indicated.

The movement SHALL be continuous, i.e., not a step function, and the time taken to move to the new color SHALL be equal to the Transition Time field, in 1/10ths of a second.

The path through color space taken during the transition is not specified, but it is recommended that the shortest path is taken though color space, i.e., movement is 'in a straight line' across the CIE xyY Color Space. Note also that if the required step is larger than can be represented by signed 16-bit integers then more than one step command SHOULD be issued.
""",
        "Move to Color Temperature": """
On receipt of this command, a device SHALL set the value of the ColorMode attribute, where implemented, to 0x02, and SHALL then move from its current color to the color given by the Color Temperature Mireds field.

The movement SHALL be continuous, i.e., not a step function, and the time taken to move to the new color SHALL be equal to the Transition Time field, in 1/10ths of a second.

By definition of this color mode, the path through color space taken during the transition is along the 'Black Body Line'.
""",
        "Enhanced Move to Hue": """
On receipt of this command, a device SHALL set the ColorMode attribute to 0x00 and set the EnhancedColorMode attribute to the value 0x03. The device SHALL then move from its current enhanced hue to the value given in the Enhanced Hue field.

The movement SHALL be continuous, i.e., not a step function, and the time taken to move to the new enhanced hue SHALL be equal to the Transition Time field.
""",
        "Enhanced Move Hue": """
On receipt of this command, a device SHALL set the ColorMode attribute to 0x00 and set the EnhancedColorMode attribute to the value 0x03. The device SHALL then move from its current enhanced hue in an up or down direction in a continuous fashion, as detailed in Table 5.23.
Table 5.23
Move Mode Action on Receipt
Stop If moving, stop, else ignore the command (i.e., the command is accepted but has no effect). NB This MAY also be used to stop an Enhanced Move to Hue command or an enhanced Move to Hue and Saturation command.
Up Increase the device's enhanced hue at the rate given in the Rate field. If the enhanced hue reaches the maximum allowed for the device, proceed to its minimum allowed value.
Down Decrease the device's enhanced hue at the rate given in the Rate field. If the hue reaches the minimum allowed for the device, proceed to its maximum allowed value.
""",
        "Enhanced Step Hue": """
On receipt of this command, a device SHALL set the ColorMode attribute to 0x00 and the EnhancedColorMode attribute to the value 0x03. The device SHALL then move from its current enhanced hue in an up or down direction by one step, as detailed in Table 5.24.

Table 5.24. Actions on Receipt for the Enhanced Step Hue Command

Move Mode

Action on Receipt

Up

Increase the device’s enhanced hue by one step. If the enhanced hue reaches the maximum allowed for the device, proceed to its minimum allowed value.

Down

Decrease the device’s enhanced hue by one step. If the hue reaches the minimum allowed for the device, proceed to its maximum allowed value.
""",
        "Color Loop Set": """
On receipt of this command, the device SHALL first update its color loop attributes according to the value of the Update Flags field, as follows.
If the Update Direction sub-field is set to 1, the device SHALL set the ColorLoopDirection attribute to the value of the Direction field.
If the Update Time sub-field is set to 1, the device SHALL set the ColorLoopTime attribute to the value of the Time field.
If the Update Start Hue subfield is set to 1, the device SHALL set the ColorLoopStartEnhancedHue attribute to the value of the Start Hue field.
If the color loop is active (and stays active), the device SHALL immediately react on updates of the ColorLoopDirection and ColorLoopTime attributes.

If the Update Action sub-field of the Update Flags field is set to 1, the device SHALL adhere to the action specified in the Action field, as follows.
If the value of the Action field is set to 0x00 and the color loop is active, i.e. the ColorLoopActive attribute is set to 0x01, the device SHALL de-active the color loop, set the ColorLoopActive attribute to 0x00 and set the EnhancedCurrentHue attribute to the value of the ColorLoopStoredEnhancedHue attribute.
If the value of the Action field is set to 0x00 and the color loop is inactive, i.e. the ColorLoopActive attribute is set to 0x00, the device SHALL ignore the action update component of the command.
If the value of the action field is set to 0x01, the device SHALL set the ColorLoopStoredEnhancedHue attribute to the value of the EnhancedCurrentHue attribute, set the ColorLoopActive attribute to 0x01 and activate the color loop, starting from the value of the ColorLoopStartEnhancedHue attribute.
If the value of the Action field is set to 0x02, the device SHALL set the ColorLoopStoredEnhancedHue attribute to the value of the EnhancedCurrentHue attribute, set the ColorLoopActive attribute to 0x01 and activate the color loop, starting from the value of the EnhancedCurrentHue attribute.
If the color loop is active, the device SHALL cycle over the complete range of values of the EnhancedCurrentHue attribute in the direction of the ColorLoopDirection attribute over the time specified in the ColorLoopTime attribute. The level of increments/decrements is application specific.
""",
        "Stop Move Step": """
Upon receipt of this command, any Move to, Move or Step command currently in process SHALL be terminated.
The values of the CurrentHue, EnhancedCurrentHue and CurrentSaturation attributes SHALL be left at their present value upon receipt of the Stop Move Step command, and the RemainingTime attribute SHALL be set to zero.
"""
    },
    "Alarms": {
        "Reset Alarm": """
This command resets all alarms. Any alarm conditions that were in fact still active will cause a new notification to be generated and, where implemented, a new record added to the alarm log.
""",
        "Get Alarm": """
This command causes the alarm with the earliest generated alarm entry in the alarm table to be reported in a get alarm response command 3.11.2.5.2.
This command enables the reading of logged alarm conditions from the alarm table.
Once an alarm condition has been reported the corresponding entry in the table is removed.
This command does not have a payload.
""",
        "Reset Alarm Log": """
This command causes the alarm table to be cleared, and does not have a payload.
"""
    },
    "DoorLock": {
        "Lock Door": """
This command causes the lock device to lock the door.
As of HA 1.2, this command includes an optional code for the lock.
The door lock MAY require a PIN depending on the value of the [Require PIN for RF Operation attribute].
""",
        "Unlock Door": """
This command causes the lock device to unlock the door.
As of HA 1.2, this command includes an optional code for the lock.
The door lock MAY require a code depending on the value of the [Require PIN for RF Operation attribute].
""",
        "Toggle": """
Request the status of the lock.
As of HA 1.2, this command includes an optional code for the lock.
The door lock MAY require a code depending on the value of the [Require PIN for RF Operation attribute].
""",
        "Unlock with Timeout": """
This command causes the lock device to unlock the door with a timeout parameter.
After the time in seconds specified in the timeout field, the lock device will relock itself automatically.
This timeout parameter is only temporary for this message transition only and overrides the default relock time as specified in the [Auto Relock Time attribute] attribute.
If the door lock device is not capable of or does not want to support temporary Relock Timeout, it SHOULD not support this optional command.
""",
        "Get Log Record": """
Request a log record.
Log number is between 1 - [Number of Log Records Supported attribute]. If log number 0 is requested then the most recent log entry is returned.
""",
        "Set PIN Code": """
Set a PIN into the lock.
User ID is between 0 - [# of PIN Users Supported attribute].
Only the values 1 (Occupied/Enabled) and 3 (Occupied/Disabled) are allowed for User Status.
""",
        "Get PIN Code": """
Retrieve a PIN Code. User ID is between 0 - [# of PIN Users Supported attribute].
""",
        "Clear PIN Code": """
Delete a PIN. User ID is between 0 - [# of PIN Users Supported attribute].
If you delete a PIN Code and this user didn't have a RFID Code, the user status is set to "0 Available", the user type is set to the default value and all schedules are also set to the default values.
""",
        "Clear All PIN Codes": """
Clear out all PINs on the lock.
On the server, the clear all PIN codes command SHOULD have the same effect as the Clear PIN Code command with respect to the setting of user status, user type and schedules.
""",
        "Set User Status": """
Set the status of a user ID. User Status value of 0x00 is not allowed.
In order to clear a user id, the Clear ID Command SHALL be used.
For user status value please refer to User Status Value.
""",
        "Get User Status": """
Get the status of a user.
""",
        "Set Week Day Schedule": """
Set a weekly repeating schedule for a specified user.
Schedule ID: number is between 0 - [# of Week Day Schedules Per User attribute].
User ID: is between 0 - [# of Total Users Supported attribute].
Days mask is listed as bitmask for flexibility to set same schedule across multiple days.
For the door lock that does not support setting schedule across multiple days within one command, it SHOULD respond with ZCL INVALID_FIELD (0x85) status when received the set schedule command days bitmask field has multiple days selected.
Start Hour: in decimal format represented by 0x00 - 0x17 (00 to 23 hours).
Start Minute: in decimal format represented by 0x00 - 0x3B (00 to 59 mins).
End Hour: in decimal format represented by 0x00 - 0x17 (00 to 23 hours). End Hour SHALL be equal or greater than Start Hour.
End Minute: in decimal format represented by 0x00 - 0x3B (00 to 59 mins).
If End Hour is equal with Start Hour, End Minute SHALL be greater than Start Minute.
When the Server Device receives the command, the Server Device MAY change the user type to the specific schedule user type.
""",
        "Get Week Day Schedule": """
Retrieve the specific weekly schedule for the specific user.
""",
        "Clear Week Day Schedule": """
Clear the specific weekly schedule for the specific user.
""",
        "Set Year Day Schedule": """
Set a time-specific schedule ID for a specified user.
Schedule ID number is between 0 - [# of Year Day Schedules Supported Per User attribute]. User ID is between 0 – [# of Total Users Supported attribute].
Start time and end time are given in LocalTime. End time must be greater than the start time.
When the Server Device receives the command, the Server Device MAY change the user type to the specific schedule user type. Please refer to Process for Creating a New User with Schedule at the beginning of this cluster.
""",
        "Get Year Day Schedule": """
Retrieve the specific year day schedule for the specific user.
""",
        "Clear Year Day Schedule": """
Clears the specific year day schedule for the specific user.
""",
        "Set Holiday Schedule": """
Set the holiday Schedule by specifying local start time and local end time with respect to any Lock Operating Mode.
Holiday Schedule ID number is between 0 - [# of Holiday Schedules Supported attribute].
Start time and end time are given in LocalTime.
End time must be greater than the start time.
Operating Mode is valid enumeration value as listed in operating mode attribute.
""",
        "Get Holiday Schedule": """
Get the holiday Schedule by specifying Holiday ID.
""",
        "Clear Holiday Schedule": """
Clear the holiday Schedule by specifying Holiday ID.
""",
        "Set User Type": """
Set the type byte for a specified user.
For user type value please refer to User Type Value.
""",
        "Get User Type": """
Retrieve the type byte for a specific user.
""",
        "Set RFID Code": """
Set an ID for RFID access into the lock.
User ID: Between 0 - [# of RFID Users Supported attribute]. Only the values 1 (Occupied/Enabled) and 3 (Occupied/Disabled) are allowed for User Status.

User Status: Used to indicate what the status is for a specific user ID. The values are according to “Set PIN” while not all are supported.
User Type: The values are the same as used for “Set PIN Code.”
""",
        "Get RFID Code": """
Retrieve an ID. User ID is between 0 - [# of RFID Users Supported attribute].
""",
        "Clear RFID Code": """
Delete an ID.
User ID is between 0 - [# of RFID Users Supported attribute].
If you delete a RFID code and this user didn't have a PIN code, the user status has to be set to "0 Available", the user type has to be set to the default value, and all schedules which are supported have to be set to the default values.
""",
        "Clear All RFID Codes": """
Clear out all RFIDs on the lock.
If you delete all RFID codes and this user didn't have a PIN code, the user status has to be set to "0 Available", the user type has to be set to the default value, and all schedules which are supported have to be set to the default values.
"""
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

