# Unmatched finding — task8_vuln_udm_full (1A_sast_hint_full) — agent, rep 3

| field | value |
| --- | --- |
| function | `HandleGetSupi` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:L/SI:L/SA:L` |
| score declared | 5.1 |
| score computed (official CVSS 4.0 math) | 5.3 |
| group (shared with matched table) | a |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `HandleGetSupi` are **bolded** below to help locate the relevant passage._

**Answer:**

The UDM implementation contains critical security flaws including inconsistent SUPI/UEID validation across multiple handlers, a DoS vulnerability via unsafe JSON unmarshaling of query parameters, and information leakage through raw error responses. Additionally, the custom routing logic in `OneLayerPathHandlerFunc` is fragile and could lead to incorrect handler execution.

**Reasoning:**

1. **Missing Input Validation (SUPI/UEID):**
   - **Location:** `HandleGetSmfSelectData`, **`HandleGetSupi`**, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`, and `HandleModifyForSharedData`.
   - **Pattern:** These functions extract `supi` or `ueId` from `c.Params.ByName()` but fail to call `validator.IsValidSupi()` or `validator.IsValidGpsi()` before passing the value to the `Processor` layer.
   - **Impact:** In a 5G Core, the SUPI is a critical identifier. Lack of validation allows malformed, oversized, or unexpected strings to reach the business logic and database layers. This can lead to backend crashes (DoS), database query errors, or potentially injection attacks if the processor does not sanitize the input.
   - **Fix:** Implement a consistent validation check using `validator.IsValidSupi(supi)` at the start of every handler that accepts a SUPI/UEID.

2. **Unsafe JSON Unmarshaling of Query Parameters:**
   - **Location:** `getPlmnIDStruct`.
   - **Pattern:** The code takes the raw string from the `plmn-id` query parameter and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** This is a non-standard use of query parameters. An attacker can provide a specially crafted, deeply nested, or extremely large JSON string in the URL. This can lead to excessive CPU and memory consumption during the unmarshaling process, resulting in a Denial of Service (DoS) of the UDM NF.
   - **Fix:** Avoid using JSON in query parameters. Use standard key-value pairs or a dedicated request body. If JSON must be used, implement strict length limits on the input string before unmarshaling.

3. **Information Leakage via Error Messages:**
   - **Location:** `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern:** The code assigns `err.Error()` (from `c.GetRawData()` or `openapi.Deserialize`) directly to the `Detail` field of the `ProblemDetails` response sent to the client.
   - **Impact:** Returning raw internal error messages to the SBI can leak implementation details, library versions, or internal memory state. This provides an attacker with reconnaissance data to craft more precise exploits.
   - **Fix:** Use generic error messages for the client (e.g., "Invalid request body") and log the detailed error internally for debugging.

4. **Fragile Route Dispatching Logic:**
   - **Location:** `OneLayerPathHandlerFunc`.
   - **Pattern:** The function iterates through routes and uses `strings.Contains(route.Pattern, supi)` to determine if a handler should be called.
   - **Impact:** This is a logic error. If the `supi` parameter contains a string that happens to be a substring of another route's pattern, the wrong handler may be triggered. While SUPIs are typically numeric, the lack of validation (Finding 1) makes this a viable path for request smuggling or unauthorized function execution within the NF.
   - **Fix:** Use exact matching or a proper regex-based router instead of `strings.Contains`.

<details>
<summary>Prompt sent to the model (system + user)</summary>

**System:**

```
You are a 5G network engineer experienced in core network analysis and code review.
Reply ONLY in Markdown using the response format in the task. No extra text before or after.
```

**User:**

````
# Task — Security Code Review: UDM (complete file)

**ID:** task8_vuln_udm_full
**Tipo:** textual
**Difficoltà:** alta

---

## Scenario

The following is the **complete** Go source file `api_subscriberdatamanagement.go` from the **UDM** Network Function of a free5GC 5G core implementation. It is an SBI (Service-Based Interface) HTTP handler using the Gin framework.

Perform a **security code review** of the entire file. Read it in full, function by function, before deciding what to report — do not select preventively or stop after finding the first few issues. Identify all security vulnerabilities, logic errors, and unsafe coding patterns present in the code; there is no limit on how many findings you may report, including minor ones or ones that recur with small variations across similar handlers.

```go
package sbi

import (
	"encoding/json"
	"net/http"
	"net/url"
	"strings"

	"github.com/gin-gonic/gin"

	"github.com/free5gc/openapi"
	"github.com/free5gc/openapi/models"
	"github.com/free5gc/udm/internal/logger"
	"github.com/free5gc/util/metrics/sbi"
	"github.com/free5gc/util/validator"
)

func (s *Server) getSubscriberDataManagementRoutes() []Route {
	return []Route{
		{
			"Index",
			http.MethodGet,
			"/",
			s.HandleIndex,
		},
	}
}

// GetAmData - retrieve a UE's Access and Mobility Subscription Data
func (s *Server) HandleGetAmData(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("supported-features", c.Query("supported-features"))

	logger.SdmLog.Infof("Handle GetAmData")

	// TS 29.503 6.1.3.5.2
	// Validate SUPI format
	supi := c.Params.ByName("supi")
	if !validator.IsValidSupi(supi) {
		problemDetail := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: "Supi is invalid",
			Cause:  "MANDATORY_IE_INCORRECT",
		}
		logger.SdmLog.Warnln("Supi is invalid")
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(problemDetail.Status)))
		c.JSON(int(problemDetail.Status), problemDetail)
		return
	}

	// use c.Request.URL.Query() only for getPlmnIDStruct
	plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
	if problemDetails != nil {
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetails.Cause)
		c.JSON(int(problemDetails.Status), problemDetails)
		return
	}

	var plmnID string
	if plmnIDStruct != nil {
		plmnID = plmnIDStruct.Mcc + plmnIDStruct.Mnc
	}
	supportedFeatures := query.Get("supported-features")

	s.Processor().GetAmDataProcedure(c, supi, plmnID, supportedFeatures)
}

func (s *Server) getPlmnIDStruct(
	queryParameters url.Values,
) (plmnIDStruct *models.PlmnId, problemDetails *models.ProblemDetails) {
	values, exists := queryParameters["plmn-id"]
	if !exists {
		// not exist like: http:{ip:port}/api/.../
		return nil, nil
	}
	if len(values) == 0 || strings.TrimSpace(values[0]) == "" {
		// exist but it is empty like: http:{ip:port}/api/.../?plmn-id=
		problemDetails = &models.ProblemDetails{
			Title:  "Invalid Parameter",
			Status: http.StatusBadRequest,
			Cause:  "plmn-id parameter cannot be empty",
		}
		return nil, problemDetails
	}

	// exist and not empty link: http:{ip:port}/api/.../?plmn-id=xxx
	plmnIDJson := values[0]
	plmnIDStruct = &models.PlmnId{}
	err := json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)
	if err != nil {
		logger.SdmLog.Warnln("Unmarshal Error in targetPlmnListtruct: ", err)
		problemDetails = &models.ProblemDetails{
			Title:  "Invalid Parameter",
			Status: http.StatusBadRequest,
			Cause:  "Failed to parse plmn-id JSON",
			InvalidParams: []models.InvalidParam{{
				Param:  "plmn-id",
				Reason: err.Error(),
			}},
		}
		return nil, problemDetails
	}
	return plmnIDStruct, nil
}

// Info - Nudm_Sdm Info service operation
func (s *Server) HandleInfo(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

// PutUpuAck - Nudm_Sdm Info for UPU service operation
func (s *Server) HandlePutUpuAck(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

// GetSmfSelectData - retrieve a UE's SMF Selection Subscription Data
func (s *Server) HandleGetSmfSelectData(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("supported-features", c.Query("supported-features"))

	logger.SdmLog.Infof("Handle GetSmfSelectData")

	supi := c.Params.ByName("supi")
	// use c.Request.URL.Query() only for getPlmnIDStruct
	plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
	if problemDetails != nil {
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetails.Cause)
		c.JSON(int(problemDetails.Status), problemDetails)
		return
	}
	var plmnID string
	if plmnIDStruct != nil {
		plmnID = plmnIDStruct.Mcc + plmnIDStruct.Mnc
	}
	supportedFeatures := query.Get("supported-features")

	s.Processor().GetSmfSelectDataProcedure(c, supi, plmnID, supportedFeatures)
}

// GetSmsMngData - retrieve a UE's SMS Management Subscription Data
func (s *Server) HandleGetSmsMngData(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{})
}

// GetSmsData - retrieve a UE's SMS Subscription Data
func (s *Server) HandleGetSmsData(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{})
}

// GetSupi - retrieve multiple data sets
func (s *Server) HandleGetSupi(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("dataset-names", c.Query("dataset-names"))
	query.Set("supported-features", c.Query("supported-features"))

	logger.SdmLog.Infof("Handle GetSupiRequest")

	supi := c.Params.ByName("supi")
	// use c.Request.URL.Query() only for getPlmnIDStruct
	plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
	if problemDetails != nil {
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetails.Cause)
		c.JSON(int(problemDetails.Status), problemDetails)
		return
	}
	var plmnID string
	if plmnIDStruct != nil {
		plmnID = plmnIDStruct.Mcc + plmnIDStruct.Mnc
	}
	dataSetNames := strings.Split(query.Get("dataset-names"), ",")
	supportedFeatures := query.Get("supported-features")

	s.Processor().GetSupiProcedure(c, supi, plmnID, dataSetNames, supportedFeatures)
}

// GetSharedData - retrieve shared data
func (s *Server) HandleGetSharedData(c *gin.Context) {
	logger.SdmLog.Infof("Handle GetSharedData")

	sharedDataIds := c.QueryArray("shared-data-ids")
	supportedFeatures := c.QueryArray("supported-features")

	supportedFeature := ""
	if len(supportedFeatures) > 0 {
		supportedFeature = supportedFeatures[0]
	}

	s.Processor().GetSharedDataProcedure(c, sharedDataIds, supportedFeature)
}

// SubscribeToSharedData - subscribe to notifications for shared data
func (s *Server) HandleSubscribeToSharedData(c *gin.Context) {
	var sharedDataSubsReq models.SdmSubscription

	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{
			Title:  "System failure",
			Status: http.StatusInternalServerError,
			Detail: err.Error(),
			Cause:  "SYSTEM_FAILURE",
		}
		logger.SdmLog.Errorf("Get Request Body error: %+v", err)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}

	err = openapi.Deserialize(&sharedDataSubsReq, requestBody, "application/json")
	if err != nil {
		problemDetail := "[Request Body] " + err.Error()
		rsp := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: problemDetail,
		}
		logger.SdmLog.Errorln(problemDetail)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(rsp.Status)))
		c.JSON(int(rsp.Status), rsp)
		return
	}

	logger.SdmLog.Infof("Handle SubscribeToSharedData")

	s.Processor().SubscribeToSharedDataProcedure(c, &sharedDataSubsReq)
}

// Subscribe - subscribe to notifications
func (s *Server) HandleSubscribe(c *gin.Context) {
	var sdmSubscriptionReq models.SdmSubscription

	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{
			Title:  "System failure",
			Status: http.StatusInternalServerError,
			Detail: err.Error(),
			Cause:  "SYSTEM_FAILURE",
		}
		logger.SdmLog.Errorf("Get Request Body error: %+v", err)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}

	err = openapi.Deserialize(&sdmSubscriptionReq, requestBody, "application/json")
	if err != nil {
		problemDetail := "[Request Body] " + err.Error()
		rsp := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: problemDetail,
		}
		logger.SdmLog.Errorln(problemDetail)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(rsp.Status)))
		c.JSON(int(rsp.Status), rsp)
		return
	}

	logger.SdmLog.Infof("Handle Subscribe")

	supi := c.Params.ByName("supi")
	s.Processor().SubscribeProcedure(c, &sdmSubscriptionReq, supi)
}

// Unsubscribe - unsubscribe from notifications
func (s *Server) HandleUnsubscribe(c *gin.Context) {
	logger.SdmLog.Infof("Handle Unsubscribe")

	// TS 29.503 6.1.3.4.2
	// Validate SUPI and GPSI format the UE ID (SUPI or GPSI)
	ueId := c.Params.ByName("ueId")
	valid := validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)
	if !valid {
		problemDetail := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: "UE ID is invalid",
			Cause:  "MANDATORY_IE_INCORRECT",
		}
		logger.SdmLog.Warnln("UE ID is invalid")
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(problemDetail.Status)))
		c.JSON(int(problemDetail.Status), problemDetail)
		return
	}
	subscriptionID := c.Params.ByName("subscriptionId")

	s.Processor().UnsubscribeProcedure(c, ueId, subscriptionID)
}

// UnsubscribeForSharedData - unsubscribe from notifications for shared data
func (s *Server) HandleUnsubscribeForSharedData(c *gin.Context) {
	logger.SdmLog.Infof("Handle UnsubscribeForSharedData")

	subscriptionID := c.Params.ByName("subscriptionId")
	s.Processor().UnsubscribeForSharedDataProcedure(c, subscriptionID)
}

// Modify - modify the subscription
func (s *Server) HandleModify(c *gin.Context) {
	var sdmSubsModificationReq models.SdmSubsModification

	// TS 29.503 6.1.3.4.2
	// Validate SUPI and GPSI format the UE ID (SUPI or GPSI)
	ueId := c.Params.ByName("ueId")
	valid := validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)
	if !valid {
		problemDetail := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: "UE ID is invalid",
			Cause:  "MANDATORY_IE_INCORRECT",
		}
		logger.SdmLog.Warnln("UE ID is invalid")
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(problemDetail.Status)))
		c.JSON(int(problemDetail.Status), problemDetail)
		return
	}
	subscriptionID := c.Params.ByName("subscriptionId")

	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{
			Title:  "System failure",
			Status: http.StatusInternalServerError,
			Detail: err.Error(),
			Cause:  "SYSTEM_FAILURE",
		}
		logger.SdmLog.Errorf("Get Request Body error: %+v", err)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}

	err = openapi.Deserialize(&sdmSubsModificationReq, requestBody, "application/json")
	if err != nil {
		problemDetail := "[Request Body] " + err.Error()
		rsp := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: problemDetail,
		}
		logger.SdmLog.Errorln(problemDetail)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(rsp.Status)))
		c.JSON(int(rsp.Status), rsp)
		return
	}

	logger.SdmLog.Infof("Handle Modify")

	s.Processor().ModifyProcedure(c, &sdmSubsModificationReq, ueId, subscriptionID)
}

// ModifyForSharedData - modify the subscription
func (s *Server) HandleModifyForSharedData(c *gin.Context) {
	var sharedDataSubscriptions models.SdmSubsModification
	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{
			Title:  "System failure",
			Status: http.StatusInternalServerError,
			Detail: err.Error(),
			Cause:  "SYSTEM_FAILURE",
		}
		logger.SdmLog.Errorf("Get Request Body error: %+v", err)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}

	err = openapi.Deserialize(&sharedDataSubscriptions, requestBody, "application/json")
	if err != nil {
		problemDetail := "[Request Body] " + err.Error()
		rsp := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: problemDetail,
		}
		logger.SdmLog.Errorln(problemDetail)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(rsp.Status)))
		c.JSON(int(rsp.Status), rsp)
		return
	}

	logger.SdmLog.Infof("Handle ModifyForSharedData")

	supi := c.Params.ByName("supi")
	subscriptionID := c.Params.ByName("subscriptionId")

	s.Processor().ModifyForSharedDataProcedure(c, &sharedDataSubscriptions, supi, subscriptionID)
}

// GetTraceData - retrieve a UE's Trace Configuration Data
func (s *Server) HandleGetTraceData(c *gin.Context) {
	logger.SdmLog.Infof("Handle GetTraceData")

	supi := c.Params.ByName("supi")
	plmnID := c.Query("plmn-id")

	s.Processor().GetTraceDataProcedure(c, supi, plmnID)
}

// GetUeContextInSmfData - retrieve a UE's UE Context In SMF Data
func (s *Server) HandleGetUeContextInSmfData(c *gin.Context) {
	logger.SdmLog.Infof("Handle GetUeContextInSmfData")

	supi := c.Params.ByName("supi")
	supportedFeatures := c.Query("supported-features")

	s.Processor().GetUeContextInSmfDataProcedure(c, supi, supportedFeatures)
}

// GetUeContextInSmsfData - retrieve a UE's UE Context In SMSF Data
func (s *Server) HandleGetUeContextInSmsfData(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{})
}

// GetNssai - retrieve a UE's subscribed NSSAI
func (s *Server) HandleGetNssai(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("supported-features", c.Query("supported-features"))

	logger.SdmLog.Infof("Handle GetNssai")

	supi := c.Params.ByName("supi")
	// use c.Request.URL.Query() only for getPlmnIDStruct
	plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
	if problemDetails != nil {
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetails.Cause)
		c.JSON(int(problemDetails.Status), problemDetails)
		return
	}
	var plmnID string
	if plmnIDStruct != nil {
		plmnID = plmnIDStruct.Mcc + plmnIDStruct.Mnc
	}
	supportedFeatures := query.Get("supported-features")

	s.Processor().GetNssaiProcedure(c, supi, plmnID, supportedFeatures)
}

// GetSmData - retrieve a UE's Session Management Subscription Data
func (s *Server) HandleGetSmData(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("dnn", c.Query("dnn"))
	query.Set("single-nssai", c.Query("single-nssai"))
	query.Set("supported-features", c.Query("supported-features"))

	logger.SdmLog.Infof("Handle GetSmData")

	supi := c.Params.ByName("supi")
	// use c.Request.URL.Query() only for getPlmnIDStruct
	plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
	if problemDetails != nil {
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetails.Cause)
		c.JSON(int(problemDetails.Status), problemDetails)
		return
	}
	var plmnID string
	if plmnIDStruct != nil {
		plmnID = plmnIDStruct.Mcc + plmnIDStruct.Mnc
	}
	Dnn := query.Get("dnn")
	Snssai := query.Get("single-nssai")
	supportedFeatures := query.Get("supported-features")

	s.Processor().GetSmDataProcedure(c, supi, plmnID, Dnn, Snssai, supportedFeatures)
}

// GetIdTranslationResult - retrieve a UE's SUPI
func (s *Server) HandleGetIdTranslationResult(c *gin.Context) {
	// req.Query.Set("SupportedFeatures", c.Query("supported-features"))

	logger.SdmLog.Infof("Handle GetIdTranslationResultRequest")

	// TS 29.503 6.1.3.12.2
	// Validate SUPI and GPSI format the UE ID (SUPI or GPSI)
	ueId := c.Params.ByName("ueId")
	valid := validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)
	if !valid {
		problemDetail := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: "UE ID is invalid",
			Cause:  "MANDATORY_IE_INCORRECT",
		}
		logger.SdmLog.Warnln("UE ID is invalid")
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(problemDetail.Status)))
		c.JSON(int(problemDetail.Status), problemDetail)
		return
	}

	s.Processor().GetIdTranslationResultProcedure(c, ueId)
}

func (s *Server) HandleGetMultipleIdentifiers(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleGetGroupIdentifiers(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleGetLcsBcaData(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleGetLcsMoData(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleGetLcsPrivacyData(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleGetMbsData(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleGetProseData(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleGetUcData(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleGetUeCtxInAmfData(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleGetV2xData(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleGetIndividualSharedData(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleCAGAck(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleGetEcrData(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleSNSSAIsAck(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleUpdateSORInfo(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) HandleUpuAck(c *gin.Context) {
	c.JSON(http.StatusNotImplemented, gin.H{})
}

func (s *Server) OneLayerPathHandlerFunc(c *gin.Context) {
	supi := c.Param("supi")
	oneLayerPathRouter := s.getOneLayerRoutes()
	for _, route := range oneLayerPathRouter {
		if strings.Contains(route.Pattern, supi) && route.Method == c.Request.Method {
			route.HandlerFunc(c)
			return
		}
	}

	// special case for :supi
	if c.Request.Method == http.MethodGet {
		s.HandleGetSupi(c)
		return
	}

	c.String(http.StatusNotFound, "404 page not found")
}

func (s *Server) TwoLayerPathHandlerFunc(c *gin.Context) {
	supi := c.Param("supi")
	op := c.Param("subscriptionId")

	logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)

	// for "/shared-data-subscriptions/:subscriptionId"
	if supi == "shared-data-subscriptions" && http.MethodDelete == c.Request.Method {
		s.HandleUnsubscribeForSharedData(c)
		return
	}

	// for "/shared-data-subscriptions/:subscriptionId"
	if supi == "shared-data-subscriptions" && http.MethodPatch == c.Request.Method {
		s.HandleModifyForSharedData(c)
		return
	}

	// for "/:ueId/id-translation-result"
	if op == "id-translation-result" && http.MethodGet == c.Request.Method {
		c.Params = append(c.Params, gin.Param{Key: "ueId", Value: c.Param("supi")})
		s.HandleGetIdTranslationResult(c)
		return
	}

	// for "/shared-data/:sharedDataId"
	if supi == "shared-data" && http.MethodGet == c.Request.Method {
		s.HandleGetIndividualSharedData(c)
		return
	}

	twoLayerPathRouter := s.getTwoLayerRoutes()
	for _, route := range twoLayerPathRouter {
		if strings.Contains(route.Pattern, op) && route.Method == c.Request.Method {
			route.HandlerFunc(c)
			return
		}
	}

	c.String(http.StatusNotFound, "404 page not found")
}

func (s *Server) ThreeLayerPathHandlerFunc(c *gin.Context) {
	op := c.Param("subscriptionId")
	thirdLayer := c.Param("thirdLayer")

	// for "/:ueId/sdm-subscriptions/:subscriptionId"
	if op == "sdm-subscriptions" && http.MethodDelete == c.Request.Method {
		var tmpParams gin.Params
		tmpParams = append(tmpParams, gin.Param{Key: "ueId", Value: c.Param("supi")})
		tmpParams = append(tmpParams, gin.Param{Key: "subscriptionId", Value: c.Param("thirdLayer")})
		c.Params = tmpParams
		s.HandleUnsubscribe(c)
		return
	}

	// for "/:supi/am-data/sor-ack"
	if op == "am-data" && http.MethodPut == c.Request.Method && thirdLayer == "sor-ack" {
		s.HandleInfo(c)
		return
	}

	// for "/:supi/am-data/cag-ack"
	if op == "am-data" && http.MethodPut == c.Request.Method && thirdLayer == "cag-ack" {
		s.HandleCAGAck(c)
		return
	}

	// for "/:supi/am-data/ecr-data"
	if op == "am-data" && http.MethodGet == c.Request.Method && thirdLayer == "ecr-data" {
		s.HandleGetEcrData(c)
		return
	}

	// for "/:supi/am-data/subscribed-snssais-ack"
	if op == "am-data" && http.MethodPut == c.Request.Method &&
		thirdLayer == "subscribed-snssais-ack" {
		s.HandleSNSSAIsAck(c)
		return
	}

	// for "/:supi/am-data/update-sor"
	if op == "am-data" && http.MethodPost == c.Request.Method && thirdLayer == "update-sor" {
		s.HandleUpdateSORInfo(c)
		return
	}

	// for "/:supi/am-data/upu-ack"
	if op == "am-data" && http.MethodPut == c.Request.Method && thirdLayer == "upu-ack" {
		s.HandleUpuAck(c)
		return
	}

	// for "/:ueId/sdm-subscriptions/:subscriptionId"
	if op == "sdm-subscriptions" && http.MethodPatch == c.Request.Method {
		var tmpParams gin.Params
		tmpParams = append(tmpParams, gin.Param{Key: "ueId", Value: c.Param("supi")})
		tmpParams = append(tmpParams, gin.Param{Key: "subscriptionId", Value: c.Param("thirdLayer")})
		c.Params = tmpParams
		s.HandleModify(c)
		return
	}

	c.String(http.StatusNotFound, "404 page not found")
}

func (s *Server) getOneLayerRoutes() []Route {
	return []Route{
		{
			"GetDataSets",
			http.MethodGet,
			"/:supi",
			s.HandleGetSupi,
		},

		{
			"GetSharedData",
			http.MethodGet,
			"/shared-data",
			s.HandleGetSharedData,
		},

		{
			"SubscribeToSharedData",
			http.MethodPost,
			"/shared-data-subscriptions",
			s.HandleSubscribeToSharedData,
		},

		{
			"GetMultipleIdentifiers",
			http.MethodGet,
			"/multiple-identifiers",
			s.HandleGetMultipleIdentifiers,
		},
	}
}

func (s *Server) getTwoLayerRoutes() []Route {
	return []Route{
		{
			"GetAmData",
			http.MethodGet,
			"/:supi/am-data",
			s.HandleGetAmData,
		},

		{
			"GetSmfSelData",
			http.MethodGet,
			"/:supi/smf-select-data",
			s.HandleGetSmfSelectData,
		},

		{
			"GetSmsMngtData",
			http.MethodGet,
			"/:supi/sms-mng-data",
			s.HandleGetSmsMngData,
		},

		{
			"GetSmsData",
			http.MethodGet,
			"/:supi/sms-data",
			s.HandleGetSmsData,
		},

		{
			"GetSmData",
			http.MethodGet,
			"/:supi/sm-data",
			s.HandleGetSmData,
		},

		{
			"GetNSSAI",
			http.MethodGet,
			"/:supi/nssai",
			s.HandleGetNssai,
		},

		{
			"Subscribe",
			http.MethodPost,
			"/:ueId/sdm-subscriptions",
			s.HandleSubscribe,
		},

		{
			"GetTraceConfigData",
			http.MethodGet,
			"/:supi/trace-data",
			s.HandleGetTraceData,
		},

		{
			"GetUeCtxInSmfData",
			http.MethodGet,
			"/:supi/ue-context-in-smf-data",
			s.HandleGetUeContextInSmfData,
		},

		{
			"GetUeCtxInSmsfData",
			http.MethodGet,
			"/:supi/ue-context-in-smsf-data",
			s.HandleGetUeContextInSmsfData,
		},

		{
			"GetGroupIdentifiers",
			http.MethodGet,
			"/group-data/group-identifiers",
			s.HandleGetGroupIdentifiers,
		},

		{
			"GetLcsBcaData",
			http.MethodGet,
			"/:supi/lcs-bca-data",
			s.HandleGetLcsBcaData,
		},

		{
			"GetLcsMoData",
			http.MethodGet,
			"/:supi/lcs-mo-data",
			s.HandleGetLcsMoData,
		},

		{
			"GetLcsPrivacyData",
			http.MethodGet,
			"/:ueId/lcs-privacy-data",
			s.HandleGetLcsPrivacyData,
		},

		{
			"GetMbsData",
			http.MethodGet,
			"/:supi/5mbs-data",
			s.HandleGetMbsData,
		},

		{
			"GetProseData",
			http.MethodGet,
			"/:supi/prose-data",
			s.HandleGetProseData,
		},

		{
			"GetUcData",
			http.MethodGet,
			"/:supi/uc-data",
			s.HandleGetUcData,
		},

		{
			"GetUeCtxInAmfData",
			http.MethodGet,
			"/:supi/ue-context-in-amf-data",
			s.HandleGetUeCtxInAmfData,
		},

		{
			"GetV2xData",
			http.MethodGet,
			"/:supi/v2x-data",
			s.HandleGetV2xData,
		},
	}
}
```

---

## Question

Identify all security vulnerabilities or logic errors present in this file. For each finding:

1. Name the vulnerability class or error type
2. Identify the exact function(s) where the issue occurs and describe the specific code pattern
3. Explain the security impact in the context of the UDM in a 5G core network
4. Propose a correct fix

---

## Agent Instructions

Reply ONLY in Markdown using this template:

```md
### Reasoning
Detailed analysis for each finding: class, location, impact, fix

### Answer
Brief summary of main findings (1-3 sentences)

### Confidence
0.0
```


---

## Static analysis findings (SonarQube)

The alerts below were generated by an automated static-analysis tool (SonarQube) on this file, unfiltered. Most describe code-style issues (e.g. duplicated string literals, TODO comments) and are NOT security vulnerabilities. Use them only if and where they are actually relevant to your security assessment — do not assume every alert below points to a real issue.
- L32 [CRITICAL] go:S1192: Define a constant instead of duplicating this literal "plmn-id" 13 times.
- L33 [CRITICAL] go:S1192: Define a constant instead of duplicating this literal "supported-features" 17 times.
- L42 [CRITICAL] go:S1192: Define a constant instead of duplicating this literal "Malformed request syntax" 8 times.
- L157 [CRITICAL] go:S1192: Define a constant instead of duplicating this literal "dataset-names" 3 times.
- L202 [CRITICAL] go:S1192: Define a constant instead of duplicating this literal "System failure" 4 times.
- L207 [CRITICAL] go:S1192: Define a constant instead of duplicating this literal "Get Request Body error: %+v" 4 times.
- L213 [CRITICAL] go:S1192: Define a constant instead of duplicating this literal "application/json" 4 times.
- L215 [CRITICAL] go:S1192: Define a constant instead of duplicating this literal "[Request Body] " 4 times.
- L282 [CRITICAL] go:S1192: Define a constant instead of duplicating this literal "UE ID is invalid" 6 times.
- L452 [CRITICAL] go:S1192: Define a constant instead of duplicating this literal "single-nssai" 3 times.
- L582 [CRITICAL] go:S1192: Define a constant instead of duplicating this literal "404 page not found" 3 times.
- L627 [CRITICAL] go:S3776: Refactor this method to reduce its Cognitive Complexity from 16 to the 15 allowed.
- L642 [CRITICAL] go:S1192: Define a constant instead of duplicating this literal "am-data" 6 times.


**System context:** the code under review is a Network Function (NF) inside a 5G core network (free5GC architecture). In a standard 5G core deployment, the Service-Based Interface (SBI) between NFs runs behind mutual TLS and OAuth2 authorization by default. Use this when judging the *impact* (confidentiality/integrity/availability) of a vulnerability: do not assume a bug automatically exposes data — consider what is actually reachable or corrupted given this baseline.


---

## CVSS Estimate (required)

For each vulnerability reported in your Answer, also estimate its CVSS 4.0 base
metrics. Add this exact section to your response, after the Answer section and
before Confidence, repeating the four lines below for each finding. Each finding names exactly ONE
function: if the same vulnerability affects several functions, repeat the whole
block once per affected function (same vector/score, one `function:` line each)
instead of listing multiple function names in a single line.

### CVSS Estimate
- function: <name of the Go function containing the issue>
- vector: CVSS:4.0/AV:_/AC:_/AT:_/PR:_/UI:_/VC:_/VI:_/VA:_/SC:_/SI:_/SA:_
- score: <your estimated CVSS 4.0 base score, 0.0-10.0>
- snippet: <one exact line of code, copied verbatim from the source above, that supports this finding>

Replace each `_` in the vector with one of the allowed values:

- AV Attack Vector: N (Network), A (Adjacent), L (Local), P (Physical)
- AC Attack Complexity: L (Low), H (High)
- AT Attack Requirements: N (None), P (Present)
- PR Privileges Required: N (None), L (Low), H (High)
- UI User Interaction: N (None), P (Passive), A (Active)
- VC / VI / VA Confidentiality / Integrity / Availability impact on the
  vulnerable system: H (High), L (Low), N (None)
- SC / SI / SA Confidentiality / Integrity / Availability impact on
  subsequent systems (other components reachable from the vulnerable one):
  H (High), L (Low), N (None)


---
Note: you already attempted this task. Review your previous attempt below, then try again from scratch.

### Previous Answer
The UDM implementation suffers from inconsistent input validation of SUPI/UEID across multiple handlers, unsafe JSON parsing of URL query parameters, and potential information leakage through raw error responses. These issues could lead to Denial of Service (DoS) or facilitate targeted attacks against the subscriber database.

### Previous Reasoning
1. **Missing Input Validation (SUPI/UEID):** Several handlers that retrieve or modify subscriber data fail to validate the `supi` or `ueId` parameters. Specifically, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`, and `HandleModifyForSharedData` do not call `validator.IsValidSupi()` or `validator.IsValidGpsi()`. In a 5G Core, the SUPI is a sensitive identifier; allowing malformed or oversized strings to reach the `Processor` layer can lead to backend database errors, injection vulnerabilities, or unexpected behavior in the data layer.

2. **Unsafe JSON Unmarshaling of Query Parameters:** The function `getPlmnIDStruct` takes a query parameter (`plmn-id`) and passes it directly to `json.Unmarshal`. Query parameters are typically plain strings. Expecting a JSON-encoded string within a URL query parameter is non-standard and dangerous. An attacker could potentially provide a very large or deeply nested JSON object in the URL to cause excessive CPU/memory consumption (DoS) during the unmarshaling process.

3. **Information Leakage via Error Messages:** In `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, and `HandleModifyForSharedData`, the code returns `err.Error()` from `c.GetRawData()` or `openapi.Deserialize` directly to the client in the `ProblemDetails.Detail` field. This can leak internal system information, such as library versions, memory addresses, or internal structure details, which aids an attacker in reconnaissance.

4. **Logic Error in Route Dispatching (Path Traversal/Collision):** The `OneLayerPathHandlerFunc` uses `strings.Contains(route.Pattern, supi)` to match routes. If a `supi` parameter contains a substring that matches another route pattern, it could lead to the wrong handler being executed. While `supi` is usually numeric, if the validator is bypassed or if the input is manipulated, this logic is fragile.

### Previous Confidence
0.9

Please reason again from scratch and follow the response format in the task.
````

</details>

---
_Source: `results/task8_vuln_udm_full/1A_sast_hint_full/agent/*.json`, run_id `20260723T081003Z`, repetition 3._
