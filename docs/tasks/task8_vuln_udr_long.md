# Task 8b — 5G Core Security Review: UDR Data Repository Handler (Full File)

**ID:** task8_vuln_udr_long  
**Tipo:** textual  
**Difficoltà:** alta

---

## Scenario

You are reviewing the main HTTP handler file for the **UDR (Unified Data Repository)** SBI layer in a 5G core network implementation. The file manages subscription data, policy data, application data, and exposure data for UEs. It is a large file — review it carefully for all security and correctness vulnerabilities.

```go
package sbi

import (
	"encoding/json"
	"net/http"
	"regexp"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"

	"github.com/free5gc/openapi"
	"github.com/free5gc/openapi/models"
	udr_context "github.com/free5gc/udr/internal/context"
	"github.com/free5gc/udr/internal/logger"
	"github.com/free5gc/udr/internal/util"
	"github.com/free5gc/util/metrics/sbi"
)

func (s *Server) getDataRepositoryRoutes() []Route {
	return []Route{
		{"Index", "GET", "/", Index},
		{"AmfContext3gpp", strings.ToUpper("Patch"), "/subscription-data/:ueId/:servingPlmnId/amf-3gpp-access", s.HandleAmfContext3gpp},
		{"CreateAmfContext3gpp", strings.ToUpper("Put"), "/subscription-data/:ueId/:servingPlmnId/amf-3gpp-access", s.HandleCreateAmfContext3gpp},
		{"QueryAmfContext3gpp", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/amf-3gpp-access", s.HandleQueryAmfContext3gpp},
		{"AmfContextNon3gpp", strings.ToUpper("Patch"), "/subscription-data/:ueId/:servingPlmnId/amf-non-3gpp-access", s.HandleAmfContextNon3gpp},
		{"CreateAmfContextNon3gpp", strings.ToUpper("Put"), "/subscription-data/:ueId/:servingPlmnId/amf-non-3gpp-access", s.HandleCreateAmfContextNon3gpp},
		{"QueryAmfContextNon3gpp", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/amf-non-3gpp-access", s.HandleQueryAmfContextNon3gpp},
		{"QueryAmData", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/provisioned-data/am-data", s.HandleQueryAmData},
		{"QueryAuthenticationStatus", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/authentication-status", s.HandleQueryAuthenticationStatus},
		{"CreateAuthenticationStatus", strings.ToUpper("Put"), "/subscription-data/:ueId/:servingPlmnId/authentication-status", s.HandleCreateAuthenticationStatus},
		{"ModifyAuthentication", strings.ToUpper("Patch"), "/subscription-data/:ueId/:servingPlmnId/authentication-subscription", s.HandleModifyAuthentication},
		{"QueryAuthSubsData", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/authentication-subscription", s.HandleQueryAuthSubsData},
		{"CreateAuthenticationSoR", strings.ToUpper("Put"), "/subscription-data/:ueId/:servingPlmnId/sor-data", s.HandleCreateAuthenticationSoR},
		{"QueryAuthSoR", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/sor-data", s.HandleQueryAuthSoR},
		{"ApplicationDataInfluenceDataGet", strings.ToUpper("Get"), "/application-data/influenceData", s.HandleApplicationDataInfluenceDataGet},
		{"ApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete", strings.ToUpper("Delete"), "/application-data/influenceData/:influenceId/:subscriptionId", s.HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete},
		{"ApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet", strings.ToUpper("Get"), "/application-data/influenceData/:influenceId/:subscriptionId", s.HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet},
		{"ApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut", strings.ToUpper("Put"), "/application-data/influenceData/:influenceId/:subscriptionId", s.HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut},
		{"ApplicationDataPfdsAppIdDelete", strings.ToUpper("Delete"), "/application-data/pfds/:appId", s.HandleApplicationDataPfdsAppIdDelete},
		{"ApplicationDataPfdsAppIdGet", strings.ToUpper("Get"), "/application-data/pfds/:appId", s.HandleApplicationDataPfdsAppIdGet},
		{"ApplicationDataPfdsAppIdPut", strings.ToUpper("Put"), "/application-data/pfds/:appId", s.HandleApplicationDataPfdsAppIdPut},
		{"ApplicationDataPfdsGet", strings.ToUpper("Get"), "/application-data/pfds", s.HandleApplicationDataPfdsGet},
		{"PolicyDataBdtDataBdtReferenceIdDelete", strings.ToUpper("Delete"), "/policy-data/bdt-data/:bdtReferenceId", s.HandlePolicyDataBdtDataBdtReferenceIdDelete},
		{"PolicyDataBdtDataBdtReferenceIdGet", strings.ToUpper("Get"), "/policy-data/bdt-data/:bdtReferenceId", s.HandlePolicyDataBdtDataBdtReferenceIdGet},
		{"PolicyDataBdtDataBdtReferenceIdPut", strings.ToUpper("Put"), "/policy-data/bdt-data/:bdtReferenceId", s.HandlePolicyDataBdtDataBdtReferenceIdPut},
		{"PolicyDataBdtDataGet", strings.ToUpper("Get"), "/policy-data/bdt-data", s.HandlePolicyDataBdtDataGet},
		{"PolicyDataPlmnsPlmnIdUePolicySetGet", strings.ToUpper("Get"), "/policy-data/plmns/:plmnId/ue-policy-set", s.HandlePolicyDataPlmnsPlmnIdUePolicySetGet},
		{"PolicyDataSponsorConnectivityDataSponsorIdGet", strings.ToUpper("Get"), "/policy-data/sponsor-connectivity-data/:sponsorId", s.HandlePolicyDataSponsorConnectivityDataSponsorIdGet},
		{"PolicyDataSubsToNotifyPost", strings.ToUpper("Post"), "/policy-data/subs-to-notify", s.HandlePolicyDataSubsToNotifyPost},
		{"PolicyDataSubsToNotifySubsIdDelete", strings.ToUpper("Delete"), "/policy-data/subs-to-notify/:subsId", s.HandlePolicyDataSubsToNotifySubsIdDelete},
		{"PolicyDataSubsToNotifySubsIdPut", strings.ToUpper("Put"), "/policy-data/subs-to-notify/:subsId", s.HandlePolicyDataSubsToNotifySubsIdPut},
		{"PolicyDataUesUeIdAmDataGet", strings.ToUpper("Get"), "/policy-data/ues/:ueId/am-data", s.HandlePolicyDataUesUeIdAmDataGet},
		{"PolicyDataUesUeIdOperatorSpecificDataGet", strings.ToUpper("Get"), "/policy-data/ues/:ueId/operator-specific-data", s.HandlePolicyDataUesUeIdOperatorSpecificDataGet},
		{"PolicyDataUesUeIdOperatorSpecificDataPatch", strings.ToUpper("Patch"), "/policy-data/ues/:ueId/operator-specific-data", s.HandlePolicyDataUesUeIdOperatorSpecificDataPatch},
		{"PolicyDataUesUeIdOperatorSpecificDataPut", strings.ToUpper("Put"), "/policy-data/ues/:ueId/operator-specific-data", s.HandlePolicyDataUesUeIdOperatorSpecificDataPut},
		{"PolicyDataUesUeIdSmDataGet", strings.ToUpper("Get"), "/policy-data/ues/:ueId/sm-data", s.HandlePolicyDataUesUeIdSmDataGet},
		{"PolicyDataUesUeIdSmDataPatch", strings.ToUpper("Patch"), "/policy-data/ues/:ueId/sm-data", s.HandlePolicyDataUesUeIdSmDataPatch},
		{"PolicyDataUesUeIdSmDataUsageMonIdDelete", strings.ToUpper("Delete"), "/policy-data/ues/:ueId/sm-data/:usageMonId", s.HandlePolicyDataUesUeIdSmDataUsageMonIdDelete},
		{"PolicyDataUesUeIdSmDataUsageMonIdGet", strings.ToUpper("Get"), "/policy-data/ues/:ueId/sm-data/:usageMonId", s.HandlePolicyDataUesUeIdSmDataUsageMonIdGet},
		{"PolicyDataUesUeIdSmDataUsageMonIdPut", strings.ToUpper("Put"), "/policy-data/ues/:ueId/sm-data/:usageMonId", s.HandlePolicyDataUesUeIdSmDataUsageMonIdPut},
		{"PolicyDataUesUeIdUePolicySetGet", strings.ToUpper("Get"), "/policy-data/ues/:ueId/ue-policy-set", s.HandlePolicyDataUesUeIdUePolicySetGet},
		{"PolicyDataUesUeIdUePolicySetPatch", strings.ToUpper("Patch"), "/policy-data/ues/:ueId/ue-policy-set", s.HandlePolicyDataUesUeIdUePolicySetPatch},
		{"PolicyDataUesUeIdUePolicySetPut", strings.ToUpper("Put"), "/policy-data/ues/:ueId/ue-policy-set", s.HandlePolicyDataUesUeIdUePolicySetPut},
		{"QueryProvisionedData", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/provisioned-data", s.HandleQueryProvisionedData},
		{"RemovesdmSubscriptions", strings.ToUpper("Delete"), "/subscription-data/:ueId/:servingPlmnId/sdm-subscriptions/:subsId", s.HandleRemovesdmSubscriptions},
		{"Updatesdmsubscriptions", strings.ToUpper("Put"), "/subscription-data/:ueId/:servingPlmnId/sdm-subscriptions/:subsId", s.HandleUpdatesdmsubscriptions},
		{"CreateSdmSubscriptions", strings.ToUpper("Post"), "/subscription-data/:ueId/:servingPlmnId/sdm-subscriptions", s.HandleCreateSdmSubscriptions},
		{"Querysdmsubscriptions", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/sdm-subscriptions", s.HandleQuerysdmsubscriptions},
		{"CreateSmfContextNon3gpp", strings.ToUpper("Put"), "/subscription-data/:ueId/:servingPlmnId/smf-registrations/:pduSessionId", s.HandleCreateSmfContextNon3gpp},
		{"DeleteSmfContext", strings.ToUpper("Delete"), "/subscription-data/:ueId/:servingPlmnId/smf-registrations/:pduSessionId", s.HandleDeleteSmfContext},
		{"QuerySmfRegistration", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/smf-registrations/:pduSessionId", s.HandleQuerySmfRegistration},
		{"QuerySmfRegList", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/smf-registrations", s.HandleQuerySmfRegList},
		{"QuerySmfSelectData", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/provisioned-data/smf-selection-subscription-data", s.HandleQuerySmfSelectData},
		{"CreateSmsfContext3gpp", strings.ToUpper("Put"), "/subscription-data/:ueId/:servingPlmnId/smsf-3gpp-access", s.HandleCreateSmsfContext3gpp},
		{"DeleteSmsfContext3gpp", strings.ToUpper("Delete"), "/subscription-data/:ueId/:servingPlmnId/smsf-3gpp-access", s.HandleDeleteSmsfContext3gpp},
		{"QuerySmsfContext3gpp", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/smsf-3gpp-access", s.HandleQuerySmsfContext3gpp},
		{"CreateSmsfContextNon3gpp", strings.ToUpper("Put"), "/subscription-data/:ueId/:servingPlmnId/smsf-non-3gpp-access", s.HandleCreateSmsfContextNon3gpp},
		{"DeleteSmsfContextNon3gpp", strings.ToUpper("Delete"), "/subscription-data/:ueId/:servingPlmnId/smsf-non-3gpp-access", s.HandleDeleteSmsfContextNon3gpp},
		{"QuerySmsfContextNon3gpp", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/smsf-non-3gpp-access", s.HandleQuerySmsfContextNon3gpp},
		{"QuerySmsMngData", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/provisioned-data/sms-mng-data", s.HandleQuerySmsMngData},
		{"QuerySmsData", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/provisioned-data/sms-data", s.HandleQuerySmsData},
		{"QuerySmData", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/provisioned-data/sm-data", s.HandleQuerySmData},
		{"QueryTraceData", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/provisioned-data/trace-data", s.HandleQueryTraceData},
		{"CreateAMFSubscriptions", strings.ToUpper("Put"), "/subscription-data/:ueId/:servingPlmnId/ee-subscriptions/:subsId/amf-subscriptions", s.HandleCreateAMFSubscriptions},
		{"ModifyAmfSubscriptionInfo", strings.ToUpper("Patch"), "/subscription-data/:ueId/:servingPlmnId/ee-subscriptions/:subsId/amf-subscriptions", s.HandleModifyAmfSubscriptionInfo},
		{"RemoveAmfSubscriptionsInfo", strings.ToUpper("Delete"), "/subscription-data/:ueId/:servingPlmnId/ee-subscriptions/:subsId/amf-subscriptions", s.HandleRemoveAmfSubscriptionsInfo},
		{"GetAmfSubscriptionInfo", strings.ToUpper("Get"), "/subscription-data/:ueId/:servingPlmnId/ee-subscriptions/:subsId/amf-subscriptions", s.HandleGetAmfSubscriptionInfo},
		{"GetSharedData", strings.ToUpper("Get"), "/subscription-data/shared-data", s.HandleGetSharedData},
		{"PostSubscriptionDataSubscriptions", strings.ToUpper("Post"), "/subscription-data/subs-to-notify", s.HandlePostSubscriptionDataSubscriptions},
		{"RemovesubscriptionDataSubscriptions", strings.ToUpper("Delete"), "/subscription-data/subs-to-notify/:subsId", s.HandleRemovesubscriptionDataSubscriptions},
		{"QueryEEData", strings.ToUpper("Get"), "/subscription-data/:ueId/ee-profile-data", s.HandleQueryEEData},
		{"PatchOperSpecData", strings.ToUpper("Patch"), "/subscription-data/:ueId/operator-specific-data", s.HandlePatchOperSpecData},
		{"QueryOperSpecData", strings.ToUpper("Get"), "/subscription-data/:ueId/operator-specific-data", s.HandleQueryOperSpecData},
		{"GetppData", strings.ToUpper("Get"), "/subscription-data/:ueId/pp-data", s.HandleGetppData},
		{"ModifyPpData", strings.ToUpper("Patch"), "/subscription-data/:ueId/pp-data", s.HandleModifyPpData},
		{"GetIdentityData", strings.ToUpper("Get"), "/subscription-data/:ueId/identity-data", s.HandleGetIdentityData},
		{"GetOdbData", strings.ToUpper("Get"), "/subscription-data/:ueId/operator-determined-barring-data", s.HandleGetOdbData},
		{"CreateEeGroupSubscriptions", strings.ToUpper("Post"), "/subscription-data/group-data/:ueGroupId/ee-subscriptions", s.HandleCreateEeGroupSubscriptions},
		{"QueryEeGroupSubscriptions", strings.ToUpper("Get"), "/subscription-data/group-data/:ueGroupId/ee-subscriptions", s.HandleQueryEeGroupSubscriptions},
		{"CreateEeSubscriptions", strings.ToUpper("Post"), "/subscription-data/:ueId/context-data/ee-subscriptions", s.HandleCreateEeSubscriptions},
		{"Queryeesubscriptions", strings.ToUpper("Get"), "/subscription-data/:ueId/context-data/ee-subscriptions", s.HandleQueryeesubscriptions},
		{"RemoveeeSubscriptions", strings.ToUpper("Delete"), "/subscription-data/:ueId/context-data/ee-subscriptions/:subsId", s.HandleRemoveeeSubscriptions},
		{"UpdateEesubscriptions", strings.ToUpper("Put"), "/subscription-data/:ueId/context-data/ee-subscriptions/:subsId", s.HandleUpdateEesubscriptions},
		{"UpdateEeGroupSubscriptions", strings.ToUpper("Put"), "/subscription-data/group-data/:ueGroupId/ee-subscriptions/:subsId", s.HandleUpdateEeGroupSubscriptions},
		{"RemoveEeGroupSubscriptions", strings.ToUpper("Delete"), "/subscription-data/group-data/:ueGroupId/ee-subscriptions/:subsId", s.HandleRemoveEeGroupSubscriptions},
		{"CreateSessionManagementData", strings.ToUpper("Put"), "/exposure-data/:ueId/session-management-data/:pduSessionId", s.HandleCreateSessionManagementData},
		{"DeleteSessionManagementData", strings.ToUpper("Delete"), "/exposure-data/:ueId/session-management-data/:pduSessionId", s.HandleDeleteSessionManagementData},
		{"QuerySessionManagementData", strings.ToUpper("Get"), "/exposure-data/:ueId/session-management-data/:pduSessionId", s.HandleQuerySessionManagementData},
		{"CreateAccessAndMobilityData", strings.ToUpper("Put"), "/exposure-data/:ueId/access-and-mobility-data", s.HandleCreateAccessAndMobilityData},
		{"DeleteAccessAndMobilityData", strings.ToUpper("Delete"), "/exposure-data/:ueId/access-and-mobility-data", s.HandleDeleteAccessAndMobilityData},
		{"QueryAccessAndMobilityData", strings.ToUpper("Get"), "/exposure-data/:ueId/access-and-mobility-data", s.HandleQueryAccessAndMobilityData},
		{"ExposureDataSubsToNotifyPost", strings.ToUpper("Post"), "/exposure-data/subs-to-notify", s.HandleExposureDataSubsToNotifyPost},
		{"ExposureDataSubsToNotifySubIdDelete", strings.ToUpper("Delete"), "/exposure-data/subs-to-notify/:subId", s.HandleExposureDataSubsToNotifySubIdDelete},
		{"ExposureDataSubsToNotifySubIdPut", strings.ToUpper("Put"), "/exposure-data/subs-to-notify/:subId", s.HandleExposureDataSubsToNotifySubIdPut},
		{"ApplicationDataInfluenceDataSubsToNotifyGet", strings.ToUpper("Get"), "/application-data/influenceData/subs-to-notify", s.HandleApplicationDataInfluenceDataSubsToNotifyGet},
		{"ApplicationDataInfluenceDataSubsToNotifyPost", strings.ToUpper("Post"), "/application-data/influenceData/subs-to-notify", s.HandleApplicationDataInfluenceDataSubsToNotifyPost},
		{"ApplicationDataInfluenceDataInfluenceIdDelete", strings.ToUpper("Delete"), "/application-data/influenceData/:influenceId", s.HandleApplicationDataInfluenceDataInfluenceIdDelete},
		{"ApplicationDataInfluenceDataInfluenceIdPatch", strings.ToUpper("Patch"), "/application-data/influenceData/:influenceId", s.HandleApplicationDataInfluenceDataInfluenceIdPatch},
		{"ApplicationDataInfluenceDataInfluenceIdPut", strings.ToUpper("Put"), "/application-data/influenceData/:influenceId", s.HandleApplicationDataInfluenceDataInfluenceIdPut},
		{"ApplicationDataInfluenceDataInfluenceIdPut", strings.ToUpper("Post"), "/application-data/influenceData/:influenceId", s.HandleApplicationDataInfluenceDataInfluenceIdPost},
	}
}

func Index(c *gin.Context) {
	c.String(http.StatusNotImplemented, "Hello World!")
}

func (s *Server) HandleAmfContext3gpp(c *gin.Context) {
	var patchItemArray []models.PatchItem
	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{Title: "System failure", Status: http.StatusInternalServerError, Detail: err.Error(), Cause: "SYSTEM_FAILURE"}
		logger.DataRepoLog.Errorf("Get Request Body error: %+v", err)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}
	err = openapi.Deserialize(&patchItemArray, requestBody, "application/json")
	if err != nil {
		problemDetail := "[Request Body] " + err.Error()
		rsp := models.ProblemDetails{Title: "Malformed request syntax", Status: http.StatusBadRequest, Detail: problemDetail}
		logger.DataRepoLog.Errorln(problemDetail)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(rsp.Status)))
		c.JSON(http.StatusBadRequest, rsp)
		return
	}
	logger.DataRepoLog.Tracef("Handle AmfContext3gpp")
	collName := "subscriptionData.contextData.amf3gppAccess"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	s.Processor().AmfContext3gppProcedure(c, collName, ueId, patchItemArray)
}

func (s *Server) HandleCreateAmfContext3gpp(c *gin.Context) {
	var amf3GppAccessRegistration models.Amf3GppAccessRegistration
	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{Title: "System failure", Status: http.StatusInternalServerError, Detail: err.Error(), Cause: "SYSTEM_FAILURE"}
		logger.DataRepoLog.Errorf("Get Request Body error: %+v", err)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}
	err = openapi.Deserialize(&amf3GppAccessRegistration, requestBody, "application/json")
	if err != nil {
		problemDetail := "[Request Body] " + err.Error()
		rsp := models.ProblemDetails{Title: "Malformed request syntax", Status: http.StatusBadRequest, Detail: problemDetail}
		logger.DataRepoLog.Errorln(problemDetail)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(rsp.Status)))
		c.JSON(http.StatusBadRequest, rsp)
		return
	}
	logger.DataRepoLog.Tracef("Handle CreateAmfContext3gpp")
	collName := "subscriptionData.contextData.amf3gppAccess"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	s.Processor().CreateAmfContext3gppProcedure(c, collName, ueId, amf3GppAccessRegistration)
}

func (s *Server) HandleQueryAmfContext3gpp(c *gin.Context) {
	logger.DataRepoLog.Tracef("Handle QueryAmfContext3gpp")
	ueId := c.Params.ByName("ueId")
	collName := "subscriptionData.contextData.amf3gppAccess"
	if ueId == "" {
		problemDetail := &models.ProblemDetails{Title: util.MALFORMED_REQUEST, Status: http.StatusBadRequest, Detail: "ueId is required"}
		util.GinProblemJson(c, problemDetail)
		return
	}
	s.Processor().QueryAmfContext3gppProcedure(c, collName, ueId)
}

func (s *Server) HandleAmfContextNon3gpp(c *gin.Context) {
	var patchItemArray []models.PatchItem
	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{Title: "System failure", Status: http.StatusInternalServerError, Detail: err.Error(), Cause: "SYSTEM_FAILURE"}
		logger.DataRepoLog.Errorf("Get Request Body error: %+v", err)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}
	err = openapi.Deserialize(&patchItemArray, requestBody, "application/json")
	if err != nil {
		problemDetail := "[Request Body] " + err.Error()
		rsp := models.ProblemDetails{Title: "Malformed request syntax", Status: http.StatusBadRequest, Detail: problemDetail}
		logger.DataRepoLog.Errorln(problemDetail)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(rsp.Status)))
		c.JSON(http.StatusBadRequest, rsp)
		return
	}
	logger.DataRepoLog.Tracef("Handle AmfContextNon3gpp")
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	filter := bson.M{"ueId": ueId}
	s.Processor().AmfContextNon3gppProcedure(c, ueId, "subscriptionData.contextData.amfNon3gppAccess", patchItemArray, filter)
}

func (s *Server) HandleCreateAmfContextNon3gpp(c *gin.Context) {
	var amfNon3GppAccessRegistration models.AmfNon3GppAccessRegistration
	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{Title: "System failure", Status: http.StatusInternalServerError, Detail: err.Error(), Cause: "SYSTEM_FAILURE"}
		logger.DataRepoLog.Errorf("Get Request Body error: %+v", err)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}
	err = openapi.Deserialize(&amfNon3GppAccessRegistration, requestBody, "application/json")
	if err != nil {
		problemDetail := "[Request Body] " + err.Error()
		rsp := models.ProblemDetails{Title: "Malformed request syntax", Status: http.StatusBadRequest, Detail: problemDetail}
		logger.DataRepoLog.Errorln(problemDetail)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(rsp.Status)))
		c.JSON(http.StatusBadRequest, rsp)
		return
	}
	logger.DataRepoLog.Tracef("Handle CreateAmfContextNon3gpp")
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	s.Processor().CreateAmfContextNon3gppProcedure(c, amfNon3GppAccessRegistration, "subscriptionData.contextData.amfNon3gppAccess", ueId)
}

func (s *Server) HandleQueryAmfContextNon3gpp(c *gin.Context) {
	logger.DataRepoLog.Tracef("Handle QueryAmfContextNon3gpp")
	collName := "subscriptionData.contextData.amfNon3gppAccess"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	s.Processor().QueryAmfContextNon3gppProcedure(c, collName, ueId)
}

func (s *Server) HandleQueryAmData(c *gin.Context) {
	logger.DataRepoLog.Tracef("Handle QueryAmData")
	collName := "subscriptionData.provisionedData.amData"
	servingPlmnId := c.Params.ByName("servingPlmnId")
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	s.Processor().QueryAmDataProcedure(c, collName, ueId, servingPlmnId)
}

func (s *Server) HandleCreateAuthenticationStatus(c *gin.Context) {
	var authEvent models.AuthEvent
	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{Title: "System failure", Status: http.StatusInternalServerError, Detail: err.Error(), Cause: "SYSTEM_FAILURE"}
		logger.DataRepoLog.Errorf("Get Request Body error: %+v", err)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}
	err = openapi.Deserialize(&authEvent, requestBody, "application/json")
	if err != nil {
		problemDetail := "[Request Body] " + err.Error()
		rsp := models.ProblemDetails{Title: "Malformed request syntax", Status: http.StatusBadRequest, Detail: problemDetail}
		logger.DataRepoLog.Errorln(problemDetail)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(rsp.Status)))
		c.JSON(http.StatusBadRequest, rsp)
		return
	}
	logger.DataRepoLog.Tracef("Handle CreateAuthenticationStatus")
	putData := util.ToBsonM(authEvent)
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	collName := "subscriptionData.authenticationData.authenticationStatus"
	s.Processor().CreateAuthenticationStatusProcedure(c, collName, ueId, putData)
}

func (s *Server) HandleQueryAuthenticationStatus(c *gin.Context) {
	logger.DataRepoLog.Tracef("Handle QueryAuthenticationStatus")
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	collName := "subscriptionData.authenticationData.authenticationStatus"
	s.Processor().QueryAuthenticationStatusProcedure(c, collName, ueId)
}

func (s *Server) HandleModifyAuthentication(c *gin.Context) {
	var patchItemArray []models.PatchItem
	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{Title: "System failure", Status: http.StatusInternalServerError, Detail: err.Error(), Cause: "SYSTEM_FAILURE"}
		logger.DataRepoLog.Errorf("Get Request Body error: %+v", err)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}
	err = openapi.Deserialize(&patchItemArray, requestBody, "application/json")
	if err != nil {
		problemDetail := "[Request Body] " + err.Error()
		rsp := models.ProblemDetails{Title: "Malformed request syntax", Status: http.StatusBadRequest, Detail: problemDetail}
		logger.DataRepoLog.Errorln(problemDetail)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(rsp.Status)))
		c.JSON(http.StatusBadRequest, rsp)
		return
	}
	logger.DataRepoLog.Tracef("Handle ModifyAuthentication")
	collName := "subscriptionData.authenticationData.authenticationSubscription"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	s.Processor().ModifyAuthenticationProcedure(c, collName, ueId, patchItemArray)
}

func (s *Server) HandleQueryAuthSubsData(c *gin.Context) {
	logger.DataRepoLog.Tracef("Handle QueryAuthSubsData")
	collName := "subscriptionData.authenticationData.authenticationSubscription"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	s.Processor().QueryAuthSubsDataProcedure(c, collName, ueId)
}

func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete(c *gin.Context) {
	logger.DataRepoLog.Tracef("Handle ApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete")
	influenceId := c.Param("influenceId")
	if influenceId != "subs-to-notify" {
		c.String(http.StatusNotFound, "404 page not found")
	}
	subscriptionId := c.Params.ByName("subscriptionId")
	s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdDeleteProcedure(c, subscriptionId)
}

func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet(c *gin.Context) {
	logger.DataRepoLog.Tracef("Handle ApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet")
	influenceId := c.Param("influenceId")
	if influenceId != "subs-to-notify" {
		c.String(http.StatusNotFound, "404 page not found")
	}
	subscriptionId := c.Params.ByName("subscriptionId")
	s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdGetProcedure(c, subscriptionId)
}

func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut(c *gin.Context) {
	influenceId := c.Param("influenceId")
	if influenceId != "subs-to-notify" {
		c.String(http.StatusNotFound, "404 page not found")
	}
	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{Title: "System failure", Status: http.StatusInternalServerError, Detail: err.Error(), Cause: "SYSTEM_FAILURE"}
		logger.DataRepoLog.Errorf("Get Request Body error: %+v", err)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}
	var trafficInfluSub models.TrafficInfluSub
	err = openapi.Deserialize(&trafficInfluSub, requestBody, "application/json")
	if err != nil {
		problemDetail := "[Request Body] " + err.Error()
		rsp := models.ProblemDetails{Title: "Malformed request syntax", Status: http.StatusBadRequest, Detail: problemDetail}
		logger.DataRepoLog.Errorln(problemDetail)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(rsp.Status)))
		c.JSON(http.StatusBadRequest, rsp)
		return
	}
	logger.DataRepoLog.Tracef("Handle ApplicationDataInfluenceDataSubsToNotifySubscriptiondIdPut")
	subscriptionId := c.Params.ByName("subscriptionId")
	s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdPutProcedure(c, subscriptionId, &trafficInfluSub)
}

func getDataFromRequestBody(c *gin.Context, data interface{}) error {
	reqBody, err := c.GetRawData()
	if err != nil {
		logger.DataRepoLog.Errorf("Get Request Body error: %+v", err)
		pd := openapi.ProblemDetailsSystemFailure(err.Error())
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, pd.Cause)
		c.JSON(http.StatusInternalServerError, pd)
		return err
	}
	err = openapi.Deserialize(data, reqBody, "application/json")
	if err != nil {
		logger.DataRepoLog.Errorf("Deserialize Request Body error: %+v", err)
		pd := util.ProblemDetailsMalformedReqSyntax(err.Error())
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, pd.Cause)
		c.JSON(http.StatusBadRequest, pd)
		return err
	}
	return err
}

func (s *Server) HandleApplicationDataPfdsAppIdDelete(c *gin.Context) {
	appID := c.Params.ByName("appId")
	s.Processor().DeleteApplicationDataIndividualPfdFromDBProcedure(c, appID)
}

func (s *Server) HandleApplicationDataPfdsAppIdGet(c *gin.Context) {
	appID := c.Params.ByName("appId")
	s.Processor().GetApplicationDataIndividualPfdFromDBProcedure(c, appID)
}

func (s *Server) HandleApplicationDataPfdsAppIdPut(c *gin.Context) {
	var pfdDataforApp models.PfdDataForApp
	if err := getDataFromRequestBody(c, &pfdDataforApp); err != nil {
		return
	}
	appID := c.Params.ByName("appId")
	s.Processor().PutApplicationDataIndividualPfdToDBProcedure(c, appID, &pfdDataforApp)
}

func (s *Server) HandleApplicationDataPfdsGet(c *gin.Context) {
	query := c.Request.URL.Query()
	pfdsAppIDs := query["appId"]
	s.Processor().GetApplicationDataPfdsFromDBProcedure(c, pfdsAppIDs)
}

func (s *Server) HandleExposureDataSubsToNotifyPost(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleExposureDataSubsToNotifySubIdDelete(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleExposureDataSubsToNotifySubIdPut(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandlePolicyDataBdtDataBdtReferenceIdDelete(c *gin.Context) {
	collName := "policyData.bdtData"
	bdtReferenceId := c.Params.ByName("bdtReferenceId")
	s.Processor().PolicyDataBdtDataBdtReferenceIdDeleteProcedure(c, collName, bdtReferenceId)
}

func (s *Server) HandlePolicyDataBdtDataBdtReferenceIdGet(c *gin.Context) {
	collName := "policyData.bdtData"
	bdtReferenceId := c.Params.ByName("bdtReferenceId")
	s.Processor().PolicyDataBdtDataBdtReferenceIdGetProcedure(c, collName, bdtReferenceId)
}

func (s *Server) HandlePolicyDataBdtDataBdtReferenceIdPut(c *gin.Context) {
	var bdtData models.BdtData
	if err := getDataFromRequestBody(c, &bdtData); err != nil {
		return
	}
	collName := "policyData.bdtData"
	bdtReferenceId := c.Params.ByName("bdtReferenceId")
	s.Processor().PolicyDataBdtDataBdtReferenceIdPutProcedure(c, collName, bdtReferenceId, bdtData)
}

func (s *Server) HandlePolicyDataBdtDataGet(c *gin.Context) {
	collName := "policyData.bdtData"
	s.Processor().PolicyDataBdtDataGetProcedure(c, collName)
}

func (s *Server) HandlePolicyDataPlmnsPlmnIdUePolicySetGet(c *gin.Context) {
	collName := "policyData.plmns.uePolicySet"
	plmnId := c.Params.ByName("plmnId")
	s.Processor().PolicyDataPlmnsPlmnIdUePolicySetGetProcedure(c, collName, plmnId)
}

func (s *Server) HandlePolicyDataSponsorConnectivityDataSponsorIdGet(c *gin.Context) {
	collName := "policyData.sponsorConnectivityData"
	sponsorId := c.Params.ByName("sponsorId")
	s.Processor().PolicyDataSponsorConnectivityDataSponsorIdGetProcedure(c, collName, sponsorId)
}

func (s *Server) HandlePolicyDataSubsToNotifyPost(c *gin.Context) {
	var policyDataSubscription models.PolicyDataSubscription

	reqBody, err := c.GetRawData()
	if err != nil {
		logger.DataRepoLog.Errorf("Get Request Body error: %+v", err)
		pd := openapi.ProblemDetailsSystemFailure(err.Error())
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, pd.Cause)
		c.JSON(http.StatusInternalServerError, pd)
	}

	err = openapi.Deserialize(policyDataSubscription, reqBody, "application/json")
	if err != nil {
		logger.DataRepoLog.Errorf("Deserialize Request Body error: %+v", err)
		pd := util.ProblemDetailsMalformedReqSyntax(err.Error())
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, pd.Cause)
		c.JSON(http.StatusBadRequest, pd)
	}

	logger.DataRepoLog.Tracef("Handle PolicyDataSubsToNotifyPost")

	s.Processor().PolicyDataSubsToNotifyPostProcedure(c, policyDataSubscription)
}

func (s *Server) HandlePolicyDataSubsToNotifySubsIdDelete(c *gin.Context) {
	subsId := c.Params.ByName("subsId")
	s.Processor().PolicyDataSubsToNotifySubsIdDeleteProcedure(c, subsId)
}

func (s *Server) HandlePolicyDataSubsToNotifySubsIdPut(c *gin.Context) {
	var policyDataSubscription models.PolicyDataSubscription

	reqBody, err := c.GetRawData()
	if err != nil {
		logger.DataRepoLog.Errorf("Get Request Body error: %+v", err)
		pd := openapi.ProblemDetailsSystemFailure(err.Error())
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, pd.Cause)
		c.JSON(http.StatusInternalServerError, pd)
	}

	err = openapi.Deserialize(policyDataSubscription, reqBody, "application/json")
	if err != nil {
		logger.DataRepoLog.Errorf("Deserialize Request Body error: %+v", err)
		pd := util.ProblemDetailsMalformedReqSyntax(err.Error())
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, pd.Cause)
		c.JSON(http.StatusBadRequest, pd)
	}

	logger.DataRepoLog.Tracef("Handle PolicyDataSubsToNotifySubsIdPut")
	subsId := c.Params.ByName("subsId")
	s.Processor().PolicyDataSubsToNotifySubsIdPutProcedure(c, subsId, policyDataSubscription)
}

func (s *Server) HandlePolicyDataUesUeIdAmDataGet(c *gin.Context) {
	collName := "policyData.ues.amData"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	s.Processor().PolicyDataUesUeIdAmDataGetProcedure(c, collName, ueId)
}

func (s *Server) HandlePolicyDataUesUeIdOperatorSpecificDataGet(c *gin.Context) {
	collName := "policyData.ues.operatorSpecificData"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	s.Processor().PolicyDataUesUeIdOperatorSpecificDataGetProcedure(c, collName, ueId)
}

func (s *Server) HandlePolicyDataUesUeIdOperatorSpecificDataPatch(c *gin.Context) {
	var patchItemArray []models.PatchItem
	if err := getDataFromRequestBody(c, &patchItemArray); err != nil {
		return
	}
	collName := "policyData.ues.operatorSpecificData"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	s.Processor().PolicyDataUesUeIdOperatorSpecificDataPatchProcedure(c, collName, ueId, patchItemArray)
}

func (s *Server) HandlePolicyDataUesUeIdOperatorSpecificDataPut(c *gin.Context) {
	var operatorSpecificDataContainerMap map[string]models.OperatorSpecificDataContainer
	if err := getDataFromRequestBody(c, &operatorSpecificDataContainerMap); err != nil {
		return
	}
	collName := "policyData.ues.operatorSpecificData"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	s.Processor().PolicyDataUesUeIdOperatorSpecificDataPutProcedure(c, collName, ueId, operatorSpecificDataContainerMap)
}

func (s *Server) HandlePolicyDataUesUeIdSmDataGet(c *gin.Context) {
	collName := "policyData.ues.smData"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	sNssai := models.Snssai{}
	sNssaiQuery := c.Request.URL.Query().Get("snssai")
	dnn := c.Request.URL.Query().Get("dnn")

	err := json.Unmarshal([]byte(sNssaiQuery), &sNssai)
	if err != nil {
		logger.DataRepoLog.Warnln(err)
	}
	s.Processor().PolicyDataUesUeIdSmDataGetProcedure(c, collName, ueId, sNssai, dnn)
}

func (s *Server) HandlePolicyDataUesUeIdSmDataPatch(c *gin.Context) {
	var usageMonDataMap map[string]models.UsageMonData
	if err := getDataFromRequestBody(c, &usageMonDataMap); err != nil {
		return
	}
	collName := "policyData.ues.smData.usageMonData"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	s.Processor().PolicyDataUesUeIdSmDataPatchProcedure(c, collName, ueId, usageMonDataMap)
}

func (s *Server) HandlePolicyDataUesUeIdSmDataUsageMonIdDelete(c *gin.Context) {
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	usageMonId := c.Params.ByName("usageMonId")
	collName := "policyData.ues.smData.usageMonData"
	s.Processor().PolicyDataUesUeIdSmDataUsageMonIdDeleteProcedure(c, collName, ueId, usageMonId)
}

func (s *Server) HandlePolicyDataUesUeIdSmDataUsageMonIdGet(c *gin.Context) {
	collName := "policyData.ues.smData.usageMonData"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	usageMonId := c.Params.ByName("usageMonId")
	s.Processor().PolicyDataUesUeIdSmDataUsageMonIdGetProcedure(c, collName, usageMonId, ueId)
}

func (s *Server) HandlePolicyDataUesUeIdSmDataUsageMonIdPut(c *gin.Context) {
	var usageMonData models.UsageMonData
	if err := getDataFromRequestBody(c, &usageMonData); err != nil {
		return
	}
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	usageMonId := c.Params.ByName("usageMonId")
	collName := "policyData.ues.smData.usageMonData"
	s.Processor().PolicyDataUesUeIdSmDataUsageMonIdPutProcedure(c, collName, ueId, usageMonId, usageMonData)
}

func (s *Server) HandlePolicyDataUesUeIdUePolicySetGet(c *gin.Context) {
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	collName := "policyData.ues.uePolicySet"
	s.Processor().PolicyDataUesUeIdUePolicySetGetProcedure(c, collName, ueId)
}

func (s *Server) HandlePolicyDataUesUeIdUePolicySetPatch(c *gin.Context) {
	var uePolicySet models.UePolicySet
	if err := getDataFromRequestBody(c, &uePolicySet); err != nil {
		return
	}
	collName := "policyData.ues.uePolicySet"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	s.Processor().PolicyDataUesUeIdUePolicySetPatchProcedure(c, collName, ueId, uePolicySet)
}

func (s *Server) HandlePolicyDataUesUeIdUePolicySetPut(c *gin.Context) {
	var uePolicySet models.UePolicySet
	if err := getDataFromRequestBody(c, &uePolicySet); err != nil {
		return
	}
	collName := "policyData.ues.uePolicySet"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	s.Processor().PolicyDataUesUeIdUePolicySetPutProcedure(c, collName, ueId, uePolicySet)
}
```

---

## Question

Review the complete file above for security and correctness vulnerabilities. List all distinct issues you find, specifying the type, the exact handler function and location, and the potential impact of each.

---

## Agent Instructions

Reply ONLY in JSON format. Include one entry per distinct vulnerability found:

```json
{
  "answer": [
    {
      "vulnerability_type": "...",
      "location": "...",
      "impact": "..."
    }
  ],
  "reasoning": "...",
  "confidence": 0.0
}
```
