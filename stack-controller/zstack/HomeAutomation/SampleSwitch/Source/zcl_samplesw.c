/**************************************************************************************************
  Filename:       zcl_samplesw.c
  Revised:        $Date: 2015-08-19 17:11:00 -0700 (Wed, 19 Aug 2015) $
  Revision:       $Revision: 44460 $

  Description:    Zigbee Cluster Library - sample switch application.


  Copyright 2006-2013 Texas Instruments Incorporated. All rights reserved.

  IMPORTANT: Your use of this Software is limited to those specific rights
  granted under the terms of a software license agreement between the user
  who downloaded the software, his/her employer (which must be your employer)
  and Texas Instruments Incorporated (the "License").  You may not use this
  Software unless you agree to abide by the terms of the License. The License
  limits your use, and you acknowledge, that the Software may not be modified,
  copied or distributed unless embedded on a Texas Instruments microcontroller
  or used solely and exclusively in conjunction with a Texas Instruments radio
  frequency transceiver, which is integrated into your product.  Other than for
  the foregoing purpose, you may not use, reproduce, copy, prepare derivative
  works of, modify, distribute, perform, display or sell this Software and/or
  its documentation for any purpose.

  YOU FURTHER ACKNOWLEDGE AND AGREE THAT THE SOFTWARE AND DOCUMENTATION ARE
  PROVIDED �AS IS� WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED,
  INCLUDING WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY, TITLE,
  NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT SHALL
  TEXAS INSTRUMENTS OR ITS LICENSORS BE LIABLE OR OBLIGATED UNDER CONTRACT,
  NEGLIGENCE, STRICT LIABILITY, CONTRIBUTION, BREACH OF WARRANTY, OR OTHER
  LEGAL EQUITABLE THEORY ANY DIRECT OR INDIRECT DAMAGES OR EXPENSES
  INCLUDING BUT NOT LIMITED TO ANY INCIDENTAL, SPECIAL, INDIRECT, PUNITIVE
  OR CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA, COST OF PROCUREMENT
  OF SUBSTITUTE GOODS, TECHNOLOGY, SERVICES, OR ANY CLAIMS BY THIRD PARTIES
  (INCLUDING BUT NOT LIMITED TO ANY DEFENSE THEREOF), OR OTHER SIMILAR COSTS.

  Should you have any questions regarding your right to use this Software,
  contact Texas Instruments Incorporated at www.TI.com.
**************************************************************************************************/

/*********************************************************************
  This application implements a ZigBee On/Off Switch, based on Z-Stack 3.0.

  This application is based on the common sample-application user interface. Please see the main
  comment in zcl_sampleapp_ui.c. The rest of this comment describes only the content specific for
  this sample applicetion.
  
  Application-specific UI peripherals being used:

  - none (LED1 is currently unused by this application).

  Application-specific menu system:

    <TOGGLE LIGHT> Send an On, Off or Toggle command targeting appropriate devices from the binding table.
      Pressing / releasing [OK] will have the following functionality, depending on the value of the 
      zclSampleSw_OnOffSwitchActions attribute:
      - OnOffSwitchActions == 0: pressing [OK] will send ON command, releasing it will send OFF command;
      - OnOffSwitchActions == 1: pressing [OK] will send OFF command, releasing it will send ON command;
      - OnOffSwitchActions == 2: pressing [OK] will send TOGGLE command, releasing it will not send any command.

*********************************************************************/

#if ! defined ZCL_ON_OFF
#error ZCL_ON_OFF must be defined for this project.
#endif

/*********************************************************************
 * INCLUDES
 */
#include "ZComDef.h"
#include "OSAL.h"
#include "OSAL_Memory.h"
#include "nwk_util.h"
#include "AF.h"
#include "ZDApp.h"
#include "ZDObject.h"
#include "ZDProfile.h"
#include "MT_SYS.h"
#include "AddrMgr.h"
#include "OSAL_Timers.h"

#include "zcl.h"
#include "zcl_general.h"
#include "zcl_closures.h"
#include "zcl_ha.h"
#include "zcl_poll_control.h"
#include "zcl_samplesw.h"
#include "zcl_diagnostic.h"

#include "onboard.h"

/* HAL */
//#include "hal_lcd.h"
#include "hal_led.h"
#include "hal_key.h"
//#include "hal_adc.h"

#include <stdio.h>

#if defined (OTA_CLIENT) && (OTA_CLIENT == TRUE)
#include "zcl_ota.h"
#include "hal_ota.h"
#endif

#include "bdb.h"
#include "bdb_interface.h"

//#include <stdio.h>

/*********************************************************************
 * MACROS
 */

#define APP_TITLE "TI Sample Switch"

/*********************************************************************
 * TYPEDEFS
 */

/*********************************************************************
 * GLOBAL VARIABLES
 */
byte zclSampleSw_TaskID;
uint8 zclSampleSwSeqNum;
uint8 zclSampleSw_OnOffSwitchType = ON_OFF_SWITCH_TYPE_MOMENTARY;
uint8 zclSampleSw_OnOffSwitchActions;
static uint8 af_transferId = 0;
static uint8 zcl_transferId = 0;

/*********************************************************************
 * GLOBAL FUNCTIONS
 */

/*********************************************************************
 * LOCAL VARIABLES
 */
afAddrType_t zclSampleSw_DstAddr;

// Endpoint to allow SYS_APP_MSGs
static endPointDesc_t sampleSw_HAEp =
{
  SAMPLESW_HA_ENDPOINT,                  // endpoint
  0,
  &zclSampleSw_TaskID,
  &zclSampleSw_HASimpleDesc,
  //(SimpleDescriptionFormat_t *)NULL,  // No Simple description for this test endpoint
  (afNetworkLatencyReq_t)0            // No Network Latency req
};

static endPointDesc_t sampleSw_ZLLEp =
{
  SAMPLESW_ZLL_ENDPOINT,                  // endpoint
  0,
  &zclSampleSw_TaskID,
  &zclSampleSw_ZLLSimpleDesc,
  //(SimpleDescriptionFormat_t *)NULL,  // No Simple description for this test endpoint
  (afNetworkLatencyReq_t)0            // No Network Latency req
};

static endPointDesc_t sampleSw_GPEp =
{
  SAMPLESW_GP_ENDPOINT,                  // endpoint
  0,
  &zclSampleSw_TaskID,
  &zclSampleSw_GPSimpleDesc,
  //(SimpleDescriptionFormat_t *)NULL,  // No Simple description for this test endpoint
  (afNetworkLatencyReq_t)0            // No Network Latency req
};

//static uint8 aProcessCmd[] = { 1, 0, 0, 0 }; // used for reset command, { length + cmd0 + cmd1 + data }

devStates_t zclSampleSw_NwkState = DEV_INIT;

#if defined (OTA_CLIENT) && (OTA_CLIENT == TRUE)
#define DEVICE_POLL_RATE                 8000   // Poll rate for end device
#endif

#define SAMPLESW_TOGGLE_TEST_EVT   0x1000
/*********************************************************************
 * LOCAL FUNCTIONS
 */
static void zclSampleSw_HandleKeys( byte shift, byte keys );
static void zclSampleSw_BasicResetCB( void );
ZStatus_t zclSampleSw_handleDoorLockRsp(zclIncoming_t *pInMsg, uint8 status);
static void zclSampleSw_handleGroupRsp(zclGroupRsp_t* zclGroupRsp);
static void zclSampleSw_handleSceneRsp(zclSceneRsp_t* zclSceneRsp);
static void zclSampleSw_handleIdentifyQueryRsp(zclIdentifyQueryRsp_t* zclIdentifyRsp);

static void zclSampleSw_ProcessCommissioningStatus(bdbCommissioningModeMsg_t *bdbCommissioningModeMsg);

// Functions to process ZCL Foundation incoming Command/Response messages
static void zclSampleSw_ProcessIncomingMsg( zclIncomingMsg_t *msg );
static uint8 zclSampleSw_ProcessInReadRspCmd( zclIncomingMsg_t *pInMsg );
static uint8 zclSampleSw_ProcessInWriteRspCmd( zclIncomingMsg_t *pInMsg );
static uint8 zclSampleSw_ProcessInConfigReportRspCmd( zclIncomingMsg_t *pInMsg );
static uint8 zclSampleSw_ProcessInDefaultRspCmd( zclIncomingMsg_t *pInMsg );
#ifdef ZCL_DISCOVER
static uint8 zclSampleSw_ProcessInDiscCmdsRspCmd( zclIncomingMsg_t *pInMsg );
static uint8 zclSampleSw_ProcessInDiscAttrsRspCmd( zclIncomingMsg_t *pInMsg );
static uint8 zclSampleSw_ProcessInDiscAttrsExtRspCmd( zclIncomingMsg_t *pInMsg );
#endif

#if defined (OTA_CLIENT) && (OTA_CLIENT == TRUE)
static void zclSampleSw_ProcessOTAMsgs( zclOTA_CallbackMsg_t* pMsg );
#endif

#define ZCLSAMPLESW_UART_BUF_LEN        64
#define SHORT_SYMBOL_LEN                32

static void zclSampleSw_InitUart(void);
static void zclSampleSw_UartCB(uint8 port, uint8 event);

//static int parse_uart_elements(char input[], char output[][SHORT_SYMBOL_LEN]);
//static void hexStr_2_Bytes(uint8* dest, char* str, int length);
static afStatus_t inject_afData(uint16 destNwkAddr, uint8 flag, uint16 ep, uint16 cid, uint16 pid, uint8 len, uint8 *data);
static afStatus_t inject_zclData(uint16 destNwkAddr, uint8 flag, uint16 ep, uint16 cid, uint16 pid, uint8 cmd, uint8 clusterSpecific, uint16 manuCode, uint16 len, uint8* cmdFormat);
static void zclSampleSw_ProcessZDOMsgs(zdoIncomingMsg_t *pMsg);
static uint8 zclSampleSw_ProcessUartMsgs( uint8 *uartMsg, uint8 msgLen);
static uint8 locate_ep_given_profile(uint16 profileId);

static uint8 current_cmd_type = 0;
static uint8 endpoint_cmd_rx = 0;
static uint8 node_cmd_rx = 0;
static uint8 cluster_cmd_rx = 0;
static uint8 rx_zcl_cmd_id = 0;

/*********************************************************************
 * CONSTANTS
 */

/*********************************************************************
 * REFERENCED EXTERNALS
 */
extern int16 zdpExternalStateTaskID;

/*********************************************************************
 * ZCL General Profile Callback table
 */
static zclGeneral_AppCallbacks_t zclSampleSw_CmdCallbacks =
{
  NULL,               // Basic Cluster Reset command
  NULL,                                   // Identify Trigger Effect command
  NULL,                                   // On/Off cluster commands
  NULL,                                   // On/Off cluster enhanced command Off with Effect
  NULL,                                   // On/Off cluster enhanced command On with Recall Global Scene
  NULL,                                   // On/Off cluster enhanced command On with Timed Off
#ifdef ZCL_LEVEL_CTRL
  NULL,                                   // Level Control Move to Level command
  NULL,                                   // Level Control Move command
  NULL,                                   // Level Control Step command
  NULL,                                   // Level Control Stop command
#endif
  zclSampleSw_handleGroupRsp,                                   // Group Response commands
  zclSampleSw_handleSceneRsp,                                   // Scene Response command
#ifdef ZCL_SCENES
  NULL,                                   // Scene Store Request command
  NULL,                                   // Scene Recall Request command
#endif
#ifdef ZCL_ALARMS
  NULL,                                   // Alarm (Response) commands
#endif
#ifdef SE_UK_EXT
  NULL,                                   // Get Event Log command
  NULL,                                   // Publish Event Log command
#endif
  NULL,                                   // RSSI Location command
  NULL,                                   // RSSI Location Response command
  zclSampleSw_handleIdentifyQueryRsp      // ZCL Identify Query Response Command
};

static zclClosures_DoorLockAppCallbacks_t zclSampleSw_ClosureCmdCallbacks = 
{
  zclSampleSw_handleDoorLockRsp
};

/*********************************************************************
 * @fn          zclSampleSw_Init
 *
 * @brief       Initialization function for the zclGeneral layer.
 *
 * @param       none
 *
 * @return      none
 */
void zclSampleSw_Init( byte task_id )
{
  zclSampleSw_TaskID = task_id;

  // Set destination address to indirect
  zclSampleSw_DstAddr.addrMode = (afAddrMode_t)AddrNotPresent;
  zclSampleSw_DstAddr.endPoint = 0;
  zclSampleSw_DstAddr.addr.shortAddr = 0;

  // Register the Simple Descriptor for this application
  bdb_RegisterSimpleDescriptor( &zclSampleSw_HASimpleDesc );
  bdb_RegisterSimpleDescriptor( &zclSampleSw_ZLLSimpleDesc );
  bdb_RegisterSimpleDescriptor( &zclSampleSw_GPSimpleDesc );

  // Register the ZCL General Cluster Library callback functions
  zclGeneral_RegisterCmdCallbacks( sampleSw_HAEp.endPoint, &zclSampleSw_CmdCallbacks );
  zclGeneral_RegisterCmdCallbacks( sampleSw_ZLLEp.endPoint, &zclSampleSw_CmdCallbacks );
  zclGeneral_RegisterCmdCallbacks( sampleSw_GPEp.endPoint, &zclSampleSw_CmdCallbacks );
  zclClosures_RegisterDoorLockCmdCallbacks(sampleSw_HAEp.endPoint, &zclSampleSw_ClosureCmdCallbacks);
  zclClosures_RegisterDoorLockCmdCallbacks(sampleSw_ZLLEp.endPoint, &zclSampleSw_ClosureCmdCallbacks);
  zclClosures_RegisterDoorLockCmdCallbacks( sampleSw_GPEp.endPoint, &zclSampleSw_ClosureCmdCallbacks);

  zclSampleSw_ResetAttributesToDefaultValues();
  
  // Register the application's attribute list
  // zcl_registerAttrList( SAMPLESW_ENDPOINT, zclSampleSw_NumAttributes, zclSampleSw_Attrs );

  // Register the Application to receive the unprocessed Foundation command/response messages
  zcl_registerForMsg( zclSampleSw_TaskID );
  
  // Register for all key events - This app will handle all key events
  RegisterForKeys( zclSampleSw_TaskID );
  
  bdb_RegisterCommissioningStatusCB( zclSampleSw_ProcessCommissioningStatus );

  // Register for a test endpoint
  afRegister( &sampleSw_HAEp );
  afRegister( &sampleSw_ZLLEp);
  afRegister( &sampleSw_GPEp);
  
#ifdef ZCL_DIAGNOSTIC
  // Register the application's callback function to read/write attribute data.
  // This is only required when the attribute data format is unknown to ZCL.
  zcl_registerReadWriteCB( SAMPLESW_ENDPOINT, zclDiagnostic_ReadWriteAttrCB, NULL );

  if ( zclDiagnostic_InitStats() == ZSuccess )
  {
    // Here the user could start the timer to save Diagnostics to NV
  }
#endif

  zdpExternalStateTaskID = zclSampleSw_TaskID;

  // Form the network and initiate the coordinator
  bdb_StartCommissioning(BDB_COMMISSIONING_MODE_NWK_FORMATION | BDB_COMMISSIONING_MODE_FINDING_BINDING);

  // Init HAL and Uart
  zclSampleSw_InitUart();
  /**
   * JC NOTES: Register a list of ZDO messages
   * Device_annce: Would like to know when any new devices join the network.
   * Active endpoint response: Would like to know which active endpoints the target device has.
   * Simple Descriptor response: Would like to know which clusters are running on the given endpoint.
  **/
  ZDO_RegisterForZDOMsg(task_id, Node_Desc_rsp);
  ZDO_RegisterForZDOMsg(task_id, Active_EP_rsp);
  ZDO_RegisterForZDOMsg(task_id, Simple_Desc_rsp);

}

/*********************************************************************
 * @fn          zclSample_event_loop
 *
 * @brief       Event Loop Processor for zclGeneral.
 *
 * @param       none
 *
 * @return      none
 */
uint16 zclSampleSw_event_loop( uint8 task_id, uint16 events )
{
  afIncomingMSGPacket_t *MSGpkt;
  (void)task_id;  // Intentionally unreferenced parameter
  
  if ( events & SYS_EVENT_MSG )
  {
    while ( (MSGpkt = (afIncomingMSGPacket_t *)osal_msg_receive( zclSampleSw_TaskID )) )
    {
      switch ( MSGpkt->hdr.event )
      {
        case ZDO_CB_MSG:
        {
          // Incomming ZDO messages which the application subscribed to (By ZDO_RegisterForZDOMsg)
          zclSampleSw_ProcessZDOMsgs((zdoIncomingMsg_t *)MSGpkt);
          break;
        }
        case ZCL_INCOMING_MSG:
        {
          // Incoming ZCL Foundation command/response messages
          zclSampleSw_ProcessIncomingMsg((zclIncomingMsg_t *)MSGpkt);
          break;
        }
        case KEY_CHANGE:
        {
          zclSampleSw_HandleKeys( ((keyChange_t *)MSGpkt)->state, ((keyChange_t *)MSGpkt)->keys );
          break;
        }
        case ZDO_STATE_CHANGE:
        {
          break;
        }
        default:
        {
          break;
        }
      }

      // Release the memory
      osal_msg_deallocate( (uint8 *)MSGpkt );
    }

    // return unprocessed events
    return (events ^ SYS_EVENT_MSG);
  }

  // When activation Event timeout SAMPLEAPP_ACT_TIMEOUT reaches
  if ( events & SAMPLEAPP_ACT_EVT )
  {
    uint16 rsps[2] = {0}; uint8 length = 0;
    rsps[length++] = current_cmd_type;
    rsps[length++] = ERR_CMD_TIMEOUT;
    HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
    return ( events ^ SAMPLEAPP_ACT_EVT );
  }
  
  // Rejoin
#ifdef ZDO_COORDINATOR
#else
  if ( events & SAMPLEAPP_REJOIN_EVT )
  {
   bdb_StartCommissioning(BDB_COMMISSIONING_MODE_NWK_STEERING |
                      BDB_COMMISSIONING_MODE_FINDING_BINDING );
    
    return ( events ^ SAMPLEAPP_REJOIN_EVT );
  }
#endif
  
  // Discard unknown events
  return 0;
}

//static void hexStr_2_Bytes(uint8* dest, char* str, int length)
//{
//  int i, n;
//  for(i=0; i<length; i++)
//  {
//    sscanf(str+2*i, "%2X", &n);
//    dest[i] = (uint8)n;
//  }
//}

/*********************************************************************
 * @fn      zclSampleSw_ProcessZDOMsgs
 *
 * @brief   Called when this node receives a ZDO/ZDP response.
 *
 * @param   none
 *
 * @return  status
 */
static void zclSampleSw_ProcessZDOMsgs( zdoIncomingMsg_t *pMsg )
{
  if (AssocGetWithShort(pMsg->srcAddr.addr.shortAddr) != NULL)
  {
    if (pMsg->clusterID == Device_annce)
    {
      // Send back Device Announcement Info in format: [cmd, nwkAddr, extAddr, capabilities]
      ZDO_DeviceAnnce_t Annce;
      osal_memset(&Annce, 0, sizeof(ZDO_DeviceAnnce_t));
      ZDO_ParseDeviceAnnce(pMsg, &Annce);
    }
    else if (pMsg->clusterID == Node_Desc_rsp && node_cmd_rx)
    {
      // Stop the Timeout watchdog and check its status. If it hast not reached timeouts, do not send UART message back to fuzzer.
      if (osal_stop_timerEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT) != INVALID_EVENT_ID) {
        // Send back Node Descriptor response in format: [cmd, stat, nwkAddr, status, LogicalType, CapabilityFlag, ManufactuerCode]
        node_cmd_rx = 0;
        ZDO_NodeDescRsp_t pNDRsp;
        ZDO_ParseNodeDescRsp(pMsg, &pNDRsp);
        uint16 rsps[20] = {0}; uint8 length = 0;
        rsps[length++] = CMD_JC_NODEREQ;
        rsps[length++] = SUCCESS;
        rsps[length++] = pNDRsp.nwkAddr;
        rsps[length++] = pNDRsp.status;
        rsps[length++] = pNDRsp.nodeDesc.LogicalType;
        rsps[length++] = pNDRsp.nodeDesc.CapabilityFlags;
        rsps[length++] = BUILD_UINT16(pNDRsp.nodeDesc.ManufacturerCode[0], pNDRsp.nodeDesc.ManufacturerCode[1]);
        HalUARTWrite(HAL_UART_PORT_0,  (uint8 *)rsps, length*2);
      }
    }
    else if (pMsg->clusterID == Active_EP_rsp && endpoint_cmd_rx)
    {
        // Stop the Timeout watchdog and check its status. If it hast not reached timeouts, do not send UART message back to fuzzer.
        if (osal_stop_timerEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT) != INVALID_EVENT_ID) {
          // Send back Node Descriptor response in format: [cmd, nwkAddr, activeEP1, activeEP2,...]
          endpoint_cmd_rx = 0;
          uint16 rsps[20] = {0}; uint8 length = 0;
          ZDO_ActiveEndpointRsp_t *pRsp = ZDO_ParseEPListRsp( pMsg );
          rsps[length++] = CMD_JC_AEPREQ;
          rsps[length++] = SUCCESS;
          for(int i = 0; i < pRsp->cnt; i++)
          {
            rsps[length++] = pRsp->epList[i];
          }
          HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
        }
    }
    else if (pMsg->clusterID == Simple_Desc_rsp && cluster_cmd_rx)
    {
      // Stop the Timeout watchdog and check its status. If it hast not reached timeouts, do not send UART message back to fuzzer.
      if (osal_stop_timerEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT) != INVALID_EVENT_ID) {
        cluster_cmd_rx = 0;
        ZDO_SimpleDescRsp_t simpleDescRsp;
        osal_memset(&simpleDescRsp, 0, sizeof(ZDO_SimpleDescRsp_t));
        ZDO_ParseSimpleDescRsp(pMsg, &simpleDescRsp);
        zAddrType_t dstAddr;
        dstAddr.addr.shortAddr = simpleDescRsp.nwkAddr;
        dstAddr.addrMode = Addr16Bit;
        SimpleDescriptionFormat_t simpleDesc = simpleDescRsp.simpleDesc;

        // Send back Simple Descriptor response in format: [cmd, nwkAddr, endpoint, AppProfId, AppDeviceID, AppDevVer, cluster1, cluster2,...]
        uint16 answer[20] = {0}; uint8 length = 0;
        answer[length++] = CMD_JC_CLUREQ;
        answer[length++] = SUCCESS;
        answer[length++] = dstAddr.addr.shortAddr;
        answer[length++] = simpleDesc.EndPoint;
        answer[length++] = simpleDescRsp.status;
        if(simpleDesc.AppNumInClusters > 0)
        {
          answer[length++] = simpleDesc.AppProfId;
          answer[length++] = simpleDesc.AppDeviceId;
          answer[length++] = simpleDesc.AppDevVer;
          for (int i = 0; i < simpleDesc.AppNumInClusters; i++)
          {
            answer[length++] = simpleDesc.pAppInClusterList[i];
          }
        }
        HalUARTWrite(HAL_UART_PORT_0, (uint8 *)answer, length*2);
      }
    }
  }
  else
  {
    //printf("A ZDO message is received from device %X, but it is not in the association list!\n", pMsg->srcAddr.addr.shortAddr);
  }
}

/*********************************************************************
 * @fn      zclSampleSw_HandleKeys
 *
 * @brief   Handles all key events for this device.
 *
 * @param   shift - true if in shift/alt.
 * @param   keys - bit field for key events. Valid entries:
 *                 HAL_KEY_SW_5
 *                 HAL_KEY_SW_4
 *                 HAL_KEY_SW_2
 *                 HAL_KEY_SW_1
 *
 * @return  none
 */
static void zclSampleSw_HandleKeys( byte shift, byte keys )
{ 
  if(keys & HAL_KEY_SW_6)
  {
    uint8 readVal;
    static uint8 writeVal = 0;
    
    char readValStr[30];
    char writeValStr[30];
    
    // init USER_NV_TEST
    osal_nv_item_init(USER_NV_TEST, 1, NULL);
    
    // write
    sprintf(writeValStr, "Write: %d", writeVal);
    osal_nv_write( USER_NV_TEST, 0, 1, &writeVal );
    
    writeVal++;
    
    // read
    osal_nv_read( USER_NV_TEST, 0, 1, &readVal );
    sprintf(readValStr, "Read: %d", readVal);
    
    // lcd show
    //HalLcdWriteString(writeValStr, HAL_LCD_LINE_1);
    //HalLcdWriteString(readValStr,  HAL_LCD_LINE_2);
    
    // uart show
    HalUARTWrite(HAL_UART_PORT_0, (uint8 *)writeValStr, osal_strlen(writeValStr));
    HalUARTWrite(HAL_UART_PORT_0, "\r\n", 2);
    HalUARTWrite(HAL_UART_PORT_0, (uint8 *)readValStr, osal_strlen(readValStr));
    HalUARTWrite(HAL_UART_PORT_0, "\r\n", 2);
    
    // led indication
    HalLedSet(HAL_LED_1, HAL_LED_MODE_TOGGLE);
  }
}
  
/*********************************************************************
 * @fn      zclSampleSw_ProcessCommissioningStatus
 *
 * @brief   Callback in which the status of the commissioning process are reported
 *
 * @param   bdbCommissioningModeMsg - Context message of the status of a commissioning process
 *
 * @return  none
 */
static void zclSampleSw_ProcessCommissioningStatus(bdbCommissioningModeMsg_t *bdbCommissioningModeMsg)
{
  switch(bdbCommissioningModeMsg->bdbCommissioningMode)
  {
    case BDB_COMMISSIONING_FORMATION:
      if(bdbCommissioningModeMsg->bdbCommissioningStatus == BDB_COMMISSIONING_SUCCESS)
      {
        //After formation, perform nwk steering again plus the remaining commissioning modes that has not been processed yet
        bdb_StartCommissioning(BDB_COMMISSIONING_MODE_NWK_STEERING | bdbCommissioningModeMsg->bdbRemainingCommissioningModes);
        //printf("The BDB formation operation succeeds.\n");
      }
      else
      {
        //Want to try other channels?
        //try with bdb_setChannelAttribute
      }
    break;
    case BDB_COMMISSIONING_NWK_STEERING:
      if(bdbCommissioningModeMsg->bdbCommissioningStatus == BDB_COMMISSIONING_SUCCESS)
      {
        //YOUR JOB:
        //We are on the nwk, what now?
      }
      else
      {
        #ifdef ZDO_COORDINATOR
        #else
        osal_start_timerEx(zclSampleSw_TaskID, 
                           SAMPLEAPP_REJOIN_EVT, 
                           SAMPLEAPP_REJOIN_PERIOD);
        #endif
         
        //See the possible errors for nwk steering procedure
        //No suitable networks found
        //Want to try other channels?
        //try with bdb_setChannelAttribute
      }
    break;
    case BDB_COMMISSIONING_FINDING_BINDING:
      if(bdbCommissioningModeMsg->bdbCommissioningStatus == BDB_COMMISSIONING_SUCCESS)
      {
        //printf("[BDB finding and binding] Succeed.\n");
      }
      else if(bdbCommissioningModeMsg->bdbCommissioningStatus == BDB_COMMISSIONING_FB_NO_IDENTIFY_QUERY_RESPONSE)
      {
        //printf("[BDB finding and binding] No identify query response is identified.\n");
      }
      else if(bdbCommissioningModeMsg->bdbCommissioningStatus == BDB_COMMISSIONING_FAILURE)
      {
        //printf("[BDB finding and binding] Fail.");
      }
      else
      {
        //YOUR JOB:
        //retry?, wait for user interaction?
      }
    break;
    case BDB_COMMISSIONING_INITIALIZATION:
      //Initialization notification can only be successful. Failure on initialization 
      //only happens for ZED and is notified as BDB_COMMISSIONING_PARENT_LOST notification
      
      //YOUR JOB:
      //We are on a network, what now?
      
    break;
#if ZG_BUILD_ENDDEVICE_TYPE    
    case BDB_COMMISSIONING_PARENT_LOST:
      if(bdbCommissioningModeMsg->bdbCommissioningStatus == BDB_COMMISSIONING_NETWORK_RESTORED)
      {
        //We did recover from losing parent
      }
      else
      {
        //Parent not found, attempt to rejoin again after a fixed delay
        osal_start_timerEx(zclSampleSw_TaskID, SAMPLEAPP_END_DEVICE_REJOIN_EVT, SAMPLEAPP_END_DEVICE_REJOIN_DELAY);
      }
    break;
#endif 
  }
}

/*********************************************************************
 * @fn      zclSampleSw_BasicResetCB
 *
 * @brief   Callback from the ZCL General Cluster Library
 *          to set all the Basic Cluster attributes to  default values.
 *
 * @param   none
 *
 * @return  none
 */
static void zclSampleSw_BasicResetCB( void )
{
  zclSampleSw_ResetAttributesToDefaultValues();
}

ZStatus_t zclSampleSw_handleDoorLockRsp(zclIncoming_t *pInMsg, uint8 status)
{
  uint32 cur_tick_count = osal_get_timeoutEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT);
  uint32 elapsed_tick_count = SAMPLEAPP_ACT_TIMEOUT - cur_tick_count;

  if (osal_stop_timerEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT) != INVALID_EVENT_ID) {
    uint16 rsps[10] = {0}; uint8 length = 0;
    rsps[length++] = CMD_JC_ZCLREQ;
    rsps[length++] = SUCCESS;
    rsps[length++] = CMD_JC_ZCLREQ;
    rsps[length++] = status;
    rsps[length++] = (uint16)(elapsed_tick_count & 0xffff);
    rsps[length++] = (uint16)((elapsed_tick_count >> 16) & 0xffff);
    HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
  }
  return SUCCESS;
}

// JC NOTE: Implemented function for handling Group Response
/*********************************************************************
 * @fn      zclSampleSw_handleGroupRsp
 *
 * @brief   Callback from the ZCL General Cluster Library
 *          to handle ZCL Group Response.
 *          Callback logic:
 *          (1) In sampleswInit, we registered CmdCallbacks (encoding this function) under various endpoints.
 *          (2) When a ZCL Group Response comes, ZCL will call zclGeneral_ProcessInGroupsClient (Line 2039) to process the message, and return the zclGroupRsp_t result to the callback function.
 *          (3) Since we previously registered the callback function as this function, eventually this function gets called.
 *
 * @param   none
 *
 * @return  none
 */
static void zclSampleSw_handleGroupRsp(zclGroupRsp_t* zclGroupRsp)
{
  // Calculate the elpased time and stop the Timeout watchdog
  uint32 cur_tick_count = osal_get_timeoutEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT);
  uint32 elapsed_tick_count = SAMPLEAPP_ACT_TIMEOUT - cur_tick_count;

  if (osal_stop_timerEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT) != INVALID_EVENT_ID) {
    uint16 rsps[10] = {0}; uint8 length = 0;
    rsps[length++] = CMD_JC_ZCLREQ;
    rsps[length++] = SUCCESS;
    rsps[length++] = zclGroupRsp->cmdID;
    rsps[length++] = zclGroupRsp->status;
    rsps[length++] = (uint16)(elapsed_tick_count & 0xffff);
    rsps[length++] = (uint16)((elapsed_tick_count >> 16) & 0xffff);
    HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
  }
}

static void zclSampleSw_handleSceneRsp(zclSceneRsp_t* zclSceneRsp)
{
  // Calculate the elpased time and stop the Timeout watchdog
  uint32 cur_tick_count = osal_get_timeoutEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT);
  uint32 elapsed_tick_count = SAMPLEAPP_ACT_TIMEOUT - cur_tick_count;

  if (osal_stop_timerEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT) != INVALID_EVENT_ID) {
    uint16 rsps[10] = {0}; uint8 length = 0;
    rsps[length++] = CMD_JC_ZCLREQ;
    rsps[length++] = SUCCESS;
    rsps[length++] = zclSceneRsp->cmdID;
    rsps[length++] = zclSceneRsp->status;
    rsps[length++] = (uint16)(elapsed_tick_count & 0xffff);
    rsps[length++] = (uint16)((elapsed_tick_count >> 16) & 0xffff);
    HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
  }
}

static void zclSampleSw_handleIdentifyQueryRsp(zclIdentifyQueryRsp_t* zclIdentifyRsp)
{

  // Calculate the elpased time and stop the Timeout watchdog
  uint32 cur_tick_count = osal_get_timeoutEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT);
  uint32 elapsed_tick_count = SAMPLEAPP_ACT_TIMEOUT - cur_tick_count;

  if (osal_stop_timerEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT) != INVALID_EVENT_ID) {
    uint16 rsps[10] = {0}; uint8 length = 0;
    rsps[length++] = CMD_JC_ZCLREQ;
    rsps[length++] = SUCCESS;
    rsps[length++] = 0;
    rsps[length++] = SUCCESS;
    rsps[length++] = (uint16)(elapsed_tick_count & 0xffff);
    rsps[length++] = (uint16)((elapsed_tick_count >> 16) & 0xffff);
    HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
  }

}

/*********************************************************************
 * @fn      zclSampleSw_ProcessIncomingMsg
 *
 * @brief   Process ZCL Foundation incoming message
 *
 * @param   pInMsg - pointer to the received message
 *
 * @return  none
 */
static void zclSampleSw_ProcessIncomingMsg( zclIncomingMsg_t *pInMsg )
{
  switch ( pInMsg->zclHdr.commandID )
  {
    case ZCL_CMD_READ_RSP:
      zclSampleSw_ProcessInReadRspCmd( pInMsg );
      break;
    case ZCL_CMD_WRITE_RSP:
      zclSampleSw_ProcessInWriteRspCmd( pInMsg );
      break;
    // See ZCL Test Applicaiton (zcl_testapp.c) for sample code on Attribute Reporting
    case ZCL_CMD_CONFIG_REPORT:
      //zclSampleSw_ProcessInConfigReportCmd( pInMsg );
      break;

    case ZCL_CMD_CONFIG_REPORT_RSP:
      zclSampleSw_ProcessInConfigReportRspCmd( pInMsg );
      break;

    case ZCL_CMD_READ_REPORT_CFG:
      //zclSampleSw_ProcessInReadReportCfgCmd( pInMsg );
      break;

    case ZCL_CMD_READ_REPORT_CFG_RSP:
      //zclSampleSw_ProcessInReadReportCfgRspCmd( pInMsg );
      break;

    case ZCL_CMD_REPORT:
      //zclSampleSw_ProcessInReportCmd( pInMsg );
      break;
    case ZCL_CMD_DEFAULT_RSP:
      zclSampleSw_ProcessInDefaultRspCmd(pInMsg);
      break;
#ifdef ZCL_DISCOVER
    case ZCL_CMD_DISCOVER_CMDS_RECEIVED_RSP:
      zclSampleSw_ProcessInDiscCmdsRspCmd( pInMsg );
      break;

    case ZCL_CMD_DISCOVER_CMDS_GEN_RSP:
      zclSampleSw_ProcessInDiscCmdsRspCmd( pInMsg );
      break;

    case ZCL_CMD_DISCOVER_ATTRS_RSP:
      zclSampleSw_ProcessInDiscAttrsRspCmd( pInMsg );
      break;

    case ZCL_CMD_DISCOVER_ATTRS_EXT_RSP:
      zclSampleSw_ProcessInDiscAttrsExtRspCmd( pInMsg );
      break;
#endif
    default:
      break;
  }
  if (pInMsg->attrCmd)
    osal_mem_free( pInMsg->attrCmd );
}

/*********************************************************************
 * @fn      zclSampleSw_ProcessInReadRspCmd
 *
 * @brief   Process the "Profile" Read Response Command
 *
 * @param   pInMsg - incoming message to process
 *
 * @return  none
 */
static uint8 zclSampleSw_ProcessInReadRspCmd( zclIncomingMsg_t *pInMsg )
{
  zclReadRspCmd_t *readRspCmd;
  uint8 i;

  // Calculate the elpased time and stop the Timeout watchdog
  uint32 cur_tick_count = osal_get_timeoutEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT);
  uint32 elapsed_tick_count = SAMPLEAPP_ACT_TIMEOUT - cur_tick_count;

  // Stop the Timeout watchdog and check its status. If it has not reached timeouts, do not send UART message back to fuzzer.
  if (osal_stop_timerEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT) != INVALID_EVENT_ID) {
    readRspCmd = (zclReadRspCmd_t *)pInMsg->attrCmd;
    uint16 rsps[20] = {0}; uint8 length = 0;
    rsps[length++] = CMD_JC_ZCLREQ;
    rsps[length++] = SUCCESS;
    rsps[length++] = ZCL_CMD_READ_RSP; // This field is not necessary, which is kept just for uninformity of response UART message formats
    for (i = 0; i < readRspCmd->numAttr; i++) {
      rsps[length++] = readRspCmd->attrList[i].status;
    }
    rsps[length++] = (uint16)(elapsed_tick_count & 0xffff);
    rsps[length++] = (uint16)((elapsed_tick_count >> 16) & 0xffff);
    HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
  }

  return TRUE;
}

/*********************************************************************
 * @fn      zclSampleSw_ProcessInWriteRspCmd
 *
 * @brief   Process the "Profile" Write Response Command
 *
 * @param   pInMsg - incoming message to process
 *
 * @return  none
 */
static uint8 zclSampleSw_ProcessInWriteRspCmd( zclIncomingMsg_t *pInMsg )
{
  zclWriteRspCmd_t *writeRspCmd;
  uint8 i;

  // Calculate the elpased time and stop the Timeout watchdog
  uint32 cur_tick_count = osal_get_timeoutEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT);
  uint32 elapsed_tick_count = SAMPLEAPP_ACT_TIMEOUT - cur_tick_count;

  // Stop the Timeout watchdog and check its status. If it has not reached timeouts, do not send UART message back to fuzzer.
  if (osal_stop_timerEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT) != INVALID_EVENT_ID) {
    writeRspCmd = (zclWriteRspCmd_t *)pInMsg->attrCmd;
    uint16 rsps[20] = {0}; uint8 length = 0;
    rsps[length++] = CMD_JC_ZCLREQ;
    rsps[length++] = SUCCESS;
    rsps[length++] = ZCL_CMD_WRITE_RSP; // This field is not necessary, which is kept just for uninformity of response UART message formats
    for (i = 0; i < writeRspCmd->numAttr; i++) {
      rsps[length++] = writeRspCmd->attrList[i].status;
    }
    rsps[length++] = (uint16)(elapsed_tick_count & 0xffff);
    rsps[length++] = (uint16)((elapsed_tick_count >> 16) & 0xffff);
    HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
  }

  return TRUE;
}

/*********************************************************************
 * @fn      zclSampleSw_ProcessInConfigReportRspCmd
 *
 * @brief   Process the "Profile" Configure Reporting Response Command
 *
 * @param   pInMsg - incoming message to process
 *
 * @return  none
 */
static uint8 zclSampleSw_ProcessInConfigReportRspCmd( zclIncomingMsg_t *pInMsg )
{
  zclCfgReportRspCmd_t *cfgReportRspCmd;
  uint8 i;

  // Calculate the elpased time and stop the Timeout watchdog
  uint32 cur_tick_count = osal_get_timeoutEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT);
  uint32 elapsed_tick_count = SAMPLEAPP_ACT_TIMEOUT - cur_tick_count;

  // Stop the Timeout watchdog and check its status. If it has not reached timeouts, do not send UART message back to fuzzer.
  if (osal_stop_timerEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT) != INVALID_EVENT_ID) {
    cfgReportRspCmd = (zclCfgReportRspCmd_t *)pInMsg->attrCmd;
    uint16 rsps[20] = {0}; uint8 length = 0;
    rsps[length++] = CMD_JC_ZCLREQ;
    rsps[length++] = SUCCESS;
    rsps[length++] = ZCL_CMD_WRITE_RSP; // This field is not necessary, which is kept just for uninformity of response UART message formats
    for (i = 0; i < cfgReportRspCmd->numAttr; i++) {
      rsps[length++] = cfgReportRspCmd->attrList[i].status;
    }
    rsps[length++] = (uint16)(elapsed_tick_count & 0xffff);
    rsps[length++] = (uint16)((elapsed_tick_count >> 16) & 0xffff);
    HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
  }

  return TRUE;
}

/*********************************************************************
 * @fn      zclSampleSw_ProcessInDefaultRspCmd
 *
 * @brief   Process the "Profile" Default Response Command
 *
 * @param   pInMsg - incoming message to process
 *
 * @return  none
 */
static uint8 zclSampleSw_ProcessInDefaultRspCmd( zclIncomingMsg_t *pInMsg )
{
  zclDefaultRspCmd_t *defaultRspCmd = (zclDefaultRspCmd_t *)pInMsg->attrCmd;
  if (defaultRspCmd->commandID != rx_zcl_cmd_id) {
      // If the default response is not related with our injected ZCL command: Just skip it.
  }
  else {
      // Calculate the elpased time and stop the Timeout watchdog
      uint32 cur_tick_count = osal_get_timeoutEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT);
      uint32 elapsed_tick_count = SAMPLEAPP_ACT_TIMEOUT - cur_tick_count;
      // Stop the Timeout watchdog and check its status. If it has not reached timeouts, do not send UART message back to fuzzer.
      if (osal_stop_timerEx(zclSampleSw_TaskID, SAMPLEAPP_ACT_EVT) != INVALID_EVENT_ID) {
        // Generate the response
        // Device is notified of the Default Response command.
        uint16 rsps[20] = {0}; uint8 length = 0;
        rsps[length++] = CMD_JC_ZCLREQ;
        rsps[length++] = SUCCESS;
        rsps[length++] = defaultRspCmd->commandID;
        rsps[length++] = defaultRspCmd->statusCode;
        rsps[length++] = (uint16)(elapsed_tick_count & 0xffff);
        rsps[length++] = (uint16)((elapsed_tick_count >> 16) & 0xffff);
        HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
      }
  }
  return TRUE;
}

#ifdef ZCL_DISCOVER
/*********************************************************************
 * @fn      zclSampleSw_ProcessInDiscCmdsRspCmd
 *
 * @brief   Process the Discover Commands Response Command
 *
 * @param   pInMsg - incoming message to process
 *
 * @return  none
 */
static uint8 zclSampleSw_ProcessInDiscCmdsRspCmd( zclIncomingMsg_t *pInMsg )
{
  zclDiscoverCmdsCmdRsp_t *discoverRspCmd;
  uint8 i;

  discoverRspCmd = (zclDiscoverCmdsCmdRsp_t *)pInMsg->attrCmd;
  for ( i = 0; i < discoverRspCmd->numCmd; i++ )
  {
    // Device is notified of the result of its attribute discovery command.
  }

  return TRUE;
}

/*********************************************************************
 * @fn      zclSampleSw_ProcessInDiscAttrsRspCmd
 *
 * @brief   Process the "Profile" Discover Attributes Response Command
 *
 * @param   pInMsg - incoming message to process
 *
 * @return  none
 */
static uint8 zclSampleSw_ProcessInDiscAttrsRspCmd( zclIncomingMsg_t *pInMsg )
{
  zclDiscoverAttrsRspCmd_t *discoverRspCmd;
  uint8 i;

  discoverRspCmd = (zclDiscoverAttrsRspCmd_t *)pInMsg->attrCmd;
  for ( i = 0; i < discoverRspCmd->numAttr; i++ )
  {
    // Device is notified of the result of its attribute discovery command.
  }

  return TRUE;
}

/*********************************************************************
 * @fn      zclSampleSw_ProcessInDiscAttrsExtRspCmd
 *
 * @brief   Process the "Profile" Discover Attributes Extended Response Command
 *
 * @param   pInMsg - incoming message to process
 *
 * @return  none
 */
static uint8 zclSampleSw_ProcessInDiscAttrsExtRspCmd( zclIncomingMsg_t *pInMsg )
{
  zclDiscoverAttrsExtRsp_t *discoverRspCmd;
  uint8 i;

  discoverRspCmd = (zclDiscoverAttrsExtRsp_t *)pInMsg->attrCmd;
  for ( i = 0; i < discoverRspCmd->numAttr; i++ )
  {
    // Device is notified of the result of its attribute discovery command.
  }

  return TRUE;
}
#endif // ZCL_DISCOVER

/**
 * @fn      zclSampleSw_InitUart
 *
 * @brief   init. and open Uart
 */
static void zclSampleSw_InitUart(void)
{
  halUARTCfg_t uartConfig;

  /* UART Configuration */
  uartConfig.configured           = TRUE;
  uartConfig.baudRate             = HAL_UART_BR_115200;
  uartConfig.flowControl          = FALSE;
  uartConfig.flowControlThreshold = 0;
  uartConfig.rx.maxBufSize        = ZCLSAMPLESW_UART_BUF_LEN;
  uartConfig.tx.maxBufSize        = 0;
  uartConfig.idleTimeout          = 6;
  uartConfig.intEnable            = TRUE;
  uartConfig.callBackFunc         = zclSampleSw_UartCB;

  /* Start UART */
  HalUARTOpen(HAL_UART_PORT_0, &uartConfig);
}

/*********************************************************************
 * @fn      zclSampleSw_ProcessUartMsgs
 *
 * @brief   Called when this node receives a ZDO/ZDP response.
 *
 * @param   uint8 *uartMsg
 *
 * @return  status
 */
static uint8 zclSampleSw_ProcessUartMsgs( uint8 *uartMsg, uint8 msgLen)
{
  uint8 stat = SUCCESS;
  current_cmd_type = uartMsg[0];
  switch (uartMsg[0])
  {
    case CMD_JC_STEER:         // RX: (uint8)CMD_JC_STEER+(uint8)period  TX: [CMD_JC_STEER,stat]
    {
      stat = NLME_PermitJoiningRequest(uartMsg[1]);
      uint16 rsps[2] = {0}; uint8 length = 0;
      rsps[length++] = CMD_JC_STEER;
      rsps[length++] = stat;
      HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
      break;
    }
    case CMD_JC_LIST:         // RX: (uint8)CMD_JC_LIST   TX: [CMD_JC_LIST,Nwkaddr,nodeRelation]
    {
      uint16 n_asso = AssocCount(PARENT, CHILD_RFD) + AssocCount(PARENT, CHILD_RFD_RX_IDLE) +\
                      AssocCount(PARENT, CHILD_FFD) + AssocCount(PARENT, CHILD_FFD_RX_IDLE);
      
      uint16 rsps[10] = {0}; uint8 length = 0;
      rsps[length++] = CMD_JC_LIST;
      rsps[length++] = stat;
      for (uint16 i = 0; i < n_asso; i++)
      {
        rsps[length++] = AssociatedDevList[i].shortAddr;
        rsps[length++] = AssociatedDevList[i].nodeRelation;
      }
      HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
      break;
    }
    case CMD_JC_NODEREQ:         // RX: (uint8)CMD_JC_NODEREQ+(uint16)nwkAddr
    {
      node_cmd_rx = 1;
      zAddrType_t srcAddr;
      srcAddr.addr.shortAddr = BUILD_UINT16(uartMsg[1], uartMsg[2]);
      srcAddr.addrMode = Addr16Bit;
      stat = ZDP_NodeDescReq(&srcAddr, srcAddr.addr.shortAddr, 0);
      if (stat != afStatus_SUCCESS) {
        uint16 rsps[2] = {0}; uint8 length = 0;
        rsps[length++] = CMD_JC_NODEREQ;
        rsps[length++] = stat;
        HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
      }
      else {
        // The successfull UART response is generated in function
        // Set a timer for TIMEOUT detection
        osal_start_timerEx(zclSampleSw_TaskID, 
                           SAMPLEAPP_ACT_EVT, 
                           SAMPLEAPP_ACT_TIMEOUT);
      }
      break;
    }
    case CMD_JC_AEPREQ:         // RX: (uint8)CMD_JC_AEPREQ+(uint16)nwkAddr
    {
      endpoint_cmd_rx = 1;
      zAddrType_t srcAddr;
      srcAddr.addr.shortAddr = BUILD_UINT16(uartMsg[1], uartMsg[2]);
      srcAddr.addrMode = Addr16Bit;
      stat = ZDP_ActiveEPReq(&srcAddr, srcAddr.addr.shortAddr, 0);
      if (stat != afStatus_SUCCESS) {
        uint16 rsps[2] = {0}; uint8 length = 0;
        rsps[length++] = CMD_JC_AEPREQ;
        rsps[length++] = stat;
        HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
      }
      else {
        // The successfull UART response is generated in function
        // Set a timer for TIMEOUT detection
        osal_start_timerEx(zclSampleSw_TaskID, 
                           SAMPLEAPP_ACT_EVT, 
                           SAMPLEAPP_ACT_TIMEOUT);
      }
      break;
    }
    case CMD_JC_CLUREQ:         // RX: (uint8)CMD_JC_AEPREQ+(uint16)nwkAddr+(uint8)ep
    {
      cluster_cmd_rx = 1;
      zAddrType_t srcAddr;
      srcAddr.addr.shortAddr = BUILD_UINT16(uartMsg[1], uartMsg[2]);
      srcAddr.addrMode = Addr16Bit;
      stat = ZDP_SimpleDescReq(&srcAddr, srcAddr.addr.shortAddr, uartMsg[3], 0);
      if (stat != afStatus_SUCCESS) {
        uint16 rsps[2] = {0}; uint8 length = 0;
        rsps[length++] = CMD_JC_CLUREQ;
        rsps[length++] = stat;
        HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
      }
      else {
        // The successfull UART response is generated in function
        // Set a timer for TIMEOUT detection
        osal_start_timerEx(zclSampleSw_TaskID, 
                           SAMPLEAPP_ACT_EVT, 
                           SAMPLEAPP_ACT_TIMEOUT);
      }
      break;
    }
    case CMD_JC_CMDREQ:         // RX: (uint8)CMD_JC_CMDREQ+(uint16)nwkAddr+(uint8)flag+(uint8)ep+(uint16)cid+(uint16)pid+(uint8)len+(byte *)payload
    {
      uint16 nwkAddr = BUILD_UINT16(uartMsg[1], uartMsg[2]);
      uint8 flag = uartMsg[3];
      uint8 endpoint = uartMsg[4];
      uint16 cid = BUILD_UINT16(uartMsg[5], uartMsg[6]);
      uint16 pid = BUILD_UINT16(uartMsg[7], uartMsg[8]);
      uint8 len = uartMsg[9];
      uint8 *payload = osal_mem_alloc(len);
      for (int i = 1; i <= len; i++)
      {
        payload[len-i] = uartMsg[msgLen-i];
      }
      stat = inject_afData(nwkAddr, flag, endpoint, cid, pid, len, payload);
      osal_mem_free(payload);
      if (stat != afStatus_SUCCESS) {
        uint16 rsps[2] = {0}; uint8 length = 0;
        rsps[length++] = CMD_JC_CMDREQ;
        rsps[length++] = stat;
        HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
      }
      else {
        // The successfull UART response is generated in function
        // Set a timer for TIMEOUT detection
        osal_start_timerEx(zclSampleSw_TaskID, 
                           SAMPLEAPP_ACT_EVT, 
                           SAMPLEAPP_ACT_TIMEOUT);
      }
      break;
    }
    case CMD_JC_ZCLREQ:
    {
      uint16 nwkAddr = BUILD_UINT16(uartMsg[1], uartMsg[2]);
      uint8 flag = uartMsg[3];
      uint8 endpoint = uartMsg[4];
      uint16 cid = BUILD_UINT16(uartMsg[5], uartMsg[6]);

      uint16 pid = BUILD_UINT16(uartMsg[7], uartMsg[8]);
      //sampleSw_TestEp.simpleDesc->AppProfId = pid;
      uint8 cmd = uartMsg[9]; rx_zcl_cmd_id = cmd;
      uint8 clusterSpecific = uartMsg[10];
      uint16 manuCode = BUILD_UINT16(uartMsg[11], uartMsg[12]);
      uint8 monitor_response_flag = uartMsg[13];
      uint16 len = BUILD_UINT16(uartMsg[14], uartMsg[15]);
      uint8 *payload = NULL;
      if (len > 0)
      {
        payload = osal_mem_alloc(len);
        for (int i = 1; i <= len; i++)
        {
          payload[len-i] = uartMsg[msgLen-i];
        }
      }
      stat = inject_zclData(nwkAddr, flag, endpoint, cid, pid, cmd, clusterSpecific, manuCode, len, payload);
      if (len > 0)
      {
        osal_mem_free(payload);
      }
      if (stat != afStatus_SUCCESS)
      {
        uint16 rsps[2] = {0}; uint8 length = 0;
        rsps[length++] = CMD_JC_ZCLREQ;
        rsps[length++] = stat;
        HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
      }
      else {
        // The successfull UART response is generated in function
        // Set a timer for TIMEOUT detection
        // It really depends on whether the response is needed.
        // If not needed, the timer will not be set, and the coordinator will not send any UART response.
        if (monitor_response_flag > 0) {
          osal_start_timerEx(zclSampleSw_TaskID, 
                             SAMPLEAPP_ACT_EVT, 
                             SAMPLEAPP_ACT_TIMEOUT);
        }
      }
      break;
    }
    case CMD_JC_LEVREQ:
    {
      zAddrType_t srcAddr;
      srcAddr.addr.shortAddr = BUILD_UINT16(uartMsg[1], uartMsg[2]);
      srcAddr.addrMode = Addr16Bit;
      uint8 extAddr[8] = {0};
      stat = AddrMgrExtAddrLookup(srcAddr.addr.shortAddr, extAddr);
      if (stat == true)
      {
        stat = ZDP_MgmtLeaveReq(&srcAddr, extAddr, 0, 0, 0);
      }
      uint16 rsps[2] = {0}; uint8 length = 0;
      rsps[length++] = CMD_JC_LEVREQ;
      rsps[length++] = stat;
      HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
      break;
    }
    default:
    {
      uint16 rsps[2] = {0}; uint8 length = 0;
      rsps[length++] = uartMsg[0];
      rsps[length++] = ERR_CMD_NOTFOUND;
      HalUARTWrite(HAL_UART_PORT_0, (uint8 *)rsps, length*2);
      break;
    }
  }
  return stat;
}

/**
 * @fn      zclSampleSw_UartCB
 *
 * @brief   Uart Callback. When there are UART messages comming in, this callback function will handle the message.
 */
static void zclSampleSw_UartCB(uint8 port, uint8 event)
{
  uint8 rxLen = Hal_UART_RxBufLen(HAL_UART_PORT_0);
  if(rxLen != 0)
  {
    while (1)
    {
      halSleepWait(50000); // Wait for 50 ms
      if (rxLen == Hal_UART_RxBufLen(HAL_UART_PORT_0))
      {
        break;
      }
      else
      {
        rxLen = Hal_UART_RxBufLen(HAL_UART_PORT_0);
      }
    }
    uint8 *zclSampleSw_UartReadBuf = osal_mem_alloc(ZCLSAMPLESW_UART_BUF_LEN);
    if(zclSampleSw_UartReadBuf==NULL)
    {
      char *point = "[fail,memfail]";
      HalUARTWrite(HAL_UART_PORT_0, (uint8 *)point, osal_strlen(point));
    }
    else
    {
      osal_memset(zclSampleSw_UartReadBuf, 0, ZCLSAMPLESW_UART_BUF_LEN);
      HalUARTRead(HAL_UART_PORT_0, zclSampleSw_UartReadBuf, rxLen);
      zclSampleSw_ProcessUartMsgs(zclSampleSw_UartReadBuf, rxLen);
      osal_mem_free(zclSampleSw_UartReadBuf); zclSampleSw_UartReadBuf = NULL;
    }
  }
}

static afStatus_t inject_afData(uint16 destNwkAddr, uint8 flag, uint16 ep, uint16 cid, uint16 pid, uint8 len, uint8 *data)
{
/**
 * This function is responsible for injecting applicaiton-layer data (APS + ZCL)
 * Note 1: In order to successfully send AF data, destNwkAddr must exist in the association table.
 * Note 2: The profileID (e.g., ZHA or ZDO) is configured by changing sampleSw_TestEp variable. However, it is unknown if there is any side effect, as the variable has been registered before.
 * params
    * destNwkAddr: The target device address.
    * Flag: Determine whether the packet is broadcast, groupcast, or unicast
    * ep: Target endpoint number.
    * cid: Target cluster ID.
    * pid: The profile ID.
    * len: Length of the payload.
    * data: AF-layer payload.
**/
	afAddrType_t dstAddr;  
  //sampleSw_TestEp.simpleDesc->AppProfId = pid;

	/* Destination */
  if (flag==SAMPLEAPP_BROADCAST)
  {
    dstAddr.addrMode = afAddrBroadcast;
	  dstAddr.addr.shortAddr = 0xffff;
  }
  else if (flag==SAMPLEAPP_GROUPCAST)
  {
    dstAddr.addrMode = afAddrGroup;
    dstAddr.addr.shortAddr = destNwkAddr;
  }
  else if (flag==SAMPLEAPP_UNICAST)
  {
	  dstAddr.addrMode = afAddr16Bit;
	  dstAddr.addr.shortAddr = destNwkAddr;
  }
	dstAddr.endPoint = ep;
	af_transferId++;

	return AF_DataRequest(&dstAddr, 
		&sampleSw_HAEp,
		cid,    
		len, 
		data,    
		&af_transferId,
		AF_SKIP_ROUTING,
		AF_DEFAULT_RADIUS);
}

static afStatus_t inject_zclData(uint16 destNwkAddr, uint8 flag, uint16 ep, uint16 cid, uint16 pid, uint8 cmd, uint8 clusterSpecific, uint16 manuCode, uint16 len, uint8* cmdFormat)
{
/**
 * This function is responsible for injecting applicaiton-layer data (ZCL)
 * Note 1: In order to successfully send AF data, destNwkAddr must exist in the association table.
 * Note 2: The profileID (e.g., ZHA or ZDO) is configured by changing sampleSw_TestEp variable. However, it is unknown if there is any side effect, as the variable has been registered before.
 * params
    * destNwkAddr: The target device address.
    * Flag: Determine whether the packet is broadcast, groupcast, or unicast
    * ep: Target endpoint number.
    * cid: Target cluster ID.
**/
	afAddrType_t dstAddr;  

	/* Destination */
  if (flag==SAMPLEAPP_BROADCAST)
  {
    dstAddr.addrMode = afAddrBroadcast;
	  dstAddr.addr.shortAddr = 0xffff;
  }
  else if (flag==SAMPLEAPP_GROUPCAST)
  {
    dstAddr.addrMode = afAddrGroup;
    dstAddr.addr.shortAddr = destNwkAddr;
  }
  else if (flag==SAMPLEAPP_UNICAST)
  {
	  dstAddr.addrMode = afAddr16Bit;
	  dstAddr.addr.shortAddr = destNwkAddr;
  }
	dstAddr.endPoint = ep;
	zcl_transferId++;

  uint8 sep = locate_ep_given_profile(pid);

  ZStatus_t cmd_stat = zcl_SendCommand(sep,
    &dstAddr,
    cid,
    cmd,
    clusterSpecific,
    0,
    0,
    manuCode,
    zcl_transferId,
    len,
    cmdFormat);

  return cmd_stat;

}

static uint8 locate_ep_given_profile(uint16 profileId)
{
  uint8 ep = 0;
  switch (profileId)
  {
    case ZCL_HA_PROFILE_ID:
    {
      ep = SAMPLESW_HA_ENDPOINT;
      break;
    }
    case ZCL_ZLL_PROFILE_ID:
    {
      ep = SAMPLESW_ZLL_ENDPOINT;
      break;
    }
    case ZCL_GP_PROFILE_ID:
    {
      ep = SAMPLESW_GP_ENDPOINT;
      break;
    }
    default:
    {
      ep = 0;
      break;
    }
  }
  return ep;
}