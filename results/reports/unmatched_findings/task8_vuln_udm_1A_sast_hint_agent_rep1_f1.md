# Unmatched finding — task8_vuln_udm (1A_sast_hint) — agent, rep 1

| field | value |
| --- | --- |
| function | `HandleGetNssai` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| score declared | 5.1 |
| score computed (official CVSS 4.0 math) | 5.3 |
| group (shared with matched table) | a |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `HandleGetNssai` are **bolded** below to help locate the relevant passage._

**Answer:**

The UDM implementation suffers from inconsistent input validation of the `supi` identifier. While `HandleGetAmData` and `HandleUnsubscribe` validate the identifier, six other handlers (`HandleGetSmfSelectData`, **`HandleGetNssai`**, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, and `HandleGetSupi`) pass the raw URL parameter directly to the processor, risking injection or DoS attacks.

**Reasoning:**

The code exhibits a critical inconsistency in input validation for the `supi` parameter across different SBI handlers. The `supi` (Subscription Permanent Identifier) is a sensitive unique identifier used as a primary key to retrieve subscriber data from the UDM database.

1. **Vulnerability Class:** Improper Input Validation / Missing Input Validation.
2. **Affected Handlers:** 
   - `HandleGetAmData`: **Validated** (calls `validator.IsValidSupi(supi)`).
   - `HandleUnsubscribe`: **Validated** (calls `validator.IsValidSupi(ueId)`).
   - `HandleGetSmfSelectData`: **NOT Validated**.
   - **`HandleGetNssai`**: **NOT Validated**.
   - `HandleGetSmData`: **NOT Validated**.
   - `HandleGetTraceData`: **NOT Validated**.
   - `HandleGetUeContextInSmfData`: **NOT Validated**.
   - `HandleGetSupi`: **NOT Validated**.
3. **Security Impact:** In the context of a 5G Core, while SBI traffic is typically protected by mTLS and OAuth2, the lack of validation at the handler level allows for "Malformed Request" attacks. If the underlying `Processor` or database layer does not perform strict validation, an attacker (or a compromised NF) could inject specially crafted strings into the `supi` parameter. This could lead to:
   - **Unauthorized Data Access:** If the database query is susceptible to injection or if the logic allows wildcard-like behavior.
   - **Denial of Service (DoS):** Passing extremely long strings or unexpected characters that cause the backend processor or database to crash or consume excessive resources.
   - **Logic Errors:** Bypassing intended business logic by providing identifiers that do not follow the 3GPP standard format.
4. **Proposed Fix:** Implement a consistent validation check using `validator.IsValidSupi(supi)` at the beginning of every handler that accepts a `supi` parameter, returning a `400 Bad Request` (ProblemDetails) if the validation fails, mirroring the implementation in `HandleGetAmData`.

<details>
<summary>Prompt sent to the model (system + user)</summary>

**System:**

```
You are a 5G network engineer experienced in core network analysis and code review.
Reply ONLY in Markdown using the response format in the task. No extra text before or after.
```

**User:**

````
# Task 8 — Security Code Review: UDM Subscriber Data Management Handler (Go)

**ID:** task8_vuln_udm  
**Tipo:** textual  
**Difficoltà:** media-alta

---

## Scenario

The following Go source file is the Subscriber Data Management SBI handler of the **Unified Data Management (UDM)** function in a free5GC 5G core implementation. The UDM stores and provides access to UE subscription data (mobility, session management, authentication) to other NFs. Each endpoint is keyed by a SUPI (Subscription Permanent Identifier) or GPSI.

Perform a **security code review** of the representative handler selection below. Focus on input validation consistency — pay attention to which handlers validate identifiers before use and which do not.

```go
package sbi

import (
	"net/http"
	"strings"
	"net/url"
	"encoding/json"

	"github.com/gin-gonic/gin"

	"github.com/free5gc/openapi"
	"github.com/free5gc/openapi/models"
	"github.com/free5gc/udm/internal/logger"
	"github.com/free5gc/util/metrics/sbi"
	"github.com/free5gc/util/validator"
)

// GetAmData - retrieve a UE's Access and Mobility Subscription Data
func (s *Server) HandleGetAmData(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("supported-features", c.Query("supported-features"))

	supi := c.Params.ByName("supi")
	if !validator.IsValidSupi(supi) {
		problemDetail := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: "Supi is invalid",
			Cause:  "MANDATORY_IE_INCORRECT",
		}
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(problemDetail.Status)))
		c.JSON(int(problemDetail.Status), problemDetail)
		return
	}

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

// GetSmfSelectData - retrieve a UE's SMF Selection Subscription Data
func (s *Server) HandleGetSmfSelectData(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("supported-features", c.Query("supported-features"))

	supi := c.Params.ByName("supi")
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

// GetNssai - retrieve a UE's subscribed NSSAI
func (s *Server) HandleGetNssai(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("supported-features", c.Query("supported-features"))

	supi := c.Params.ByName("supi")
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

	supi := c.Params.ByName("supi")
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

// GetTraceData - retrieve a UE's Trace Configuration Data
func (s *Server) HandleGetTraceData(c *gin.Context) {
	supi := c.Params.ByName("supi")
	plmnID := c.Query("plmn-id")
	s.Processor().GetTraceDataProcedure(c, supi, plmnID)
}

// GetUeContextInSmfData - retrieve a UE's UE Context In SMF Data
func (s *Server) HandleGetUeContextInSmfData(c *gin.Context) {
	supi := c.Params.ByName("supi")
	supportedFeatures := c.Query("supported-features")
	s.Processor().GetUeContextInSmfDataProcedure(c, supi, supportedFeatures)
}

// GetSupi - retrieve multiple data sets
func (s *Server) HandleGetSupi(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("dataset-names", c.Query("dataset-names"))
	query.Set("supported-features", c.Query("supported-features"))

	supi := c.Params.ByName("supi")
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

// Unsubscribe - unsubscribe from notifications
func (s *Server) HandleUnsubscribe(c *gin.Context) {
	ueId := c.Params.ByName("ueId")
	valid := validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)
	if !valid {
		problemDetail := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: "UE ID is invalid",
			Cause:  "MANDATORY_IE_INCORRECT",
		}
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(problemDetail.Status)))
		c.JSON(int(problemDetail.Status), problemDetail)
		return
	}
	subscriptionID := c.Params.ByName("subscriptionId")
	s.Processor().UnsubscribeProcedure(c, ueId, subscriptionID)
}
```

---

## Question

Identify all security vulnerabilities or inconsistencies in this file. For each finding:

1. Name the vulnerability class or error type
2. Identify which specific handlers are affected and which are not — this is essential
3. Explain the security impact in the context of a UDM managing SUPI-indexed subscription data
4. Propose a correct fix


---

## Agent Instructions

Reply ONLY in Markdown using this template:

```md
### Reasoning
Detailed analysis: vulnerability class, location, impact, fix

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
````

</details>

---
_Source: `results/task8_vuln_udm/1A_sast_hint/agent/*.json`, run_id `20260721T143747Z`, repetition 1._
